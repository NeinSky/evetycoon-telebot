import requests
import json
import sqlalchemy as db
from datetime import datetime, timezone
from database.models import Region, Request
from database.connection import session
from loader import EMPIRE_REGIONS, REGIONS_ID_TO_NAMES
from config import NUM_OF_RESULTS
from os.path import exists


BASE_URL = 'https://evetycoon.com/api/v1/market'


def _save_result_to_file(filename: str, data: dict) -> None:
    """Saves result to cache file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


def _load_from_cache_file(filename: str) -> dict:
    """Load result  from cache file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def _expires_header_to_datetime(date_str: str) -> datetime:
    """Converts Expires header date format, which looks like 'Mon, 27 May 2024 07:04:13 GMT' to datetime"""
    date_list = date_str.split(' ')
    date_time = date_list[4].split(':')
    date_tuple = (
        date_list[1],  # day
        date_list[2],  # month
        date_list[3],  # year
        date_time[0],  # hour
        date_time[1],  # minutes
        date_time[2],  # seconds
    )

    return datetime.strptime(" ".join(date_tuple), "%d %b %Y %H %M %S")


def _get_best_regions(raw_data: dict[int: dict]) -> dict:
    """Processes raw data and returns of top markets. Market value define by sum of buy and sell orders"""
    unprocessed_list = []
    for region_id, data in raw_data.items():
        unprocessed_list.append((
            region_id,
            data['buyOrders'] + data['sellOrders']))
    sorted_list = sorted(unprocessed_list, key=lambda x: x[1], reverse=True)
    counter = 0
    result = {}
    for region_id, market_value in sorted_list:
        result[region_id] = raw_data[region_id]
        counter += 1
        if counter >= NUM_OF_RESULTS:
            break
    return result


def _security_check(security_filter: str, system_id: int, system_data: dict) -> bool:
    """Compares system security with security filter applied. Returns True if system secure enough."""
    value = float(system_data[str(system_id)]['security'])

    if security_filter == 'all':
        return True
    elif security_filter == 'low':
        return value > 0.0
    elif security_filter == 'high':
        return value >= 0.5
    else:
        return False


def _get_station_name(system_data: dict, station_id: int):
    """Checks stationNames and structureNames dicts for station name."""
    structure_id = str(station_id)

    if structure_id in system_data['stationNames'].keys():
        return system_data['stationNames'][structure_id]

    if structure_id in system_data['structureNames'].keys():
        return system_data['structureNames'][structure_id]

    return f"STATION {station_id} NOT FOUND"


def _to_datetime(timestamp: str):
    """Converts timestamp with milliseconds to datetime."""
    raw_time = int(timestamp)/1000
    return datetime.utcfromtimestamp(raw_time)


def _get_best_orders(raw_data: dict[int: dict], is_buy_order: bool, security: str) -> dict[str: list]:
    """Processes raw data and returns top orders. Highest price orders for wts command and lowest for wtb."""
    unprocessed_list = []
    for region_id, data in raw_data.items():
        for order in data['orders']:
            if (order['isBuyOrder'] == is_buy_order
                    and _security_check(security,
                                        order['systemId'],
                                        data['systems'])):

                system_id = str(order['systemId'])
                unprocessed_list.append([
                    REGIONS_ID_TO_NAMES[int(order['regionId'])],  # region name
                    data['systems'][system_id]['solarSystemName'],  # system name
                    data['systems'][system_id]['security'],  # system security
                    _get_station_name(data, order['locationId']),  # station name
                    order['price'],  # price per unit
                    _to_datetime(order['issued']).isoformat(),  # date of issue
                    order['duration'],
                    order['volumeRemain'],
                    order['minVolume']
                ])

    sorted_list = sorted(unprocessed_list, key=lambda x: x[4], reverse=is_buy_order)
    result = {'orders': []}
    counter = 0
    for order in sorted_list:
        result['orders'].append(order)
        counter += 1
        if counter >= NUM_OF_RESULTS:
            break

    return result


def _request_raw_data(formatted_url: str, mineral_id: int, regions: tuple) -> tuple[dict, datetime]:
    """Takes url and parameters, makes API request and returns raw dict, where key is region_id"""
    expires = None
    raw_data = {}
    for region in regions:
        region_id = region[0]
        request = requests.get(formatted_url.format(region_id=region_id, mineral_id=mineral_id))
        # save Expires header of the first request
        if not expires:
            expires_header = request.headers['Expires']
            expires = _expires_header_to_datetime(expires_header)
        raw_data[region_id] = request.json()
    return raw_data, expires


def _request_market_stats(data: dict, now: datetime) -> tuple[dict, datetime, str]:
    """Requests, processes and returns stats data"""
    mineral_id = data['mineral_id']
    empire_id = data['empire_filter']

    regions: tuple = Region.get_regions() if empire_id == 'All' else EMPIRE_REGIONS[empire_id]
    url = BASE_URL + '/stats/{region_id}/{mineral_id}'
    raw_data, expires = _request_raw_data(url, mineral_id, regions)

    processed_data: dict = _get_best_regions(raw_data)
    cached_file = f'cache/{now.timestamp():.0f}.json'
    _save_result_to_file(cached_file, processed_data)

    return processed_data, expires, cached_file


def _request_market_orders(data: dict, now: datetime) -> tuple[dict, datetime, str]:
    """Requests, processes and returns orders data"""
    mineral_id = data['mineral_id']
    empire_id = data['empire_filter']
    security = data['system_filter']
    is_buy_order = 'wts' in data['order_type']

    regions: tuple = Region.get_regions() if empire_id == 'All' else EMPIRE_REGIONS[empire_id]
    url = BASE_URL + '/orders/{mineral_id}?regionId={region_id}'
    raw_data, expires = _request_raw_data(url, mineral_id, regions)

    processed_data: dict = _get_best_orders(raw_data, is_buy_order, security)
    cached_file = f'cache/{now.timestamp():.0f}.json'
    _save_result_to_file(cached_file, processed_data)

    return processed_data, expires, cached_file


def _get_message_from_processed_stats_data(data: dict, is_cached: bool) -> str:
    """Converts stats dict into prepared message"""
    message = '**cached**\n\n' if is_cached else '**new request**\n\n'
    for region_id, region_data in data.items():
        name = REGIONS_ID_TO_NAMES[int(region_id)]

        row = (f"{name}\n"
               f"Value (buy | sell) : {region_data['buyVolume']} | {region_data['sellVolume']}\n"
               f"Orders (buy | sell): {region_data['buyOrders']} | {region_data['sellOrders']}\n"
               f"Max buy | Min sell : {region_data['maxBuy']:.2f} | {region_data['minSell']:.2f}\n"
               f"Avg buy | sell: {region_data['buyAvgFivePercent']:.2f} | {region_data['sellAvgFivePercent']:.2f}\n"
               f"---------\n\n")
        message += row
    return message


def _get_message_from_processed_orders(data: dict, is_cached: bool) -> str:
    """Converts orders dict into prepared message"""
    message = '**cached**\n\n' if is_cached else '**new request**\n\n'
    for data in data['orders']:
        row = (f"{data[0]} - {data[1]} ({data[2]:.2f})\n"  # region - system (security)
               f"{data[3]}\n"  # station name
               f"Price: {data[4]}\n"
               f"Issued: {data[5]}\n"
               f"Duration: {data[6]}\n"
               f"Volume: {data[7]}\n"
               f"Min. vol.: {data[8]}\n"
               f"-----------\n")
        message += row
    return message


def get_market_stats(data: dict) -> str:
    mineral_id = data['mineral_id']
    empire_id = data['empire_filter']
    command = f"stats;{mineral_id};{empire_id}"

    # check if request was made earlier and not expired:
    last_same_request: Request = (session.query(Request)
                                  .filter(Request.command == command)
                                  .order_by(db.column('expires').desc())
                                  .first())
    now: datetime = datetime.utcnow()

    # if same request exists and not expires, load result from cached file
    if last_same_request and last_same_request.expires >= now:
        if exists(last_same_request.cache_file):
            is_cached = True
            cached_file = last_same_request.cache_file
            processed_data = _load_from_cache_file(cached_file)
            expires = last_same_request.expires
        else:
            is_cached = False
            processed_data, expires, cached_file = _request_market_stats(data, now)

    # else make new request and process data
    else:
        is_cached = False
        processed_data, expires, cached_file = _request_market_stats(data, now)

    query_data = {
        'user_id': data['user_id'],
        'command': command,
        'date': datetime.now(timezone.utc),
        'expires': expires,
        'cache_file': cached_file
    }

    session.add(Request(**query_data))
    session.commit()

    return _get_message_from_processed_stats_data(processed_data, is_cached)


def get_market_orders(data: dict) -> str:
    mineral_id = data['mineral_id']
    empire_id = data['empire_filter']
    security = data['system_filter']
    order_type = data['order_type']
    command = f"{order_type};{mineral_id};{empire_id};{security}"

    # check if request was made earlier and not expired:
    last_same_request: Request = (session.query(Request)
                                  .filter(Request.command == command)
                                  .order_by(db.column('expires').desc())
                                  .first())
    now: datetime = datetime.utcnow()

    # if same request exists and not expires, load result from cached file
    if last_same_request and last_same_request.expires >= now:
        if exists(last_same_request.cache_file):
            is_cached = True
            cached_file = last_same_request.cache_file
            processed_data = _load_from_cache_file(cached_file)
            expires = last_same_request.expires
        else:
            is_cached = False
            processed_data, expires, cached_file = _request_market_orders(data, now)

    # else make new request and process data
    else:
        is_cached = False
        processed_data, expires, cached_file = _request_market_orders(data, now)

    query_data = {
        'user_id': data['user_id'],
        'command': command,
        'date': datetime.now(timezone.utc),
        'expires': expires,
        'cache_file': cached_file
    }

    session.add(Request(**query_data))
    session.commit()

    return _get_message_from_processed_orders(processed_data, is_cached)

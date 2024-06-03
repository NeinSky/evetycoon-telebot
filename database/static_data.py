"""
This file contains static data to load into database. It includes empires, regions and minerals
"""

from .models import Empire, Region, Mineral
from .connection import session
import json

REGIONS_JSON_FILE = 'database/regions.json'
MINERALS_JSON_FILE = 'database/minerals.json'


def load_static_data():
    """
    Loads static data into db if no static data was loaded
    """
    if not session.query(Empire).all():
        empires = [
            (0, 'All', 'All'),
            (1, 'Amarr Empire', 'Amarr'),
            (2, 'Caldari State', 'Caldari'),
            (3, 'Gallente Federation', 'Gallente'),
            (4, 'Minmatar Republic', 'Republic'),
        ]

        with open(REGIONS_JSON_FILE, 'r') as f:
            regions_dict = json.loads(f.read())

        regions = []
        for empire_id, regions_data in regions_dict.items():
            for region in regions_data:
                regions.append((
                    region['id'],
                    region['name'],
                    int(empire_id)
                ))

        with open(MINERALS_JSON_FILE, 'r') as f:
            minerals_data = json.loads(f.read())

        minerals = []
        for name, data in minerals_data.items():
            minerals.append((
                data[0],  # ID
                name,
                data[1],  # short name

            ))

        for empire in empires:
            session.add(Empire(
                id=empire[0],
                name=empire[1],
                short_name=empire[2],
            ))
            session.commit()

        for data in regions:
            session.add(Region(
                id=data[0],
                name=data[1],
                empire_id=data[2],
            ))
            session.commit()

        for data in minerals:
            session.add(Mineral(
                id=data[0],
                name=data[1],
                short_name=data[2],
            ))
            session.commit()

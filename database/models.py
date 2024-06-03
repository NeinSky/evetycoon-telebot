import sqlalchemy as db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .connection import session
from datetime import datetime, timezone
from config import NUM_OF_RESULTS

Base = declarative_base()


class Mineral(Base):
    """ Model contains minerals data """
    __tablename__ = 'minerals'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    short_name = Column(String(10), nullable=False)

    @staticmethod
    def get_minerals_short_name() -> dict[str: tuple[int, str]]:
        """
        Returns dictionary of minerals short names, IDs and full names.

        :return: dict, where key is minerals' short name and values are IDs and full names
        """

        minerals = session.query(Mineral).all()
        return {mineral.short_name: (mineral.id, mineral.name) for mineral in minerals}

    @staticmethod
    def mineral_id_to_short_name() -> dict[int: str]:
        minerals = session.query(Mineral).all()
        return {mineral.id: mineral.short_name for mineral in minerals}


class Empire(Base):
    """ Model contains empires data """
    __tablename__ = 'empires'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    short_name = Column(String(10), nullable=False)

    regions = relationship("Region", back_populates="empires")

    @staticmethod
    def get_empires() -> dict[str: tuple[int, str]]:
        """
        Get dictionary of empires.

        :return: dict, where key is empire's short name and values are tuples containing ID and full name
        """
        empires = session.query(Empire).all()
        return {empire.short_name: (empire.id, empire.name) for empire in empires}

    @staticmethod
    def empires_ids_to_short_names() -> dict[int: str]:
        """
        Returns dictionary of IDs and short names

        :return: dict, where key is an ID and value is a short name
        """
        empires = session.query(Empire).all()
        return {empire.id: empire.short_name for empire in empires}


class Region(Base):
    """ Model contains regions data """

    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    empire_id = Column(Integer,  ForeignKey('empires.id'), nullable=False)

    empires = relationship("Empire", back_populates="regions")

    @staticmethod
    def get_regions() -> tuple[tuple]:
        """
        Returns tuple, which contains tuples of IDs, region names and empire IDs
        It used when filter "all" specified
        """
        regions = session.query(Region).all()
        return tuple((region.id, region.name, region.empire_id) for region in regions)

    @staticmethod
    def get_empire_regions() -> dict[str: list[tuple]]:
        """
        Returns dictionary of empires' regions.
        It used when specific empire provided in filters

        :return: dict, where key is empire short_name and value is a list of region's ID and name
        """
        regions = session.query(Region).all()
        empires = Empire.empires_ids_to_short_names()
        result = {}
        for region in regions:
            empire_name = empires[region.empire_id]
            if result.get(empire_name):
                result[empire_name].append((region.id, region.name))
            else:
                result[empire_name] = [(region.id, region.name)]

        return result

    @staticmethod
    def get_region_id_to_name() -> dict[int: str]:
        """
        Return dict of region id's and names

        :return: dict, where key is a region id and value is its name
        """
        regions = session.query(Region).all()
        return {region.id: region.name for region in regions}


class Request(Base):
    """
    Contains requests data

    user_id - user's id from telebot, used to show user's last commands
    link - full requests link
    date - date of request, used to show user's last commands
    expires - request expiration date to determine whether new request should be sent or cache file used
    cache_file - full path to file, which contains cache of this request

    """

    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    command = Column(String(50), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    expires = Column(DateTime, nullable=False)
    cache_file = Column(String(100), nullable=False)

    @staticmethod
    def get_users_last_requests(user_id: int) -> list:
        """Returns user's last NUM_OF_RESULTS commands and dates"""
        data = (session.query(Request.command, Request.date)
                .filter(Request.user_id == user_id)
                .order_by(db.column('date').desc())
                .limit(NUM_OF_RESULTS))

        # Convert datetime to str
        return [(row[0], row[1].isoformat(sep=' ', timespec='seconds'))
                for row in data]

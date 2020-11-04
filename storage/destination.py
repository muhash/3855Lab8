from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Destination(Base):
    """ Destination """

    __tablename__ = "destination"

    id = Column(Integer, primary_key=True)
    home_address = Column(String(250), nullable=False)
    dest_address = Column(String(250), nullable=False)
    num_passengers = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, home_address, dest_address, num_passengers):
        """ Initializes a destination """
        self.home_address = home_address
        self.dest_address = dest_address
        self.num_passengers = num_passengers
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a destination """
        dict = {}
        dict['id'] = self.id
        dict['home_address'] = self.home_address
        dict['dest_address'] = self.dest_address
        dict['num_passengers'] = self.num_passengers
        dict['date_created'] = self.date_created

        return dict

from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class Order(Base):
    """ Order """

    __tablename__ = "ordr"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    ordr = Column(String(250), nullable=False)
    price = Column(Float, nullable=False)
    address = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)


    def __init__(self, customer_id, ordr, price, address, timestamp):
        """ Initializes an order """
        self.customer_id = customer_id
        self.ordr = ordr
        self.price = price
        self.address = address
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of an order """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['ordr'] = self.ordr
        dict['price'] = self.price
        dict['address'] = self.address
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict

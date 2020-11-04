import connexion
from connexion import NoContent
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from order import Order
import logging
import logging.config
from destination import Destination
import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import json

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(app_config['datastore']['user'], app_config['datastore']['password'], app_config['datastore']['hostname'], app_config['datastore']['port'], app_config['datastore']['db']))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger.info('Connecting to DB. Hostname: ' + app_config['datastore']['hostname'] + ', Port:' + str(app_config['datastore']['port']))

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group='event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "Order":
            session = DB_SESSION()
            ord = Order(msg['payload']['customer_id'],
                        msg['payload']['ordr'],
                        msg['payload']['price'],
                        msg['payload']['address'],
                        msg['payload']['timestamp'])

            session.add(ord)
            session.commit()
            session.close()
        elif msg["type"] == "Destination":
            session = DB_SESSION()
            dest = Destination(msg['payload']['home_address'],
                               msg['payload']['dest_address'],
                               msg['payload']['num_passengers'])

            session.add(dest)
            session.commit()
            session.close()
        consumer.commit_offsets()

def report_order(body):
    """ Receives an order"""
    unique_id = datetime.datetime.now().strftime('%H%M%S%f') + body['address'].replace(" ", "")
    logger.info('Received event <addOrder> request with a unique id of ' + unique_id)
    session = DB_SESSION()

    ord = Order(body['customer_id'],
                body['ordr'],
                body['price'],
                body['address'],
                body['timestamp'])

    session.add(ord)

    session.commit()
    session.close()
    logger.info('Returned event <addOrder> response (id: ' + unique_id + ') with status ' + '201')

    return NoContent, 201


def report_destination(body):
    """ Receives a destination """
    unique_id = datetime.datetime.now().strftime('%H%M%S%f')
    logger.info('Received event <addDestination> request with a unique id of ' + unique_id)

    session = DB_SESSION()

    dest = Destination(body['home_address'],
                       body['dest_address'],
                       body['num_passengers'])

    session.add(dest)
    logger.info(
        'Returned event <addDestination> response (id: ' + unique_id + ') with status ' + '201')
    session.commit()
    session.close()

    return NoContent, 201

def get_order(timestamp):
    """ Gets new order after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = timestamp
    readings = session.query(Order).filter(Order.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for order after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

def get_destination(timestamp):
    """ Gets new destination after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = timestamp
    readings = session.query(Destination).filter(Destination.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for destination after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
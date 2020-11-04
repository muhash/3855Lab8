import connexion
import json
import os
import requests
import yaml
import logging
import logging.config
from datetime import datetime
from pykafka import KafkaClient
from connexion import NoContent

MAX_EVENTS = 10

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def initJsonFile():
    if os.path.isfile('events.json') == False:
        with open('events.json', 'w') as jsonfile:
            json.dump({"requests": []}, jsonfile)

def write_json(data, filename='events.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

def writeJsonFile(body):
    with open('events.json', 'r+') as jsonfile:
        data = json.load(jsonfile)
        temp = data['requests']
        temp.append(body)
        if len(temp) > MAX_EVENTS:
            temp.pop(0)
    write_json(data)

def addOrder(body):
    #writeJsonFile(body)
    #return(NoContent, 201)
    unique_id = datetime.now().strftime('%H%M%S%f') + body['address'].replace(" ", "")
    logger.info('Received event <addOrder> request with a unique id of ' + unique_id)
    client = KafkaClient(hosts=app_config['events']['hostname']+':'+ str(app_config['events']['port']))
    topic = client.topics[app_config['events']['topic']]
    producer = topic.get_sync_producer()
    msg = {"type": "Order",
           "datetime":
               datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    print(msg['payload'])
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    #response = requests.post(app_config['eventstore1']['url'], json=body)
    #logger.info('Returned event <addOrder> response (id: ' + unique_id + ') with status ' + str(response.status_code))
    return(NoContent, 201)
    #return (NoContent, response.status_code)

def addDestlocation(body):
    #writeJsonFile(body)
    #return(NoContent, 201)
    unique_id = datetime.now().strftime('%H%M%S%f')
    logger.info('Received event <addDestination> request with a unique id of ' + unique_id)
    client = KafkaClient(hosts=app_config['events']['hostname'] + ':' + str(app_config['events']['port']))
    topic = client.topics[app_config['events']['topic']]
    producer = topic.get_sync_producer()
    msg = {"type": "Destination",
           "datetime":
               datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    print(msg['payload']['home_address'])
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    #response = requests.post(app_config['eventstore2']['url'], json=body)
    #logger.info('Returned event <addDestination> response (id: ' + unique_id + ') with status ' + str(response.status_code))
    return (NoContent, 201)
    #return (NoContent, response.status_code)

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)



if __name__ == "__main__":
    app.run(port=8080)
""" This service contains the source of truth for all messages coming in.

    Proof of concept! use PSQL for state and write directly to kafka instead of using CDC to eliminate write anomalies 
    (eliminates the situation where we write to the DB first and the service dies and we don't propogate the message down stream) 

    We would use some more appropriate database here rather than psql like influxdb or one of the many k:v databases out there
"""
# Bottle requires gevent.monkey.patch_all() even if you don't like it.
from gevent import monkey; monkey.patch_all()
from gevent import sleep
from gevent.util import format_run_info

from bottle import route, run, GeventServer, get, response, request
from kafka import KafkaConsumer

import os

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")
BOTTLE_HOST = os.getenv("BOTTLE_HOST", "localhost")
BOTTLE_PORT = os.getenv("BOTTLE_PORT", 8081)

# FIXME: decode lambda for consumer

@get('/receive/<chatroom_id>')
def consume(chatroom_id):
    # Server Sent Events (SSE) largely borrowed from https://gist.github.com/werediver/4358735
    response.content_type  = 'text/event-stream'
    response.cache_control = 'no-cache'

    # we could source the chatroom_ids from the query string or have some smarts about where this consumer is if we wanted to monitor more than one channel like this
    # we could consume from a specific offset if we use the confluent library, but you know, proof of concept liberties and all!
    consumer = KafkaConsumer(chatroom_id, bootstrap_servers=KAFKA_BROKERS.split(','))
    for message in consumer:
        yield f"[{message.key.decode('utf-8')}]: {message.value.decode('utf-8')}\n" 

run(server=GeventServer, debug=True)

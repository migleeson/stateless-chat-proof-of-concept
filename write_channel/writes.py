""" This service contains the source of truth for all messages coming in.

    Proof of concept! use PSQL for state and write directly to kafka instead of using CDC to eliminate write anomalies 
    (eliminates the situation where we write to the DB first and the service dies and we don't propogate the message down stream) 

    We would use some more appropriate database here rather than psql like influxdb or one of the many k:v databases out there
"""

from bottle import route, run, Bottle, request
from kafka import KafkaProducer

import psycopg2

import os

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")
BOTTLE_HOST = os.getenv("BOTTLE_HOST", "localhost")
BOTTLE_PORT = os.getenv("BOTTLE_PORT", 8081)

# "dbname=asdf user=postgres password=postgres"
PSQL_CONNECTION_STRING = os.getenv("PSQL_CONNECTION_STRING")

connection = psycopg2.connect(PSQL_CONNECTION_STRING)
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS.split(","))

app = Bottle()

@app.post('/send')
def persist():
    msg = request.json.get("message")
    print(f"msg: {msg}")
    # NOTE: we would track this with whatever we're using for auth rather than the json coming in, but I'm taking proof of concept liberties here :)
    user = request.json.get("user")
    chatroom_id = request.json.get("chatroom_id")
    # do some validation if needed
    insert_query = """
    INSERT INTO messages (message) VALUES (%s)
    """
    with connection.cursor() as cursor:
        cursor.execute(insert_query, (msg,))
        connection.commit()
        # ideally if possible we would do the producer send downstream of the insert (rather than beside) to ensure no message is lost once persisted to db
        # by using CDC and the outbox pattern https://microservices.io/patterns/data/transactional-outbox.html

        producer.send(chatroom_id, value=bytes(msg, encoding="utf-8"), key=bytes(user, encoding="utf-8"))

with connection.cursor() as cur:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
       message_id serial PRIMARY KEY,
       message VARCHAR (200),
       persisted_at TIMESTAMP without time zone default (now() at time zone 'utc')
    );
    """
    )
    connection.commit()

run(app, host=BOTTLE_HOST, port=BOTTLE_PORT, debug=True)

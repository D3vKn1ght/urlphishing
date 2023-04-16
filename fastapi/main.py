from random import randint
from typing import Set, Any
from fastapi import FastAPI, UploadFile,File
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from kafka import TopicPartition
import pandas as pd
import uvicorn
import aiokafka
import asyncio
import json
import logging
import os
from kafka import KafkaProducer

# instantiate the API
app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')


# global variables
consumer_task = None
consumer = None
listData = []

topic_producer="ai-phishing"
topic_result="result"

bootrap_server="42.96.42.99:9092"
topic_group=f"{topic_result}-group"
# env variables
KAFKA_TOPIC = topic_result
KAFKA_CONSUMER_GROUP_PREFIX = topic_group
KAFKA_BOOTSTRAP_SERVERS = bootrap_server

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[bootrap_server],
    value_serializer=serializer
)

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    log.info('Initializing API ...')
    await initialize()
    await consume()


@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')
    consumer_task.cancel()
    await consumer.stop()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/listResult")
async def listResult():
    global listData
    #send and  convert listData to emptry
    copy_listData = listData.copy()
    listData = []
    return copy_listData

@app.post("/sendUrl/")
async def sendUrl(url: str):
    global producer
    datadict={"url":url}
    producer.send(topic_producer,datadict)
    return {"message": "success"}

@app.post("/upload")
async def upload(colName:str="url",file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        print(len(contents))
        # read csv pandas
        df = pd.read_csv(BytesIO(contents))
        # get col by name
        listUrl = df[colName].tolist()
        for url in listUrl:
            print(url)
            producer.send(topic_producer,{"url":url})            
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded"}

async def initialize():
    loop = asyncio.get_event_loop()
    global consumer
    group_id = f'{KAFKA_CONSUMER_GROUP_PREFIX}-{randint(0, 10000)}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_TOPIC}, group_id {group_id}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    consumer = aiokafka.AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                         group_id=group_id)
    # get cluster layout and join group
    await consumer.start()

    partitions: Set[TopicPartition] = consumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await consumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return

        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        consumer.seek(tp, end_offset-1)
        msg = await consumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')

        # update the API state
        _update_state(msg)
        return


async def consume():
    global consumer_task
    consumer_task = asyncio.create_task(send_consumer_message(consumer))


async def send_consumer_message(consumer):
    try:
        # consume messages
        async for msg in consumer:
            # x = json.loads(msg.value)
            log.info(f"Consumed msg: {msg}")

            # update the API state
            _update_state(msg)
    finally:
        # will leave consumer group; perform autocommit if enabled
        log.warning('Stopping consumer')
        await consumer.stop()


def _update_state(message: Any) -> None:
    value = json.loads(message.value)
    print(value)
    global listData
    listData.append(value)
    # _state = value['state']


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

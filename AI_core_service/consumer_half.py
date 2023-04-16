# pip install kafka-python
import json 
from kafka import KafkaConsumer
from kafka import KafkaProducer


topic_name="model_half1"
bootrap_server="42.96.42.99:9092"
topic_result = "result"

import datetime
from feature_half import FeatureExtraction
import pickle
import numpy as np
import pandas as pd
import json
import os

# Kafka Consumer 
consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[bootrap_server],
        group_id=f'{topic_name}-group',
        auto_offset_reset='earliest'
    )

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[bootrap_server],
    value_serializer=serializer
)

file = open("pickle/model_1.pkl","rb")
gbc = pickle.load(file)
file.close()

count = 0
def gradient_boost(url):
    global count
    global producer
    
    start_time = datetime.datetime.now()
    print("Đang test cháu =>", url)
    obj = FeatureExtraction(url)
    print(obj.getFeaturesList())
    
    x = np.array(obj.getFeaturesList()).reshape(1,19) 
    print(x)
    y_pred =gbc.predict(x)[0]
    print(y_pred)
    #1 is safe       
    #-1 is unsafe
    y_pro_phishing = gbc.predict_proba(x)[0,0]
    y_pro_non_phishing = gbc.predict_proba(x)[0,1]
    # if(y_pred ==1 ):
    pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
    print(pred)
    
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time

    print("Thời gian test url : ", elapsed_time)
    xx =round(y_pro_non_phishing,2)
    de = 0
    if xx < 0.5 : de = 1
    
    result = {
        "url":url,
        "is_phishing": de,
        "phishing_type" : "model-half-detect",
        "time" : datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    producer.send(topic_result,result)


from threading import Thread

if __name__ == '__main__':
    
    for message in consumer:
        try:
            my_bytes_value = message.value
            my_json = my_bytes_value.decode('utf8')
            dict = eval(my_json)
            # print(dict)
            gradient_boost(dict['url'])
        except Exception as e:
            print("error ", e)
        
    consumer.close()
    
    
    
    
    
    
    
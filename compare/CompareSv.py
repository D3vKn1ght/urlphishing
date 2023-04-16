from Levenshtein import distance
import time
import json
import tldextract
from difflib import SequenceMatcher
import csv
# pip install kafka-python
from kafka import KafkaConsumer
from datetime import datetime
from kafka import KafkaProducer
import tldextract
print("Start compare service...")

topic_name = "compare"
topic_result="result"
bootrap_server = "42.96.42.99:9092"
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

def get_domain_from_url(url):
    extracted = tldextract.extract(url)
    domain = "{}.{}".format(extracted.domain, extracted.suffix) 
    if("www" not in extracted.subdomain and extracted.subdomain != ""):
        domain= f"{extracted.subdomain}.{domain}"

    # print(domain)
    return domain



def load_domain_list_from_file(file_path):
    domain_set=set()
    # read csv file and get urls
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            url = row[1]  # assuming URL is in second column

            # remove http, https, www, /, etc.
            url = get_domain_from_url(url)
            domain_set.add(url)
    print("Loaded {} domains from file {}".format(len(domain_set), file_path))
    return domain_set



def find_most_similar_domain(input_domain, domain_set):
    min_distance = float('inf')
    most_similar_domain = None

    for domain in domain_set:
        cur_distance = distance(input_domain, domain)
        if cur_distance < min_distance:
            min_distance = cur_distance
            most_similar_domain = domain

    return most_similar_domain, min_distance


def similarity_percentage(s1, s2):
    similarity = SequenceMatcher(None, s1, s2).ratio() * 100
    return similarity

# Danh sách các domain
domain_set = load_domain_list_from_file("top-1m.csv")


while True:
    for message in consumer:
        try:
            my_bytes_value = message.value
            my_json = my_bytes_value.decode('utf8')
            dictData = eval(my_json)
            url = dictData.get("url")
            print("url: ", url)
            if url is None or url == "":
                continue
            dictData["phishing_type"] = "compare"
            dictData["time"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Tìm domain tương tự nhất
            most_similar_domain,min_distance = find_most_similar_domain(url, domain_set)
            url1 = most_similar_domain

            similarity = similarity_percentage(url1, url)
            if similarity >= 80 and similarity != 100:
                dictData["is_phishing"] = "1"
                dictData["phishing_domain"] = most_similar_domain
                dictData["phishing_similarity"] = similarity
                dictData["phishing_distance"] = min_distance
            else:
                dictData["is_phishing"] = "0"            
            producer.send(topic_result, dictData)           
        except Exception as e:
            print("Error: ", e)
            dictData["is_phishing"] = "0"
            producer.send(topic_result, dictData)

consumer.close()


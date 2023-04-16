# pip install kafka-python
import json
from kafka import KafkaConsumer
from datetime import datetime
from kafka import KafkaProducer
import tldextract
import requests

MODEL_FULL_FEATURE=1
MODEL_HALF_FEATURE=2 
COMPARE_MODE=3

topic_name = "ai-phishing"
topic_result="result"
topic_comare="compare"
topic_model_full="model_full"
topic_model_half="model_half"
bootrap_server = "42.96.42.99:9092"
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[bootrap_server],
    group_id=f'{topic_name}-group',
    auto_offset_reset='earliest'
)
index_full=-1
index_half=-1
def choisetopic(listtopic,index_current):
    if index_current==len(listtopic)-1:
        index_current=0
    else:
        index_current=index_current+1
    return index_current,listtopic[index_current]

def add_http(url, type='http'):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = type + '://' + url
    return url

def choose_mode_url_die(url):
    # Kiểm tra độ dài của URL
    if len(url) < 35:  # Chỉ số này có thể thay đổi tùy theo độ dài tối thiểu của URL rút gọn
        return COMPARE_MODE
    else:
        return MODEL_HALF_FEATURE

def get_real_url(url,timeout=0.5):
    print("Get real url: ",url)
    url=add_http(url)
    try:
        # Gửi yêu cầu GET đến URL rút gọn
        response = requests.get(url, allow_redirects=False,timeout=timeout)
        
        # Kiểm tra mã trạng thái của phản hồi
        if response.status_code == 301 or response.status_code == 302:
            # Trích xuất URL thật từ phản hồi
            print("Redirect to: ",response.headers['Location'])
            real_url = response.headers['Location']
            return real_url,MODEL_FULL_FEATURE
        elif response.status_code==200:
            return url,MODEL_FULL_FEATURE
        else:
            # Nếu không phải URL rút gọn, trả về None
            return url,choose_mode_url_die(url)
    except requests.exceptions.RequestException as e:
        print("Lỗi: ", e)
        return url,choose_mode_url_die(url)

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
    # if("www" not in extracted.subdomain and extracted.subdomain != ""):
    #     domain= f"{extracted.subdomain}.{domain}"
    return domain

# read list blacklist


def load_domain_list_from_file(file_path="blacklist.json"):
    dataDictBlackList = []
    with open(file_path, "r", encoding="utf-8") as f:
        dataDictBlackList = json.load(f)
    domain_set = set()
    for dicturl in dataDictBlackList:
        domain_set.add(get_domain_from_url(dicturl["url"]))
    print("Loaded {} domains from file {}".format(len(domain_set), file_path))
    return domain_set


domain_blacklist = load_domain_list_from_file("blacklist.json")

# find domain in blacklist
def send_to_AI_Server(dictData):
    global producer
    url=dictData.get("url")
    url,mode=get_real_url(url)
    if mode==MODEL_FULL_FEATURE:
        dictData["url"]=url
        topic_send=topic_model_full
    elif mode==MODEL_HALF_FEATURE:
        dictData["url"]=url
        topic_send=topic_model_half
    else:
        topic_send=topic_comare
        
    print(f"Send to {topic_send} Server: ", dictData)

    producer.send(topic_send, dictData)

def find_domain_in_blacklist(domain):
    global domain_blacklist
    return domain in domain_blacklist


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
            if find_domain_in_blacklist(get_domain_from_url(url)):
                print("Found domain in blacklist: ", url)
                dictData["is_phishing"] = "1"
                dictData["phishing_type"] = "blacklist"
                dictData["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                producer.send("result", dictData)
            else:
                send_to_AI_Server(dictData)
        except Exception as e:
            print("Error: ", e)

consumer.close()

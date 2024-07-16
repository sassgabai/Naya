from kafka import KafkaProducer
import time,json,requests
from datetime import datetime
import  configuration as c

while True:
    # ======== Read from Remote API  ==================== #
    response = requests.get(url=c.green_taxi_events_api)
    for line in range(len(response.json())):
        row = response.json()[line]
        print(row)
        time.sleep(1)
        #==============send to consumer==========================#
        producer = KafkaProducer(bootstrap_servers="course-kafka:9092")
        producer.send(topic="my_trip", value=json.dumps(row).encode('utf-8'))
    print(datetime.fromtimestamp(time.time()))
    time.sleep(3)

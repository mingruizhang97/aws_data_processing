import boto3
import json
import random
import time
import requests

kinesis = boto3.client(
    'kinesis',
    region_name = 'us-east-1'
)
def get_data():
    res = requests.get("https://randomuser.me/api/?results=2")
    res = res.json()
    res = res['results'][0]
    return res

def format_data(res):

    data = {}
    location = res['location']
    #data['id'] = uuid.uuid4()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

for i in range(100):
     res = get_data()
     res = format_data(res)
     payload = json.dumps(res)
     response = kinesis.put_record(
            StreamName="DataProcessingKinesis",
            Data=payload,
            PartitionKey=str(random.randint(1, 10))
        )
     print(f"RecordId: {response['SequenceNumber']}")

     time.sleep(1)


'''''
for i in range(5):
        data = {
        'timestamp': int(time.time()),
        'value': random.randint(1, 100)
    }
    
        payload = json.dumps(data)
    
        response = kinesis.put_record(
            StreamName="my-first-kinesis",
            Data=payload,
            PartitionKey=str(random.randint(1, 10))
        )

        print(f"RecordId: {response['SequenceNumber']}")

        time.sleep(1)
'''''
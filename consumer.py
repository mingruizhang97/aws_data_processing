import boto3
import time

kinesis = boto3.client(
    'kinesis',
    region_name = 'us-east-1'
)
response = kinesis.describe_stream(StreamName = 'my-first-kinesis')
my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis.get_shard_iterator(
    StreamName='my-first-kinesis',
    ShardId=my_shard_id,  
    ShardIteratorType='LATEST'  
)['ShardIterator']


response = kinesis.get_records(
        ShardIterator=shard_iterator,
        Limit=2  
    )
while 'NextShardIterator' in response:
    response = kinesis.get_records(ShardIterator = response['NextShardIterator'],
                                   Limit = 2)  
    print(response)
    time.sleep(2)
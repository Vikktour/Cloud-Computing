import json
import boto3

#for insert to dynamoDB
import csv
from decimal import Decimal
import datetime

#for elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from botocore.vendored import requests

"""
NYU Tandon
Cloud Computing
Victor Zheng
10-17-2019
Lambda function for dynamo insert, which grabs yelp data from S3 bucket (Note the data was originally obtained from yelp-fushion.py and uploaded to S3 bucket)
Data is also parsed to proper format and moved to ElasticSearch for fast querying for our dining app.
"""

def lambda_handler(event, context):
    # TODO implement
    
    """
    #get restaurant csv data from S3 bucket and then insert them into dynamoDB table
    dataList = getDataFromS3();
    for restaurant in dataList:
        dynamoInsert(restaurant)
    print("Done inserting to table")
    """
    
    #add to elasticIndex
    print("Getting dataList")
    dataList = getDataFromS3();
    #print("dataList: ", dataList)
    #dataList = dataList[1]
    elasticIndex(dataList)

    return {
        #'statusCode': 200,
        #'body': json.dumps('Hello from Lambda!')
    }

def getDataFromS3():

    s3 = boto3.resource(u's3')

    #get handle on bucket
    bucket = s3.Bucket(u'hw1cuisinedata')
    
    fileKey = "yelpData.csv"

    #get handle on object
    obj = bucket.Object(key=fileKey)
    print("object in bucket: ", obj)
    
    response = obj.get()
    
    
    lines = response['Body'].read().splitlines(True)
    #lines = response['Body'].read()
    final_list = []
    counter = 0
    for line in lines:
        counter += 1
        #print("counter: ",counter)
        if counter == 3:
            print("line being added: ", line)     
        final_list.append(line.decode('UTF-8')) #decode the binary format

    #print("final_list: ", final_list)
    print("final_list length: ", len(final_list))
    print("End of code")

    reader = csv.reader(final_list)

    dataDictionaryList = []
    i = 0
    print("start of row in reader")
    for row in reader:
        #print("inside row")
        #print("row: ", row)
        if i != 0:
            #if float(row[-1]) == 1.0:
                dataObject = {
                    'cuisine_type': row[0],
                    'business_id': row[1],
                    'name': row[2],
                    'address': row[3],
                    'coordinates': {'longitude': Decimal(row[4]),'latitude:': Decimal(row[5])},
                    'num_reviews': int(row[6]),
                    'rating': Decimal(row[7]),
                    'zipcode': int(row[8]),
                    #add a timestamp
                    'insertedAtTimestamp': str(datetime.datetime.now())
                }
                dataDictionaryList.append(dataObject)
        i = i+1
        #print("i: ", i)
    print("done with rows")

    #print("dataDictionaryList length: ", len(dataDictionaryList)) #print the first value to verify
    #print("dataDictionaryList[1]: ", dataDictionaryList[1]) #print the first value to verify, (not sure why [0] doesn't work)
    #print("dataDictionaryList: ", dataDictionaryList)
    return dataDictionaryList

#pass in a restaurant that is already formated for the right attributes (e.g getDataFromS3)
def dynamoInsert(restaurantItem):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('yelp-restaurants')
    
    #print("restaurant item to insert: ", restaurantItem)
    table.put_item(Item= restaurantItem)

"""
#Add index data to ElasticSearch
def elasticIndex(restaurants):
    host = 'https://search-hw1restaurants2-n4hj7inaadwu2grwsjorxsdoje.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'us-east-1'
    
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)
    
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        # http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    
    #restaurants = restaurants[1:3] #attempt to lower amount of restaurants for debug
    for each_restaurants in restaurants:
        
        dataObject = {
            'business_id': each_restaurants['business_id'],
            'cuisine_type': each_restaurants['cuisine_type']
        }
        
        # alreadyExists = es.indices.exists(index="restaurants")
                            
        print ('dataObject', dataObject)
        
        # if alreadyExists:
        indexName = "hw1restaurants2"
        print("attempting to index")
        #es.index(index=indexName, doc_type="Restaurant", id=each_restaurants['business_id'], body=dataObject, refresh=True)
        es.index(index=indexName, id=each_restaurants['business_id'], body=dataObject, refresh='wait_for')
        print("Done indexing")
        # else:
        #     es.create(index="restaurants", doc_type="Restaurant", body=dataObject)
"""
def elasticIndex(restaurants):
    #host = 'https://search-hw1restaurants2-n4hj7inaadwu2grwsjorxsdoje.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    host = 'search-hw1try3-h4blgrryb4syisdcz5jb4ybjzq.us-east-1.es.amazonaws.com'
    region = 'us-east-1'
    
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)
    

    print("Starting Elasticsearch()")
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        # http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    print("Done with Elasticsearch()")
    for each_restaurants in restaurants:
        
        dataObject = {
            'business_id': each_restaurants['business_id'],     
            'cuisine_type': each_restaurants['cuisine_type']
        }
        
        # alreadyExists = es.indices.exists(index="restaurants")
                            
        print ('dataObject', dataObject)
        
        print("Adding to es.index")
        # if alreadyExists:
        es.index(index="hw1try3", doc_type="Restaurant", id=each_restaurants['business_id'], body=dataObject, refresh=True)




if __name__ == '__main__':

    lambda_handler(None,None)


#lambda_function.lambda_handler
#lambda_dynamo.lambda_handler //if this file is called lambda_dynamo.py, we have to modify the lambda_handler
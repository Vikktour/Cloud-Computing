Dining App

This is the code I contributed for the Dining App assignment in Cloud Computing.
I utilized yelpfushion.py to retrieve data from yelp, and then parsed and formatted the retrieved data into a file.
This data is then parsed again in Lambda1.0 (a lambda function placed in AWS) to take the yelp data (uploaded to S3 bucket),
and insert it into DynamoDB (AWS noSQL database) and also to ElasticSearch.

Summary:
* Pulled Yelp's restaurant data with Yelp Fusion API. Formatted the data into a file, which is then parsed using lambda functions to push the data into dynamoDB
* AWS: S3, API Gateway, Lambda, Lex, SQS, SNS, DynamoDB, ElasticSearch
* Programming: Python, noSQL, csv, json

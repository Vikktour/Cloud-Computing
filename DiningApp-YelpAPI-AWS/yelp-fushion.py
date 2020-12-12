# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""

"""
NYU Tandon
Cloud Computing
Victor Zheng
10-12-2019
Querying API for yelp data, pack data into json, which can be inserted into DynamoDB and used to fill data for dining suggestions.
"""

from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import csv

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY = ""


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

"""
# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
"""
#Querying for Cloud Computing Hw1

#DEFAULT_TERM = 'Chinese'
#DEFAULT_TERM = 'American Cuisine'
#DEFAULT_TERM = 'Thai Cuisine'
#DEFAULT_TERM = 'Mexican Cuisine'
#DEFAULT_TERM = 'Indian Cuisine'
#DEFAULT_TERM = 'Chinese Cuisine'
#DEFAULT_TERM = 'Vietnamese Cuisine'
#DEFAULT_TERM = 'Japanese Cuisine'
#DEFAULT_TERM = 'Soul Food'
#DEFAULT_TERM = 'Italy'
#DEFAULT_TERM = 'French Cuisine'
DEFAULT_LOCATION = 'Manhattan, NY'
SEARCH_LIMIT = 50
#SEARCH_LIMIT = 2
#offset = 0
data = [] #for adding in cuisine data and dumping into file at the end

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, offset):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
        offset (int): I added this to get more unique queries (past 50 limit)
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, 0)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    #pprint.pprint(response, indent=2)

    #saving to JSON file
    #Get the file name for the new file to write
    #filename = "ChineseCuisine.json"
    filename = "AmericanCuisine.json"

    # If the file name exists, write a JSON string into the file.
    if filename:
        # Writing JSON data
        count = 0
        with open(filename, 'a') as f:
            json.dump(response, f)

def query_api_multiple(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """

    
    count = 0 #to keep track of how many items are appended per cuisine
    #since there's a limit of 50 yelp business returns, we use offset to get unique ones in the next 50
    #for i in range(0,3):
    for i in range(0,10):
        offset = SEARCH_LIMIT*i
        try:
            response = search(API_KEY, term, location, offset)
            businesses = response.get('businesses')
        except:
            #there's a connection error
            businesses = None

        
        
        if not businesses:
            print(u'No businesses for {0} in {1} found with offset{2}.'.format(term, location,offset))
            return
        
        #print(u'{0} businesses found, querying business info ' .format(len(businesses)))

        
        #loop through businesses append to data to be written to json
        for business in businesses:
            business_id = business['id']
            
            #Store only: Business ID, Name, Address, Coordinates,Number of Reviews, Rating, Zip Code
            #pprint.pprint(response, indent=2)
            try:
                response = get_business(API_KEY, business_id)
                tempDict = {}
                tempDict["cuisine_type"] = term
                tempDict["business_id"] = response["id"]
                tempDict["name"] = response["name"]
                tempDict["address"] = response["location"]["address1"] #response[location[address1]]
                tempDict["coordinates"] = response["coordinates"]
                tempDict["num_reviews"] = response["review_count"] #response[location[review_count]]
                tempDict["rating"] = response["rating"]
                tempDict["zipcode"] = response["location"]["zip_code"]

                ##print(u'Result for business "{0}" found'.format(business_id)) #business found, there's the id
                #pprint.pprint(response, indent=2)
                #print("term: ", term)
                data.append(tempDict)
                #print("appended to data: ", tempDict)
                count += 1
            except KeyError:
                print(u'KeyError for person "{0}". Not appending this.'.format(business_id))
    
    print("Appended {0} values for {1}".format(count,term))
            
            

def main():

    #DefaultTerms = ['American Cuisine','Thai Cuisine','Mexican Cuisine','Indian Cuisine','Chinese Cuisine','Vietnamese Cuisine','Japanese Cuisine','Soul Food','Italy Cuisine','French Cuisine']
    DefaultTerms = ['Italy Cuisine','French Cuisine','Vegetarian Cuisine'] #add 3 more cuisines since the previous run ran out of api calls at around 900

    #for each of the search terms, get data and save as searchTerm.json
    for defaultTerm in DefaultTerms:

        parser = argparse.ArgumentParser()

        parser.add_argument('-q', '--term', dest='term', default=defaultTerm,
                            type=str, help='Search term (default: %(default)s)')
        parser.add_argument('-l', '--location', dest='location',
                            default=DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')

        input_values = parser.parse_args()

        try:
            query_api_multiple(input_values.term, input_values.location)
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )

    #insert all the data into yelpData.json
    filename = "YelpData/yelpData.json"
    #filename = "YelpData/yelpData.json"
    # If the file name exists, write a JSON string into the file.
    if filename:
        # Writing JSON data
        with open(filename, 'w') as f:
            json.dump(data,f)


if __name__ == '__main__':
    main()
    #NOTE RUN THIS USING PYTHON 3.7, otherwise the dictionary is unorderd (e.g. instead of business_id being first, we have ratings)

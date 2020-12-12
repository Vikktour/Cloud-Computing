/*
Code from tutorial: https://youtu.be/ijyeE-pXFk0
Node.js 8.10

NYU Tandon
Cloud Computing
Victor Zheng
10-11-2019

This code will insert an entry to the dynamoDB table with a certain business_id and display it onto terminal
*/

'use strict'
const AWS = require('aws-sdk');

AWS.config.update({ region: "us-east-1"});

exports.handler = async (event, context) => {
    //const ddb = new AWS.DynamoDB({apiVersion: "2012-10-08"});
    const documentClient = new AWS.DynamoDB.DocumentClient({region: "us-east-1"});
    
    //define params to be the new row of data inserted
    const params = {
        TableName: "yelp-restaurants",
        Item: {
            business_id: "testingId123",
            cuisine_type: "American Cuisine",
            name: "Bea", 
            address: "403 W 43rd St", 
            coordinates: {"latitude": 40.7591968, "longitude": -73.9923361}, 
            num_reviews: 2390, 
            rating: 4.0, 
            zipcode: "10036"    
        }
    }

    try{
        const data = await documentClient.put(params).promise();
        console.log(data);
    }
    catch(err){
        console.log(err);
    }

}
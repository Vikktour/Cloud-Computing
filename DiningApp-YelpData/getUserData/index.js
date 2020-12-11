/*
Code from tutorial: https://youtu.be/ijyeE-pXFk0
Node.js 8.10

NYU Tandon
Cloud Computing
Victor Zheng
10-11-2019

This code will take an entry from the dynamoDB table with a certain business_id and display it onto terminal
*/

'use strict'
const AWS = require('aws-sdk');

AWS.config.update({ region: "us-east-1"});

exports.handler = async (event, context) => {
    //const ddb = new AWS.DynamoDB({apiVersion: "2012-10-08"});
    const documentClient = new AWS.DynamoDB.DocumentClient({region: "us-east-1"});
    
    const params = {
        TableName: "yelp-restaurants",
        Key: {
            business_id: "Rc1lxc5lSKJYd162JHNMfQ"    
        }
    }

    try{
        const data = await documentClient.get(params).promise();
        console.log(data);
    }
    catch(err){
        console.log(err);
    }

}
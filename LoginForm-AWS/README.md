This is a partial implementation of a Ecommerce website.
I created a login form that utilizes AWS services to host the site.


Upon registration, the user login data is stored in DynamoDB database.
Upon login, a request to the server checks to see if the user matches with it's password. If yes, then the user is signed in.

AWS services used: S3, API Gateway, DynamoDB

Part of the login webpage implementation source code: 
https://www.youtube.com/watch?v=OWNxUVnY3pg&ab_channel=EasyTutorials
http://www.avinashkr.com/blog/create-login-form-in-html-css/
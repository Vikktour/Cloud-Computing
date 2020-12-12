function register(x,y) {
    var apigClient = apigClientFactory.newClient(); //defined in sdk
    let params = {};
    var body = {
        email: x,
        password: y
    };
    additionalParams = {};
    apigClient
        .registerPost(params, body, additionalParams) //apigateway loginPost
        .then(function(result) {
            //alert("test alert in then")
            m = result.data.body;
            console.log("main.js body: ",m);
            window.location.href = "index.html"
        })
        .catch(function(result) { //if not 200
            alert("alert in catch")
            console.log("main.js catch result: ",result);
        });
}


function login(x,y){
    console.log(`main.js login version 2 x:${x},y:${y}`);
    console.log("callLogin 1")
    var apigClient = apigClientFactory.newClient(); //defined in sdk
    let params = {};
    var body = {
        email: x,
        password: y
    };
    
    var additionalParams = {};/*
    var apigClient = apigClientFactory.newClient({
        accessKey: "",
        secretKey: "",
        region: "us-east-1"
    });*/
    
    
    apigClient
        .loginPost(params, body, additionalParams) //apigateway loginPost
        .then(function(result) {
            //debugger;
            m = result.data.body;
            console.log("statusCode: ", result.data.statusCode)
            if(result.data.statusCode == 200){
                //alert("login successful")
                window.location.href = "home.html"
            }
            else if (result.data.statusCode == 400){
                alert("incorrect login")
            }
            else{
                alert("neither 200 nor 400")
            }
            console.log("main.js body: ",m);
        })
        .catch(function(result) { //if not 200 (wrong password), then throw error
            alert("Error in catch");
            //console.log("main.js catch result: ",result);
        });
}
var express = require('express');
var app = express();
var bodyParser = require('body-parser');


var fs = require('fs');
var path = require('path');
var axios = require('axios')
var FormData = require('form-data');
var md5File = require('md5-file');
var url = require('url');

var http = require('http');

const { response } = require('express');

const PORT = process.env.PORT || 3000;
let httpServer= app.listen(PORT, () => console.log(`HTTP server listening at http://localhost:${PORT}`));



app.engine('.html', require('ejs').__express);
app.set('views', __dirname + '/views');
app.set('view engine', 'html');

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended : false}));


app.get('/', function (req, res) {
    // if(!req.session.name)
    //     res.redirect('/main');
    // else   
        res.redirect('/main');

});

//main page
app.get('/main', function (req, res) {
    
    res.render('main.html');
    
});


//login page
app.get('/login', function (req, res) {
    
    res.render('login.html');

});
 
app.post('/login', async function (req, res) {
    console.log("try login")
    try{
        
        data=0
        const test_result = await axios.post('http://127.0.0.1:5000/api/v1/user/login')
        console.log(test_result)
        
        
        console.log(test_result);
    
        
        
               
    }catch(e){console.log("[ERROR|success login] : ",e)}
    

});

//logout page
app.get('/logout',async function(req,res){
    try{
        
        var test_result =  await axios.post('http://127.0.0.1:5000/api/v1/user/logout', {
            
            headers: { 'access_token': '1234', 'Content-Type': 'application/json' }
            
        });
            
        //res.end();  //클라이언트에게 응답을 전송한다
        

        console.log("post image to pre_test")
        console.log(test_result)
        console.log(test_result.status)
        console.log(test_result.data)
        
        if(test_result.status == 200){
            test_result_responsedata = test_result.data
            console.log("ssssssssssss")
            console.log(test_result_responsedata)
            
        }
        res.json(test_result.data)       
    }catch(e){console.log("[ERROR|success pass pre_test error] : ",e)}

	res.redirect("/main");
});




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

//로그인 페이지 (앱을 키면 가장 먼저 보이는 화면)
//로그인 GET
app.get('/main', function (req, res) {
    //if(!req.session.name)
        res.render('main.html');
    // else  
    //     res.redirect('/pre_user_main');

 });

app.get('/login', function (req, res) {
    //if(!req.session.name)
        res.render('login.html');
    // else  
    //     res.redirect('/pre_user_main');

 });
 




app.get('/logout',function(req,res){//로그아웃기능
    	
	res.redirect("/main");
});




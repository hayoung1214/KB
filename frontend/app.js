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
 






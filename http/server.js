// variables
var APPPORT = 80;
var APPTITLE = "sprayBot"
var express = require('express');
var app = express();
var engine = require('ejs').__express;
var p1State = "";
var p2State = "";

// app configurations
app.set('views', __dirname+'/views');
app.set('view engine', 'ejs');
app.use("/css", express.static(__dirname + '/views/css'));

// index page 
app.get('/', function(req, res) {

  var relay = req.query['relay'] || "none";
  var state = req.query['state'] || "none";

  var execSync = require('exec-sync');

  if ( relay != "none" && state != "none") {
    execSync('/appli/bin/relay.py ' + relay + ' ' + state);
  }

  // relay 1
  var data = execSync('/usr/local/bin/gpio -g read 17');
  if ( parseInt(data) == 1 ) { p1State = "OFF"; }
  if ( parseInt(data) == 0 ) { p1State = "ON"; }

  // relay 2
  var data = execSync('/usr/local/bin/gpio -g read 18');
  if ( parseInt(data) == 1 ) { p2State = "OFF"; }
  if ( parseInt(data) == 0 ) { p2State = "ON"; }

  res.render('pages/index', {
    title: APPTITLE,
    p1State: p1State,
    p2State: p2State
  });
});

// error page
app.use(function(req, res, next){
  res.status(404);

  if (req.accepts('html')) {
    res.render('pages/error', {
      title: APPTITLE,
      errorCode: '404',
      errorDesc: 'The page ' + req.url + ' is not found on this server'
    });
  }
});

app.listen(APPPORT);
console.log('HTTP(s) server is running on port ' + APPPORT);

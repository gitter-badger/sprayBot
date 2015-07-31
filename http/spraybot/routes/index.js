var express = require('express');
var router = express.Router();
var config = require('../config/config.global.js');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { appTitle: config.appTitle + " - Accueil" });
});

module.exports = router;

var express = require('express');
var router = express.Router();

var data = {};
var score = 0;

/* GET home page. */
router.get('/', function(req, res, next) {
  	res.render('index.html', { title: 'Demo' });
});

router.post('/', function(req, res, next) {
	console.log(req);
	var body = req.body;
	score = body['score'];
	delete body['score'];
	data = body;
})

router.get('/data', function(req, res, next) {
	res.send(data);
})

router.get('/score', function (req,res,next) {
	res.send(score);
})

module.exports = router;

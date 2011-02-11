var express = require('express');
var mustache_view = require('./mustache_view');
var app = express.createServer();

app.configure(function() {
    app.use(app.router);
    app.register(".html", mustache_view);
    app.set("view options", {layout: false});
    app.set('views', __dirname + '/views');
    app.use(express.bodyDecoder());
    app.use(express.methodOverride());
    app.use(app.router);
    app.use(express.staticProvider(__dirname + '/public'));
});

app.configure('development', function(){
    app.use(express.errorHandler({ dumpExceptions: true, showStack: true })); 
});

app.configure('production', function(){
    app.use(express.errorHandler()); 
});

// Routes

app.get('/', function(req, res){
    res.render('index.html', {
        locals: {
            title: 'Express'
        }
    });
});

// Only listen on $ node app.js

if (!module.parent) {
  app.listen(3000);
  console.log("Express server listening on port %d", app.address().port)
}

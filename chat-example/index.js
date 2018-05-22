let app = require('express')();
let http = require('http').Server(app);
let io = require('socket.io')(http);
users = {}

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html')
});

io.on('connection', function(socket){
    // Log when a user connects
    socket.on('chat message', function(msg){
        console.log('hi')
       io.emit('chat message', msg);
    });
});

http.listen(5000, function(){
    console.log('listening on *:5000');
});
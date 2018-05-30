// initialize express
let app = require('express')();
// pass the app to the server
let http = require('http').Server(app);
// pass in http to the socket
let io = require('socket.io')(http);

// when app.get takes the route, it will call the callback function.
app.get('/chat', function(req, res){
    res.sendFile(__dirname + '/templates/chat.html')
});

// everytime someone joins the server, will receive the message
io.on('connection', function(socket){
    socket.on('chat message', function(msg){
    io.emit('chat message', msg);
    });
});

// when server is opened.
http.listen(5000, function(){
    console.log('listening on *:5000');
});



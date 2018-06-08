$(document).ready(function() {

    let sessionIds = [];

    function getSessionIds(){
        $.get('/matches_for_chat.json', function(sessionId){
            sessionIds.push(...sessionId)
        });
    }
    getSessionIds()


    // Chat socket.io
    namespace='/munchbuddies';

    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function() {
        console.log('connected');
    
        if (sessionIds){
            sessionIds.forEach(function(userId) {
                socket.emit('join', { room: String(userId) });
            });
        }

        
        $('.user-id').click(function(event){
            $(".notification-box").attr('hidden', true)
            $('.panel-default').attr('hidden', false)
            $("form#send_room").show();
            

            let room = $(this).attr('target')
            let name_id = $(this).attr('name')

            socket.emit('join', {room: room});

            function displayMessages(results) {
                let messages = results;
                $('#log').html(messages);
                if (messages[room]){
                    for (let message in messages[room]){
                        $('#log').append(`
                                <p><small><small><i> 
                                ${messages[room][message]['date']} 
                                </i></small></small><br>
                                ${messages[room][message]['from']}: 
                                ${messages[room][message]['message']} </p>`);
                    }
                }
                
            };

            function getMessages() {
                $.get('/messages.json', displayMessages);
            };

            getMessages();

            let msgSender = new Object({name:""});
            function getSenderName(){
                $.get('/sender_name', function(senderName){
                    let result = senderName
                    msgSender.name = result
               
                });
            }

            getSenderName();

            $('form.mess').submit(function(event) {
                let msg = {sender: msgSender.name,
                          receiver_id: name_id,
                          room: room,
                          meg: 'You have a message from',
                          data: $('#room_data').val()}
                socket.emit('my_room_event', msg);
                $('#room_data').val('');

                return false;
            });

            $('.close-chat').click(function(event) {
                event.preventDefault()
                setInterval(window.location.reload(), 1000);                
                return false;
            });

            socket.on('my_response', function(msg) {
                $('#log').append(`<p> ${msg.sender}: ${msg.data}</p>`);

            });
        });
            socket.on('my_response', function(msg) {
            $('.notification-box').append(`<p> ${msg.meg} ${msg.sender} </p>`)
            $('.notification-box').fadeIn(100).fadeOut(10000);
        });
    });
});




function addRestaurant(restaurant){
    $.post('/add_restaurant', {data: restaurant}, function(data){
        $('#restaurants').append(`
            <p id=${restaurant}> 
                  <img src=${data[restaurant]['image']} width="50px" height="50px"> 
                  <a href=${data[restaurant]['url']}>
                    ${data[restaurant]['title']}
                  </a>
                  <button id=${restaurant} onClick='deleteRestaurant(this.id)'>DELETE</button>
              </p>
            `);
    });
}


$('.restaurant-suggestion').on('click', function(evt) {
    event.preventDefault()
    let id = this.id;
    console.log(id);
    $('#card-'+id).attr('hidden', false);
});

$('.close-restaurant').on('click', function() {

    $('.restaurant-card').attr('hidden', true);
})



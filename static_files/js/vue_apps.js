Vue.config.devtools = true;

var photoshop = VueColor.Photoshop;
var chrome = VueColor.Chrome;
var compact = VueColor.Compact;
var swatches = VueColor.Swatches;
var sketch = VueColor.Sketch;
var material = VueColor.Material;
var slider = VueColor.Slider;

var colors = {
  hex: '#2F2F2F',
  hsl: { h: 150, s: 0.5, l: 0.2, a: 1 },
  hsv: { h: 150, s: 0.66, v: 0.30, a: 1 },
  rgba: { r: 25, g: 77, b: 51, a: 1 },
  a: 1
};

var chat = new Vue({
    el: '#chatapp',
    delimiters: ['[[', ']]'],

    data: {
        distance: 10,
        token: 'token',
        chat_username: null,
        chat_user_id: null,
        loggedOut: true,
        loggedIn: false,
        members: [],
        rooms: [],
        errors: [],
        session: null,
        channel_user: null,
        is_user_channel: false,
        chattext:"",
        data: [],
        list: [],
        busy: false,
        colors: colors,
        newroom: null,
    },

    scroll: function (event) {
        var elem = document.getElementById("chat-window");

        if (elem) {
            elem.scrollTop = elem.clientHeight*10000000;
        }
    },

    beforeRouteEnter(to,from,next){
        this.session = VueSession.getInstance();
        this.loggedOut = true;
        this.loggedIn = false;
        this.room(1);
        var elem = document.getElementById("chat-window");

        if (elem) {
            elem.scrollTop = elem.clientHeight*10000000;
        }

    },

    created: function () {
      
        var room_name = $('#room-name-1').val();
        $('#chattext').val("");
        $('#active-room').attr('value', 1);
        $('#active-room-name').attr('value', "Курилка");
        $('#current-channel').html("<strong>Курилка=></strong>");
        this.room(1);
      //  this.refresh_color();
        var elem = document.getElementById("chat-window");

        if (elem) {
            elem.scrollTop = elem.clientHeight*10000000;
        }

    },
    methods: {
            
           scroll: function (event) {
                var elem = document.getElementById("chat-window");
                if (elem) {
                     elem.scrollTop = elem.clientHeight*10000000;
                }
           },
           update: function (event) {
               this.is_user_channel = eval($('#is-user-channel').val());
               if (this.is_user_channel) {
                   let user_id = $("#active-room-user-id").val();
                   this.user(user_id);
               } else {
                   let room_id = $('#active-room').val();
                   let room_name = $('#active-room-name').val();
                   if (room_id) { 
                       this.room(room_id);
                   } else {
                  //     this.room(1);
                   }
               }
               this.sync_incoming();
               return false;
           },
           sync_incoming: function (event) {

               let user_id = $("#chat-user-id").val()
               
               if (user_id) {
                   let url = '/channels/?owner_id='+user_id;
                   $.get(url, function(data) {
                       if (data[0]['pending_messages'].length) {
                           $('.pending-user').html("<span onclick='user("+user_id+");' class=\"red\" style=\"font-size:0.88em;color:#ff0000;font-weight:bold;transition: all .2s ease-out;\">"+data[0]['pending_messages'].length+"</span>");
                       }   
                   });
               }
           },
           enterchat: function (event) {
               this.refresh_color(); 
               this.data = [];
               this.chat_username = $('#session_user_name').val();
               this.chat_user_id =  $('#user_id').val();
               $('#chat-user-id').attr('value', this.chat_user_id); 
               $('#chattext').attr("value","");

               var arr = {
                   "user_id": this.chat_user_id
               };

               this.colors.hex = this.read_color(); 


               $.ajax({
                    type: "POST",
                    url: "https://lovehate.io/chat/enter/",
                    crossDomain: true,
                    data: JSON.stringify(arr),
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    success: function(data) {
                       redirect_url('chat');
                    },
                    error: function(data){
                      console.log("failure: "+data);
                    }
               });

                 $('#active-room').attr('value', 1);
                 $('#active-room-name').attr('value', "Курилка");
                 $.get('/chatmessages?room_id='+room_id, function(data)
                {

                            var messages = "";
                            var temp = [];
                            for(var i=0; i<data.length; i++) {
                                var list_item = "<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username']+" - "+data[i]['body']+"</div>";
                                temp.push(list_item);
                                messages = messages+"<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username'];
                                messages = messages+" - "+data[i]['body'];
                                messages = messages+"</div>";
                            }
                            this.list = temp;
                         //   $("#chat-window").html(messages);
                            $("#chattext").attr("value","");

                });
                this.room(1);
                var elem = document.getElementById("chat-window");

                if (elem) {
                    elem.scrollTop = elem.clientHeight*10000000;
                }

                return false;
            },

            exitchat: function (event) {
              // this.refresh_color(); 
               this.chat_username = $('#session_user_name').val();
               this.chat_user_id =  $('#user_id').val();
               $('#chat-user-id').attr('value', null);
               var arr = {
                   "user_id": this.chat_user_id
               };

               $.ajax({
                    type: "POST",
                    url: "https://lovehate.io/chat/exit/",
                    crossDomain: true,
                    data: JSON.stringify(arr),
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    success: function(data) {
                        redirect_url('chat'); 
                    },
                    error: function(data){
                        console.log("failure:"+data.message);
                    }
               });

               var elem = document.getElementById("chat-window");

               if (elem) {
                   elem.scrollTop = elem.clientHeight*10000000;
               }

               return false;
            },

            user: function(user_id) {
                // this.refresh_color();
                 let chat_user_id = $("#chat-user-id").val();
                 let room_id = $('#active-room').val();
                 this.leave_room(room_id);

                 if (chat_user_id==user_id) {

                    var arr = {
                        "user_id": user_id,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/cleanpending/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                             $('.pending-user').html("");
                        },
                        error: function(data) {
                        }
                    });

                 }

                 this.is_user_channel = true;
                 $("#is-user-channel").attr("value",true);

                 this.data = [];
                 let url = '/chatmessages?receivers='+user_id;
                 $.get(url, function(data)
                {
                            var messages = "";
                            var temp = [];
                            for(var i=0; i<data.length; i++) {
                                var list_item = "<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username']+" - "+data[i]['body']+"</div>";
                                temp.push(list_item);

                                messages = messages+"<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username'];
                                messages = messages+" - "+data[i]['body'];
                                messages = messages+"</div>";

                            }
                            this.list = temp;

                            $("#chat-window").html(messages);

                            var elem = document.getElementById("chat-window");

                            if (elem) {
                              elem.scrollTop = elem.clientHeight*10000000;
                            }


                });

                var user = $("#chat-active-user-"+user_id).val();

                $('#active-room-user-id').attr('value', user_id); 
                $('#active-room-name').attr('value', user);

                this.channel_user = user;

//                $('#current-channel').html("<strong>@"+user+"=></strong>");

                var elem = document.getElementById("chat-window");

                if (elem) {
                     elem.scrollTop = elem.clientHeight*10000000;
                }

            },
            room: function (room_id) {
                 //this.refresh_color();
                 let chat_user_id = $('#chat-user-id').val();
                 this.data = [];
                 this.is_user_channel = false;
                 $("#is-user-channel").attr("value", false);
                 var room_name = $('#room-name-'+room_id).val();     
                 $('#current-channel').html("<strong>"+room_name+"=></strong>");
                 $('#active-room').attr('value', room_id);
                 $('#active-room-name').attr('value', room_name);
                 $('#chattext').attr("value","");

                 this.join_room(room_id);

                 $.get('/chatmessages?room_id='+room_id, function(data)
                {

                            var messages = "";
                            var temp = [];
                            for(var i=0; i<data.length; i++) {
                                var list_item = "<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username']+" - "+data[i]['body']+"</div>";
                                temp.push(list_item);
                                messages = messages+"<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username'];
                                messages = messages+" - "+data[i]['body'];
                                messages = messages+"</div>";

                            }
                            this.list = temp;
                            $("#chat-window").html(messages);

                            var elem = document.getElementById("chat-window");
                            if (elem) {
                                  elem.scrollTop = elem.clientHeight*10000000;
                            }

                });
            },
            talk: function (event) {
            //    this.refresh_color();
                let chat_user_id = $('#chat-user-id').val();
                let message = $('#chattext').val();
                $('#chattext').val("");
                let current_color = $('#current-color').val();
                this.chat_user_id = $("#user_id").val();
                $.get("/profiles?id="+this.chat_user_id, function(data){
                    if (data[0]['chat_color']) {
                        $('#current-color').attr('value', data[0]['chat_color']);
                        current_color = data[0]['chat_color']; 
                    }
                });


                let active_room_id = $('#active-room').val();
                let active_room_name = $('#active-room-name').val();
                let is_default = false;
                if (!message || message.length==0) { 
                     return;
                }

                
                let user_messages = {};
                let room_messages = {};
                let users = message.match(/(?<=@)[\w\u0430-\u044f]+/ig);
                let rooms = message.match(/(?<=#)[\w\u0430-\u044f]+/ig); 
                //let rooms_texts =  message.match(/(?<=#(\w+)\s)\w+(\w+\s?){1,}/g);
                //let users_texts = message.match(/(?<=@(\w+)\s)\w+(\w+\s?){1,}/g);
//                let rooms_texts = message.match("/(?<=#([\w\u0451\u0430-\u044f]+)\s)([\,\.-\w\u0451\u0430-\u044f]+\s?){1,}/ig");
 //               let users_texts = message.match("/(?<=@([\w\u0451\u0430-\u044f]+)\s)([\,\.-\w\u0451\u0430-\u044f]+\s?){1,}/ig");
                let rooms_texts = message.match(/(?<=#([\w\u0451\u0430-\u044f]+)\s)([\,\.-\w\u0451\u0430-\u044f]+\s?){1,}/ig);
                let users_texts = message.match(/(?<=@([\w\u0451\u0430-\u044f]+)\s)([\,\.-\w\u0451\u0430-\u044f]+\s?){1,}/ig);


                var start_message = message.split(/(?:@|#)+/)[0];

                if (start_message && start_message.length > 0) {
                   is_default=true;
                } 
                if (rooms && rooms_texts) {
      //              is_default = false;
                    for(var i=0; i<rooms.length; i++) {
                        rooms_texts[i] = rooms_texts[i].replace(/^\s+|\s+$/g, "");
                        if (!room_messages[rooms_texts[i]]) {
                           room_messages[rooms_texts[i]] = [];
                        } 

  
                        var room = {};
                        room['room'] = rooms[i];
                        room['sender'] = this.chat_user_id;
                          
                        room_messages[rooms_texts[i]].push(room);
                    }
                } 
                if (users && users_texts) {

        //            is_default = false;


                    for(var i=0; i<users.length; i++) {
                        users_texts[i] = users_texts[i].replace(/^\s+|\s+$/g, "");
                        if (!user_messages[users_texts[i]]) {
                            user_messages[users_texts[i]] = [];
                        }  
                       
                        var user = {};
                        user['user'] = users[i];
                        user['sender'] = this.chat_user_id;
                        user_messages[users_texts[i]].push(user);

                    }
                }
                
               
                Object.keys(user_messages).forEach(function(key) {
                    let users_str = "";
                    let userlist = user_messages[key];
                    for(var i=0; i<userlist.length; i++) {
                        
                        users_str = users_str+userlist[i]['user'];
                        if (i < userlist.length-1) {
                             users_str = users_str+",";
                        }
                    }

                    var arr = {
                        "users": users_str,
                        "message": key,
                        "sender_id": $("#user_id").val(),
                        "color": current_color, 
                    };
                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postusers/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                            //redirect_url('chat');
                            $("#chattext").attr("value","");
                        },
                        error: function(data){
                            console.log("Failure - "+data);
                        }
                    });


                });


                Object.keys(room_messages).forEach(function(key) {
                    let rooms_str = "";
                    let roomlist = room_messages[key];
                    for(var i=0; i<roomlist.length; i++) {
                        rooms_str = rooms_str+roomlist[i]['room']
                        if (i < roomlist.length-1) {
                            rooms_str = rooms_str+",";
                        }
                    }
                    
                    var arr = {
                        "rooms": rooms_str,
                        "message": key,
                        "active_room": $('#active-room').val(),
                        "sender_id": $("#user_id").val(),
                        "color": current_color,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postrooms/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                           // redirect_url('chat');
                            var messages = "";
                            var temp = [];
                            for(var i=0; i<data['messages'].length; i++) {
                                var list_item = "<div style=\"color:"+data['messages'][i]['color']+"\"> @"+data['messages'][i]['sender']['username']+" - "+data['messages'][i]['body']+"</div>";
                                temp.push(list_item);
                                messages = messages+list_item;
                            }

                            var roomHtml = "<div>";
                            for(var i=0; i<data["rooms"].length; i++) {
                                 var room_users = "";
                                 if (data["rooms"]["active_users"].length > 0) {
                                     room_users = " - "+data["rooms"]["active_users"].length;
                                 }

                                 var delete_room = "<span style='text-decoration:none;font-weight:bold;font-size:1.8em;'>&nbsp;</span>";

                                 if (chat_user_id==data["rooms"][i]["creator"]["id"]) {
                                     delete_room = "<a href=\"#\" style=\"text-decoration:none;font-weight:bold;font-size:1.8em;\">-</a>";
                                 }

                                 roomHtml=roomHtml+"<div class='neutral-messages' style='padding-top:0.0em;padding-bottom:0.0em;'>";
                                 roomHtml=roomHtml+"<div style='float:left;width:86%;' id='room-"+data["rooms"][i]['id']+"' onclick='room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;'>";
                                 roomHtml=roomHtml+data["rooms"][i]['name']+room_users;
                                 roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data["rooms"][i]['id']+"\" value=\""+data["rooms"][i]['name']+"\" />";
                                 roomHtml=roomHtml+"</div>"
                                 roomHtml=roomHtml+"<div id='delete-room-";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+"' style='width:12%;float:left;margin-top:-0.6em;' onclick=\"delete_room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;\">"+delete_room+"</div><div class='clear'></div></div>";
 


                            }
                            let current_room_name = $('#active-room-name').val();
                            $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
                            $("#active-room-name").attr("value", current_room_name);
                            $('#rooms-container').html(roomHtml);

                            this.list = temp;
            //                redirect_url('chat');
                            $("#chat-window").html(messages);

                            var elem = document.getElementById("chat-window");

                            if (elem) {
                                 elem.scrollTop = elem.clientHeight*10000000;
                            }

                            $("#chattext").val("");
                         
                        },
                        error: function(data){
                            alert("Failure - "+data);
                        }
                    });
                 

                });



                
                if (is_default && this.is_user_channel) {
                    var arr = {
                        "users": this.channel_user,
                        "message": message,
                        "sender_id": $("#user_id").val(),
                        "color": current_color,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postusers/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
 //                       alert("call time two");
                        var messages = "";
                        var temp = [];
/*
                        for(var i=0; i<data['messages'].length; i++) {
                              var list_item = "<div style=\"color:"+data['messages'][i]['color']+"\"> @"+data['messages'][i]['sender']['username']+" - "+data['messages'][i]['body']+"</div>";
                              temp.push(list_item);
                              messages = messages+"<div style=\"color:"+data['messages'][i]['color']+"\"> @"+data['messages'][i]['sender']['username'];
                              messages = messages+" - "+data['messages'][i]['body'];
                              messages = messages+"</div>";
                        }
                        this.list = temp;
                        $("#chat-window").html(messages);

                        var elem = document.getElementById("chat-window");

                        if (elem) {
                            elem.scrollTop = elem.clientHeight*10000000;
                        }
*/
                        
                        },
                        error: function(data){
                            console.log("Failure - "+data);
                        }
                    });


                     
                }
                else if (is_default && !this.is_user_channel) {
                    var rooms_str = $('#active-room').val();

                    var arr = {
                        "rooms": $('#active-room-name').val(),
                        "message": message,
                        "active_room": $('#active-room').val(),
                        "sender_id": $("#user_id").val(),
                        "color": current_color,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postrooms/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                            var messages = "";

                            var temp = [];
                            for(var i=0; i<data['messages'].length; i++) {
                                var list_item = "<div style=\"color:"+data['messages'][i]['color']+"\"> @"+data['messages'][i]['sender']['username']+" - "+data['messages'][i]['body']+"</div>";
                                chat.list.push(list_item);
                                messages = messages+list_item;
                                
                            }
                            this.list = temp;
                            $("#chat-window").html(messages);
                            var elem = document.getElementById("chat-window");

                            if (elem) {
                             elem.scrollTop = elem.clientHeight*10000000;
                            }

                            $("#chattext").attr("value","");
              //              redirect_url('chat');
                        },
                        error: function(data){
                            console.log("Failure - "+data);
                        }
                    });


                }

             /*
                if (rooms && rooms_texts) {
                    $.get("/rooms/", function(data){ 
                        var roomHtml = "<div>";
                        for(var i=0; i<data.length; i++) {
                             roomHtml=roomHtml+"<div id='room-"+data[i]['id']+"' onclick='room("+data[i]['id']+");return false;'>"+data[i]['name']+"</div>";
                             roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data[i]['id']+"\" value=\""+data[i]['name']+"\" />";
                        }
                        roomHtml=roomHtml+"</div>";
                        alert("ROOMS HERE "+roomHtml+" AND TOTAL "+data.length);
                        let current_room_name = $('#active-room-name').val();
                        $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
                        $("#active-room-name").attr("value", current_room_name);
                        $('#rooms-container').html(roomHtml);
                    });
                }
*/ 
/*
                if (start_message && start_message.length > 0) {

                    var rooms_str = $('#active-room').val();

                    var arr = {
                        "rooms": $('#active-room-name').val(),
                        "message": start_message,
                        "active_room": $('#active-room').val(),
                        "sender_id": $("#user_id").val(),
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postrooms/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                            var messages = "";

                       //     for(var i=0; i<data['messages'].length; i++) {
                        //        messages = messages+"<div> @"+data['messages'][i]['sender']['username'];
                        //        messages = messages+" - "+data['messages'][i]['body'];
                        //        messages = messages+"</div>";

                       //     }
                       //     $("#chat-window").html(messages);
                            $("#chattext").attr("value","");

                            var messages = "";

                            var temp = [];

                            for(var i=0; i<data['messages'].length; i++) {

                                var list_item = "<div> @"+data['messages'][i]['sender']['username']+" - "+data['messages'][i]['body']+"</div>";
                                temp.push(list_item);

                                messages = messages+"<div> @"+data['messages'][i]['sender']['username'];
                                messages = messages+" - "+data['messages'][i]['body'];
                                messages = messages+"</div>";

                            }
                            this.list = temp;
                    //        $("#chat-window").html(messages);
                            $("#chattext").attr("value","");
                         //   redirect_url('chat');
                         },
                         error: function(data){
                            alert("failure:"+data.message);
                         }
                    });

                }
*/
                for (var i = 0; i < user_messages.length; i++) {
                    
                }

                for (var i = 0; i < room_messages.length; i++) {

                }
/*
                alert("LET US COUNT ROOMS");
                    $.get("/rooms/", function(data){
                        var roomHtml = "<div>";
                        for(var i=0; i<data.length; i++) {
                             roomHtml=roomHtml+"<div id='room-"+data[i]['id']+"' onclick='room("+data[i]['id']+");return false;'>"+data[i]['name']+"</div>";
                             roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data[i]['id']+"\" value=\""+data[i]['name']+"\" />";
                        }
                        roomHtml=roomHtml+"</div>";
                        alert("OUR ROOMS HERE "+roomHtml+" AND TOTAL "+data.length);
                        let current_room_name = $('#active-room-name').val();
                        $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
                        $("#active-room-name").attr("value", current_room_name);
                        $('#rooms-container').html(roomHtml);
                    });
*/
                //this.room(active_room_id);
                var elem = document.getElementById("chat-window");
                if (elem) {
                    elem.scrollTop = elem.clientHeight*10000000;
                }
                $('#chattext').val("");
            },
            refresh_color: function (event) {
                var current_color = $('#current-color').val();
                current_color = this.read_color();
                $('#current-color').attr('value', current_color);
            },
            join_room: function (room_id) {

                 let chat_user_id = $('#chat-user-id').val();
                 let room_name =  $('#room-name-'+room_id).val();

                 var arr = {
                    "room_id": room_id,
                    "user_id": chat_user_id,
                 };

                 $.ajax({
                    type: "POST",
                    url: "https://lovehate.io/chat/join/",
                    crossDomain: true,
                    data: JSON.stringify(arr),
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    success: function(data) {
                      var messages = "";
                        var temp = [];

                        var roomHtml = "<div>";

                        for(var i=0; i<data["rooms"].length; i++) {
                            var room_users = "";
                            if (data["rooms"][i]["active_users"].length > 0) {
                                room_users = " - "+data["rooms"][i]["active_users"].length;
                            }

                                 var delete_room = "<span style='text-decoration:none;font-weight:bold;font-size:1.8em;'>&nbsp;</span>";

                                 if (chat_user_id==data["rooms"][i]["creator"]["id"]) {
                                     delete_room = "<a href=\"#\" style=\"text-decoration:none;font-weight:bold;font-size:1.8em;\">-</a>";
                                 }

                                 roomHtml=roomHtml+"<div class='neutral-messages' style='padding-top:0.0em;padding-bottom:0.0em;'>";
                                 roomHtml=roomHtml+"<div style='float:left;width:86%;' id='room-"+data["rooms"][i]['id']+"' onclick='room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;'>";
                                 roomHtml=roomHtml+data["rooms"][i]['name']+room_users;
                                 roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data["rooms"][i]['id']+"\" value=\""+data["rooms"][i]['name']+"\" />";
                                 roomHtml=roomHtml+"</div>"
                                 roomHtml=roomHtml+"<div id='delete-room-";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+"' style='width:12%;float:left;margin-top:-0.6em;' onclick=\"delete_room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;\">"+delete_room+"</div><div class='clear'></div></div>";






 
                        }

                        let current_room_name = $('#active-room-name').val();
                        $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
                        $("#active-room-name").attr("value", current_room_name);
                        $('#rooms-container').html(roomHtml);
                    },
                    error: function(data) {
                       console.log("Error joining room "+data);
                    }
                 });
                 return false;
            },


            leave_room: function (room_id) {

                 let chat_user_id = $('#chat-user-id').val();
                 let room_name =  $('#room-name-'+room_id).val();

                 var arr = {
                    "room_id": room_id,
                    "user_id": chat_user_id,
                 };

                 $.ajax({
                    type: "POST",
                    url: "https://lovehate.io/chat/leave/",
                    crossDomain: true,
                    data: JSON.stringify(arr),
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    success: function(data) {
                        var messages = "";
                        var temp = [];

                        var roomHtml = "<div>";

                        for(var i=0; i<data["rooms"].length; i++) {

                            var room_users = "";
                            if (data["rooms"][i]["active_users"].length > 0) {
                               room_users = " - "+data["rooms"][i]["active_users"].length;
                            }

                                 var delete_room = "<span style='text-decoration:none;font-weight:bold;font-size:1.8em;'>&nbsp;</span>";

                                 if (chat_user_id==data["rooms"][i]["creator"]["id"]) {
                                     delete_room = "<a href=\"#\" style=\"text-decoration:none;font-weight:bold;font-size:1.8em;\">-</a>";
                                 }

                                 roomHtml=roomHtml+"<div class='neutral-messages' style='padding-top:0.0em;padding-bottom:0.0em;'>";
                                 roomHtml=roomHtml+"<div style='float:left;width:86%;' id='room-"+data["rooms"][i]['id']+"' onclick='room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;'>";
                                 roomHtml=roomHtml+data["rooms"][i]['name']+room_users;
                                 roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data["rooms"][i]['id']+"\" value=\""+data["rooms"][i]['name']+"\" />";
                                 roomHtml=roomHtml+"</div>"
                                 roomHtml=roomHtml+"<div id='delete-room-";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+"' style='width:12%;float:left;margin-top:-0.6em;' onclick=\"delete_room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;\">"+delete_room+"</div><div class='clear'></div></div>";





                        }

                        let current_room_name = $('#active-room-name').val();
                        $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
                        $("#active-room-name").attr("value", current_room_name);
                        $('#rooms-container').html(roomHtml);
                    },
                    error: function(data) {
                       console.log("Error leaving room "+data);
                    }
                 });
                 return false;
            },
          
            sendmessage: function (event) {

            },
            read_color: function (event) {
                var user_id = $("#user_id").val();
               
                if (user_id) {
                    $.get("/profiles?id="+user_id, function(data){
                         if( data[0]['chat_color']) {
                              return  data[0]['chat_color'];
                         }
                    });
                }
                return '#000000';
            },
            delete_room: function() {
                let delete_room_id = $("#delete_room_id").val();
                var arr = {
                        "room_id": delete_room_id,
                };

 
                $.ajax({
                    type: "POST",
                    url: "https://lovehate.io/chat/deleteroom/",
                    crossDomain: true,
                    data: JSON.stringify(arr),
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    success: function(data) {
                    var message = "Сделано.";
                    $("#delete-room-message").html(message);
                    $(".delete-room-modal").fadeOut();
                    },
                    error: function(data){
                      console.log("failure: "+data);
                    }
               });
               this.room(1);
               return false;
            },
            addroom: function(event) {
                let chat_user_id = $('#chat-user-id').val(); 
                if (!this.newroom || this.newroom.length==0) {
                    $("#newroom").attr("style","border:1px solid #FF0000"); 
                    window.setTimeout(function() {  $("#newroom").attr("style",""); }, 1200);
                } else {
                    let current_color = $('#current-color').val();
                    var arr = {
                        "rooms": this.newroom,
                        "message": "Создана новая комната "+this.newroom,
                        "active_room": $('#active-room').val(),
                        "sender_id": $("#chat-user-id").val(),
                        "color": current_color,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postrooms/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                            var messages = "";
                            var temp = [];
                            var roomHtml = "<div>";
                            for(var i=0; i<data["rooms"].length; i++) {

                                 var room_users = "";
                                 if (data["rooms"][i]["active_users"].length > 0) {
                                     room_users = " - "+data["rooms"][i]["active_users"].length;
                                 }

                                 var delete_room = "<span style='text-decoration:none;font-weight:bold;font-size:1.8em;'>&nbsp;</span>";

                                 if (chat_user_id==data["rooms"][i]["creator"]["id"]) {
                                     delete_room = "<a href=\"#\" style=\"text-decoration:none;font-weight:bold;font-size:1.8em;\">-</a>";
                                 }

                                 roomHtml=roomHtml+"<div class='neutral-messages' style='padding-top:0.0em;padding-bottom:0.0em;'>";
                                 roomHtml=roomHtml+"<div style='float:left;width:86%;' id='room-"+data["rooms"][i]['id']+"' onclick='room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;'>";
                                 roomHtml=roomHtml+data["rooms"][i]['name']+room_users;
                                 roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data["rooms"][i]['id']+"\" value=\""+data["rooms"][i]['name']+"\" />";
                                 roomHtml=roomHtml+"</div>"
                                 roomHtml=roomHtml+"<div id='delete-room-";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+"' style='width:12%;float:left;margin-top:-0.6em;' onclick=\"delete_room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;\">"+delete_room+"</div><div class='clear'></div></div>";

 



                            }
                            let current_room_name = $('#active-room-name').val();
                            $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
                            $("#active-room-name").attr("value", current_room_name);
                            $('#rooms-container').html(roomHtml);

                        },
                        error: function(data) {
                        }
                    });

                    $("#add-room-modal").fadeOut();

                }
            }

    },
    mounted:function() {
       this.loggedIn = false;       
       var elem = document.getElementById("chat-window");
       if (elem) {
                elem.scrollTop = elem.clientHeight*10000000;
       }
       $('#chattext').val("");
       //this.refresh_color();
    },
    components: {
        'photoshop-picker': photoshop,
        'material-picker': material,
        'compact-picker': compact,
        'swatches-picker': swatches,
        'slider-picker': slider,
        'sketch-picker': sketch,
        'chrome-picker': chrome,
    }

});

function delete_room(room_id) {
    $("#delete-room-modal").show();

    $.get("/rooms?id="+room_id, function(data){
         var message = "Удалить комнату  "+data[0]['name']+"?";
         $("#delete-room-message").html(message);
         $("#delete_room_id").attr("value", data[0]['id']);
    });


    return false;
}

function join_room(room_id) {
    let chat_user_id = $('#chat-user-id').val();
    let room_name =  $('#room-name-'+room_id).val();

    var arr = {
        "room_id": room_id,
        "user_id": chat_user_id,
    };

    $.ajax({
        type: "POST",
        url: "https://lovehate.io/chat/join/",
        crossDomain: true,
        data: JSON.stringify(arr),
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            var messages = "";
            var temp = [];

            var roomHtml = "<div>";

            for(var i=0; i<data["rooms"].length; i++) {
                var room_users = "";
                if (data["rooms"][i]["active_users"].length > 0) {
                    room_users = " - "+data["rooms"][i]["active_users"].length;
                }

                                 var delete_room = "<span style='text-decoration:none;font-weight:bold;font-size:1.8em;'>&nbsp;</span>";

                                 if (chat_user_id==data["rooms"][i]["creator"]["id"]) {
                                     delete_room = "<a href=\"#\" style=\"text-decoration:none;font-weight:bold;font-size:1.8em;\">-</a>";
                                 }

                                 roomHtml=roomHtml+"<div class='neutral-messages' style='padding-top:0.0em;padding-bottom:0.0em;'>";
                                 roomHtml=roomHtml+"<div style='float:left;width:86%;' id='room-"+data["rooms"][i]['id']+"' onclick='room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;'>";
                                 roomHtml=roomHtml+data["rooms"][i]['name']+room_users;
                                 roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data["rooms"][i]['id']+"\" value=\""+data["rooms"][i]['name']+"\" />";
                                 roomHtml=roomHtml+"</div>"
                                 roomHtml=roomHtml+"<div id='delete-room-";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+"' style='width:12%;float:left;margin-top:-0.6em;' onclick=\"delete_room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;\">"+delete_room+"</div><div class='clear'></div></div>";




            }

            let current_room_name = $('#active-room-name').val();
            $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
            $("#active-room-name").attr("value", current_room_name);
            $('#rooms-container').html(roomHtml);
       },
       error: function(data) {
            console.log("Error joining room "+data);
       }
    });
    return false;



}

function leave_room(room_id) {
    let chat_user_id = $('#chat-user-id').val();
    let room_name =  $('#room-name-'+room_id).val();

    var arr = {
        "room_id": room_id,
        "user_id": chat_user_id,
    };

    $.ajax({
        type: "POST",
        url: "https://lovehate.io/chat/leave/",
        crossDomain: true,
        data: JSON.stringify(arr),
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            var messages = "";
            var temp = [];

            var roomHtml = "<div>";

            for(var i=0; i<data["rooms"].length; i++) {
                var room_users = "";
            
                if (data["rooms"][i]["active_users"].length > 0) {
                    room_users = " - "+data["rooms"][i]["active_users"].length;
                }

                                 var delete_room = "<span style='text-decoration:none;font-weight:bold;font-size:1.8em;'>&nbsp;</span>";

                                 if (chat_user_id==data["rooms"][i]["creator"]["id"]) {
                                     delete_room = "<a href=\"#\" style=\"text-decoration:none;font-weight:bold;font-size:1.8em;\">-</a>";
                                 }

                                 roomHtml=roomHtml+"<div class='neutral-messages' style='padding-top:0.0em;padding-bottom:0.0em;'>";
                                 roomHtml=roomHtml+"<div style='float:left;width:86%;' id='room-"+data["rooms"][i]['id']+"' onclick='room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;'>";
                                 roomHtml=roomHtml+data["rooms"][i]['name']+room_users;
                                 roomHtml=roomHtml+"<input type='hidden' id=\"room-name-"+data["rooms"][i]['id']+"\" value=\""+data["rooms"][i]['name']+"\" />";
                                 roomHtml=roomHtml+"</div>"
                                 roomHtml=roomHtml+"<div id='delete-room-";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+"' style='width:12%;float:left;margin-top:-0.6em;' onclick=\"delete_room(";
                                 roomHtml=roomHtml+data["rooms"][i]['id']+");return false;\">"+delete_room+"</div><div class='clear'></div></div>";




            }

            let current_room_name = $('#active-room-name').val();
            $('#current-channel').html("<strong>"+current_room_name+"=></strong>");
            $("#active-room-name").attr("value", current_room_name);
            $('#rooms-container').html(roomHtml);
       },
       error: function(data) {
            console.log("Error joining room "+data);
       }
    });
    return false;

}

function user(user_id) {
                 let chat_user_id = $("#chat-user-id").val();
                 let room_id = $('#active-room').val();
                 leave_room(room_id);

                 if (chat_user_id==user_id) {

                    var arr = {
                        "user_id": user_id,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/cleanpending/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                             $('.pending-user').html("");
                        },
                        error: function(data) {
                        }
                    });

                 }

                 chat.is_user_channel = true;
                 $("#is-user-channel").attr("value",true);

                 chat.data = [];
                 let url = '/chatmessages?receivers='+user_id;
                 $.get(url, function(data)
                {
                            var messages = "";
                            var temp = [];
                            for(var i=0; i<data.length; i++) {
                                var list_item = "<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username']+" - "+data[i]['body']+"</div>";
                                temp.push(list_item);

                                messages = messages+"<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username'];
                                messages = messages+" - "+data[i]['body'];
                                messages = messages+"</div>";

                            }
                            chat.list = temp;

                            $("#chat-window").html(messages);

                            var elem = document.getElementById("chat-window");

                            if (elem) {
                              elem.scrollTop = elem.clientHeight*10000000;
                            }


                });

                var user = $("#chat-active-user-"+user_id).val();

                $('#active-room-user-id').attr('value', user_id); 
                $('#active-room-name').attr('value', user);

                chat.channel_user = user;

//                $('#current-channel').html("<strong>@"+user+"=></strong>");

                var elem = document.getElementById("chat-window");

                if (elem) {
                     elem.scrollTop = elem.clientHeight*10000000;
                }


    return false;
}
 
function room(room_id) {
                 
    chat.data = [];
    chat.is_user_channel = false;
    let chat_user_id = $('#chat-user-id').val();
    let room_name =  $('#room-name-'+room_id).val();

    $("#is-user-channel").attr("value", false);
    $('#current-channel').html("<strong>"+room_name+"=></strong>");
    $('#active-room').attr('value', room_id);
    $('#active-room-name').attr('value', room_name);
    $('#chattext').attr("value","");

    join_room(room_id);

    $.get('/chatmessages?room_id='+room_id, function(data) {

        let messages = "";
        let temp = [];

        for(var i=0; i<data.length; i++) {
            var list_item = "<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username']+" - "+data[i]['body']+"</div>";
            temp.push(list_item);
            messages = messages+"<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username'];
            messages = messages+" - "+data[i]['body'];
            messages = messages+"</div>";
        }
        chat.list = temp;
        $("#chat-window").html(messages);

        var elem = document.getElementById("chat-window");
        if (elem) {
            elem.scrollTop = elem.clientHeight*10000000;
        }
    });

}

function animate() {
     if ($(".pending-user").is(":visible")) {
         $(".pending-user").hide();
     } else {
         $(".pending-user").show();
     }
}

function childOf(c, p){
     while((c=c.parentNode)&&c!==p);
        return !!c
}

$(document).ready(function() {
           console.log("update will happen here");
           window.setInterval(function(){
               chat.update();
           }, 5000);

           $('#add-room').click(function() {
                 
                if ($("#add-room-modal").is(":visible")) {
                    $("#add-room-modal").hide();
                } else {
                    $('#newroom').val("");
                    $('#add-room-modal').show();
                }
           });
            
     //      window.setInterval(animate, 1000);

/*
           setTimeout(function() {
                if ($(".pending-user").is(":visible")) {  
                    $(".pending-user").hide();
               } else {
                    $(".pending-user").show();
                }
            },2000);
*/
           $(".vc-chrome").hide();
           $(".vc-chrome").css("position","fixed");        
           $("#chat-window").css("z-index","0");
           $("#chat-window").css("position","relative");
           $(".vc-chrome").css("z-index","5");
           $(".vc-chrome").css("margin-top","-20em");

           $('#messages-color').click(function() {
               $(".vc-chrome").show();
           });        

           $('#messages-palette').click(function() {
                $(".vc-chrome").show();
           });



           $(document).mouseup(function(e)  {
                var container = $(".add-room-modal");

                 if (!container.is(e.target) && container.has(e.target).length === 0) {
                     container.fadeOut();
                 }

                var delete_container = $(".delete-room-modal"); 

                if (!delete_container.is(e.target) && delete_container.has(e.target).length === 0) {
                     delete_container.fadeOut();
                }
                    
                var container = $(".vc-chrome");
                

                if (!container.is(e.target) && container.has(e.target).length === 0)
                {
                    if ($(".vc-chrome").is(":visible")) {
                        container.hide();
                        $('.current-color').css("background",chat.colors.hex);
                        $('#current-color').attr('value', chat.colors.hex);         

                        console.log("user id "+ $("#user_id").val()+" and color "+chat.colors.hex); 
                        if ($("#user_id").val()) {
                            var arr = {
                                "user_id": $("#user_id").val(),
                                "color": $("#current-color").val(),
                            };
                            $.ajax({
                                type: "POST",
                                url: "https://lovehate.io/chat/savecolor/",
                                crossDomain: true,
                                data: JSON.stringify(arr),
                                dataType: 'json',
                                contentType: "application/json; charset=utf-8",
                                success: function(data) {
                                },
                                error: function(data) {
                                }
                            });
                        }
                    }
                }
           });

           $.get('/chatmessages?room_id=1', function(data)
           {

                            var messages = "";
                            for(var i=0; i<data.length; i++) {
                                var list_item = "<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username']+" - "+data[i]['body']+"</div>";
                                chat.list.push(list_item);
                                messages = messages+"<div style=\"color:"+data[i]['color']+"\"> @"+data[i]['sender']['username'];
                                messages = messages+" - "+data[i]['body'];
                                messages = messages+"</div>";
                            }
                            $("#chat-window").html(messages);
                            chat.scroll();
                            $('#chattext').val("");

          });


}); 

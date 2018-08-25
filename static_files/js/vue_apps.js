Vue.config.devtools = true;

var photoshop = VueColor.Photoshop;
var chrome = VueColor.Chrome;
var compact = VueColor.Compact;
var swatches = VueColor.Swatches;
var sketch = VueColor.Sketch;
var material = VueColor.Material;
var slider = VueColor.Slider;

var colors = {
  hex: read_color(),
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
        color: read_color(),
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
        $('#chattext').attr("value","");
        $('#active-room').attr('value', 1);
        $('#active-room-name').attr('value', "Курилка");
        $('#current-channel').html("<strong>Курилка=></strong>");
        this.room(1);
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
                   this.room(room_id);
               }
               return false;
           },
           enterchat: function (event) {
               this.data = [];
               this.chat_username = $('#session_user_name').val();
               this.chat_user_id =  $('#user_id').val();
               $('#chattext').attr("value","");
               var arr = {
                   "user_id": this.chat_user_id
               };
               this.colors.hex = read_color(); 


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
               this.chat_username = $('#session_user_name').val();
               this.chat_user_id =  $('#user_id').val();
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
                        alert("failure:"+data.message);
                    }
               });

               var elem = document.getElementById("chat-window");

               if (elem) {
                   elem.scrollTop = elem.clientHeight*10000000;
               }

               return false;
            },

            user: function(user_id) {
                 this.is_user_channel = true;
                 $("#is-user-channel").attr("value",true);

                 this.data = [];
                 $.get('/chatmessages?receivers='+user_id+"&sender_id="+$("#user_id").val(), function(data)
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
                $('#current-channel').html("<strong>@"+user+"=></strong>");

                var elem = document.getElementById("chat-window");

                if (elem) {
                     elem.scrollTop = elem.clientHeight*10000000;
                }

            },
            room: function (room_id) {
                 this.data = [];
                 this.is_user_channel = false;
                 $("#is-user-channel").attr("value", false);
                 var room_name = $('#room-name-'+room_id).val();     
                 $('#current-channel').html("<strong>"+room_name+"=></strong>");
                 $('#active-room').attr('value', room_id);
                 $('#active-room-name').attr('value', room_name);
                 $('#chattext').attr("value","");
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
                let active_room_id = $('#active-room').val();
                let is_default = false;
                this.chat_user_id = $("#user_id").val();
                let message = $('#chattext').val();
                $('#chattext').attr("value",""); 


                if (!message || message.length==0) { 
                     return;
                }

                let user_messages = {};
                let room_messages = {};
                let users = message.match(/(?<=@)[\w\u0430-\u044f]+/ig);
                let rooms = message.match(/(?<=#)[\w\u0430-\u044f]+/ig); 
                //let rooms_texts =  message.match(/(?<=#(\w+)\s)\w+(\w+\s?){1,}/g);
                //let users_texts = message.match(/(?<=@(\w+)\s)\w+(\w+\s?){1,}/g);
                let rooms_texts = message.match(/(?<=#([\w\u0430-\u044f]+)\s)([\w\u0430-\u044f]+\s?){1,}/ig);
                let users_texts = message.match(/(?<=@([\w\u0430-\u044f]+)\s)([\w\u0430-\u044f]+\s?){1,}/ig);


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
                        "color": this.colors.hex, 
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
                            rooms_str = rooms_Str+",";
                        }
                    }
                    var arr = {
                        "rooms": rooms_str,
                        "message": key,
                        "active_room": $('#active-room').val(),
                        "sender_id": $("#user_id").val(),
                        "color": this.colors.hex,
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
                            //    messages = messages+"<div> @"+data['messages'][i]['sender']['username'];
                            //    messages = messages+" - "+data['messages'][i]['body'];
                             //   messages = messages+"</div>";
                            }
                            this.list = temp;
            //                redirect_url('chat');
                            $("#chat-window").html(messages);

                            var elem = document.getElementById("chat-window");

                            if (elem) {
                                 elem.scrollTop = elem.clientHeight*10000000;
                            }

                            $("#chattext").attr("value","");
                         
                        },
                        error: function(data){
                            console.log("Failure - "+data);
                        }
                    });
                 

                });

                if (is_default && this.is_user_channel) {
                    var arr = {
                        "users": this.channel_user,
                        "message": message,
                        "sender_id": $("#user_id").val(),
                        "color": this.colors.hex,
                    };

                    $.ajax({
                        type: "POST",
                        url: "https://lovehate.io/chat/postusers/",
                        crossDomain: true,
                        data: JSON.stringify(arr),
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        success: function(data) {
                            
                        var messages = "";
                        var temp = [];
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
                        "color": this.colors.hex,
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
                             //   messages = messages+"<div> @"+data['messages'][i]['sender']['username'];
                             //   messages = messages+" - "+data['messages'][i]['body'];           
                             //   messages = messages+"</div>";
                                
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


                this.room(active_room_id);
                var elem = document.getElementById("chat-window");
                if (elem) {
                    elem.scrollTop = elem.clientHeight*10000000;
                }

                $('#chattext').attr("value","");
            },
            joinroom: function (event) {

            },

            leaveroom: function (event) {

            },
          
            sendmessage: function (event) {

            }
    },
    mounted:function() {
//       this.room(1); 
       this.loggedIn = false;       
       var elem = document.getElementById("chat-window");
       if (elem) {
                elem.scrollTop = elem.clientHeight*10000000;
       }
       this.color = read_color();
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

function read_color() {
     var arr = {
         "user_id": $("#user_id").val(),
     };

     $.ajax({
         type: "POST",
         url: "https://lovehate.io/chat/readcolor/",
         crossDomain: true,
         data: JSON.stringify(arr),
         dataType: 'json',
         contentType: "application/json; charset=utf-8",
         success: function(data) {
             return  data['color'];
         },
         error: function(data) {
             return "#000000";
         }
     });
     return '#000000';
}

$(document).ready(function() {
           console.log("update will happen here");
           window.setInterval(function(){
               chat.update();
           }, 5000);

           $(".vc-chrome").hide();
           $(".vc-chrome").css("position","fixed");        
           $("#chat-window").css("z-index","0");
           $("#chat-window").css("position","relative");
           $(".vc-chrome").css("z-index","5");
           $(".vc-chrome").css("margin-top","-20em");

           $('#messages-color').click(function() {
               $(".vc-chrome").show();
           });        

           $(document).mouseup(function(e)  {
                var container = $(".vc-chrome");
                

                if (!container.is(e.target) && container.has(e.target).length === 0)
                {
                    if ($(".vc-chrome").is(":visible")) {
                        container.hide();
                        $('.current-color').css("background",chat.colors.hex);
         
                        console.log("user id "+ $("#user_id").val()+" and color "+chat.colors.hex); 
                        if ($("#user_id").val()) {
                            var arr = {
                                "user_id": $("#user_id").val(),
                                "color": chat.colors.hex,
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
                             $("#chattext").attr("value","");

          });


}); 

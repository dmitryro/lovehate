       var i = 0;
       var speed = 300; /* The speed/duration of the effect in milliseconds */
       var is_login_open = false;
       
       function typeWriter(txt) {
          if (i < txt.length) {
               document.getElementById("runner").innerHTML += txt.charAt(i);
               i++;
               setTimeout(typeWriter, speed);
          } 
       }

       function line_one() {

           var l = $('#runner-index').html();
           
           if (l=='One') {
                 $('#runner').css('display', 'block');
             //    var text = "Чтобы был хороший стул";
                 var text = "Eсли не удаётся авторизоваться";
                 $('#runner-index').html('Two');
            //     typeWriter(text);
                 $('#runner').html('<p class="line-1 anim-typewriter">'+text+'</p>')
           } else if (l=='Two') {
                  $('#runner').css('display', 'block');
                // var text = "должен быть хороший стол.";
                 var text = "пишите на dmitryro@gmail.com";
                 $('#runner-index').html('Three');
              //   typeWriter(text);
                 $('#runner').html('<p class="line-1 anim-typewriter">'+text+'</p>');
           } else {
                  $('#runner').css('display', 'block');
                // var text = "должен б▒~K▒~B▒~L ▒~Eо▒~@о▒~Hий ▒~A▒~Bол.";
                 var text = "Разослано новостное письмо";
                 $('#runner-index').html('One');
              //   typeWriter(text);
                 $('#runner').html('<p class="line-1 anim-typewriter">'+text+'</p>');
           }
           
            
           return false;
       }


       $(document).ready(function() {
           $('#submenu-main').css('display','none');
           $('#runner').html('Чтобы был хороший стул');
           $('#runner').css('display', 'none');
           $('#runner-index').html('One');       
           setInterval(line_one, 3000);

/*
           window.setInterval(function(){
               chat.update();
           }, 5000);
*/
          // for(var i = 0; i< 10; i++) {
          //    chat.list.push(i);
          // }




/*
            $(document).mouseup(function(e)  {
                var container = $("#modal-login");

                if (!container.is(e.target) && container.has(e.target).length === 0) 
                {
                     container.hide();
                }
            });
*/
            $(document).mouseup(function(e)  {
                var container = $("#send-reset-link-modal");

                // if the target of the click isn't the container nor a descendant of the container
                if (!container.is(e.target) && container.has(e.target).length === 0)
                {
                     container.hide();
                }
            });

            $(document).mouseup(function(e)  {
                var container = $("#modal-send-activation");

                // if the target of the click isn't the container nor a descendant of the container
                if (!container.is(e.target) && container.has(e.target).length === 0)
                {
                     container.hide();
                }
            });

            var attitude = { love:1, indifferent:2, hate:3 };
            $('#comment').html('');
            $('#feeling').html('');
            $('#message').html('');
            $('#comment').html($('#comment-body').val());
            $('#blogedit_post').html($('#blog_body_edit').val());
            $('#bio').html($('#profile_bio').val());
            $('#forumedit_feeling').html($('#emotion_emotion').val());
            $('#blognew_post').html('');
            $("#activation-success" ).fadeIn( 200 ).delay( 500 ).fadeOut( 300 );
            $("#activation-failure" ).fadeIn( 200 ).delay( 500 ).fadeOut( 300 );
            $("#retry-activation").click(function() {
            });
            
         //   $('#submenu-forum').hide();
          //  $('#submenu-blog').hide();
          //  $('#submenu-mylh').hide(); 
          //  $('#submenu-statistics').hide();
           // $('#submenu-private-messages').hide();

            $('#change_password').click(function(event) {
                $('#change-password-modal').show();
            });
           
            $('#reset-password-modal-close').click(function(event) {
                   $("#reset-password-modal").hide();
            });

            $('#send-reset-link-modal-open-activate').click(function(event) {
                   $('#modal-send-activation').hide();
                   $('#send-reset-link-modal').show();
            });

            $('#send-reset-link-modal-open').click(function(event) {
                   $('#modal-login').hide();
                   $('#send-reset-link-modal').show();
            });

            $('#send-reset-link-modal-close').click(function(event) {
                  $('#send-reset-link-modal').hide();
            });

            $('#change-password-modal-close').click(function(event) {
                $('#change-password-modal').hide();
           });


           $('#submenu-1').click(function(event) {
                console.log("MAIN");
                $('#submenu-forum').css('display', 'none');
                $('#submenu-blog').css('display', 'none');
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-private-messages').css('display', 'none');
                $('#submenu-main').css('display', 'block');
                $('#submenu-statistics').css('display', 'none');
            });


           $('#submenu-2').click(function(event) {
                console.log("FORUM");
                $('#submenu-forum').css('display', 'block');
                $('#submenu-main').css('display', 'none');
                $('#submenu-blog').css('display', 'none');
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-private-messages').css('display', 'none');
                $('#submenu-statistics').css('display', 'none');
            });


           $('#submenu-3').click(function(event) {
                console.log("BLOG");
                $('#submenu-main').css('display', 'none');
                $('#submenu-forum').css('display', 'none');
                $('#submenu-blog').css('display', 'block');
                $('#submenu-mylh').css('display', 'none');             
                $('#submenu-private-messages').css('display', 'none');
                $('#submenu-statistics').css('display', 'none');
            });

           $('#submenu-4').click(function(event) {
                console.log("MY");
                $('#submenu-mylh').css('display', 'block');
                $('#submenu-blog').css('display', 'none');
                $('#submenu-forum').css('display', 'none');
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-private-messages').css('display', 'none');
                $('#submenu-statistics').css('display', 'none');
            });

           $('#submenu-5').click(function(event) {
                console.log("PRIVATE");
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-blog').css('display', 'none');
                $('#submenu-forum').css('display', 'none');
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-private-messages').css('display', 'block');
                $('#submenu-statistics').css('display', 'none');
            });

           $('#submenu-6').click(function(event) {
                console.log("STATISTICS");
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-blog').css('display', 'none');
                $('#submenu-forum').css('display', 'none');
                $('#submenu-mylh').css('display', 'none');
                $('#submenu-private-messages').css('display', 'none');
                $('#submenu-statistics').css('display', 'block');
            });
            if ($('#current_page').val()==='home') { 
                       $('#submenu-main').show();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-1').addClass('active');
            } else if ($('#current_page').val()==='relationships') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').show();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-4').addClass('active');
            } else if ($('#current_page').val()==='mylh' || $('#current_page').val()==='mylh_settings') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').show();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-4').addClass('active');
            } else if ($('#current_page').val()==='forum') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').show();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-2').addClass('active');
            } else if ($('#current_page').val()==='blog') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').show();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-3').addClass('active');
            } else if ($('#current_page').val()==='statistics') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').show();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-6').addClass('active');
            } else if ($('#current_page').val()==='private' || $('#current_page').val()==='private_contacts' || $('#current_page').val()==='private_settings') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').show();
                       $('.active').removeClass('active');
                       $('#submenu-div-5').addClass('active');
            } else if ($('#current_page').val()==='outgoing') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').show();
                       $('.active').removeClass('active');
                       $('#submenu-div-5').addClass('active');

            } else if ($('#current_page').val()==='new_blog') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').show();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                        $('#submenu-div-3').addClass('active');

            } else if ($('#current_page').val()==='new_comment') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').show();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-3').addClass('active');

            } else if ($('#current_page').val()==='blog_comments') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').show();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-3').addClass('active');
            } else if ($('#current_page').val()==='user_blog') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').show();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-3').addClass('active');
            }

            else if ($('#current_page').val()==='incoming') {
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').show();
                       $('.active').removeClass('active');
                       $('#submenu-div-5').addClass('active');
            }


            $('.menu-item').click(function(event) {
                   event.preventDefault();
                   $('.active').removeClass('active');
                   $(this).addClass('active');

                   if ($(this).attr('id')==='submenu-div-1') {
                       var url = '/';
                       window.location.href = url;
                       $('#submenu-main').show();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                   } else if ($(this).attr('id')==='submenu-div-2') {
                       var url = '/forum/';
                       window.location.href = url;
                       $('#submenu-main').hide();
                       $('#submenu-forum').show();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                   } else if ($(this).attr('id')==='submenu-div-3') {
                       var url = '/blog/';
                       window.location.href = url;
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').show();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                   } else if ($(this).attr('id')==='submenu-div-4') {
                       var url = '/mylh/';
                       window.location.href = url;
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').show();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                   } else if ($(this).attr('id')==='submenu-div-5') {
                       var url = '/private/';
                       window.location.href = url;
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').show();
                   } else if ($(this).attr('id')==='submenu-div-6') {
                       var url = '/statistics/';
                       window.location.href = url;
                       $('#submenu-main').hide();
                       $('#submenu-forum').hide();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').show();
                       $('#submenu-private-messages').hide();
                   }
            });
          if ($('#current_page').val()==='new_feeling') {
                       $("#resend-activation-errors").hide(); 
                       $('#submenu-main').hide();
                       $('#submenu-forum').show();
                       $('#submenu-blog').hide();
                       $('#submenu-mylh').hide();
                       $('#submenu-statistics').hide();
                       $('#submenu-private-messages').hide();
                       $('.active').removeClass('active');
                       $('#submenu-div-2').addClass('active');
            }
            
            $('#newfriendform').validate({

                      rules: {
                //            friend_username: "required",
                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                  //         friend_username: {
                   //            required: "Введите ник будущего друга!"
                    //       }
                      }



            });

            $('#newenemyform').validate({

                      rules: {
                //            enemy_username: "required",
                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                  //         enemy_username: {
                  //             required: "Введите ник будущего врага!"
                  //        }
                      }



            });

            $('#newcommentform').validate({
                      rules: {
                            comment_attitude: "required",
                            comment: "required",
                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {  
                           comment: {
                               required: "Введите ваш комментарий!",
                           },
                           comment_attitude: {
                               required: "?~R?~K?~Aкажи?~Bе ?~Aвое о?~Bно?~Hение к о?~B?~A?~Kлаемом?~C!",
                           },               
                      }
            }); 

            $('#editprofileform').validate({
                      rules: {
                            profile_username: {
                                     required: true,
                                     minlength: 1
                            },
                            profile_email: {
                                     required: true,
                                     email: true
                            }

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           profile_email: {
                               required: "Введите адрес электронной почты!",
                               email: "Неверный формат электронной почты!",
                           },
                           profile_username: {
                               required: "Введите ник (имя пользователя)!",
                           },
                      }                          
      
            });

            $('#newcommentunauthform').validate({
                      rules: {
                            comment_attitude: "required",
                            comment_username: "required",
                            comment_password: "required",
                            comment: "required",
                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           comment: {
                               required: "Введите Ваш Комментарий!",
                           },
                           comment_attitude: {
                               required: "Выскажите свое отношение к опубликованному!",
                           },
                           comment_username: {
                               required: "Введите Ваш Ник!",
                           },
                           comment_password: {
                               required: "Введите Ваш Пароль!",
                           },

                      }
            });

            $("#recover-password").validate({

                      rules: {
                            reset_username: {
                                     required: true,
                                     minlength: 1
                            },
                            reset_email: {
                                     required: true,
                                     email: true
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {

                           reset_username: {
                               required: "Введите имя пользователя!",
                               minlength: "Имя пользователя минимум 1 символ!",
                           },
                           reset_email: {
                               required:"Введите адрес электронной почты!", 
                               email: "Неверный формат электронной почты!", 
                           },

                      }



            });

            $('#recover-password-steptwo').validate({
                   rules: {
                            newpassword_recover: {
                                     required: true,
                                     minlength: 8
                            },
                            newpassword_recover_confirmed: {
                                     required: true,
                                     minlength: 8,
                                     equalTo: "#newpassword_recover"
                            }


                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {

                           newpassword_recover_confirmed: {
                               required: "Подтвердите новый пароль!",
                               minlength: "Пароль должен быть минимум 8 символов!",
                               equalTo:  "Подтверждение должно быть идентично!",
                           },
                           newpassword_recover: {
                               required: "Введите новый пароль!",
                               minlength: "Пароль должен быть минимум 8 символов!",
                           },



                      }

            });



            $('#changepassword').validate({
                      rules: {
                            oldpassword: {
                                     required: true,
                                     minlength: 8
                            },
                            newpassword: {
                                     required: true,
                                     minlength: 8
                            },
                            newpassword_confirmed: {
                                     required: true,
                                     minlength: 8,
                                     equalTo: "#newpassword"
                            }


                      },

                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {

                           newpassword_confirmed: {
                               required: "Подтверждающий пароль необходим!",
                               minlength: "Подтверждение минимум 8 символов!",
                               equalTo:  "Подтверждение не идентично!",
                           },
                           newpassword: {
                               required: "Новый пароль необходим!",
                               minlength: "Новый пароль - минимум 8 символов!",
                           },
                           oldpassword: {
                               required: "Старый пароль необходим!",
                               minlength: "Старый пароль - минимум 8 символов!",
                           },



                      }

            });

            $('#newmessageform').validate({
                      rules: {
                            message_attitude: "required",
                            message: "required",
                            recipient: "required",
                            subject: {
                                     required: true,
                                     minlength: 2
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           subject: {
                               required: "Введите тему сообщения!",
                               minlength: "Введите тему сообщения!"
                           },
                           message: {
                               required: "Введите текст сообщения!",
                               minlength: "Введите текст сообщения!"
                           },
                           recipient: {
                               required: "Введите минимум одного получателя!",
                               minlength: "Введите минимум одного получателя!",
                           },
                           message_attitude: {
                               required: "Выскажите свое отношение к отсылаемому!",
                           },


                     }
             });

            $('#newmessageunauthform').validate({
                      rules: {
                            message_attitude: "required",
                            message: "required",
                            recipient: "required",
                            message_username: "required",
                            message_password: "required",
                            subject: {
                                     required: true,
                                     minlength: 2
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           subject: {
                               required: "Введите тему сообщения!",
                               minlength: "Введите тему сообщения!",
                           },
                           message: {
                               required: "Введите текст сообщения!",
                               minlength: "Введите текст сообщения!",
                           },
                           recipient: {
                               required: "Введите минимум одного получателя сообщения!",
                               minlength: "Введите минимум одного получателя сообщения!",
                           },
                           message_attitude: {
                               required: "Выскажите Ваше отношение к теме сообщения!",
                           },
                           "message_username": {
                               required: "Введите ник (имя пользователя)!",
                           },
                           "message_password": {
                               required: "Введите пароль!",
                           }

                     }
             });



            $('#newforumform').validate({
                      rules: {
                            forumnew_attitude: "required",
                            feeling: "required",
                            subject: {
                                     required: true,
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           subject: {
                               required: "Название темы не может быть пустым!",
                           },
                           feeling: {
                               required: "Ваше сообщение не может быть пустым!",
                               minlength: "Опишите Ваше отношение не менее чем в десяти символах!"
                           },
                           forumnew_attitude: {
                               required: "Ваше отношение должно быть высказано!",
                           },

 
                     }
             });

            $('#editforumform').validate({
                      rules: {
                            forumedit_attitude: "required",
                            forumedit_subject: {
                                     required: true,
                                     minlength: 1
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           forumedit_subject: {
                               required: "Название темы не может быть пустым!",
                               minlength: "Название темы не может быть короче одного символа!",
                           },
                           forumedit_attitude: {
                               required: "Ваше отношение должно быть высказано!",
                           },


                     }
             });

            $('#newunauthforumform').validate({
                      rules: {
                            forumnew_attitude: "required",
                            feeling: "required",
                            forumnew_username: "required",
                            forumnew_password: "required",
                            subject: {
                                     required: true,
                                     minlength: 2
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           subject: {
                               required: "Название темы не может быть пустым!",
                               minlength: "Название темы не может быть пустым!",
                           },
                           feeling: {
                               required: "Сообщение не может быть пустым!",
                               minlength: "Сообщение не может быть пустым!",
                           },
                           forumnew_attitude: {
                               required: "Ваше относение к публикуемому должно быть высказано!",
                           },
                           forumnew_username: {
                               required: "Имя Пользователя (Ник) Обязательно для заполнения!",
                           },
                           forumnew_password: {
                               required: "Пароль Обязателен для заполнения!",
                           }




                     }
             });


            $('#editblogform').validate({
                      rules: {
                            blogedit_attitude: "required",
                //            blogedit_post: "required",
                            blogedit_subject: {
                                     required: true,
                                     minlength: 2
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           blogedit_subject: {
                               required: "Введите тему сообщения!",
                               minlength: "Введите тему сообщения!",
                           },
/*
                           blogedit_post: {
                               required: "Введите текст сообщения!",
                               minlength: "Введите текст сообщения!",
                           },
*/
                           blogedit_attitude: {
                               required: "Выскажите свое отношение к публикуемому!"
                           },


                     }

            });

            $('#newblogform').validate({
                      rules: {
                            blognew_attitude: "required",
                            blognew_post: "required",
                            blognew_subject: {
                                     required: true,
                                     minlength: 2
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           blognew_subject: {
                               required: "Введите тему сообщения!",
                               minlength: "Введите тему сообщения!",
                           },
                           blognew_post: {
                               required: "Введите текст сообщения!",
                               minlength: "Введите текст сообщения!",
                           },
                           blognew_attitude: {
                               required: "Выскажите свое отношение к публикуемому!",
                           },


                     }
             });


            $('#newblogunauthform').validate({
                      rules: {
                            blognew_attitude: "required",
                            blognew_post: "required",
                            blognew_username: "required",
                            blognew_password: "required",
                            blognew_subject: {
                                     required: true,
                                     minlength: 2
                            },

                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           blognew_subject: {
                               required: "Тема сообщеняи обязательна!",
                               minlength: "Тема сообщеняи обязательна!",
                           },
                           blognew_post: {
                               required: "Текст сообщения обязателен!",
                               minlength: "Текст сообщения обязателен!",
                           },
                           blognew_attitude: {
                               required: "Выскажите свое отношение к публикуемому!",
                           },
                           blognew_username: {
                               required: "Ник (имя пользователя) обязателен!",
                           },
                           blognew_password: {
                               required: "Пароль обязателен!",
                           }

                     }
             });
            $('#authenticateform').validate({
                      rules: {
                             login_username:   "required",
                             login_password: {
                                      required: true,
                                      minlength: 8
                             }                 
                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           login_username: {
                               required: "Ник (имя пользователя) обязателен!",
                           },
                           login_password: {
                               required: "Пароль обязателен!",
                               minlength: "Пароль минимум 8 символов!",
 
                           },
                      }

            });
         
            $('#registration').validate({
                      rules: {
                            register_username: {
                                     minlength: 1,
                                     required: true
                            },
                            register_password: {
                                     required: true,
                                     minlength: 8
                            },
                            register_email: {
                                     required: true,
                                     email: true
                            },
/*
                            register_name: {
                                     required: true,
                                     minlength: 2
                            },
                            register_confirm_password: {
                                     required: true,
                                     minlength: 8,
                                     equalTo: "#register_password"
                            }
*/
                      },
                      highlight: function (element) {
                            $(element).closest('.control-group').removeClass('success').addClass('error');
                      },
                      success: function (element) {
                           element.text('').addClass('valid')
                              .closest('.control-group').removeClass('error').addClass('success');
                      },
                      messages: {
                           register_username: {
                               required: "Введите имя пользователя!",
                               minlength: "Имя пользователя должно быть длиной не менее 5 символов!"
                           },
                           register_password: {
                               required: "Введите пароль!",
                               minlength: "Ваш пароль должен быть длиной не меньше 8 символов!"
                           },
/*
                           register_confirm_password: {
                               required: "Подтвердите пароль!",
                               minlength: "Ваш пароль должен быть длиной не меньше 8 символов!",
                               equalTo: "Ваш подтверждающий пароль должен быть идентичен!"
                           },
                           register_name: {
                               required: "Введите полное имя или имя собственное!",
                               minlength: "Ваше имя должно быть длиной не меньше 2 символов!",
                           },
*/
                           register_email: {
                               required: "Введите адрес электронной почты!",
                               email: "Используйте формат электронной почты!"    
                           }
                     }
              });
              $('div.errors').hide();
              $('#modal-login').hide();      
              $('#modal-send-activation').hide();

              $('#modal-send-activation-close').click(function() {
                  $('#modal-send-activation').hide();
              });

              $('#modal-login-close').click(function() {
                  $('#modal-login').hide();
                  is_login_open = false;
              });

              $('#modal-login-open').click(function() {
                  $('#modal-register').hide();
              });
              
              $('#modal-login-open').click(function() {
                  $('.login-errors').hide();
                  $('#login_username').attr('value','');
                  $('#login_password').attr('value','');
                  $('#modal-login').show();
                  is_login_open = true;
              });
             
              $('#newfriendform-publish').click(function() {
                  if($("#newfriendform").valid()) {
                         var friends_check_box_values = $('#newfrienddeleteform [name="friends_delete"]:checked').map(function () {
                             return this.value;
                         }).get();


                         var user_id = $("#user_id").val();


                         var arr = {
                              username: $("#friend_username").val(),
                              user_id: user_id,
                              friends_delete: friends_check_box_values,
                         };


                         $.ajax({
                             type: "POST",
                             url: "https://lovehate.io/addnewfriend/",
                             data: JSON.stringify(arr),
                             dataType: 'json',
                             contentType: "application/json; charset=utf-8",
                             success: function(data){
                                 redirect_url('relationships'+'/'+user_id+'/');
                             },
                             error: function(data){
                                 $( ".friend-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                             }

                         });



                  }
              });

              $('#newenemyform-publish').click(function() {

                  var enemies_check_box_values = $('#newenemydeleteform [name="enemies_delete"]:checked').map(function () {
                             return this.value;
                  }).get();

                  if($("#newenemyform").valid()) {
                         var user_id = $("#user_id").val();
                         var arr = {
                              username: $("#enemy_username").val(),
                              user_id: user_id,
                              enemies_delete: enemies_check_box_values,
                         };

                         $.ajax({
                             type: "POST",
                             url: "https://lovehate.io/addnewenemy/",
                             data: JSON.stringify(arr),
                             dataType: 'json',
                             contentType: "application/json; charset=utf-8",
                             success: function(data){
                                 redirect_url('relationships'+'/'+user_id+'/');
                             },
                             error: function(data){
                                 $( ".enemy-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                             }

                         });


                  }
              });


              $('#send-reset-link').click(function() {
                     if($("#recover-password").valid()) {

                         var arr = {
                          username: $("#reset_username").val(),
                          email: $("#reset_email").val(),
                         };

                         $.ajax({
                             type: "POST",
                             url: "https://lovehate.io/recoverpassword/",
                             data: JSON.stringify(arr),
                             dataType: 'json',
                             contentType: "application/json; charset=utf-8",
                             success: function(data){
                                 $( ".sent-success" ).fadeIn(300).delay(1000).fadeOut(300).promise().done(function() {
                                         wait(1000);
                                         $('#send-reset-link-modal').hide();
                                 });
                             },
                             error: function(data){
                                 $( ".sent-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                             }

                         });



                     }
              });

              // Variable to store your files
              var files;

              // Add events
              $('input[type=file]').on('change', prepareUpload);

              // Grab the files and set them to our variable
              function prepareUpload(event)
              {
                    files = event.target.files;
              }
              
              $('#editprofile-publish').click(function(event) {
                  if($('#editprofileform').valid()) {
                      
                       event.stopPropagation(); // Stop stuff happening
                       event.preventDefault(); // Totally stop stuff happening
                      $('#editprofileform').submit();

                       // START A LOADING SPINNER HERE

                       // Create a formdata object and add the files

/*
                      var arr = {
                          user_id: $('#user_id').val(),
                          username: $("#profile_username").val(),
                          session_username:  $("#session_user_name").val(),
                          first_name: $("#first_name").val(),
                          last_name: $("#last_name").val(),
                          email: $("#profile_email").val(),
                          bio: $("#bio").val(),
                      };

                       $.each(files, function(key, value) {
                              arr[key] = value;
                      });

                       
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/saveprofile/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          processData: false,
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              $( ".profile-success" ).fadeIn(300).delay(1000).fadeOut(300).promise().done(function() {
                                     wait(1000);
                                     redirect_url('mylh/');
                              });
                          },
                          error: function(data){
                              $( ".profile-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call
               */  
              } 

              });  

              $('#password-recover-publish').click(function(event) {
                   if ($('#recover-password-steptwo').valid()) {

                      var arr = {
                          password: $("#newpassword_recover").val(),
                          user_id: $("#reset_user_id").val(),
                      };

         
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/updatepassword/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              $( ".recover-success" ).fadeIn(300).delay(1000).fadeOut(300).promise().done(function() {
                                     wait(1000);

                                     $('#reset-password-modal').hide();
                              });
                          },
                          error: function(data){

                              $( ".recover-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call



                  }

              });
              $('#newcommentunauth-publish').click(function(event) {
                  if (  $('#newcommentunauthform').valid() ) {
                      var arr = {
                          body: $("#comment").val(),
                          attitude: attitude[$('input[type=radio][name=comment_attitude]:checked').val()],
                          title: $("#comment_subject").val(),
                          user_id: $("#comment_user_id").val(),
                          post_id: $("#comment_post_id").val(),
                          comment_id: $("#comment_id").val(),
                          comment_username:  $("#comment_username").val(),
                          comment_password:  $("#comment_password").val(),
                      };                       
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/addnewcommentunauth/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_url('blog/'+$("#comment_post_id").val()+"/comments");
                          },
                          error: function(data){
                              $(".comment-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call


                  }
              });
 
              $('#newcomment-publish').click(function(event) {
                  if ($('#newcommentform').valid()) {

                      var arr = {
                          body: $("#comment").val(),
                          attitude: attitude[$('input[type=radio][name=comment_attitude]:checked').val()],
                          title: $("#comment_subject").val(),
                          user_id: $("#comment_user_id").val(),
                          post_id: $("#comment_post_id").val(),
                          comment_id: $("#comment_id").val()
                      };

                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/addnewcomment/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_url('blog/'+$("#comment_post_id").val()+"/comments");
                          },
                          error: function(data){
                              $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                      }); // end ajax call
                  }
              });

              $('#editcomment-publish').click(function(event) {
                      var arr = {
                          body: $("#comment").val(),
                          attitude: attitude[$('input[type=radio][name=comment_attitude]:checked').val()],
                          title: $("#comment_subject").val(),
                          user_id: $("#comment_user_id").val(),
                          post_id: $("#comment_post_id").val(),
                          comment_id: $("#comment_id").val()
                      };
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/addnewcomment/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_url('blog/'+$("#comment_post_id").val()+"/comments");
                          },
                          error: function(data){
                              $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                      }); // end ajax call
              });

              $('#message-publish').click(function() {
                           
                  if ($('#newmessageform').valid()) {
                      var arr = {
                          message: $("#message").val(),
                          attitude: attitude[$('input[type=radio][name=message_attitude]:checked').val()],
                          subject: $("#subject").val(),
                          recipients: $("#recipient").val(),
                          sender_id: $("#message_user_id").val(),
                      };
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/newmessage/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                             
                              redirect_url('outgoing');
                          },
                          error: function(data){
                              $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                      }); // end ajax call


                  }
              });


              $('#message-unauth-publish').click(function() {

                  if ($('#newmessageunauthform').valid()) {
                      var arr = {
                          message: $("#message").val(),
                          attitude: attitude[$('input[type=radio][name=message_attitude]:checked').val()],
                          subject: $("#subject").val(),
                          recipients: $("#recipient").val(),
                          sender_id: $("#message_user_id").val(),
                          username: $("#message_username").val(),
                          password: $("#message_password").val(),
                      };
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/newmessageunauth/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              auth($("#message_username").val(), 
                                   $("#message_password").val()); 
                              redirect_url('outgoing');
                          },
                          error: function(data){
                               $(".message-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call


                  }
              });



              $('#blogedit-publish').click(function() {

                  if ($('#editblogform').valid()) {
                      var arr = {
                          post: $("#blogedit_post").val(),
                          attitude: attitude[$('input[type=radio][name=blogedit_attitude]:checked').val()],
                          subject: $("#blogedit_subject").val(),
                          link: $("#blogedit_link").val(),
                          link_two: $("#blogedit_link_two").val(),
                          link_three: $("#blogedit_link_three").val(),
                          link_four: $("#blogedit_link_four").val(),
                          post_id: $('#edited_post_id').val(),
                          user_id: $("#blog_user_id").val(),
                      };

                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/updatepost/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_url('blog');
                          },
                          error: function(data){
                              $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                      }); // end ajax call


                  }
              });

              $('#blognew-unauth-publish').click(function(event) {
                   if ($('#newblogunauthform').valid()) {
                      var arr = {username: $("#blognew_username").val(),
                                 password: $("#blognew_password").val()};
                      // event.preventDefault();
                       //event.stopPropagation(); // Stop stuff happening
                       //event.preventDefault(); // Totally stop stuff happening
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/authenticate-user/",
                          data: "username="+$("#blognew_username").val()+"&password="+$("#blognew_password").val(), //JSON.stringify(arr),
                          dataType: 'json',

                          success: function(data){
                          //  alert(data.code);
                             $("#newblogunauthform").submit();
                            $('#logged-out').html("<a href='https://lovehate.io/signout'>"+data.username+"</a>");
                             
                            if (data.code===200) {
                                if (data.not_activated==true) {
                            //        $("#newblogunauthform").submit();
                                    $('#modal-login').hide();
                                    $("#modal-send-activation").show();
                                } else {
                                    $('#logged-out').html("<a href='https://lovehate.io/signout'>"+data.username+"</a>");
                                }
                            }
                         //   redirect_url('blog');
                          },
                          error: function(data){
                               $(".blognew-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call

 
 
                   }
              });

              $('#blognew-publish').click(function() {

                  if ($('#newblogform').valid()) {
                      var arr = {
                          post: $("#blognew_post").val(),
                          attitude: attitude[$('input[type=radio][name=blognew_attitude]:checked').val()],
                          subject: $("#blognew_subject").val(),
                          link: $("#blognew_link").val(),
                          link_two: $("#blognew_link_2").val(),
                          link_three: $("#blognew_link_3").val(),
                          link_four: $("#blognew_link_4").val(),
                          user_id: $("#blog_user_id").val(),
                      };

                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/addnewblog/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_url('blog');
                          },
                          error: function(data){
                              $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                      }); // end ajax call


                  }
              });

              $('#forumnew-unauth-publish').click(function() {

                   if ($('#newunauthforumform').valid()) {

                      var arr = {
                          emotion: $("#feeling").val(),
                          attitude: attitude[$('input[type=radio][name=forumnew_attitude]:checked').val()],
                          subject: $("#subject").val(),
                          username: $("#forumnew_username").val(),
                          password: $("#forumnew_password").val(),
                          user_id: $("#emotion_user_id").val(),
                      };

                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/addnewemotionunauth/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_main();
                          },
                          error: function(data){
                               $(".forum-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call


                   }
              });

              $('#forumedit-publish').click(function() {
                     if ($('#editforumform').valid()) {
                        var arr = {
                          feeling: $("#forumedit_feeling").val(),
                          attitude: attitude[$('input[type=radio][name=forumedit_attitude]:checked').val()],
                          subject: $("#forumedit_subject").val(),
                          user_id: $("#forumedit_user_id").val(),
                          emotion_id: $("#forumedit_emotion_id").val(),
                        };
            
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/editemotion/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_url('forum');
                          },
                          error: function(data){
                              $( ".forum-errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                       });


                     }
              });

              $('#forumnew-publish').click(function() {

                  if ($('#newforumform').valid()) {
                      
                      var arr = {
                          emotion: $("#feeling").val(),
                          attitude: attitude[$('input[type=radio][name=forumnew_attitude]:checked').val()],
                          subject: $("#subject").val(),
                          user_id: $("#emotion_user_id").val(),
                      };

                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/addnewemotion/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              redirect_main();
                          },
                          error: function(data){
                              $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                          }
                      }); // end ajax call
                  }
              });

              $('#password-change').click(function(event) {
                  if($('#changepassword').valid()) {
                      var arr = {
                          oldpassword: $("#oldpassword").val(),
                          newpassword: $("#newpassword").val(),
                          user_id: $("#user_id").val(),
                      };

                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/changepassword/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              $( ".change-success" ).fadeIn(300).delay(1000).fadeOut(300).promise().done(function() {
                                     wait(1000);
                                 
                                     $('#change-password-modal').hide();
                              });
                          },
                          error: function(data){
                              
                              $( ".change-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }
                      }); // end ajax call

                  } else {
                  }
              });
                 
              $('#user-register').click(function() {
                  var arr = {
                      username: $("#register_username").val(),
                      password: $("#register_password").val(),
  //                    bio: $("#register_bio").val(),
                      email: $("#register_email").val(),
   //                   fullname: $("#register_name").val()                      
                  };
                  if ($('#registration').valid()) {
                      $.ajax({
                          type: "POST",
                          url: "https://lovehate.io/registernew/",
                          data: JSON.stringify(arr),
                          dataType: 'json',
                          contentType: "application/json; charset=utf-8",

                          success: function(data){
                              $( ".registration-success" ).fadeIn(300).delay(1000).fadeOut(300).promise().done(function() {
                                     wait(1000);
                                     redirect_url('/');
                              });
                          },
                          error: function(data){
                              $( ".registration-errors" ).fadeIn( 100 ).delay( 1000 ).fadeOut( 300 );
                          }

                      });
                  }       
              });
              $('#user-resend-activation').click(function() {
                  var arr = {username: $("#username").val()};
                  $.ajax({
                      type: "POST",
                      url: "https://lovehate.io/resendactivationbyuser/",
                      data: JSON.stringify(arr),
                      dataType: 'json',
                      contentType: "application/json; charset=utf-8",
                      success: function(data){
                          $(".resend-success" ).fadeIn( 100 ).delay( 1500 ).fadeOut( 300 );
                          $('#modal-send-activation').delay( 1500 ).hide();
                      },
                      error: function(data){
                          $("#resend-activation-errors").fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                      }
                  }); // end ajax call
              }); // end on click for user login

/*
              document.getElementById("user-login").addEventListener("keydown", function(e) {
                   if (!e) { var e = window.event; }
                          e.preventDefault(); // sometimes useful
                          if (e.keyCode == 13) { $('#user-login').click(); }
              }, false);
*/      

  
            $('#user-login').click(function(event) {
                 if ($('#authenticateform').valid()) {
               //   event.preventDefault();
                  var arr = {username: $("#login_username").val(), 
                             password: $("#login_password").val(),
                             from_session: true}; 
                  $.ajax({
                      type: "POST",
                      url: "https://lovehate.io/authenticate-user/",
                      data: "username="+$("#login_username").val()+"&password="+$("#login_password").val(), //JSON.stringify(arr),
                      dataType: 'json',
                     // contentType: "application/json; charset=utf-8",
                      success: function(data){
                            $('#logged-out').html("<a href='https://lovehate.io/signout'>"+data.username+"</a>");
                            $('#modal-login').hide();
                            if (data.code===200) {
                                if (data.not_activated==true) {
                                    $('#modal-login').hide();
                                    $("#modal-send-activation").show();
                                } else {
                                    $('#authenticateform').submit(); 
                                    $('#modal-login').hide();
                                    $("#authenticateform").submit();
                                    $('#logged-out').html("<a href='https://lovehate.io/signout'>"+data.username+"</a>");
                                    $('#modal-login').hide();
                                }
                            }
                      },
                      error: function(data){
                        $( "div.errors" ).fadeIn( 200 ).delay( 400 ).fadeOut( 300 );
                      }
                  });

                 } //end if
                 
                       
              }); // end on click for user login
       }); // end ready

       function on_mobile_relationships(id) {
          redirect_url('relationships/'+id);
          return false;
       }

       function on_mobile_your_blog(id) {
          redirect_url('blog/user/'+id);   
          return false;
       }

       function on_mobile_new_blog() {
          redirect_url('/blog/new');
          return false;
       }

 
       function redirect_url(url) {
          var redirect = '/'+url;
          window.location.href = redirect;
       }


       function redirect_main() {
          var url = '/';
          window.location.href = url;
       }
        
       function redirect_login(data) {
           $("#authenticateform").submit();
       }

       function auth(username, password) {
            $('#newmessageunauthform').submit();
       }

       function wait(ms){
           var start = new Date().getTime();
           var end = start;
           while(end < start + ms) {
               end = new Date().getTime();
           }
       }

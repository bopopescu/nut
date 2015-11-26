define(['jquery','libs/Class'], function($, Class){

    var EventEntityLoader = Class.extend({
        init: function(){
            var event = $("#event");
            var counter = 1;

            if (event[0]) {
                var flag = false;
                $(window).scroll(function (){
                    //DUP

                    if (($(window).height() + $(window).scrollTop()) >= ($(document).height()-25) && flag == false) {
                        flag = true;
                        var aQuery = window.location.href.split('?');
                        var url = aQuery[0];
                        var last_event = event.find('.entity-selection:last');
                        var time = last_event.find('.timestr:last');
                        var timestamp = time.attr('timestamp');

                        $.ajax({
                            url: url,
                            type: 'GET',
                            data: {'timestamp':timestamp, 'p':++counter },
                            success: function(data){
                      //                console.log(data);
                                var result = $.parseJSON(data);
                                var status = parseInt(result.status);
                                if (status == 1 ) {
                                    var html = $(result.data);
                      //                console.log(html);
                      //              util.like(html);
                                    html.appendTo(event);
                                }
                                flag = false;
                      //                counter ++;
                            }
                        });
                    }
                });
            }
        }
    });
    return EventEntityLoader;


});
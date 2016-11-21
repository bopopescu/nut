define(['libs/Class','jquery'], function(
    Class,$
){
    var DeviceOrientationApp = Class.extend({
        init: function(){
            var self = this;
            if(window.DeviceOrientationEvent){
                console.log('device orientation is supported');
                window.addEventListener('deviceorientation',function(eventData){
                    var LR = eventData.gamma;
                    var FB = eventData.beta;
                    var DIR = eventData.alpha;
                    self.deviceOrientationHandler(LR,FB,DIR);
                },false);
            }else{
                console.log('device orientation is not supported');
            }
        },
        deviceOrientationHandler:function(LR,FB,DIR){
            var titles_array = $('.title-rect');
            titles_array.each(function(index,ele){
                ele.style.webkitTransform = "rotate("+(LR*-1)+"deg)";
                ele.style.transform = "rotate("+(LR*-1)+"deg)";
            });
        }
    });
    return DeviceOrientationApp;
});
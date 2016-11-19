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
                //if(index % 2 ==0){
                //    ele.style.webkitTransform = "rotate("+LR+"deg) rotate3d(1,0,0,"+(FB*-1+30)+"deg)";
                //    ele.style.transform = "rotate("+LR+"deg) rotate3d(1,0,0,"+(FB*-1+30)+"deg)";
                //}else{
                    ele.style.webkitTransform = "rotate("+(LR*-1)+"deg) rotate3d(1,0,0,"+(FB-30)+"deg)";
                    ele.style.transform = "rotate("+(LR*-1)+"deg) rotate3d(1,0,0,"+(FB-30)+"deg)";
                //}
            });
        }
    });

    return DeviceOrientationApp;
});
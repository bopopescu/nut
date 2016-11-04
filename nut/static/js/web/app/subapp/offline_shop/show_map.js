define(['libs/Class','jquery'], function(Class,$) {
    var ShowMap = Class.extend({
        init: function () {
            console.log('show baidu map');
            this.initShowMap();
        },
        initShowMap:function(){
            // 百度地图API功能
            var map = new BMap.Map("map");
            if(isFromMobile){
                map.disableDragging();
            }else{
                //启用滚轮放大缩小，默认禁用
                map.enableScrollWheelZoom();
                //启用地图惯性拖拽，默认禁用
                map.enableContinuousZoom();
            }
            var getInputLng = $('#map').attr('data-lng');
            var getInputLat =  $('#map').attr('data-lat');
            if(getInputLng && getInputLat){
                var point = new BMap.Point(getInputLng,getInputLat);
                var marker = new BMap.Marker(new BMap.Point(getInputLng,getInputLat));
                map.addOverlay(marker);
                map.centerAndZoom(point,15);
            }else{
                map.centerAndZoom("北京",15);
            }
        }
    });
    return ShowMap;
});



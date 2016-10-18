var BaiduMapManager = Class.extend({
    init: function(){
        console.log('baidu map config');
        this.initBaiduMap();
    },
    initBaiduMap:function(){
          // 百度地图API功能
        var map = new BMap.Map("allmap");
        //启用滚轮放大缩小，默认禁用
        map.enableScrollWheelZoom();
        //启用地图惯性拖拽，默认禁用
        map.enableContinuousZoom();

         //左上角,添加比例尺
        var top_left_control = new BMap.ScaleControl({
            anchor:BMAP_ANCHOR_TOP_LEFT
        });
        //左上角添加默认缩放平移控件
        var top_left_navigation = new BMap.NavigationControl();
        //右上角,仅包含平移和缩放按钮
        var top_right_navigation = new BMap.NavigationControl({
            anchor:BMAP_ANCHOR_TOP_RIGHT,
            type:BMAP_NAVIGATION_CONTROL_SMALL
        });
        map.addControl(top_left_control);
		map.addControl(top_left_navigation);
        map.addControl(top_right_navigation);

        var getInputLng = $('#id_address_lng').val();
        var getInputLat =  $('#id_address_lat').val();
        if(getInputLng && getInputLat){
            var point = new BMap.Point(getInputLng,getInputLat);
            var marker = new BMap.Marker(new BMap.Point(getInputLng,getInputLat));
            map.addOverlay(marker);
            map.centerAndZoom(point,12);
        }else{
            map.centerAndZoom("北京",12);
        }

        //单击添加Marker,并获取和设置经纬度至Form
        map.addEventListener("click",function(e){
            map.clearOverlays(); //清除地图上所有覆盖物
            var marker = new BMap.Marker(new BMap.Point(e.point.lng, e.point.lat)); //创建marker点
            map.addOverlay(marker);    //增加点
            attribute();

            function attribute(){
                var p = marker.getPosition();  //获取marker的位置
                $('#id_address_lng').val(p.lng);
                $('#id_address_lat').val(p.lat);
            }
        });
    }
});


(function($, window, document){
    $(function(){
         var baidu_map_manager = new BaiduMapManager();
    });
})(jQuery, window, document);
//requirejs.config({
//    baseUrl:base_url,
//    paths: {
//        slick: '/libs/slick'
//
//    },
//
//    shim: {
//        'slick':{
//            deps:['jquery']
//        }
//    }
//});


define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function(){
            console.log('hello lqqqqqq,hello good store!');

        }
    });
    return StoreBanner;
});




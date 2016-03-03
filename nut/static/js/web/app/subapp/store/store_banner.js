requirejs.config({
    baseUrl:base_url,
    paths: {
        slick: '/libs/slick'

    },

    shim: {
        'slick':{
            deps:['jquery']
        }
    }
});


define(['jquery', 'libs/Class'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function(){
            console.log('hello lq,hello good store!');

        }
    });
    return StoreBanner;
});




require.config({
    baseUrl: base_url,
    paths: {
        libs: './libs',
        utils: './utils',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom'
    },

    shim: {
        'bootstrap':{
            deps:['jquery']
        },
        'jquery':{
            exports:'jQuery'
        }
    }


});


require(['jquery','utils/EntityLike'], function(jQuery,AppEntityLike){

 var  app_like = new  AppEntityLike();
      console.log(jQuery);

});
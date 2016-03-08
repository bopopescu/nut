
require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike
    ){
        var app_like = new  AppEntityLike();
    });

//change filename from fastdom to fastdom.ant to avoid duplicate module name

requirejs.config({
    baseUrl: 'app/',
    paths: {
        libs: './libs',
        utils: './utils',
        bower: 'bower_components',
        component:'./component',
        subapp: './subapp',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom.ant',
        csrf:'libs/csrf',
        underscore:'libs/underscore.ant',
        cookie: 'libs/jquery.cookie',
        masonry: 'libs/masonry',
        jquery_bridget: 'libs/jquery.bridget',
        images_loaded: 'libs/imagesloaded.min',
    },

    shim: {
        // shim won't handle script load , you still need require script in your source
        'cookie':{
            deps:['jquery']
        },
        'csrf':{
            deps:['jquery']
        },
        'bootstrap':{
            deps:['jquery']
        },
        'jquery':{
            exports:'jQuery'
        },
        'underscore':{
            exports: '_'
        },
        'masonry':{
            deps:['jquery']
        }
    }
});


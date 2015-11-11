//change filename from fastdom to fastdom.ant to avoid duplicate module name


requirejs.config({
    baseUrl: 'app/',
    paths: {
        libs: './libs',
        utils: './utils',
        component:'./component',
        subapp: './subapp',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom.ant',
        csrf:'libs/csrf',
        underscore:'libs/underscore.ant',
        cookie: 'libs/jquery.cookie'
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
        }
    }

});

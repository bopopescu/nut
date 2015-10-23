// base url has been bootstraped in template file
require.config({

    baseUrl: base_url,

    paths: {
        app: '../app',
        tpl: '../app/tpl',
        models: '../app/models',
        views:'../app/views',
        util:'../app/utils',
        controllers: '../app/controllers',
        tests: '../tests'
    },
    map: {
        '*': {
        }
    },
});

require(['app/router'], function (Router) {
    var router = new Router();
    Backbone.history.start();
});
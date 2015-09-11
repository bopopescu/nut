var hero_script = document.getElementById('hero');
var hero_script_url = hero_script.src;
var base_url = hero_script_url.replace('sentinel.js', 'lib/');

require.config({

    baseUrl: base_url,

    paths: {
        app: '../app',
        tpl: '../app/tpl',
        models: '../app/models',
        views:'../app/views',
        util:'../app/utils',
        controllers: '../app/controllers',
        utils:'../app/utils',
        tests: '../tests'
    },
    map: {
        '*': {
        }
    },
});

require(['app/articleRouter'], function (Router) {
    var router = new Router();
    window.router = router;
    Backbone.history.start();
});
require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/yearseller_2016/get_current_tag_info'
    ],
    function(polyfill,
             $,
             TagInfo
    ){
       var tag_info = new TagInfo();
    });
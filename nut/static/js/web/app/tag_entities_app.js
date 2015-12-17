require(
    [
        'jquery',
        'subapp/load_tag_entity',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop'
    ],
    function (
        jQuery,
        LoadTagEntity,
        AppEntityLike,
        Menu,
        GoTop
    ){
        var app_load_tag_eneity = new LoadTagEntity();
        var app_like = new AppEntityLike();
        var menu = new Menu();
        var goto = new GoTop();

        console.log("Tag entity list init！");
});

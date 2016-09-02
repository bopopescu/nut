require(
    [
        'jquery',
        'subapp/topmenu',
        'subapp/entity/create_new_entity'
    ],
    function (
        jQuery,
        Menu,
        CreateNewEntity
    ){
        var menu = new Menu();
        var createNewEntity = new CreateNewEntity();
        console.log("entity create init！");
});

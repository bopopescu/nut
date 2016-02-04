require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/detailsidebar',
        'subapp/entitylike',
        'subapp/entityreport',
        'subapp/note/usernote',
        'subapp/detailimage',

        // entity liker part
        'models/Entity',
        'subapp/entity/liker',
        'subapp/entity/baichuan',

        'libs/csrf'

    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              SideBarManager,
              EntityLike,
              EntityReport,
              UserNote,
              EntityImageHandler,
              //entity liker part
              EntityModel,
              LikerAppController,
              BaichuanManager


    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        // disable sidebar scroll effect
        // TODO: fix the bug of flashing footer
        //var sidebar = new SideBarManager();
        var entityLike  =new EntityLike();
        var entityReport = new EntityReport();
        var userNote = new UserNote();
        var imgHandler = new EntityImageHandler();

        var baichuanManager = new BaichuanManager()

        /// begin entity liker app
        if (_.isUndefined(current_entity_id)){
            throw new Error('can not find current entity id ');
            return ;
        }
        var entity = new EntityModel();
            entity.set('id', current_entity_id);

        var likerApp = new LikerAppController(entity);

});

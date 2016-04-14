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

        'subapp/entity/entity_share',
        'subapp/tracker',

        'libs/csrf',
         'subapp/tracker'

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
              BaichuanManager,
              EntityShareApp,
              Tracker


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

        // hide baichuan recommend , for service is down now
        // by an, 2016, 3-19 .
        var baichuanManager = new BaichuanManager();

         var shareApp = new EntityShareApp();

        /// begin entity liker app
        if (_.isUndefined(current_entity_id)){
            throw new Error('can not find current entity id ');
            return ;
        }
        var entity = new EntityModel();
            entity.set('id', current_entity_id);

        var likerApp = new LikerAppController(entity);

         var tracker_list = [

            {
                selector: '.detail-breadcrumd-link',
                trigger: 'click',
                category: 'entity-detail',
                action: 'selection_entity_list',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '#detail_breadcrumb'
            },
             {
                selector: '.detail-breadcrumd-link',
                trigger: 'click',
                category: 'entity-detail',
                action: 'first_level_category_detail',
                label: 'data-first-level-category-title',
                value: 'data-first-level-category-id',
                wrapper: '#detail_breadcrumb'
            }
             ,
             {
                selector: '.detail-breadcrumd-link',
                trigger: 'click',
                category: 'entity-detail',
                action: 'second_level_category_detail',
                label: 'data-second-level-category-title',
                value: 'data-second-level-category-id',
                wrapper: '#detail_breadcrumb'
            }
        ];

        var tracker = new Tracker(tracker_list);

});

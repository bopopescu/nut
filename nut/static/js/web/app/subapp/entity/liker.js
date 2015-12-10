define(['models/Entity',
        'views/Entity/EntityLikerViewSidebar',
        'views/Entity/EntityLikerViewMobile',
        'view/Entity/UserItemView'
    ],
    function(
        EntityModel,
        EntityLikerViewSidebar,
        EntityLikerViewMobile,
        UserItemView
){

    var EntityLikerController = Class.extend({
        init: function(entity){
            this.entityModel = entity || this.getEntityModel;
            this.likerCollection = this.getLikerCollection();
            this.listenTo(entity, 'sync', this.entitySync.bind(this));
            this.likerViewSidebar = new EntityLikerViewSidebar({
                model: this.likerCollection,
                el: '.entity-liker-sidebar-wrapper'
            });
            //this.likerViewMobile  = new EntityLikerViewMobile({model: this.likerCollection});

        },
        entitySync: function(){
            console.log('entity sync');
        },

        getEntityModel: function(){
            return this.entityModel ||  new Error('can not find entity model');
        },

        getLikerCollection:function(){
            return this.entityModel.getLikeUserCollection();
        }




    });
});
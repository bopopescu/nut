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
        init: function(EntityModel){
            this.entityModel = EntityModel || this.getEntityModel;
            this.likerCollection = this.getLikerCollection()
            this.likerViewSidebar = new EntityLikerViewSidebar({model: this.likerCollection});
            this.likerViewMobile  = new EntityLikerViewMobile({model: this.likerCollection});

        },

        getEntityModel: function(){
            return this.entityModel ||  new Error('can not find entity model');
        },

        getLikerCollection:function(){
            return this.entityModel.getLikeUserColel
        }




    });
});
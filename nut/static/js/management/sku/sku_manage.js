function SKU_MNG_APP(){
    this.init();
}

_.extend(SKU_MNG_APP.prototype, {

    init: function(){

        this.render_attributes();
        this.handle_create_attribute();
    },
    handle_create_attribute:function(){

    }
});
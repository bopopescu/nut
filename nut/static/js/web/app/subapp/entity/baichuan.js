define(['libs/underscore','jquery', 'libs/Class'], function(
    _,
    $,
    Class
){
    var BaichuanManager = Class.extend({
        init: function(){
            this.initLoadEvent();
        },
        initLoadEvent: function(){
            window.setTimeout(this.loadBaichuanProducts.bind(this),500)

        },
        loadBaichuanProducts: function(){
            var url = this.getRequestUrl();
            $.when($.ajax({
                method: 'GET',
                url: url,
            }))
                .then(this.getSuccess.bind(this), this.getFail.bind(this));
            console.log('in load baichuan products');
        },

        getSuccess: function(data){
            console.log(data);
        },
        getFail: function(data){
            console.log(data);
        },

        getRequestUrl: function(){
            //current_entity_id, source, title already bootstraped in page
            //var current_entity_id = current_entity_id;
            //var current_entity_origin_source = current_entity_origin_source;
            //var current_entity_title = current_entity_title;

            if (this.isTaobaoEntity()){
                url = '/entity/taobao/recommendation/?keyword='+current_entity_id+'&count=9';
            }else{
                url = '/entity/taobao/recommendation/?keyword='+current_entity_title+'&count=9';
            }

            return url ;

        },
        isTaobaoEntity: function(){
            return /taobao/.test(current_entity_origin_source)
                   || /tmall/.test(current_entity_origin_source)
        }
    });

    return BaichuanManager;

});
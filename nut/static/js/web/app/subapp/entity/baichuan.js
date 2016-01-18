define(['underscore','jquery', 'libs/Class'], function(
    _,
    $,
    Class
){
    var BaichuanManager = Class.extend({
        init: function(){
            this.template = this.get_template();
            this.entityListWrapper = $('#baichuan_list');
            this.retry = false ;
            this.initLoadEvent();
        },
        get_template: function(){
            return _.template($('#baichuan_entity_list_template').html());
        },
        initLoadEvent: function(){
            window.setTimeout(this.loadBaichuanProducts.bind(this),500)

        },
        loadBaichuanProducts: function(url){

            var url = url || this.getRequestUrl();
            $.when($.ajax({
                method: 'GET',
                url: url,
            }))
                .then(this.getSuccess.bind(this), this.getFail.bind(this));
            console.log('in load baichuan products');
        },

        getSuccess: function(data){
            console.log(data);
            var entityList = data['result'];
            if ((!entityList || !entityList.length) && !this.retry){
                  this.retry = true;
                  var url = this.getRequestUrl(true);
                  this.loadBaichuanProducts(url);

            }else{
                 this.renderList(entityList);
            }

        },

        renderList: function(elist){
            if (!elist || !elist.length){
                this.hideGuessTitle();
                return ;
            }else{
                this.entityListWrapper
                .html(this.template({list: elist}));
            }

        },

        hideGuessTitle: function(){
            $('#baichuan_guess_title').hide();
        },
        getFail: function(data){
            console.log(data);
        },

        getRequestUrl: function(isFromTitle){
            //current_entity_id, source, title already bootstraped in page
            //var current_entity_id = current_entity_id;
            //var current_entity_origin_source = current_entity_origin_source;
            //var current_entity_title = current_entity_title;

            if (this.isTaobaoEntity() && !isFromTitle){
                url = '/entity/taobao/recommendation/?keyword='+current_entity_taobao_id+'&count=9';
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
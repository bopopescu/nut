define(['component/ajaxloader', 'jquery', 'libs/fastdom'],
    function(AjaxLoader, $, fastdom){

        RelatedArticleLoader = AjaxLoader.extend({
        init: function(){
            this.isMobile = $('body.mobile-body').length > 0;
            this._super();
            this.current_page = 1 ;
            this.ajax_data = null;
        },
        getRequestUrl: function(){
            return window.location.pathname;
        },
        getData: function(){
            return {
                page: this.current_page + 1,
                target: 'related_article'
            };
        },
        doSuccess: function(){
            var data = this.ajax_data;
            if (data.errors == 0){
                $('.more-article-wrapper').last().after(data['html']);
                this.current_page++;
                this.loading = false;
                if (!(data.has_next_page)){
                    this.handleLastPage();
                }
            }else{
                console.log('load error!');
            }
            //console.log(data);
            console.log('load related article success');
            this.ajax_data = null;

        },
        loadSuccess: function(data){
            this.ajax_data = data;
            fastdom.defer(30, this.doSuccess.bind(this));
        },
        handleLastPage:function(){

            this.detach();
        },
        _shouldLoad: function(){
            return (!this.isMobile) && this._super();
        },
    });

    return RelatedArticleLoader;
});
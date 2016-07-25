
define(['jquery', 'libs/Class'], function(
    $, Class
){
    var CategoryTabView= Class.extend({
        init: function () {
            this.$article_container = $('#selection_article_list');
            this.initHoverCategory();
            this.categoryName = '';
            this.articleCache = window.sessionStorage;
            console.log('category tab view begin');
        },
        initHoverCategory:function(){
            $('#article_category_wrapper .category-list-item').mouseenter(this.handleHoverCategory.bind(this));

        },
        handleHoverCategory:function(event){
            var dataValue = $(event.currentTarget).attr('data-value');
            var articleCache = this.articleCache.getItem(dataValue);
            this.categoryName = dataValue;
            if(articleCache){
                console.log('articleCache:'+articleCache);
                this.showContent($(articleCache));
            }else{
                console.log('no article cache.post ajaxing');
                this.postAjaxRequest(dataValue);
            }
        },
        postAjaxRequest:function(dataValue){
             var data = {
                    'dataValue': dataValue
            };
            $.when(
                $.ajax({
                    cache:true,
                    type:"get",
                    url: '/index_article_tag/',
                    data: data,
                    dataType:"json"
                })
            ).then(
                this.postSuccess.bind(this),
                this.postFail.bind(this)
            );
        },
        postSuccess:function(result){
            console.log('post request success.');
            var status = parseInt(result.status);
            if(status == 1){
                 this.showContent($(result.data));
                 this.setCache(result);
            }else{
                this.showFail(result);
            }
        },
        postFail:function(result){
            console.log('post fail');
        },
        showFail:function(result){
            console.log('get ajax data failed');
        },
        showContent: function(elemList){
            console.log('get ajax data success');
            this.$article_container.empty();
            this.$article_container.append(elemList);
        },
        setCache:function(result){
            console.log('set cache.');
            var category = this.categoryName;
            if(!this.articleCache.getItem(category)){
                this.articleCache.setItem(category,result.data);
            }
        }
    });
    return CategoryTabView;
});





define(['jquery', 'libs/Class'], function(
    $, Class
){
    var CategoryTabView= Class.extend({
        init: function () {
            this.$article_container = $('#selection_article_list');
            this.initHoverCategory();
            console.log('category tab view begin');
        },
        initHoverCategory:function(){
            $('#article_category_wrapper .category-list-item').mouseenter(this.handleHoverCategory.bind(this));

        },
        handleHoverCategory:function(event){
            var that = this;
            var dataValue = $(event.target).attr('data-value');
            console.log('data value:'+dataValue+' send ajax request');
            that.postAjaxRequest(dataValue);
        },
        postAjaxRequest:function(dataValue){
            console.log('data value:'+dataValue+' send ajax request');
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
            console.log('type of ajax result:'+typeof(result));
            console.log('post request success.');
            console.log('ajax result data content:'+result.data);
            console.log('result status: '+result.status);
            var status = parseInt(result.status);
            if(status == 1){
                 this.showContent($(result.data));
            }else{
                this.showFail(result);
            }
        },
        postFail:function(result){
            console.log('post fail');
        },
        showFail:function(result){
            console.log('ajax data failed');
        },
        showContent: function(elemList){
            console.log('ajax data success');
            console.log('append html content:'+elemList);
            var that = this;
            that.$article_container.empty();
            that.$article_container.append(elemList);
        }
    });
    return CategoryTabView;
});




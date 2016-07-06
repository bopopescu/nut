
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
            $('.category-list-item').mouseenter(this.handleHoverCategory.bind(this));

        },
        handleHoverCategory:function(event){
            var dataValue = $(event.target).attr('data-value');
            console.log('data value:'+dataValue+' send ajax request');
            var data = {
                    'dataValue': dataValue
            };

              $.when(
                    $.ajax({
                        cache:true,
                        type:"get",
                        url: '',
                        data: data
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
            var that = this;
            that.$article_container.empty();
            that.$article_container.append(elemList);
        }
    });
    return CategoryTabView;
});




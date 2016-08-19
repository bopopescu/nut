
define(['jquery', 'subapp/index/selection_entity_slick'], function(
    $,SelectionEntitySlick
){
    var EntityCategoryTab= SelectionEntitySlick.extend({
        init: function () {
            this.$entity_container = $('.latest-entity-wrapper');
            this.init_slick();
            this.initHoverCategory();
            this.currentRequestcategoryName = '';
            this.entityCache = window.sessionStorage;
            console.log('selection entity tab view begin');
        },
        initHoverCategory:function(){
            $('#entity_category_container .category-list-item').mouseenter(this.handleHoverCategory.bind(this));

        },
        handleHoverCategory:function(event){
            var dataValue = $(event.currentTarget).attr('data-value');
            var entityCache = this.entityCache.getItem(dataValue);
            this.currentRequestcategoryName = dataValue;
            if(entityCache){
                this.showContent($(entityCache));
            }else{
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
                    url: '/index_selection_entity_tag/',
                    data: data,
                    dataType:"json"
                })
            ).then(
                this.postSuccess.bind(this),
                this.postFail.bind(this)
            );
        },
        postSuccess:function(result){
            console.log(this.currentRequestcategoryName + 'post request success.');
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
            console.log('ajax data failed');
        },
        showContent: function(elemList){
            console.log(this.currentRequestcategoryName +'ajax data success');
            this.$entity_container.empty();
            this.$entity_container.append(elemList);
            this.init_slick();
        },
        setCache:function(result){
            var requestCategory = this.currentRequestcategoryName;
            var result_category = result.category;
            if(!this.entityCache.getItem(requestCategory) && requestCategory == result_category){
                this.entityCache.setItem(requestCategory,result.data);
                 console.log(requestCategory +'set cache success');
            }else{
                console.log('current hover category:'+requestCategory+',response category:'+result_category);
            }
        }
    });
    return EntityCategoryTab;
});




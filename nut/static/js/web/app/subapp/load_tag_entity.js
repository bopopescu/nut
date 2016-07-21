define(['jquery','libs/fastdom','subapp/loadentity'],function($,fastdom,LoadEntity)
{
    var LoadTagEntity = LoadEntity.extend({
        init: function () {
            this.$selection = $('#tag-entity-list');
            this.page = this.$selection.parent().find('.pager');
            this.loading_icon = $('.loading-icon');
            this.counter = 1;
            this.page.hide();
            this.read = null;
            this.write = null;
            this.loading = false;
            this.shouldLoad = true;
            this.setupLoadWatcher();
        },
        loadSuccess: function(res){
            this.attachNewSelections($(res.data), res.status,res.has_next_page);
            console.log('load success');
        },
         attachNewSelections: function(elemList, status,has_next_page){
            var that = this;

            fastdom.defer(function(){
                that.$selection.append(elemList);
            });

            fastdom.defer(function(){
                that.counter++;
                that.doClear();
                if (that.counter % 3 === 0){
                    that.loading_icon.hide();
                    if (status===1 && has_next_page){
                        that.page.show();
                    }
                }
                that.loading = false;
            });
        }
    });
    return LoadTagEntity
});

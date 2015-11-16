/**
 * Created by judy on 13/11/15.
 */

define(['jquery','libs/Class','libs/fastdom','subapp/loadentity'],
    function($,Class, fastdom, LoadEntity){

        var LoadCategoryEntity = LoadEntity.extend({
            init: function () {
                this.$selection = $('#category-entity-list');
                this.page = this.$selection.parent().find('.pager .next');
                this.loading_icon = $('.loading-icon');
                this.counter = 1;
                this.page.hide();
                this.read = null;
                this.write = null;
                this.loading = false;
                this.shouldLoad = true;
                this.setupLoadWatcher();
            }
        });
        return LoadCategoryEntity;
    });

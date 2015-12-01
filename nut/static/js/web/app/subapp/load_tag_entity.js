define(['jquery', 'subapp/loadentity'],function($,LoadEntity)
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
        }
    });
    return LoadTagEntity
});

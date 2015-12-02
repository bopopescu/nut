define(['jquery','libs/fastdom','subapp/loadentity','masonry','jquery_bridget','images_loaded' ],
    function($,fastdom, LoadEntity, Masonry){
        $.bridget('masonry', Masonry);
        var LoadTagEntity = LoadEntity.extend({
            init: function () {
                this.$selection = $('#selection');
                this.page = $('.pager');
                this.loading_icon = $('.loading-icon');
                this.shouldLoad = true;
                this.loading = false;
                this.counter = 1;
                this.page.hide();
                this.initialize();
                this.setupLoadWatcher();
            },

            initialize:function () {
                var $container = this.$selection;
                var grid = $container.masonry({
                    columnWidth: '.selection-item',
                    isAnimated: false,
                    saveOptions: true,
                    transitionDuration: 0,
                    Selector: '.selection-item'
                });

                this.grid = grid
            },

        attachNewSelections: function(elemList, status){
            var that = this;
            fastdom.defer(function(){
                that.grid.append( elemList ).masonry('appended', elemList);
                that.grid.imagesLoaded().progress( function() {
                    that.grid.masonry();
                });
            });

            fastdom.defer(function(){
                that.counter++;
                that.doClear();
                if (that.counter % 3 === 0){
                    that.loading_icon.hide();
                    if (status===1){
                        that.page.show();
                    }
                }
                that.loading = false;
            });
        }
    });

    return LoadTagEntity;
});


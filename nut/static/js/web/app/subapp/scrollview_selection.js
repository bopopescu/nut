<<<<<<< Updated upstream
define(['jquery','libs/fastdom','subapp/loadentity','masonry','jquery_bridget','images_loaded' ],
    function($,fastdom, LoadEntity, Masonry){
        $.bridget('masonry', Masonry);
        var LoadTagEntity = LoadEntity.extend({
=======
define(['jquery','libs/Class','libs/fastdom','masonry','jquery_bridget', 'images_loaded'],
    function($,Class,fastdom,Masonry){
        $.bridget('masonry', Masonry);

        var ScrollEntity = Class.extend({
>>>>>>> Stashed changes
            init: function () {
                this.$selection = $('#selection');
                this.page = $('.pager');
                this.loading_icon = $('.loading-icon');
                this.shouldLoad = true;
                this.loading = false;
                this.counter = 1;
<<<<<<< Updated upstream
                this.page.hide();
                this.initialize();
                this.setupLoadWatcher();
            },

            initialize:function () {
            var $grid = this.$selection.masonry({
                isFitWidth:true,
                itemSelector: '.selection-box',
                animate: false,
                isAnimated: false,
                saveOptions: true,
                transitionDuration: 0,
                isInitLayout: true
            });

            $grid.imagesLoaded().progress( function() {
                $grid.masonry('layout')
            });
            this.$grid = $grid;
            $(window).scroll(this.onScroll.bind(this));
        },

        attachNewSelections: function(elemList, status){
            var that = this;
            fastdom.defer(function(){
                that.$grid.append( elemList ).masonry('appended', elemList);
                that.$grid.imagesLoaded().progress( function() {
                    that.$grid.masonry();
                });
            });
=======
            },

            initialize : function () {
                var $grid = this.$selection.masonry({
                    isFitWidth: true,
                    resizeable: false,
                    isAnimated: false,
                    animate: false,
                    saveOptions: true,
                    percentPosition: true,
                    isResizeBound: true,
                    itemSelector: '.selection-box',
                    isInitLayout: true,
                });
                $grid.imagesLoaded().progress( function() {
                    $grid.masonry();
                });
                this.$grid = $grid;
                $(window).scroll(this.onScroll.bind(this));
                $(window).resize(this.onResize.bind(this));
            },

            onScroll:function(){
                if (this.read){
                    fastdom.clear(this.read)
                }
                this.read = fastdom.read(this.doRead.bind(this));
                if(this.write){
                    fastdom.clear(this.write);
                }
                this.write = fastdom.write(this.doWrite.bind(this));
            },

            onResize: function () {
                //this.$grid.imagesLoaded().progress( function() {
                //    this.$grid.masonry('layout');
                //});
            },

            doClear : function(){
                this.scrollTop = this.windowHeight = this.footerHeight = this.docHeight = null;
                this.read = null;
            },
>>>>>>> Stashed changes

            fastdom.defer(function(){
                that.counter++;
                that.doClear();
                if(status!==1) {
                    that.loading_icon.hide();
                }
<<<<<<< Updated upstream
                that.loading = false;
            });
        }
    });
=======
            },

            loadSuccess: function(res){
                this.attachNewSelections($(res.data), res.status);
            },

            loadFail:function(data){
                console.log(data)
            },

            attachNewSelections: function(elemList, status){
                var that = this;
                fastdom.defer(function(){
                    that.$grid.append( elemList ).masonry('appended', elemList);
                    that.$grid.imagesLoaded().progress( function() {
                        that.$grid.masonry();
                    });
                });

                fastdom.defer(function(){
                    that.counter++;
                    that.doClear();
                    if(status!==1) {
                        that.loading_icon.hide();
                    }
                    that.loading = false;
                });
            }
        });
>>>>>>> Stashed changes

    return LoadTagEntity;
});


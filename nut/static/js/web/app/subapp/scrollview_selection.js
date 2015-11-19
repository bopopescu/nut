define(['jquery','libs/Class','libs/fastdom','masonry','jquery_bridget', 'images_loaded'],
    function($,Class,fastdom,Masonry,imagesLoaded){
        //imagesLoaded.makeJQueryPlugin($);
        $.bridget('masonry', Masonry);
        var ScrollEntity = Class.extend({
            init: function () {
                this.$selection = $('#selection');
                this.loading_icon = $('.loading-icon');
                this.shouldLoad = true;
                this.loading = false;
                this.initialize();
                this.counter = 1;
            },

            initialize : function () {
                var $grid = this.$selection.masonry({
                    isFitWidth:true,
                    resizeable:true,
                    itemSelector: '.selection-box'
                });
                $grid.imagesLoaded().progress( function() {
                    $grid.masonry();
                });
                this.$grid = $grid;
                $(window).scroll(this.onScroll.bind(this));
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

            doClear : function(){
                this.scrollTop = this.windowHeight = this.footerHeight = this.docHeight = null;
                this.read = null;
            },

            doRead:function(){
                this.scrollTop = $(window).scrollTop();
                this.windowHeight = $(window).height();
                this.footerHeight = $('#guoku_footer').height();
                this.docHeight = $(document).height();
                this.isOverScrolled =(this.windowHeight + this.scrollTop) >  (this.docHeight - this.footerHeight);
            },

            doWrite:function(){
                var that = this;
                if(!this.loading_icon || this.loading_icon.length <= 0){
                    this.loading = true
                }
                this.shouldLoad = this.isOverScrolled && (!this.loading);
                if(!this.shouldLoad){
                    this.doClear();
                }else{
                    this.loading = true;

                    fastdom.defer(function(){
                        that.loading_icon.show();
                    });

                    var aQuery = window.location.href.split('?');
                    var url = aQuery[0];
                    var p = 1, c = 0 ;
                    if(aQuery.length > 1){
                        var param = aQuery[1].split('&');
                        var param_p ;
                        if(param.length >1){
                            param_p = param[0].split('=');
                            p = parseInt(param_p[1]);
                        }
                    }
                    var time = this.$selection.attr('data-refresh');
                    var data = {
                        'p': p+this.counter,
                        'page':p+this.counter,
                        't':time
                    };
                    if(c !== 0){
                        data['c'] = c;
                    }
                    // defer to get loading_icon
                    fastdom.defer(30, function(){
                        $.when($.ajax({
                            url: url,
                            method: "GET",
                            data: data,
                            dataType:'json'

                        })).then(
                            that.loadSuccess.bind(that),
                            that.loadFail.bind(that)
                        );
                    });
                }
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

                    //
                    //that.$selection.imagesLoaded( function() {
                    //    that.$grid.append( elemList ).masonry('appended', elemList);
                        //that.$grid.masonry('layout');
                    //}).progress( function( instance, image ) {
                    //    var result = image.isLoaded ? 'loaded' : 'broken';
                    //    that.$grid.masonry();
                    //    console.log( 'image is ' + result + ' for ' + image.img.src );
                    //});
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

    return ScrollEntity;
});


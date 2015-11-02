define(['jquery','libs/Class','libs/fastdom'],
    function($,Class,fastdom){

    var LoadEntity = Class.extend({
        init: function(){
            this.$selection = $('#selection');
            this.page = this.$selection.parent().find('.pager');
            this.loading_icon = $('.loading-icon');
            this.counter = 1;
            this.page.hide();
            //this.loading_icon.hide();

            this.read = null;
            this.write = null;
            this.loading = false;
            this.shouldLoad = true;

            this.setupLoadWatcher();
        },
        setupLoadWatcher: function(){
            if (!this.$selection[0]) return;
            var flag = false;
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
            //this.read = this.write = null;
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
            this.shouldLoad = this.isOverScrolled && (this.counter%3 !== 0) && (!this.loading);

            if(!this.shouldLoad){
                this.doClear();
                return ;
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
            this.attachNewSelections($(res.data));
        },
        loadFail:function(data){
            console.log(data)

        },
        attachNewSelections: function(elemList){
            var that = this;

            fastdom.defer(function(){
                that.$selection.append(elemList);
            });
            fastdom.defer(function(){
                that.counter++;
                that.doClear();
                if (that.counter % 3 === 0){
                    that.loading_icon.hide();
                    that.page.show();
                }
                that.loading = false;
            });
        }
    });

    return LoadEntity;
//test
});
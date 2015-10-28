define(['bootstrap', 'libs/Class','underscore','jquery', 'fastdom'],function(boot, Class,_,$,fastdom){

    var Menu = Class.extend({
        init: function(){

            ///////////////////////////
            console.log('in Menu init, ');
            console.log(jQuery);
            ////////////////////////////

            this.$menu = $('#guoku_main_nav');
            this.scrollTop = null;
            this.lastScrollTop = null;
            this.read = this.write = null;

            this.setupScrollMenu();

        },
        setupScrollMenu: function(){
            $(window).scroll(this.scheduleHeaderMove.bind(this));
            //$(window).scroll(_.debounce(this.show.bind(this), 100));
        },
        scheduleHeaderMove:function(){


            var that = this;
            if (!this.read){
                this.read = fastdom.read(function(){
                    that.scrollTop = $(window).scrollTop();
                });
            }

            if(this.write) {
                fastdom.clear(this.write);
            }

            this.write = fastdom.write(this.moveHeader.bind(this));

            //console.log('onscroll');
            //var t = new Date();
            //console.log(t.getMilliseconds());
            //console.log()
        },
        moveHeader:function(){
            //console.log('move header');

            if (_.isNull(this.scrollTop)) {
                return ;
            }

            if (_.isNull(this.lastScrollTop)){
                this.lastScrollTop = this.scrollTop;
                return ;
            }

            if(this.lastScrollTop > this.scrollTop){
                this.showHeader();
            }else{
                this.hideHeader(this.scrollTop);
            }

            this.read = null;
            this.write= null;
            this.lastScrollTop = this.scrollTop;
        },



        showHeader: function(){
            //console.log('show header');
            this.$menu.removeClass('hidden-header');
            this.$menu.addClass('shown-header');
            //console.log((new Date()).getMilliseconds());

        },
        hideHeader: function(){
            //console.log('hideHeader');
            this.$menu.removeClass('shown-header');
            this.$menu.addClass('hidden-header');
            //console.log((new Date()).getMilliseconds());

        }


    });

    return  Menu;

});
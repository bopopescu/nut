define(['jquery', 'libs/Class', 'fastdom', 'underscore'],
    function($, Class, fastdom, _){
    var SideBarManager = Class.extend({
        init: function(){
            this.$fix_sidebar = $('#sidebar_fix');
            this.$footer = $('#guoku_footer');
            this.last_scroll = 0 ;
            this.current_scroll = 0 ;
            this.sideBarWidth = this.$fix_sidebar.width();

            this.$fix_sidebar.hide();

            if (!this.$fix_sidebar.length){
                return;
            }

            this.clear();
            this.setupScrollHandler();
        },
        clear: function(){
            if(this.read){
                fastdom.clear(this.read);
            }
            if(this.write){
                fastdom.clear(this.write);
            }
        },
        setupScrollHandler:function(){
            $(window).on('scroll', this.scrollHandler.bind(this));
        },
        scrollHandler: function(){
            this.clear();
            this.read = fastdom.read(this.readAction.bind(this));
            this.write = fastdom.write(this.writeAction.bind(this));
        },
        readAction: function(){
            this.current_scroll = $(window).scrollTop();

        },
        writeAction: function(){
            if (this.current_scroll>2020 && (this.last_scroll< 2020)){
                    //console.log($(window).scrollTop());
                    this.$fix_sidebar.width(this.sideBarWidth);
                    this.$fix_sidebar.css({position:'fixed', top:'60px', display:'block',opacity:0});
                    this.$fix_sidebar.stop().animate({opacity:1})
                }

            if (this.current_scroll>2020 && (this.last_scroll >= 2020)){
                    var fixbar_bound = this.$fix_sidebar[0].getBoundingClientRect();
                    var footer_bound = this.$footer[0].getBoundingClientRect();
                    if (fixbar_bound.bottom >= footer_bound.top){
                        this.$fix_sidebar.find('.remove-ready').css({opacity:0});
                    }else{
                        if (this.last_scroll > this.current_scroll){
                             this.$fix_sidebar.find('.remove-ready').css({opacity:1});
                        }
                    }
                }

            if (this.current_scroll < 2020 ){
                    this.$fix_sidebar.width('auto');
                    this.$fix_sidebar.css({position:'relative', top:'0px', opacity:0});
                }

            this.last_scroll = this.current_scroll;
        }


    });

    return SideBarManager;
});
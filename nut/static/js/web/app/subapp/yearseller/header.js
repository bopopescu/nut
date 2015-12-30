define(['jquery','libs/Class','fastdom'], function($,Class, fastdom){

    var YearSellerHeader = Class.extend({
        init: function(){
            this._navEle = $('.seller-banner-wrapper');
            this._fixTitle = this._navEle.find('.detach_nav');
            this.sectionIntros = $('.sections-item-intro-wrapper');
            this.setupScrollEventHandler();
            this.initSectionBackgrounds();

        },

        setupScrollEventHandler:function(){
            $(window).scroll(this.handleScroll.bind(this));
        },
        handleScroll: function(){
            this.handleNavDisplay();
        },
        getWindowHeight:function(){
            return window.innerHeight || document.documentElement.clientHeight;
        },
        handleNavDisplay: function(){
              if (!this._navEle[0]){
                return ;
              }
            this._clear();
            this._read = fastdom.read(this.readValues.bind(this));
            this._write = fastdom.write(this.writeChange.bind(this));
        },

        readValues : function(){
        //   pass , do nothing
        },
        writeChange :  function(){

            if (this.needDisplayFixNav()){
                this.displayFixTitle();
            }else{
                this.hideFixTitle();
            }

            this.moveSectionBackground();
        },

        initSectionBackgrounds: function(){
            this.sectionIntros.each(this.moveIntroBg.bind(this));
            this.sectionIntros.each(this.fadeinIntro.bind(this));
        },
        fadeinIntro: function(index, ele){
            $(ele).fadeIn();
        },
        moveSectionBackground: function(){
            this.sectionIntros.each(this.moveIntroBg.bind(this));
        },

        moveIntroBg: function(index, ele){
            var ele_bottom = ele.getBoundingClientRect().bottom;
            var ele_top = ele.getBoundingClientRect().top;
            var $bg_layer = ele.$bg_layer || (ele.$bg_layer = $(ele).find('.section-intro-bg-layer'));

            var window_height = this.getWindowHeight();
            if  (!((ele_top > window_height) || (ele_bottom < 0))){
                var bg_pos_y = this.calculateBgPosY(ele_bottom, window_height)
                $bg_layer.css({'transform': 'translateY('+ bg_pos_y +'px)'});
            }else{
                return ;
            }
        },
        calculateBgPosY: function(bottom,w_height){
            return  -200 * (bottom/w_height);
        },


        needDisplayFixNav: function(){
            this._nav_bottom = this._navEle[0].getBoundingClientRect().bottom;
            return this._nav_bottom < 50;

        },

        hideFixTitle:function(){
            this._fixTitle.addClass('hidden_nav');
        },
        displayFixTitle: function(){
            this._fixTitle.removeClass('hidden_nav');
        },

        _clear: function(){
            this._clearRead();
            this._clearWrite();
        },
        _clearRead: function(){
            fastdom.clear(this._read);
            this._read = null ;
        },
        _clearWrite:function(){
            fastdom.clear(this._write);
            this._write = null ;
        }


 });


    return YearSellerHeader;
});
define(['jquery','libs/Class','fastdom'], function($,Class, fastdom){

    var YearSellerHeader = Class.extend({
        init: function(){
            this._navEle = $('.seller-banner-wrapper');
            this._fixTitle = this._navEle.find('.detach_nav');
            this.setupScrollEventHandler()
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
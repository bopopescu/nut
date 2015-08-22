define(function(require){

    var IntroView = Backbone.View.extend({

        events: {

            'touchstart': 'touchstart',
            'touchmove': 'touchmove',
            'touchend': 'touchend',
            'touchcancel': 'touchend',

            'mousedown': 'touchstart',
            'mousemove': 'touchmove',
            'mouseup': 'touchend'


        },
        initialize: function(){
            //  console.log('in Page View ');
            this.pages = this.$('.scroll-page').get();
            this.currentPageIndex = this.pages.length -1;


        },

        getTransformX: function(ele){
            if (!ele) return null;
            var value = (new WebKitCSSMatrix(getComputedStyle(ele).webkitTransform)).m41;
            return value ;

        },

        getOriginEvent: function(event){

            return event.originalEvent ? event.originalEvent: event;

        },

        getCurrentPage: function(){
            return this.pages[this.currentPageIndex];
        },

        getPrevPage: function(){

            return this.pages[this.currentPageIndex + 1 ] ;
        },



        touchstart:function(event){
            event = this.getOriginEvent(event);



            this.startX = event.pageX || event.clientX;
            this.tracking = true;
            this.curPageX = this.getTransformX(this.getCurrentPage()) ;
            this.prevPageX = this.getTransformX(this.getPrevPage());

            //console.log(this.curPageX);

            this.getCurrentPage().style.webkitTransitionDuration = '0.3s';

            if (this.getPrevPage())
                this.getPrevPage().style.webkitTransitionDuration = '0.3s';


            return false;
        },

        movePageLeft: function(){
            if (this.getPrevPage()){

                this.getPrevPage().style.webkitTransform='startTranslateX(-102%)';
            }
            this.getCurrentPage().style.webkitTransform= 'startTranslateX(' + (this.curPageX + this.delta) + 'px)';

        },

        movePageRight: function(){
            var prv  = this.getPrevPage();
            if (prv) {
                prv.style.webkitTransform= 'startTranslateX(' + (this.prevPageX + this.delta) + 'px)';

            }
            this.getCurrentPage().style.webkitTransform="startTranslateX(0px)";

        },

        touchmove:function(event){
            event = this.getOriginEvent(event);
            if (this.tracking){
                var moveX = event.pageX || event.clientX;
                this.delta =( moveX - this.startX) * 1.2;
                if (this.delta < 0){
                    fastdom.write(this.movePageLeft, this);
                }else{
                    fastdom.write(this.movePageRight, this);
                }
            }
        },
        toPrev: function(){


            var prv =  this.getPrevPage();
            if (prv){
                prv.style.webkitTransitionDuration = '0.4s';
                prv.style.webkitTransform = "startTranslateX(0px)";

            }
            var cur =  this.getCurrentPage();
            cur.style.webkitTransitionDuration = '0.4s';
            cur.style.webkitTransform = "startTranslateX(0px)";

            this.currentPageIndex++ ;
            if (this.currentPageIndex >= this.pages.length){
                this.currentPageIndex--;
            }
            return ;
        },

        toNext :function(){
            var cur = this.getCurrentPage();
            if (this.currentPageIndex ===   0){
                cur.style.webkitTransitionDuration = '0.4s';
                cur.style.webkitTransform = "startTranslateX(0px)";
                return ;
            }


            cur.style.webkitTransitionDuration = '0.4s';
            cur.style.webkitTransform = "startTranslateX(-102%)";


            this.currentPageIndex--;
            if (this.currentPageIndex < 0){
                this.currentPageIndex++;
            }

        },

        stay: function(){
            var prv = this.getPrevPage();
            if (prv){
                prv.style.webkitTransitionDuration = '0.4s';
                prv.style.webkitTransform = "startTranslateX(-102%)";
            }
            this.getCurrentPage().style.webkitTransitionDuration = '0.4s';
            this.getCurrentPage().style.webkitTransform = "startTranslateX(0px)";
        },

        touchend: function(event){
            event = this.getOriginEvent(event);

            this.startX = 0 ;
            this.tracking = false ;
            this.curPageX = 0 ;
            this.prevPageX = 0 ;

            if (this.delta >= 80){
                fastdom.write(this.toPrev, this);
//                this.toPrev();
            }else if (this.delta <=  -80){
                fastdom.write(this.toNext, this);
//                this.toNext();
            }else{
                fastdom.write(this.stay,this);
            }


        }


    });

});
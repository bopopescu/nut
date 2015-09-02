

(function(Backbone){
    "use strict";
    if (!Backbone || !Backbone.View ||  !Backbone.View.extend){
        throw  new Error("need Backbone to go on !");
    }

    var newView = Backbone.View.extend({
          viewWillAppear: function(){
//              console.log('view will appear');
          },
          viewDidAppear: function(){
//              console.log('view did appear');
          },
          viewWillDisappear: function(){
//              console.log('view will disappear');

          },
          viewDidDisappear: function(){
//              console.log('view did disappear');

          },
          later : function(fn, time){
             if (_.isUndefined(time)) time = 0 ;
             fn = fn.bind(this);
             window.setTimeout(fn,time);
          },

        clearEle: function(ele){
          if (!_.isArray(ele)){
             ele = [ele];
          }
            _.each(ele, function(element){
                while(element.lastChild){
                    element.removeChild(element.lastChild);
                }
            });
        },

         enableTouch : function(){
              var moreEvents = {
                  'touchstart': '_touchStart',
                  'touchmove': '_touchMove',
                  'touchend': '_touchEnd',
                  'touchcancel': '_touchEnd'
              };
              //TODO : this will overlap the user's events object , if it has the touch* key !!!!

              this.events = _.extend(_.result(this,'events'), moreEvents);
              this.delegateEvents();
         },

        getOrgEvent: function(event){
            return event.originalEvent || event || {};
        },
         _touchStart: function(event){
             event = this.getOrgEvent(event);
             this.tracking = true;
             this.startX = event.pageX;
             //this.startY = event.pageY;
             this.shiftX = 0 ;
             // this.shiftY = 0 ;
             //console.log(event.pageX)
             return ;

         },
         _touchMove : function(event){
             if (this.tracking){
                 event = this.getOrgEvent(event);
                // console.log('touchmove');
                 this.shiftX = event.pageX-this.startX;
                 //this.shiftY = event.pageY-this.startY;
                 //console.log(this.shiftX);
                 if(this.shiftX >=100){
                     this.tracking  = false;
                     this.shiftX = 0 ;

                     this.trigger('swiperight');
                     // console.log('swept right');
                 }else if(this.shiftX <= -100){
                     this.tracking = false ;
                     this.shiftX = 0 ;
                     this.trigger('swipeleft');
                     // console.log('swept left');
                 }else{

                 }
                 return true;
             }
         },
         _touchEnd: function(event){

             if (this.tracking){
                 this.tracking = false ;
                 this.shiftX = 0 ;
                 // this.trigger('tap');

             }
             return true ;

         }
    });
    Backbone._oldview = Backbone.View;
    Backbone.View = newView;
})(Backbone);
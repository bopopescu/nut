define(function(require){
    var loginTpl  = $('#id-login-view-template').html();
    var LoginView = Backbone.View.extend({
        className : 'grid-cell',
        events: {
            'click .btn-user' : 'enter',
            'click .back-btn' : 'leave'
        },

        initialize : function(){
           this.template = _.template(loginTpl);

        },
        viewDidAppear: function(){

        },
        viewWillAppear: function(){

        },
        enter : function(){
            fastdom.write(this.beginEnter, this);
        },
        leave: function(){
//            console.log('leave');
            fastdom.write(this.beginLeave, this);
        },
        skipTouch: function(e){
                event.preventDefault ? event.preventDefault() : event.returnValue = false;
                if (e.cancelBubble) e.cancelBubble();
                return false;
        },

        disableCloneTouchMove: function(){
            this.clone.addEventListener('touchmove',this.skipTouch , false);
        },
        beginEnter: function(){
            // disable Nav and scroll ,  or the offset of the icon will changed!

            var that = this;
            // get a clone node
            this.clone  = this.getCloneNode();
            // disable clone transition , move it to the origin element position, make it invisible;
            this.clone.style.webkitTransition = 'none';

            this.disableCloneTouchMove();

            this.cloneIcon = this.clone.querySelectorAll('.icon-wrapper')[0];
            this.cloneIcon.style.opacity = 0 ;
            // find the background layer , this layer will be scaled
            this.cloneBg  = this.clone.querySelectorAll('.bg-layer')[0];
            // find the  back button and add an one time call back for return ;
            this.cloneBkBtn = this.clone.querySelectorAll('.back-btn')[0];
            this.cloneBkBtn.addEventListener('click', function goBack(){
                that.cloneBkBtn.removeEventListener('click', goBack);
                that.leave();
            });
            // attach the clone , the class will make it full screen ;
            this.clone.className = 'grid-full-cell';
            this.el.parentNode.appendChild(this.clone);

            // following will be excuted next frame , so dom change can take effect;
            fastdom.defer(function(){
                // caculate the start position of the icon , and move  Icon to there.
                // also set icon visible
                this.originOffset = this.$(".icon-wrapper").offset();
                this.currentOffset = $(this.cloneIcon).offset();
                this.startTranslateX = this.originOffset.left - this.currentOffset.left;
                this.startTranslateY = this.originOffset.top - this.currentOffset.top;
                this.cloneIcon.style.webkitTransform = 'translate(' + this.startTranslateX + 'px , ' + this.startTranslateY + 'px )';
                this.cloneIcon.style.opacity = 1 ;
                // after dom change take effect , following will excute next frame
                fastdom.defer(function(){
//                        console.log('ready to trans');
//                         call back for clean the listener
                          function tranEnd(){
//                              console.log('icon-wrapper entering end');
                              that.cloneIcon.removeEventListener('transitionEnd', tranEnd );
                              that.cloneIcon.removeEventListener('webkitTransitionEnd', tranEnd, false);
                              APP.disableNav();
                              APP.disableScroll();
                          }
                            // add the transition end listener
                          this.cloneIcon.addEventListener('transitionEnd',tranEnd);
                          this.cloneIcon.addEventListener('webkitTransitionEnd',tranEnd ,false);
                           // begin transition ;
                          this.cloneIcon.style.webkitTransition = '-webkit-transform 1s';
                          this.cloneIcon.style.webkitTransform = 'translate(0px,0px)';
                          this.cloneBg.style.webkitTransform = 'scale(20)';
                          this.cloneBkBtn.style.webkitTransform = 'translate(10px, -60px)';

                }, this);

            }, this);
        },

        getCloneNode: function(){
            return (this.cloneNode || this.el.cloneNode(true) );
        },
        beginLeave: function(){
// TODO: add event support for other brower than webkit
            var that = this;
            APP.enableScroll();
            APP.enableNav();
            this.cloneIcon.addEventListener('webkitTransitionEnd', transBackDone, false);
            this.cloneBg.style.webkitTransform = 'scale(1)';
            this.cloneIcon.style.webkitTransform = 'translate(' + this.startTranslateX + 'px , ' + this.startTranslateY + 'px )';
            function transBackDone(){
                console.log('we are back !');
                that.cloneIcon.removeEventListener('webkitTransitionEnd', transBackDone, false);
                //todo : detach the clone
                that.clone.removeEventListener('touchmove', this.skipTouch);
                that.clone.parentNode.removeChild(that.clone);

            }




        },
        render : function(){
            this.el.innerHTML = this.template();
            return this;
        }

    });

    return LoginView;

});
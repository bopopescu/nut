define(function(require){

    var defaultLessons = [
        {
            'lesson_name' : '课程名称1',
            'lesson_desc' :'经北京公安局刑侦总队调查核实，一起利用未公开信息交易案，操控“老鼠仓”的嫌疑人曾某落网 ',
            'lesson_state' : 'lesson-fin',
            'questions': [
                {
                    'question_type': 'selection',
                    'question_title': '问题1',
                    'question_body': '1 + 1 = ',
                    'question_selections': {
                        A : '2',
                        B : '4',
                        C : '6',
                        D : '8'
                    },
                    'question_answer' : 'A'
                },
                {
                    'question_type': 'selection',
                    'question_title': '问题2',
                    'question_body': '1 + 1 = ',
                    'question_selections': {
                        A : '2',
                        B : '4',
                        C : '6',
                        D : '8'
                    },
                    'question_answer' : 'A'
                },
                {
                    'question_type': 'selection',
                    'question_title': '问题3',
                    'question_body': '1 + 1 = ',
                    'question_selections': {
                        A : '2',
                        B : '4',
                        C : '6',
                        D : '8'
                    },
                    'question_answer' : 'A'
                },
                {
                    'question_type': 'selection',
                    'question_title': '问题4',
                    'question_body': '1 + 1 = ',
                    'question_selections': {
                        A : '2',
                        B : '4',
                        C : '6',
                        D : '8'
                    },
                    'question_answer' : 'A'
                }
            ]

        },
        {
            'lesson_name' : '课程名称2',
            'lesson_desc' :'中国人寿相关人士在接受21世纪经济报道采访时，表示对这一案件并不知情。',
            'lesson_state': 'lesson-unlock'
        },
        {
            'lesson_name' : '课程名称3',
            'lesson_desc' :'尽管保险公司投研团队鲜被市场公开信息披露，不过从A股上市公司披露的信息来看',
            'lesson_state': 'lesson-lock'
        },
        {
            'lesson_name' : '课程名称4',
            'lesson_desc' :'市场上曾流传国寿有投资经理因为老鼠仓被监管机关调查的消息。',
            'lesson_state': 'lesson-lock'
        }
    ];

    var tpl  = $('#id-button-view-template').html();
    var LessonListView = require('views/home/lesson');
    var ButtonView = Backbone.View.extend({
        className : 'grid-cell',
        events: {
            'click .icon-wrapper' : 'enter',
            'click .back-btn' : 'leave'
        },

        initialize : function(){
           this.template = _.template(tpl);
          // for event

           this._remove = this.remove;
           this.remove = function(){
               this.clearEvent();
               return this._remove();

           };
           this.initEvent();
           // end event;

//           console.log(this.model);

        },
        initEvent: function(){
            this.on('entered', this.onEntered, this);
            this.on('left', this.onLeft, this);
            this.on('beginEnter', this.onBeginEnter, this);
            this.on('beginLeave', this.onBeginLeave, this);
        },
        clearEvent: function(){
            this.off('enterd', this.onEntered);
            this.off('left', this.onLeft);
            this.off('beginEnter', this.onBeginEnter, this);
            this.off('beginLeave', this.onBeginLeave, this);
        },
        onBeginEnter: function(){
            fastdom.write(this.showLessons, this);
        },
        onBeginLeave: function(){
            fastdom.defer(this.hideLessons, this);
        },
        onEntered: function(){

        },
        onLeft: function(){
        },
        showLessons: function(){
            console.log('in show Lessons , ');
            console.log(this.model);
            this.lessonsView = new LessonListView({model : this.model.lessons || defaultLessons});
            fastdom.defer(function(){
               var   lessonLayer = this.lessonsView.render().el;
                     // initial state
                        lessonLayer.style.webkitTransition = 'none';
                        lessonLayer.style.webkitTransform = 'translate3d(0px, 200px,0px)';

                        lessonLayer.style.opacity = 0 ;
                        this.clone.appendChild(lessonLayer);
                      fastdom.defer(function(){
                          lessonLayer.style.webkitTransition ='all 0.5s';
                          lessonLayer.addEventListener('webkitTransitionEnd', function entered(){
                              console.log('lesson layer had entered ');
                              lessonLayer.removeEventListener('webkitTransitionEnd',entered);
                          });
                          lessonLayer.style.webkitTransform = 'translate3d(0px,0px,0px)';
                          lessonLayer.style.opacity = 1;
                          this.lessonLayer = lessonLayer;

                      }, this);
            }, this);


        },
        hideLessons: function(){
            var that  = this;
            var promise = new RSVP.Promise(function(resolve, reject){

                that.lessonLayer.addEventListener('webkitTransitionEnd', function left(){
                    console.log('lesson layer is out');
                    that.lessonLayer.removeEventListener('webkitTransitionEnd', left);
                    resolve(true);
                });

                fastdom.defer(function(){
                    var layerStyle = this.lessonLayer.style;
                    layerStyle.webkitTransform  = 'translate3d(0px, 200px,0px)';
                    layerStyle.opacity  = 0;

                }, that);



            });

            return promise;

//            this.lessons.leave().then(function(){
//                console.log('lesson is out');
//            })
//            .catch(function(error){
//                console.log(error);
//            })
//            ;


        },
        viewDidAppear: function(){
        },
        viewWillAppear: function(){
        },
        enter : function(){
            this.disableParentScroll();
            fastdom.write(this.beginEnter, this);
        },
        leave: function(){
//            console.log('leave');
            fastdom.write(this.beginLeave, this);
        },
        skipTouchMove: function(e){
            e.preventDefault();
            e.stopImmediatePropagation();
            console.log('block');
            return false;
        },
        disableParentScroll : function(){
            console.log('disable touch');
            $('#view-home .scroll .content')[0].addEventListener('touchmove',this.skipTouchMove);
            $('#view-home .scroll .content')[0].addEventListener('touchstart',this.skipTouchMove);

        },
        enableParentScroll: function(){
            console.log('enable touch');
            $('#view-home .scroll .content')[0].removeEventListener('touchmove', this.skipTouchMove);
            $('#view-home .scroll .content')[0].removeEventListener('touchstart',this.skipTouchMove);

        },
        beginEnter: function(){

            // disable Nav and scroll ,  or the offset of the icon will changed!
            var that = this;
            // get a clone node
            this.originOffset = this.$(".icon-wrapper").offset();
//            console.log(this.originOffset);
            this.clone  = this.getCloneNode();
            // disable clone transition , move it to the origin element position, make it invisible;
            this.clone.style.webkitTransition = 'none';
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

            document.body.appendChild(this.newLayer);

            // following will be excuted next frame , so dom change can take effect;
            fastdom.read(function(){
                // caculate the start position of the icon , and move  Icon to there.
                // also set icon visible

                this.currentOffset = $(this.cloneIcon).offset();
                this.startTranslateX = this.originOffset.left - this.currentOffset.left;
                this.startTranslateY = this.originOffset.top - this.currentOffset.top;
                fastdom.write(function(){

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
                                  that.trigger('entered');
                                  APP.disableNav();
                                  APP.disableScroll();
                              }

                              this.trigger('beginEnter');
                                // add the transition end listener
                              this.cloneIcon.addEventListener('transitionEnd',tranEnd);
                              this.cloneIcon.addEventListener('webkitTransitionEnd',tranEnd ,false);
                               // begin transition ;
                              this.cloneIcon.style.webkitTransition = 'all 1s';
                              this.cloneIcon.style.webkitTransform = 'translate(0px,0px)';
                              this.cloneBg.style.webkitTransform = 'scale(20)';
                              this.cloneBkBtn.style.webkitTransform = 'translate(10px, -60px)';

                    }, this);
                }, this);

            }, this);
        },

        getCloneNode: function(){
            this.clone =  this.el.cloneNode(true);
            this.newLayer = $('<section class="drama"><div class="grid-container"></div></section>');
            this.newLayer.find('.grid-container').append(this.clone);
            this.newLayer = this.newLayer[0];
            return this.clone;
        },
        shrink: function(){

           var promise = new RSVP.Promise((function(resovle, reject){
               var that = this;
               //APP.enableNav();
               this.cloneIcon.addEventListener('webkitTransitionEnd', transBackDone, false);

               this.cloneBg.style.webkitTransform = 'scale(1)';
               this.cloneIcon.style.webkitTransform = 'translate(' + this.startTranslateX + 'px , ' + this.startTranslateY + 'px )';
               this.cloneIcon.style.opacity = 0 ;
               function transBackDone(){
                   console.log('icon transform back !');
                   that.cloneIcon.removeEventListener('webkitTransitionEnd', transBackDone, false);
                   resovle(true);
               }

            }).bind(this));
            return promise;
        },
        beginLeave: function(){
// TODO: add event support for other browser than webkit

//            this.trigger('beginLeave');

            var p1 = this.hideLessons();
            var p2 = this.shrink();
            RSVP.all([p1,p2]).then((function(){
                this.trigger('left');
                console.log('all done!');


               fastdom.defer(function(){

                   this.lessonsView.remove();
                   this.lessonsView = null;
                   document.body.removeChild(this.newLayer);
                   this.newLayer = null;
                   this.enableParentScroll();

               }, this);

            }).bind(this));



        },
        render : function(){
            this.el.innerHTML = this.template(this.model);
            return this;
        }

    });

    return ButtonView;

});
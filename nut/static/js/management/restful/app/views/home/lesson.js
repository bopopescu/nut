define(function(require){
    var tpl = _.template($('#id-lesson-list-view-template').html());
    var lessonTpl = _.template($('#id-lesson-view-template').html());

    var QuestionView  = require('views/home/questions');
    var QuestionController  = require('controllers/testingController')

    var defaultQuestions =  [
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
            'question_answer' : '2'
        },
        {
            'question_type': 'selection',
            'question_title': '问题2',
            'question_body': '1 +2 = ',
            'question_selections': {
                A : '2',
                B : '3',
                C : '6',
                D : '8'
            },
            'question_answer' : '3'
        },
        {
            'question_type': 'selection',
            'question_title': '问题3',
            'question_body': '1 + 3 = ',
            'question_selections': {
                A : '2',
                B : '4',
                C : '6',
                D : '8'
            },
            'question_answer' : '4'
        },
        {
            'question_type': 'selection',
            'question_title': '问题4',
            'question_body': '1 + 4 = ',
            'question_selections': {
                A : '2',
                B : '4',
                C : '5',
                D : '8'
            },
            'question_answer' : '5'
        }
    ];

    var LessonView = Backbone.View.extend({
        tagName : 'li',
        className: 'lesson',
        events: {
            'click .btn-lesson': 'showTest'
        },
        showTest:function(){

           this.expand()
               .then(this.showQuestion.bind(this))
               .then(this.shrink.bind(this))
               .catch(function(error){
                   console.log(error);
                   console.log(error.stack);
               });

            console.log('show' + this.model.lesson_name);
        },

        expand: function(){
            var promise = new RSVP.Promise((function(resolve, reject){

                fastdom.defer(function(){
                    console.log('expand');
                    console.log(this.tagName);

                    resolve(true);
                },this);

            }).bind(this));
            return promise;
        },

        showQuestion: function(){

            var questionController = new QuestionController({model : this.model});
            return  questionController.work();

//            var promise = new RSVP.Promise((function(resolve, reject){
//
//
//                fastdom.defer(function(){
//                    console.log('showQuestion');
//                    var question  = new QuestionView({
//                        model: this.model.questions || defaultQuestions ,
//                    });
//
//
//                    question.resolve = resolve;
//
//                    // I want showQuestion return a promise ,
//                    // only resolve when question view is being destroied !!!!
//
//                   // throw new Error("ant stuck here")
//                    document.body.appendChild(question.render().el);
//                   // resolve(true);
//                }, this);
//
//            }).bind(this));
//            return promise;
        },
        shrink: function(){
            var promise = new RSVP.Promise((function(resolve,reject){
                fastdom.defer(function(){
                    console.log('shrink');
                    resolve(true);

                }, this);
            }).bind(this));

            return promise;
        },

        render: function(){
            this.$el.html(lessonTpl(this.model  || {}));
            return this;
        }

    });

    var LessonListView = Backbone.View.extend({
        tagName : 'div',
        className  : 'lessons-container',
        events: {
//           'scroll .lesson-list': 'onScroll'
        },
        initialize: function(){
//            console.log('in lesson list');
        },
        enter: function(){
            console.log('enter');
        },
        loop : function(){
            // do something
//            var now = (new Date()).getTime();
//            console.log('frame-time : ' +  (now - this.frameStartTime));
//            console.log('frame-number : ' + this.frameCount++);
//            this.frameStartTime = now;


            this.setLessonScale();
            if(this.scrolling){
                fastdom.defer(this.loop, this);

            }else{
//                console.log('last loop');
            }
        },

        setLessonScale: function(){
//            var initialScale = 0.9,
//                factor = 0.1,
//                pi = 3.1415,
//                currentIndexPosition = ( this.scrollLeft + 160 - 40 ) / 240;
//            var position = Math.floor(currentIndexPosition);
//            var angle = (currentIndexPosition - position) * pi / 2 ;
//            var scale = initialScale + factor * Math.sin(angle);
//            this.lessions[position].style.webkitTransform='scale('+scale+')';
        },
        onScroll: function(event){

            if (!this.scrolling){
                this.frameCount = 0 ;
                this.frameStartTime = (new Date()).getTime();

                console.log('start Scroll');
                fastdom.defer(this.loop, this);

            }

            this.scrollLeft = event.target.scrollLeft;
            this.scrolling = true;

            function unsetScroll(){
                this.scrolling = false;
                console.log('stop scroll');
            }

            if (this.scrollingMarker){
                fastdom.clear(this.scrollingMarker);
                this.scrollingMarker = null;
            }

            this.scrollingMarker = fastdom.defer(10, unsetScroll, this);

        },
        render: function(){
            this.$el.html(tpl(this.model||{}));
            this.listContainer = this.$('.lesson-list')[0];
            this.listContainer.addEventListener('scroll' , this.onScroll.bind(this), false);
            _.each(this.model, function(lesson){
               var lv = new LessonView({model: lesson});
                   this.listContainer.appendChild(lv.render().el);
            },this);

            return this;
        }
    });
    return LessonListView;
});
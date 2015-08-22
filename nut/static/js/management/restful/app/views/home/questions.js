define(function(require){
    var tpl = _.template($('#id-question-view-template').html());
    var resultTpl = _.template($('#id-question-result-template').html());
    var QuestionView = Backbone.View.extend({
        tagName : 'section',
        className: 'comedy',
        events:{
            'click header .left' : 'back',
            'click .btn-check-question' : 'checkAnswer',
            'click .btn-continue' : 'nextQuestion',
            'click .answer-option' : 'setAnswer',
            'click .btn-test-over' : 'testOver'

        },
        initialize: function(){
            console.log('question view init');

            //In Backbone.View , the default mergeable property  does not include 'controller'
            // so I add it in backbone source !!!
            // dam this comment is highly likly to be fogotten
            // I should write a test on it !!!!

            this.listenTo(this.controller, 'questionfail', this.questionFail);


        },

        questionFail: function(){
           // alert('question fail');
            if (this.$('header .fa-heart').length){
                this.$('header .fa-heart')[0].classList.add('disappear');
            }


        },
        checkAnswer: function(e){
           if (!this.controller.isQuestionAnswered(this.model.questionIndex)){
               this.showAlert('请您先选择一个答案');
                return ;
           }
           var result  =   this.controller.checkQuestionAnswer(this.model.questionIndex);

            this.showQuestionResult(result).then(this.makeContinueButton.bind(this));

        },

        showQuestionResult: function(result){
            var promise = new RSVP.Promise(function(resolve, reject){
                var selector = result ? '.result_right' : '.result_wrong';
                this.$(selector).css({display: 'block'});

                resolve(true);
            });
            return promise;
        },

        makeContinueButton: function(){
            this.$('.btn-check-question')
                .removeClass('btn-check-question')
                .addClass('btn-continue')
                .html('继续');
        },

        nextQuestion: function(){
            this.controller.showNextQuestion();
        },
        setAnswer: function(event){
            var answer = event.target.innerHTML;
            this.$('.answer-option').removeClass('choosed');
            $(event.target).addClass('choosed');
            fastdom.defer(function(){
                // todo:  the "not" method  is a jquery dependent , remove it
                this.$('.answer-option').not('.choosed').css({display: 'none'});
                this.controller.recordQuestionAnswer(this.model.questionIndex,answer );

            },this);

        },

        render : function(model){
            this.model = model ;
            console.log(model);
            this.$el.html(tpl(model || {}));
            return this;
        },
        back: function(){
            console.log('back from question');
            this.remove();
            this.controller.testOver();

            //this.resolve(true);
        },

        showAlert: function(str){
            alert(str);
        },


        showQuestion: function(model){

            console.log('in question view : show Question');

            var  promise = new RSVP.Promise((function(resolve, reject){

                this.render(model);
                fastdom.write(function(){
                    if(!document.contains(this.el)){
                        document.body.appendChild(this.el);
                    }
                    fastdom.defer(function(){
                        resolve();
                    });
                }, this);


            }).bind(this));

            return promise;


        },
        showTestResult: function(result){
            console.log(result);
            var promise = new RSVP.Promise((function(resolve, reject){
                fastdom.defer(function(){
                    this.renderResult(result);
                    this.$('.test-result').css({display: 'block'});
                    resolve(true);
                },this);

            }).bind(this));

            return promise;

        },

        showTestFail: function(){

            this.$('.test-fail').css({display: 'block'});

        },
        renderResult: function(result){
             this.$('.test-result').html(resultTpl(result));
        },
        testOver: function(){

            this.controller.testOver();
        },


    });

    return QuestionView;

});
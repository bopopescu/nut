define(function(require){

   var viewsList = [
       {

       'level' : ' level1',
       'btn_class': 'btn-user',
       'btn_icon': 'fa-user',
       'lessons' :
           [
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
                   },
                   {
                       'question_type': 'selection',
                       'question_title': '问题5',
                       'question_body': '4 + 4 = ',
                       'question_selections': {
                           A : '2',
                           B : '4',
                           C : '5',
                           D : '8'
                       },
                       'question_answer' : '8'
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
           ]
       },
       {

           'level' : ' level2',
           'btn_icon': 'fa-key',
           'btn_class': 'btn-author',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程21'
                   },
                   {
                       'lesson_name' : '课程22'
                   }
               ]

       },
       {

           'level' : ' level3',
           'btn_icon': 'fa-comment',
           'btn_class': 'btn-message',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },
       {

           'level' : ' level4',
           'btn_icon': 'fa-check',
           'btn_class': 'btn-todo',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },
       {

           'level' : ' level5',
           'btn_icon': 'fa-key',
           'btn_class': 'btn-author',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level6',
           'btn_icon': 'fa-comment',
           'btn_class': 'btn-logistic',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level7',
           'btn_icon': 'fa-comment',
           'btn_class': 'btn-message',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level8',
           'btn_icon': 'fa-gear',
           'btn_class': 'btn-config',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level9',
           'btn_icon': 'fa-check',
           'btn_class': 'btn-todo',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       }, {

           'level' : ' level5',
           'btn_icon': 'fa-key',
           'btn_class': 'btn-author',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level6',
           'btn_icon': 'fa-comment',
           'btn_class': 'btn-logistic',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level7',
           'btn_icon': 'fa-comment',
           'btn_class': 'btn-message',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level8',
           'btn_icon': 'fa-gear',
           'btn_class': 'btn-config',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       },

       {

           'level' : ' level9',
           'btn_icon': 'fa-check',
           'btn_class': 'btn-todo',
           'lessons' :
               [
                   {
                       'lesson_name' : '课程31'
                   },
                   {
                       'lesson_name' : '课程32'
                   }
               ]

       }

   ];
 console.log(viewsList);
    var ButtonView = require('views/home/ButtonView');
    var views  = [];
    for (var i = 0 ; i< viewsList.length ; i++){
         views.push(new ButtonView({model: viewsList[i]}));
    }

//    var views = [
//      new  (require('views/home/login'))(),
//      new  (require('views/home/message'))(),
//      new  (require('views/home/config'))(),
//      new  (require('views/home/todo'))(),
//      new  (require('views/home/author'))(),
//        new  (require('views/home/login'))(),
//        new  (require('views/home/login'))(),
//        new  (require('views/home/login'))(),
//        new  (require('views/home/login'))(),
//        new  (require('views/home/login'))(),
//      new  (require('views/home/logistic'))()
//
//    ];
    var HomeView = Backbone.View.extend({
        initialize: function(){
            console.log('in apphome view');
            this.subViews = views;
            this.subViewContainer = this.$('.grid-container')[0];
            fastdom.write(this.render, this);

            // TODO :  current backbone has a remove method for views
            // the default remove method stop listen ,and call $(jquery or zeptor) 's remove method
            // to remove event listener's on the el ,  to prevent leak
            // but for a view that has subviews ,
            // when parent view is removed ,
            // it should call the subview remove method first, only after those are done ,
            // then parent view can call its own remove method

        },
        render: function(){
            fastdom.write(function(){
                _.each(this.subViews, this.addCell, this);
            }, this);

            return this;
        },
        addCell: function(view){

            this.subViewContainer.appendChild(view.render().el);
        }
    });
    return HomeView;
});

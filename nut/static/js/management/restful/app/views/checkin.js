define(function(require){

    var PackageListView  = require('views/package');


    var checkinDetailView = Backbone.View.extend({
        tagName : 'section',
        className : 'hidden detail_view',
        templateId : 'id-checkin-detail-template',
        template: _.template($('#id-checkin-detail-template').html()),
        events:{

            'click header .left' : "back",
            'click header .right' : "save"

        },

        initialize: function(){
            this.packageList = new PackageListView({

            });


        },
        back: function(){
            var that  = this ;
//            console.log(event);
            this.viewWillDisappear();
            var fn = function(){ that.viewDidDisappear(); };
            APP.slide( APP.views["view-checkin"].el, this.el,  "sr" ,fn);

        },


        viewWillDisappear: function(){
            fastdom.defer(this.save, this);

        },

        viewDidDisappear: function(){
            APP.enableNav();
        },

        viewWillAppear: function(){
            APP.disableNav();
        },

        render : function(){
            var that  = this;

            fastdom.defer(function(){
                    this.$el.html(that.template(this.model.toJSON()));
                    this.packageList.collection = this.model.get('packages');
                    this.packageList.collection.checkin = this.model;
                    this.$('.addtional-info').append(this.packageList.render().el);
                    this.packageList.delegateEvents();
            }, this);
           // this.$('.addtional-info').append(this.packageList.render().el);



            return this;
        },

        save : function(){
            fastdom.defer(function(){
                this.model.set(this.extractInputs());
                fastdom.defer(function(){
                    this.model.save();
                }, this);

            }, this);

        },
        extractInputs : function(){
            var obj = {};
            // use the main-info class selector to limit input extract in main fields

            this.$('.main-info input,textarea,select').each(function(index, el){

                obj[el.name] = el.value;
            });
            return obj;

        },

    });

    var checkinItemView = Backbone.View.extend({
        tagName: 'li',
        className: "list-item",
        template: _.template($('#id-checkin-item-template').html()),
        events: {
            'click .button-del' : 'deleteCheckin',
            'click .innerLi' : 'detail'

        },

        detail:function(event){
            var that = this ;
            // console.log(this.model);
            var detailView = this.getDetailView();
            detailView.model = this.model;
            detailView.render();

            detailView.viewWillAppear();
            var fn = function(){
                detailView.viewDidAppear();

            };



            APP.slide(detailView.el, APP.views["view-checkin"].el,  "sl" ,fn);
            // or we can us deferr ?
//                .start(function(){})
//                .done(function(){});



            // console.log(event);
        },

        getDetailView: function(){

            (APP.views["checkin-detail"] ) || (APP.views["checkin-detail"] = this.createDetailView());
            return APP.views["checkin-detail"];


        },

        createDetailView : function(){
            var view  = new checkinDetailView();
            view.$el.appendTo(document.body);
            return view;
        },



        deleteCheckin: function(){
            var that = this;
            // console.log('delete product');
            onTransitionEnd  = function(){
                // console.log('product item animation end');
                that.el.removeEventListener('webkitTransitionEnd', onTransitionEnd, false);
                that.el.removeEventListener('transitionEnd',       onTransitionEnd);
                that.model.destroy();
                that.remove();

            };
            this.el.addEventListener('webkitTransitionEnd', onTransitionEnd, false);
            this.el.addEventListener('transitionEnd',       onTransitionEnd);

            this.el.classList.add('deleting');
        },

        initialize: function(){
            this.listenTo(this.model, 'change', this.render);
            this.enableTouch();
            this.on('swipeleft', this.showDelButton);
            this.on('swiperight', this.hideDelButton);
        },
        showDelButton: function(){
            this.delButton  = this.$('.button-del')[0];
            this.productItem = this.$('.innerLi')[0];
            this.delButton.classList.remove('del-hide');
            this.productItem.classList.add('can-del');
        },
        hideDelButton: function(){
            this.delButton  = this.$('.button-del')[0];
            this.productItem = this.$('.innerLi')[0];
            this.delButton.classList.add('del-hide');
            this.productItem.classList.remove('can-del');

        },

        render : function(){
            fastdom.write(function(){
                var template = this.template;
                this.$el.html(template(this.model.toJSON()));
                return this;
            }, this);

            return this;

        }

    });
    var checkinView = Backbone.View.extend({

        initialize: function(){
            console.log('in checkin view');

            this.listenTo(this.collection, 'reset', this.render );
            this.listenTo(this.collection, 'add', this.collectionAdd);
            this.listContainer = this.$('.list-container')[0];
            this.clearEle(this.listContainer);

           // or ? wait for view to show , then fetch()?:
            this.collection.fetch({reset: true});
        },

        events:{
             "click #checkin-add-button" : "newItem",

        },

        logTime: function(){
            var date = new Date();
            console.log(date.getTime());
        },
        logTimeSpan: function(start){
            var date = new Date();
            console.log(date-start);
        },
        newItem : function(){
            var that = this;
            var newModel =  this.collection.create({
                supplier:"请填写供应商名称"
            });
            //console.log(newModel);
            var detailView = this.getDetailView();
            detailView.model = newModel;

            var fn = function(){
                detailView.viewDidAppear();
            };
            fastdom.write(function(){
                APP.slide(detailView.el, APP.views['view-checkin'].el,"popin",fn);
                fastdom.write(function(){
                    detailView.render();
                    detailView.viewWillAppear();
                });


            });



        },

        getDetailView: function(){

            ( APP.views["checkin-detail"] ) || (APP.views["checkin-detail"] = this.createDetailView());
            return APP.views["checkin-detail"];


        },

        createDetailView : function(){
            var view  = new checkinDetailView();
            view.$el.appendTo(document.body);
            return view;
        },

        collectionAdd: function(itemData){
            console.log(itemData);
            this.insertItemView(itemData);
            //this.render();
            // console.log('collection add');
        },

        insertItemView: function(model){
            var item = new  checkinItemView({model : model});
            fastdom.write(function(){
                this.listContainer.insertBefore(item.render().el, this.listContainer.firstChild);
            }, this);

        },

        render: function () {
            this.clearEle(this.listContainer);
            var container = this.listContainer;
            this.collection.each(function (model) {
                if (model.get('hidden') === true) {
                    return;
                }

                var item = new checkinItemView({
                    model: model
                });

                container.appendChild(item.render().el);

            });
            return  this;

        },
        test : function(){

            var PackageCollection =  require('models/package');
            var     Package = PackageCollection.prototype.model;
             // clear all local storage


             console.log('relational test begin //////////////////');

             var checkin = this.collection.create({supplier:'ant_test_999'});
             console.log(checkin);
             //create return a model instance !!!! not the promise
             //and create will save data into store!!!
            // TODO: if the create is sync or async ?


             var result =  checkin.save();

              result.then(function(re){
                  console.log('in promise then argument ');
                  console.log(re);
              });

            console.log('this should happend before the promise then argument');
            console.log(result);
          //  console.log(result.state());
             // save return a promise
              var pc = new Package({checkin:checkin});
              //pc.save();

            console.log('what is in the checkin\'s  packages ?');
            console.log(checkin.get('packages'));

               checkin.save().then(function(){

//                   pc.set('package_product_name','tooooo');
//                   checkin.save();
               });

           //  pc.save();

            console.log('package_product_name : ' + pc.get('package_product_name'));

            console.log('package\'s checkin + ' , pc.get('checkin'));

            console.log('relational test end//////////////////////');

        }

    });
    return checkinView;
});
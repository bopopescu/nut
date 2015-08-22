define(function(require){
    var PackageCollection =  require('models/package');
    var     Package = PackageCollection.prototype.model;

    var PackageItemView = Backbone.View.extend({
        tagName: 'li',
        className: 'package item-list',

        template: _.template($('#id-package-item-template').html()),
        events : {
            'click .action-remove': 'showDelButton',
            'click .btn-del': 'removePackage',
            'change ': 'packageChange'
        },


        initialize:function(){
            console.log('in package item view ');
            this.enableTouch();
            this.on('swiperight', this.hideDelButton, this);

        },
        render : function(){
            this.$el.html(this.template(this.model.toJSON()));

            return this;
        },
        showDelButton: function(){
            this.$('.package-wrap').addClass('can-del');
        },
        hideDelButton: function(){
            this.$('.package-wrap').removeClass('can-del');
        },

        packageChange: function(){
            this.model.set(this.extractInputs());
            this.model.save();
        },

        extractInputs: function(){
            var obj = {};
            this.$('input,textarea,select').each(function(index, el){

                obj[el.name] = el.value;
            });
            return obj;
        },
        removePackage: function(){

            this.$el.addClass('deleting');
            this.later(function(){
                this.model.destroy();
                this.remove();
            },500);

            console.log('removing package');
        }
    });
    var PackageListView = Backbone.View.extend({
        tagName : 'div',
        className: 'package-list',
        template: _.template($('#id-package-list-template').html()),

        events : {
            'click .tail-action': 'addPackage',

        },
        initialize: function(){
          console.log('in package list view');
        },
        render: function(){
            this.$el.html(this.template());
            var tailAction = this.$('.tail-action');
            this.collection.each(function(packageModel){
                 var item = new PackageItemView({model: packageModel});
                 tailAction.before(item.render().el);

            });

            //console.log('package list render');
            return this;
        },

        insertPackage: function(package){
                var that = this;
                var promise = new RSVP.Promise(function(resolve, reject){
                       var tailAction = this.$('.tail-action');
                       var item = new PackageItemView({model : package});


                       tailAction.before(item.render().el);
                       item.$el.addClass('adding');

                       that.later(function(){
                            resolve(item.el);
                           item.$el.removeClass('adding');
                       },500);
                });
                return promise;
        },

        addPackage: function(){
            var that = this;
            this.getNewPackage()
                .then(function(package){
                     console.log(package);

                     that.collection.add(package);
                     package.set('checkin', that.collection.checkin);

                     package.save();
                     return that.insertPackage(package);


                }).then(function(){
//                     console.log('insert new package done');
                })
                .catch(function(fail){
                    console.assert(false, fail);
                });

            console.log('add package');

        },

        getNewPackage: function(){
           var that = this;
           var promise = new RSVP.Promise(function(resolve, reject){

//
//               var that = this;
//               console.log('scan');
//               // use scandit
//               // scandit app key "joZgcLxkEeOGKAkPrHUri37zC0AkiVvCVfFz08b7KQw"
//               cordova.exec(function(result){
//                   that.$('input[name="barcode"]').val(result[0]);
//               }, function(error){
//                   console.log('scan canceled' + error);
//               }, "ScanditSDK", "scan", ["joZgcLxkEeOGKAkPrHUri37zC0AkiVvCVfFz08b7KQw", {"beep": true,
//                   "1DScanning" : true,
//                   "2DScanning" : true}]);


               that.later(function(){
                   resolve(new Package({package_product_name : 'ant_package', count:998}));
               });
           });

           return promise ;

        }

    });

    return PackageListView;
});
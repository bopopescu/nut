define(function(require){
// about git http://stackoverflow.com/questions/5772192/git-how-can-i-reconcile-detached-head-with-master-origin



    var productDetailView = Backbone.View.extend({
        tagName : 'section',
        className : 'hidden product_detail_view',
        template : _.template($('#product_detail_template').html()),
        events: {
            "click header .left" : "back",
            "click header .right": "save",

          // "click input,textarea" : "handleInputClick",
            // use keyup to handle mobile input ,
            //  : user can type in the input and press save,
            //    without triggering the change event!
           // "keyup input,textarea" : "change",

            "change" : "save",
            // we only need change event be fired once
            // , so we only use "keyup" not change!
          //  "change input,textarea" : "change"
            "click .img-holder" : "changeImg",
            "click .barcode-trigger":"scan"

        },

        scan  : function(){
            var that = this;
            console.log('scan');
            // use scandit
            // scandit app key "joZgcLxkEeOGKAkPrHUri37zC0AkiVvCVfFz08b7KQw"
            cordova.exec(function(result){
                that.$('input[name="barcode"]').val(result[0]);
            }, function(error){
                console.log('scan canceled' + error);
            }, "ScanditSDK", "scan", ["joZgcLxkEeOGKAkPrHUri37zC0AkiVvCVfFz08b7KQw", {"beep": true,
                "1DScanning" : true,
                "2DScanning" : true}]);

            // use https://github.com/wildabeast/BarcodeScanner
//            cordova.plugins.barcodeScanner.scan(function(result){
//
//               that.$('input[name="barcode"]').val(result.text);
//            }, function(error){
//                console.log(error);
//            });
        },

        changeImg: function(event){

            //TODO : save image data into data store is a VERY BAD idea
            //fix it !!!!!
            if(!navigator.camera){
                alert('no camera!!');
                return ;
            }

            var options = {
                quality: 90,
                destinationType: Camera.DestinationType.DATA_URL,
                sourceType: Camera.PictureSourceType.CAMERA,
                allowEdit : true,
                encodingType: Camera.EncodingType.JPEG,
                saveToPhotoAlbum: false

            };

            navigator.camera.getPicture(function(imgData){
                 this.$('.form-main-img').attr('src',"data:image/jpeg;base64," + imgData);


                //TODO : save image data into data store is a VERY BAD idea
                //TODO : fix it !!!!!
                 this.$('input[name="imgData"]').val(imgData);



                 console.log('got img Data');
            },function(){
                console.log('error getting pic');
            },options);
        },
        initialize: function(){

        //TODO : need focus on input element is clicked
        

        },
        extractInputs : function(){
            var obj = {};
            this.$('input,textarea').each(function(index, el){
                obj[el.name] = el.value;
            });
            return obj;

        },
        handleInputClick: function(){
          //  alert(event.target.tagName);
           // alert(event.target.tagName);
            event.target.focus();
        },

        save : function(){
             this.model.set(this.extractInputs());
             this.model.save();
        },

        change: function(event){ //
//            console.log(event.type);
//            console.log(event.currentTarget.name);
            this.model.set(event.currentTarget.name, event.currentTarget.value);

//            console.log(this.model.toJSON());
        },
        back : function(event){
            var that  = this ;
//            console.log(event);
            this.viewWillDisappear();
            var fn = function(){ that.viewDidDisappear(); };
            APP.slide( APP.views["view-product"].el, this.el,  "sr" ,fn);

        },

        viewWillDisappear: function(){
//            console.log('changed model ? ');
//            console.log('is chaged ? ' + this.model.hasChanged());
//            console.log(this.model.changedAttributes());
//
//            console.log(this.model.toJSON());
//            console.log(this.model.hasChanged());

           // if (this.model.hasChanged){
                this.save();
           // }


        },

        viewDidDisappear: function(){
            APP.enableNav();
        },

        viewWillAppear: function(){
             APP.disableNav();
        },
        render: function(){

            this.$el.html(this.template(this.model.toJSON()));
            this.removeSaveButton();
            this.model.once('change', this.addSaveButton, this);

            return this;
        },

        addSaveButton: function(){
//            console.log('add Save Button');
            this.$('button.right').removeClass('hidden');
        },
        removeSaveButton: function(){
//            console.log('remove Save button ');
            this.$('button.right').addClass('hidden');
        }

    });

    var productItemView = Backbone.View.extend({



        tagName : "li",
        className : "list-item",
        template : _.template($('#product_item_template').html()),

        initialize: function(){
            this.listenTo(this.model, 'change' , this.render);
            this.delButton  = this.$('.button-del')[0];
            this.enableTouch();
            this.on('swipeleft',this.showDelButton, this);
            this.on('swiperight', this.hideDelButton, this);
            this.on('tap', this.detail, this);
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
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },


        events:{

          "click .button-del": "deleteProduct",
          "click .innerLi" : "detail",



        },



        deleteProduct: function(event){
            var that = this;
           // console.log('delete product');

           //TODO : check event's listener still bind this view , they should be removed;

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
            APP.slide(detailView.el, APP.views["view-product"].el,  "sl" ,fn);
            // or we can us deferr ?
//                .start(function(){})
//                .done(function(){});



           // console.log(event);
        },

        getDetailView: function(){

            APP.productDetailView = APP.productDetailView || this.createDetailView();
            return APP.productDetailView;
        },

       createDetailView : function(){
           var view  = new productDetailView();
           view.$el.appendTo(document.body);
           return view;
       },



    });

    var productView = Backbone.View.extend({
        initialize: function(){
            console.log('in product view');
            this.originalCollection = this.collection;

            this.listenTo(this.collection, 'reset', this.render );
            this.listenTo(this.collection, 'add', this.collectionAdd);

            this.listContainer = this.$('.list-container');
            this.clearEle(this.listContainer.get());
            this.collection.fetch({reset: true});

        },

        events: {
            "click #product-add-button": "new",
            "keyup #product-search": "search",
            "change input":"search",
            "click #barcode-button":"scan"

        },

        scan : function(){

            var that = this;
            cordova.exec(function(result){
                that.$('#product-search').val(result[0]);
                that.search();
            }, function(error){
                console.log('scan canceled' + error);
            }, "ScanditSDK", "scan", ["joZgcLxkEeOGKAkPrHUri37zC0AkiVvCVfFz08b7KQw", {"beep": true,
                "1DScanning" : true,
                "2DScanning" : true}]);
        },

        search: function(){

            // search through collection
            // pick some field , join them , check keyword's position
            // if keyword found , set model's hidden property to false;
            // if keyword not found, set model's hidden property to true;
            // of cause , if keyword is empty , set all model's hidden prop to false, these will display them all

            //performance consideration
            //for small group of product list , just filter the whole list ,
            //for large list ,
            //         1, maybe catch the source's value
            //         2, maybe not render hole list , just change the subview's html
            //         3, paging : just filter the product to  first page , when people scroll down filter another page.
            //            you can use generator to do that !
            //         4,
           // console.log('search');
            var keyword = this.$('#product-search').val();
           // console.log(keyword);

            if (keyword.length === 0){
               this.collection.each(function(model){
                 model.set('hidden', false);
               });
               this.render();

            }else{
                this.collection.each(function(model){
                    var source = _.pick(model.attributes,'productName','barcode','productType','desc');
                        source = _.values(source).join('-');
                    if (source.indexOf(keyword) < 0){
                       model.set('hidden', true);
                    }else{
                        model.set('hidden', false);
                    }
                });
                this.render();
            }
        },

        collectionAdd: function(){
            this.render();
           // console.log('collection add');
        },



        new : function(event){
            //console.log('new product');
            var newModel =  this.collection.create({
                // a quick fix for Bacbone.relational 's bug ,
                // if you creat model with  empty attributes , it will return false instead of a Model !!!!!
                // see backbone.relational.js line 1812 to line 1825 !!

                productName:"请输入新产品名称"
            });
            //console.log(newModel);
            var that = this;
            var detailView = this.getDetailView();
            detailView.model = newModel;
            detailView.render();
            detailView.viewWillAppear();
            var fn = function(){
                detailView.viewDidAppear();
            };
            APP.slide(detailView.el, APP.views['view-product'].el,"popin",fn);


        },

        getDetailView: function(){

            APP.productDetailView = APP.productDetailView || this.createDetailView();
            return APP.productDetailView;
        },

        createDetailView : function(){
            var view  = new productDetailView();
            view.$el.appendTo(document.body);
            return view;
        },


        render : function(){

                this.clearEle(this.listContainer.get());
            var container = this.listContainer;
            this.collection.each(function(productModel){
                  if (productModel.get('hidden') === true){
                      return ;
                  }
                  var item = new productItemView({
                      model : productModel
                  });

                  container.append(item.render().el);
            });



            return this;
        }





    });
    return productView;
});
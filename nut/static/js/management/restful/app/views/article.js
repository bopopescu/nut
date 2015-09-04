define(function(require){
    "use strict";

    var ArticleListItemView = Backbone.View.extend({
        initialize: function(){
            Backbone.View.prototype.initialize.apply(this,[].slice.call(arguments));
        },
        tagName: 'tr',
        template : _.template($('#id_article_list_item_template').html()),
        events : {},
        render: function(){
            this.$el.html(this.template(this.model.toJSON()))
            return this ;
        }

    });

    var ArticleListView = Backbone.View.extend({
        initialize: function(){
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'sync', this.sync);
            this.listContainer = this.$('.list-container');
            this.clearEle(this.listContainer.get());

            this.$page_info = this.$('.page-info');
            this.$total_page = this.$('.total-page-info');
            this.$input_pagenum = this.$('#to_page_num');

            this.collection.fetch({reset:true});
        },
        events:{
            'click .page-action.first': 'goFirstPage',
            'click .page-action.prev':'goPrevPage',
            'click .page-action.next':'goNextPage',
            'change .to_page_num': 'pageNumberChanged'
        },
        pageNumberChanged: function(event){
           var pageNum =  parseInt($(event.target).val());
               if (_.isNumber(pageNum)){
                   this.collection.getPage(pageNum, {reset:true});
               }
        },

        goFirstPage: function(){
            this.collection.getFirstPage({reset: true});
        },

        goPrevPage: function(){
            this.collection.getPreviousPage({reset:true});
        },
        goNextPage:function(){
            this.collection.getNextPage({reset:true});
        },

        render: function(){
            this.clearEle(this.listContainer.get());
            var container = this.listContainer;
            var totalPageNumber = this.collection.state.totalPages;
            this.$page_info.html("第"+this.collection.state.currentPage + "页");
            this.$total_page.html("/共"+(totalPageNumber)+ "页");

            this.collection.each(function(model){
                var item = new ArticleListItemView({
                    model: model,
                });
                container.append(item.render().el);
            });
            return this;
        }

    });

    return ArticleListView ;



});
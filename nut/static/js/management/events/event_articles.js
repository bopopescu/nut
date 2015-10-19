console.log('events articles');
//==================== model part ==================
ArticleModel = Backbone.Model.extend({
    urlRoot : '/api/articles/'
});

ArticleCollection = Backbone.Collection.extend({
    model:ArticleModel,
    url: '/api/articles/'
});


EventModel = Backbone.Model.extend({
    urlRoot : '/api/event/',
    parse: function(data){
         console.log('parsing');
         console.log(data);
         return data;
     },
     add_article_id : function(id){
         id = parseInt(id);
         var current_article_list = this.get('related_articles');
         this.set('related_articles', _.union(current_article_list, [id]));
         return this.get('related_articles');
     },
     remove_article_id: function(id){
         id = parseInt(id);
         var current_article_list = this.get('related_articles');
         this.set('related_articles', _.without(current_article_list, id));
         return this.get('related_articles');
     }
});

//=============== model part end =====================
//==============  view part      ===================

EventArticleListItemView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#id-event-article-item-template').html()),
    initialize: function(){
        this.listenTo(this.model, 'sync', this.render.bind(this));
    },
    render:function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

EventArticleListView = Backbone.View.extend({
     tagName : 'div',
     template: _.template($('#id-event-article-list-template').html()),
     initialize: function(){
         this.listenTo(this.model, 'sync',this.render.bind(this));
         this.listenTo(this.model, 'change', this.render.bind(this));
         this.listenTo(this.model, 'change', function(e){
             console.log('model changed');
             console.log(e);
         });
     },

     events:{
       'click .article-remove-button' : 'remove_article_clicked',
       'click .add-article':'add_article_clicked'
     },

     add_article_clicked: function(){
         var input_value = this.$('#article_url').val();
         if (!input_value){
             window.alert('you must input a article url first');
         }
         var url_reg = /articles\/(\d+)\//i;
         result =  input_value.match(url_reg);
         if (result && result.length && result[1] ){
             this.model.add_article_id(result[1]);
         }else{
             window.alert('url format not match');
         }
     },

     remove_article_clicked: function(e){
         console.log(e);
         var article_id= $(e.currentTarget).attr('data-article-id');
         this.model.remove_article_id(parseInt(article_id))
     },
     render : function(){
         var that = this;
         var html = this.template(this.model.toJSON());
         this.$el.html(html);
         this.listContainer = this.$('.list-container')
         console.log(this.model);

         article_id_list = this.model.get('related_articles');
         _.each(article_id_list, function(id){
             var article_model = new ArticleModel();
                 article_model.set('id',id);
             var article_item_view = new EventArticleListItemView({
                 model : article_model
             });
                 that.listContainer.append(article_item_view.$el);
                 article_model.fetch({
                     error:function(){
                         window.alert('article with id' + id + 'load failed, removing!');
                         that.model.remove_article_id(id);
                     }
                 });

         });
         return this;
     },
});




// ============= view part end =======================


// ============ manager/controller part ==============
Event_Article_Manager = function(){

}
Event_Article_Manager.prototype = {
    start_manage: function(event_id){

        var viewEl  =  this.getClearedModal();

        var event_model = new  EventModel();
            event_model.set('id', event_id);
            self.event_model = event_model;

        var event_article_list_view = new EventArticleListView({
            model : event_model,
            el: viewEl,
        });

        event_model.fetch();
    },

    save_event_articles:function(){
        self.event_model.save({success:function(){
            console.log('event model saved');
        }});
        window.setTimeout(function(){
            location.reload();
        }, 300);
    },

    getClearedModal:function(){
        var that = this;
        bootbox.hideAll();
        bootbox.dialog({
            className:'event-article-modal',
            title: '专题::关联文章::列表',
            message: '<div class="" id="event_article_list"></div>',
            buttons: {
                success: {
                    label: "Save",
                    className: "btn-success",
                    callback: function () {
                        console.log('save');
                        that.save_event_articles();
                    }
                },
                quit:{
                    label:"Quit Without Save",
                    className: 'btn-danger',
                    callback:function(){
                        console.log('quit without saving')
                    }
                }

            }
        });
        return $('#event_article_list')[0];
    }
}

//============ manager/controller part end ===========

//============ main() part ===================

eam = new Event_Article_Manager();

$(document.body).delegate('.event-article-management', 'click' , function(){
    console.log($(this).attr('data-event-id'));
    var event_id = $(this).attr('data-event-id');
    eam.start_manage(event_id);
});
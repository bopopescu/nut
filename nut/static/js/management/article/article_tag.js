function  Tag_App(){
    this.init();
}

_.extend(Tag_App.prototype, {
    init: function(){
      console.log('in tag appp');
      this.tag_rec = this.get_tag_rec_list();
      this.setup_tag_click_event();

    },
    get_current_tag_list: function(){
       var tag_str =  $('#id_tags').val();
        console.log('current tags : ');
        console.log(tag_str)
        return tag_str.split(',') || [];
    },
    get_tag_rec_list: function(){
       var url = this.get_tag_request_url();
        $.when($.ajax(url)).then(
            this.tag_request_success.bind(this),
            this.tag_request_fail.bind(this)
        );
    },
    tag_request_success:function(data){
        //console.log('tag get success!')
        //console.log(data);
        var tag_list = data.content.map(function(ele,index){
           return ele[0];
        });
        console.log('tag_list : ');
        console.log(tag_list);
        this.render_rec_tag_list(tag_list);
    },

    render_rec_tag_list:function(tag_list){
       var that = this;
       var tag_wrapper =  $('#tag_btn_list').html('');
        _.map(tag_list,function(tag, index){
            tag_wrapper.append(that.create_tag_button(tag));
        });
    },

    create_tag_button:function(tag){
        return $('<span class="btn btn-info article-tag-btn">'+ tag +'</span>&nbsp;');
    },

    add_article_tag: function(tag){
        var current_tags = this.get_current_tag_list();
            current_tags.push(tag);
        var tags = _.uniq(current_tags)
        this.render_tag_list(tags);
    },

    render_tag_list:function(tags){
        $('#id_tags').val(tags.join(','));
    },
    tag_request_fail:function(data){
        console.log('tag get fail');
        console.log(data);

    },


    get_tag_request_url:function(){
        console.log('request url is : ' + tag_url);
        return tag_url;
    },
    handle_tag_button_click:function(e){
        var btn = e.currentTarget;
        var tag = $(btn).html();
        console.log(tag);
        this.add_article_tag(tag);
    },
    setup_tag_click_event:function(){
        $('#tag_btn_list').on('click','.article-tag-btn', this.handle_tag_button_click.bind(this));
    },

    }
);


var tag_app = new Tag_App();
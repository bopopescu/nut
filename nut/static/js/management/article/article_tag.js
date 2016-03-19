function  Tag_App(){
    this.init();
}

_.extend(Tag_App.prototype, {
    init: function(){
      console.log('in tag appp');
      this._tags =  this.get_tag_list();
      this.tag_rec = this.get_tag_rec_list();
      this.setup_tag_click_event()

    },
    get_tag_list: function(){

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
        this.add_select_tag(data.content);
    },

    add_select_tag: function(tags_list){
        self.tags =
    },
    tag_request_fail:function(data){
        console.log('tag get fail');
        console.log(data);

    },
    get_tag_request_url:function(){
        console.log('request url is : ' + tag_url);
        return tag_url;
    },
    setup_tag_click_event:function(){

    },

    }
);


var tag_app = new Tag_App();
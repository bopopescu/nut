function  Tag_App(){
    this.init();
}

_.extend(Tag_App.prototype, {
    init: function(){
      console.log('in tag appp');
      this.tag_rec = this.get_tag_rec_list();
      this.setup_tag_click_event()

    },
    get_tag_rec_list: function(){
       var url = this.get_tag_request_url();
        $.when($.ajax(url)).then(
            this.tag_request_success.bind(this),
            this.tag_request_fail.bind(this)
        );
    },
    tag_request_success:function(data){
        console.log('tag get success!')
        console.log(data);
    },
    tag_request_fail:function(data){
        console.log('tag get fail');
        console.log(data);

    },
    get_tag_request_url:function(){
        return tag_url;
    },
    setup_tag_click_event:function(){

    },

    }
);


var tag_app = new Tag_App();
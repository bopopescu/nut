function AuthorManager(){
    this.init();
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
;
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


AuthorManager.prototype={
    init: function(){
        this.drawSwitchery();
    },
    drawSwitchery: function(){
        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
            elems.forEach(this.initSingleSwitchery.bind(this));
    },

    initSingleSwitchery: function(ele){
        var switchery = new Switchery(ele);
            $(ele).change(this.switcheryChange.bind(this));
    },
    switcheryChange: function(e){
        ele = e.target;
        console.log(ele);
        //console.log(this['data-id']); this will return undefined
        console.log($(ele).prop('checked'));
        console.log($(ele).attr('data-id'));
        this.setAuthorState(userid=$(ele).attr('data-id'), authorState=$(ele).prop('checked'));

    },
    setAuthorState: function(userid, authorState){
        var url = this.getRequestUrl(userid, authorState);
        var data ={
            isAuthor: authorState
        };
        $.when($.ajax({
            url:'/management/user/'+ userid+'/setAuthor/',
            data: data
        })).then(
            this.postSuccess.bind(this),
            this.postFail.bind(this));
    },
    postSuccess: function(data){
        console.log('set author success');
        console.log(data);

    },
    postFail: function(data){
        console.log('set author fail! ');
        console.log(data);
    }


}


var anthorManager = new AuthorManager();
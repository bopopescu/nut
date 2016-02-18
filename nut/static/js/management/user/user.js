


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

function AuthorizeManager(){
    this.init();
}

AuthorizeManager.prototype={
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
        var group = $(ele).attr('data-group');
        var userid= $(ele).attr('data-id');
        var state = $(ele).prop('checked');
        this.setUserGroup(userid=userid, state=state, group=group);

    },

    setUserGroup: function(userid, state, group) {
        var url = this.getRequestUrl(userid, group);
        var data = this.getRequestData(group, state);

        $.when($.ajax({
            method: 'POST',
            url: url,
            data: data
        })).then(
            this.postSuccess.bind(this),
            this.postFail.bind(this));
    },

    getRequestData: function(group, state){
        var data = {};
        if (group === 'author'){
            data = {
                isAuthor: state,
            }
        }else if(group === 'seller'){
             data = {
                 isSeller : state,
             }
        }else{
            throw new Error('can not determine request data');
        }
        return data;
    },

    getRequestUrl: function(userid, group){
        var ending = '';
        if(group==='author'){
            ending = '/setAuthor/';
        }else if(group ==='seller' ){
            ending = '/setSeller/';
        }else{
            throw new Error('can not determin request url');
        }

        return '/management/user/'+ userid + ending;
    },



    postSuccess: function(data){
        console.log('set group success');
        console.log(data);
        location.reload();

    },
    postFail: function(data){
        console.log('set group fail! ');
        console.log(data);
    }


}


var anthorizeManager = new AuthorizeManager();
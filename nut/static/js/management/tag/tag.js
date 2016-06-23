var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
var targets = Array.prototype.slice.call(document.querySelectorAll('.js-switch-entity'));


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



function postSuccess(data){
    console.log(data);
}
function postFail(data){
    console.log(data);
}

function switchChange(){
    console.log(this);
    console.log(this['data-id']);
    console.log($(this).prop('checked'));
    console.log($(this).attr('data-id'));
    console.log($(this).attr('class'));
    var tag_id = $(this).attr('data-id');
    var tag_class = $(this).attr('class');
    if(tag_class === 'js-switch-entity') {
        var url = '/management/t/' + tag_id + '/publishedEntityTag/';
        var data =  {id:tag_id ,isPubishedEntityTag: $(this).prop('checked')};
    }
    else {
        url = '/management/t/' + tag_id + '/topArticleTag/';
        data =  {id:tag_id ,isTopArticleTag: $(this).prop('checked')};
    }


    $.when($.ajax({
        type:'POST',
        url: url,
        data: data,
    })).then(
        postSuccess,
        postFail
    );
}

elems.forEach(function(ele) {
  var switchery = new Switchery(ele);
      ele.onchange = switchChange;
});

targets.forEach(function(target) {
  var switchery = new Switchery(target);
      target.onchange = switchChange;
});
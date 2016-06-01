console.log('in push management!!');


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


function Test_Send(){
    this.init_test_send_button();
    this.init_boot_box();
    this.request_url = $()

}

Test_Send.prototype = {
    init_boot_box: function(){
        bootbox.setDefaults({
                className: 'no-class',
                closeButton: false,
                locale:'zh_CN'
            });
    },
    init_test_send_button: function(){
        console.log('init button ');
        $('.test_send_button').click(this.handleClick.bind(this));

    },

    get_request_url: function(event){
        var target = event.currentTarget;
        return $(target).attr('data-request-url');

    },
    handleClick:function(event){
        this.request_url = this.get_request_url(event);
        this.show_custom_dialog()
    },

    show_custom_dialog:function(){
        var that = this;
        bootbox.dialog({
            size:'small',
            message: '<p>请输入收件人的 果库 ID</p><input type="text" id="recipient_id_list"> ',
            title: '发送测试推送',
            buttons:{
                success: {
                    label: '发送' ,
                    callback: that.dialog_send.bind(that),
                },
                danger:{
                    label: '放弃',
                    callback: that.dialog_quit.bind(that),
                }
            }
        });
    },
    collect_user_id_list: function(){
        var id_list_str = $('#recipient_id_list').val()
        if (!!!id_list_str){
            alert('请输入测试用户 id');
            return null;
        }else{
            var id_list = id_list_str.split(',');
            return {recipients: id_list}
        }
    }
    ,
    dialog_send: function(){
        console.log('dialog send message!');
        var data = this.collect_user_id_list();
        if (data === null){
            return ;
        }
        $.when($.ajax({
            url: this.request_url,
            method: 'POST',
            dataType: 'json',
            data: JSON.stringify(data),
        })).then(this.postSuccess.bind(this), this.postFail.bind(this));

    },

    postSuccess: function(data){
        console.log(data);
        console.log('test send push success!');

    },
    postFail:function(data){
        console.log(data);
        console.log('test send push fail');
    },
    dialog_quit: function(){
        console.log('dialog quit sending ')
    }

}

var tsend = new Test_Send();
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


function Message_Sender(){
    this.init_test_send_button();
    this.init_real_send_button();
    this.init_boot_box();
    this.request_url = $()

}

Message_Sender.prototype = {
    init_boot_box: function(){
        bootbox.setDefaults({
                className: 'no-class',
                closeButton: false,
                locale:'zh_CN'
            });
    },

    init_real_send_button: function(){
        $('.production_send_button').click(this.handleRealClick.bind(this));
    },
    init_test_send_button: function(){
        console.log('init button ');
        $('.test_send_button').click(this.handleTestClick.bind(this));

    },

    get_request_url: function(event){
        var target = event.currentTarget;
        return $(target).attr('data-request-url');

    },
    get_formal_send_url:function(event){
        return $(event.currentTarget).attr('data-request-url');
    },


    formal_send:function(){
        $.when($.ajax(this.formal_send_url,{
            method: 'POST'
        })).then(
            this.formal_send_success.bind(this),
            this.formal_send_fail.bind(this)
        )
    },

    formal_send_success:function(){
        bootbox.hideAll();
        bootbox.alert('推送消息成功', function(){
            window.location.reload();
        });



    },
    formal_send_fail:function(){
        bootbox.hideAll();
        bootbox.alert('推送消息失败')

    },

    handleRealClick: function(event){
        this.formal_send_url = this.get_formal_send_url(event)
        var that = this;
        bootbox.hideAll();
        bootbox.prompt('输入 "确认发送" ', function(result){
            if(result == "确认发送"){
                that.formal_send();
            }else{
                bootbox.hideAll();
                bootbox.alert('输入错误, 放弃发送!');
            }
        });
    },
    handleTestClick:function(event){
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
        })).then(this.testPostSuccess.bind(this), this.testPostFail.bind(this));

    },

    testPostSuccess: function(data){
        console.log(data);
        bootbox.alert('测试推送信息发送 成功 .');


    },
    testPostFail:function(data){
        console.log(data);
        bootbox.alert('测试推送信息发送  失败    !');
    },
    dialog_quit: function(){
        console.log('dialog quit sending ')
    }

}

var tsend = new Message_Sender();
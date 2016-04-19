var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));


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

function get_request_url(entity_id){

    return '/management/brand/add/entity/'
}
function switchChange(){
    console.log(this);
    console.log(this['data-id']);
    console.log($(this).prop('checked'));
    console.log($(this).attr('data-id'));
    var entity_id = $(this).attr('data-id');
    var url =  get_request_url(entity_id)
    var data =  {
        entity_id:entity_id ,
        isBrandEntity: $(this).prop('checked'),
        brand_id : brand_id
    };

    $.when($.ajax({
        type:'POST',
        url: url,
        dataType:'json',
        data: JSON.stringify(data),
    })).then(
        postSuccess,
        postFail
    );
}

elems.forEach(function(ele) {
  var switchery = new Switchery(ele);
      ele.onchange = switchChange;
});


var BrandEntitySortApp = Class.extend({
    init: function(){
        $('#mng_brand_entity_btn').click(this.beginSort.bind(this));

    },
    beginSort: function(){
        this.getBrandEntityData().then(
            this.showDialog.bind(this),
            this.getBrandEntityDataFail.bind(this)
        );

    },

    getBrandEntityData:function(){
        var request_url = this.get_entity_data_request_url();
        return $.when($.ajax({
            url: request_url,
            method:'GET',
        }));
    },

    get_entity_data_request_url:function(){
        return  '/manage/brand/'+brand_id+'/selected_entities/'
    },

    getBrandEntityDataFail: function(data){
        console.log('get brand entity data failed');
        console.log(data)
    },

    showDialog: function(data){
        bootbox.dialog({
            title: '管理品牌商品排序',
            message: this.render_content(data),
            buttons:{
                success: {
                    label: '更新排序',
                    className: 'btn-success',
                    callback: this.updateEntityOrder.bind(this)
                },
                fail: {
                    label: '放弃操作',
                    className: 'btn-danger',
                    callback: this.quitOrder.bind(this)
                }

            }
        });

    },
    updateEntityOrder: function(){

    },
    quitOrder:function(){

    }
});


var brandEntitySortapp = new BrandEntitySortApp();
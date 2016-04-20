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
        this.template = tmpl($('#mng_brand_entity_sort_item').html());
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
        return  '/management/brand/'+brand_id+'/selected_entity/'
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
        window.setTimeout(this.enableSort.bind(this),500);
    },
    enableSort: function(){
        $('#entity_sort').sortable();
    },

    render_content: function(data){
        var entities = data['entities'];
            entities.forEach(this.handleImageSize.bind(this));
            content = this.template(data);
            return content ;
    },
    handleImageSize:function(entity){
       var origin_cover =  entity['cover'];
           entity['cover'] = origin_cover.replace('images/','images/100/');
    },
    updateEntityOrder: function(){

        var ids = this.collectSortedIds();
        var save_sort_url = 'management/brand/entities/sort/save/';
        $.when($.ajax(
            {
                url : save_sort_url,
                method: 'POST',
                dataType: 'json',
                data: JSON.stringify(
                    {
                        entity_ids:ids,
                        brand_id: brand_id,
                    }
                ),
            }
        )).then(
            this.entityOrderSavedSuccess.bind(this),
            this.entityOrderSaveFail.bind(this)
        );


    },

    collectSortedIds: function(){
        var ids = [];
          $('#entity_sort li').map(function(ele){
              ids.push($(ele).attr('data-id'));
          });
        return ids;
    },
    quitOrder:function(){
        console.log('give up sort saving');
    },

    entityOrderSavedSuccess: function(){
        bootbox.hideAll();
        bootbox.alert('排序成功保存');
    },
    entityOrderSaveFail: function(){
        bootbox.hideAll();
        bootbox.alert('保存失败,稍后再试,还不行找安晨');
    },


});


var brandEntitySortapp = new BrandEntitySortApp();
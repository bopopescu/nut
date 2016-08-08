var SkuSwitch = Class.extend({
    init: function(){
       console.log('sku switch begin');
        this.initSkuSwitch();
    },
    initSkuSwitch:function(){
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
            var sku_id = $(this).attr('data-id');
            var sku_class = $(this).attr('class');
            if(sku_class === 'js-switch') {
                var url = sku_id + '/sku_status/';
                var status_val = 0;
                if($(this).prop('checked')){
                    status_val = 1
                }
                var data =  {id:sku_id ,status: status_val};
            }

            $.when($.ajax({
                type:'POST',
                url: url,
                data: data
            })).then(
                    postSuccess,
                    postFail
            );
        }

        elems.forEach(function(ele) {
            var switchery = new Switchery(ele);
            ele.onchange = switchChange;
        });
    }

});



(function($, window, document){
    $(function(){
         var SiteBanners = new SkuSwitch();
    });
})(jQuery, window, document);


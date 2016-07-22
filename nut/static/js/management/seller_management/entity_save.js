var BatchSiteBanners = Class.extend({
    init: function(){
        var that = this;
        $('.btn.btn-success').click(function(){
                var url = $(this).attr("batch_url");
                var id = $(this).attr("id");
                var price = $("input#" +id).val();
                // alert(price);
                // alert(id);
                that.sendSaveMission(url, price);
        });
    },


    selectBannerSuccess:function(data){
        console.log('success saved ');
    },


    sendSaveMission:function(url, price){
        $.when($.ajax({
            url: url,
            method: 'POST',
            data:{
                'price':JSON.stringify(price)
            }
        })).then(
            this.saveUpdateBatchSuccess.bind(this),
            this.saveUpdateBatchFail.bind(this)
        );
    },
    saveUpdateBatchSuccess:function(data){
        console.log('success saved ');
        window.location.reload();
    },
    saveUpdateBatchFail:function(data){
        console.log('saved failed');
    }
});



(function($, window, document){
    $(function(){
         var SiteBanners = new BatchSiteBanners();
    });
})(jQuery, window, document);


var BatchSiteBanners = Class.extend({
    init: function(){
        var that = this ;

        $('#btn_batch_sitebanner_save').click(function(){
                // console.log('save sitebanner');
                var id_list = that.collectBannerId();
                that.saveUpdateBatch(id_list);
                // if(id_list[0].length || id_list[1].length || id_list[2].length){
                //     that.removeSelectionBatch(id_list);
                // }
        });

        $('#banner-select').click(function(){
                // alert('remove selection in batch');
                var checked = that.collectSelect();
                alert(checked);
                that.selectBanner(checked);
                // if(eids.length){
                //     that.removeSelectionBatch(eids);
                // }
        });
    },

    collectSelect: function(){
        
        var checked = $("#select-banner:checked").map(function(idx, item){
            return $(item).attr('value');
        });
        return [].slice.call(checked);
    },

    selectBanner:function(checked){
        $.when($.ajax({
            url: '/management/sitebanner/banners/',
            method: 'POST',
            data:{
                'checked':JSON.stringify(checked)

            }
        })).then(
            this.selectBannerSuccess.bind(this)
        );
    },

    selectBannerSuccess:function(data){
        console.log('success saved ');
        // window.location.reload();
    },

    saveUpdateBatch: function(id_list){
            var that = this ;
            bootbox.confirm('确定要保存修改吗？', function(result){
                if(result){
                    that.sendSaveMission(id_list);
                }else{
                    return ;
                }
            });
    },


    sendSaveMission:function(id_list){
        $.when($.ajax({
            url: '/management/sitebanner/banners/save/',
            method: 'POST',
            data:{
                'id_list':JSON.stringify(id_list)

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
    },
    collectBannerId: function(){
        console.log('begin collect pending selection entity id');
        var app_ids = $('#chk-app:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        var mainpage_ids = $('#chk-mainpage:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        var sidebar_ids = $('#chk-sidebar:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        var all_ids = $($("input#chk-app")).map(function(idx, item){
            return $(item).attr('value');
        });
        var positions = $($("input#position")).map(function(idx, item){
            return $(item).val();
        });
        // make sure return a array
        return [[].slice.call(app_ids), [].slice.call(mainpage_ids), [].slice.call(sidebar_ids),
            [].slice.call(all_ids), [].slice.call(positions)];
    }

});



(function($, window, document){
    $(function(){
         var SiteBanners = new BatchSiteBanners();
    });
})(jQuery, window, document);


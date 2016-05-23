var BatchSelectionApp = Class.extend({
    init: function(){
        var that = this ;
        $('#btn_batch_selection_prepare').click(function(){
                 console.log('begin batch selection');
                 var eids = that.collectEntityId();
                 if (eids.length){
                     that.showDetailBatchListModal(eids);
                 }
        });

        $('#btn_batch_selection_remove').click(function(){
                console.log('remove selection in batch');
                var eids = that.collectEntityId();
                if(eids.length){
                    that.removeSelectionBatch(eids);
                }
        });

        $('#btn_batch_selection_freeze').click(function(){
                console.log('freeze selection in batch');
                var eids = that.collectEntityId();
                if(eids.length){
                    that.freezeSelectionBatch(eids);
                }
        });
    },

    removeSelectionBatch: function(eids){
            var that = this ;
            bootbox.confirm('共 '+ eids.length +' 件商品，确定要移除精选吗？', function(result){
                if(result){
                    that.sendRemoveMission(eids);
                }else{
                    return ;
                }
            });
    },

    freezeSelectionBatch: function(eids){
            var that = this ;
            bootbox.confirm('共 '+ eids.length +' 件商品，确定要freeze精选吗？', function(result){
                if(result){
                    that.sendFreezeMission(eids);
                }else{
                    return ;
                }
            });
    },

    sendRemoveMission:function(eids){
        $.when($.ajax({
            url: '/management/selection/set/remove/batch/do/',
            method: 'POST',
            data:{'entity_id_list':JSON.stringify(eids)}
        })).then(
            this.removeSelectionBatchSuccess.bind(this),
            this.removeSelectionBatchFail.bind(this)
        );
    },

    sendFreezeMission:function(eids){
        $.when($.ajax({
            url: '/management/selection/set/freeze/batch/do/',
            method: 'POST',
            data:{'entity_id_list':JSON.stringify(eids)}
        })).then(
            this.freezeSelectionBatchSuccess.bind(this),
            this.freezeSelectionBatchFail.bind(this)
        );
    },
    removeSelectionBatchSuccess:function(data){
        console.log('success removed ');
        window.location.reload();
    },
    removeSelectionBatchFail:function(data){
        console.log('remove failed');
    },

    freezeSelectionBatchSuccess:function(data){
        console.log('success frozen ');
        window.location.reload();
    },
    freezeSelectionBatchFail:function(data){
        console.log('freeze failed');
    },
    collectEntityId: function(){
        console.log('begin collect pending selection entity id');
         var eids = $('.usite-chk:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        // make sure return a array
        return [].slice.call(eids);
    },
    showDetailBatchListModal: function(eids){
        console.log('show DetailBatchListModal');
        $.when($.ajax({
            url: '/management/selection/set/publish/batch/prepare/',
            method: 'POST',
            data : {'entity_id_list':JSON.stringify(eids)}
        })).then(
            this.getBatchDataSuccess.bind(this),
            this.getBatchDataFail.bind(this)
        );
    },
    getBatchDataSuccess: function(data){
        console.log(data);
        if (data.error){
            bootbox.alert(data.msg);
            return ;
        }
        bootbox.dialog({
            title: '批量加精选商品',
            message:this.render_list(data),
            buttons:{
                success:{
                    label:"设为精选商品",
                    className: 'btn-success',
                    callback: this.doBatchSelection.bind(this),
                },
                fail:{
                    label:"放弃操作",
                    className:'btn-danger',
                    callback:this.quitBatchSelection.bind(this),
                }
            }

        });
        window.setTimeout(this.handleBatchModalShowed.bind(this), 16);
    },
    getBatchDataFail: function(data){
         bootbox.alert('Can not load pending entities , please contact Admin.', function(result){
           //do nothing ;
         });;
    },
    render_list:function(data){
        var tmpl_str = $('#template_batch_selection_item').html();
        var list_template = tmpl(tmpl_str)
        var html =list_template(data)
        return html
    },
    handleBatchModalShowed: function(){
        var that=this;
        // bind gap change event to update_batch_selection_pub_time
        $('#publish_gap').change(this.update_batch_selection_pub_time.bind(this));
        //    make entity list sortable
        $('.batch-selection-list').sortable({
            update:function(event,ui){
                console.log('list is sorted !!');
                that.update_batch_selection_pub_time();
            }
        });
        //    update pub time base on last pub time and gap value
        this.update_batch_selection_pub_time(
        );
    },
    update_batch_selection_pub_time: function(){
        console.log('update batch selection pub time here ');
        var gap = $('.gap-wrapper input').val()
            gap = parseInt(gap);
            if(!gap){
                bootbox.alert('you must fill a number for publishing gap , in secconds');
                return ;
            }

        var last_pub_time = $('#last_publish_time').val();
        var entity_pubtime_inputs = $('.batch-selection-list .entity-pub-time input').get();
        this.fill_pub_time(entity_pubtime_inputs, last_pub_time, gap);
        return ;
    },

    fill_pub_time: function(input_list, last_pub_time_str, gap_in_seconds){
        var fmt_string = "YYYY-MM-DD HH:mm";
        var next_time_str = moment(last_pub_time_str)
        while(input_list.length){
            next_time_str = moment(next_time_str,fmt_string)
                              .add(gap_in_seconds, 'seconds')
                              .format(fmt_string);
            $(input_list.pop()).val(next_time_str);
        }
    },
    collectBatch:function(){
        var missions = $('.batch-selection-list .entity-pub-time input').map(function(idx, item){
            return {
                'id' : $(item).attr('entity_id'),
                'pub_time': $(item).val()
            }
        });
        return [].slice.call(missions);
    },
    sendPublishMission: function(missionData){
        $.when($.ajax({
            url: '/management/selection/set/publish/batch/do/',
            method: 'POST',
            data:{'batch_list':JSON.stringify(missionData)}
        })).then(
            this.batchMissionSuccess.bind(this),
            this.batchMissionFail.bind(this)
        )
    },
    doBatchSelection: function(){
         console.log('Bach selection real call from here');
         var missionData = this.collectBatch();
         if(missionData.length){
             this.sendPublishMission(missionData);
         }else{
             bootbox.alert('can not find any mission Data, pls contact admin');
         }
         return ;
    },
    quitBatchSelection: function(){
        console.log('user give up batch Selection');
    },

    batchMissionSuccess:function(data){
        if (data.error == 0){
            bootbox.alert(data.msg, function(){
                window.location.reload();
            });
        }else{
            bootbox.alert(data.msg);
        }
    },
    batchMissionFail:function(data){
        console.log('batch mission fail');
    }

});



(function($, window, document){
    $(function(){
         var batch_selection_app = new BatchSelectionApp();
    });
})(jQuery, window, document);


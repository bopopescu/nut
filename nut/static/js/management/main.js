/**
 * Created by edison on 14-9-12.
 */
;
(function ($, document, window) {

    var editor ={

    };
    var entity = {
        removeImage: function() {
//            console.log("OKOKO");
            $('#images').find('.btn').on('click', function(){
//                console.log(this);
                var image = $(this);
//                console.log(image.parent().parent());
                var index = image.attr('data-image');
                $.ajax({
                    url: this.href,
                    type: "POST",
                    dataType:'json',
                    data: {"index": index},
                    success: function(data) {
                        image.parent().parent().remove();
                    }
                });
                return false;
            });
        },

        removeBuyLink: function() {
            $('#buylinks').find('.buy-link').on('click', function(){
                var buy_link = $(this);
                //console.log(buy_link);

                var index = buy_link.attr('data-index');
                //console.log(index)
                var url = "/management/entity/" + index + "/buy/link/remove/";
                $.ajax({
                    url:url,
                    type: "POST",
                    dataType: "json",
                    success: function(data) {
                        buy_link.parent().parent().parent().remove();
                    }
                });
            });
            return false;
        }

    };

    var dashboard = {
        selectedChar: function() {
            var selection_chart = $('#selectionChart');
            var like_chart = $('#likeChart');
            var category_chart = $('#categoryChart');

            if (selection_chart[0]){
                var selection_ctx = selection_chart.get(0).getContext("2d");
                var like_ctx = like_chart.get(0).getContext("2d");
                var category_ctx = category_chart.get(0).getContext("2d");
                $.ajax({
                    url:"/management/dashboard/",
                    type: "get",
                    dataType: "json",
                    success : function(res) {
                        //console.log(res);
                        var labels = new Array();
                        var d = new Array();
                        var like_total = new Array();
                        $(res.selection).each(function(index){
                            //console.log(row.id)
                            var val = res.selection[index];
                            //console.log(val.selected_total);
                            labels.push(val.pub_date);
                            d.push(parseInt(val.selected_total));
                            like_total.push(parseInt(val.like_total));
                        });
                        var data = {
                            labels: labels,
                            datasets: [
                                {
                                    label: "publish selection ",
                                    fillColor: "rgba(151,187,205,0.2)",
                                    strokeColor: "rgba(151,187,205,1)",
                                    pointColor: "rgba(151,187,205,1)",
                                    pointStrokeColor: "#fff",
                                    pointHighlightFill: "#fff",
                                    pointHighlightStroke: "rgba(220,220,220,1)",
                                    data: d
                                }
                            ]
                        };
                        var like_data = {
                            labels: labels,
                            datasets: [
                                {
                                    label: "publish selection ",
                                    fillColor: "rgba(151,187,205,0.2)",
                                    strokeColor: "rgba(151,187,205,1)",
                                    pointColor: "rgba(151,187,205,1)",
                                    pointStrokeColor: "#fff",
                                    pointHighlightFill: "#fff",
                                    pointHighlightStroke: "rgba(220,220,220,1)",
                                    data: like_total
                                }
                            ]
                        };
                        var selectionLineChart = new Chart(selection_ctx).Line(data);
                        var likeBarChart = new Chart(like_ctx).Bar(like_data);

                        var category_labels = new Array();
                        var category_data = new Array();
                        $(res.category).each(function(index){
                            //console.log(row.id)
                            var val = res.category[index];
                            //console.log(val.selected_total);
                            category_labels.push(val.label);
                            category_data.push(parseInt(val.value));
                            //like_total.push(parseInt(val.like_total));
                        });

                        var category_data_list = {
                            labels: category_labels,
                            datasets: [
                                {
                                    label: "publish selection ",
                                    fillColor: "rgba(151,187,205,0.2)",
                                    strokeColor: "rgba(151,187,205,1)",
                                    pointColor: "rgba(151,187,205,1)",
                                    pointStrokeColor: "#fff",
                                    pointHighlightFill: "#fff",
                                    pointHighlightStroke: "rgba(220,220,220,1)",
                                    data: category_data
                                }
                            ]
                        };
                        var categoryPolarArea = new Chart(category_ctx).Bar(category_data_list);
                    }
                })
            }
        }
    };

    var comment = {
        remove: function(){
            var comment_list = $("#comment");
            comment_list.find(".btn").on('click', function(){
                //console.log(this);

                var row = $(this).parent().parent();

                var comment_id = $(this).attr('comment-id');
                var link = '/management/comment/' + comment_id + '/del/';

                //console.log(comment_id);
                $.ajax({
                    type:'post',
                    url: link,
                    success: function(res){
                        console.log(res['status']);
                        if (res['status'] === 'success') {
                            //console.log(row);
                            row.remove();

                        }
                    }
                });
            })
        }
    };

    var media= {
        remove: function(){
            var media_list = $("#media");
            //console.log(media_list);
            media_list.find('.btn-delete').on('click', function(){
                var row = $(this).parent().parent().parent();
                //console.log(row);
                var medium_id = $(this).attr('medium-id');
                var link = '/management/media/delete/';
                $.ajax({
                    type:'post',
                    url:link,
                    data: {'mid': medium_id},
                    success: function(res){
                        row.remove();
                    }
                });

                //console.log(medium_id)
            });
        }
    };

    var article={
        initAddSelectionArticle: function(){
            add_btns = jQuery('.add-selection');
            $.each(add_btns, function(idx , btn){
                $(btn).click(function(e){
                    var that = this;
                    var article_id = $(this).attr('article_id');
                    var url = $(this).attr('url');
                    $.when(
                        $.ajax(url)
                    ).then(
                        function success(data){
                            console.log('success');
                            console.log(data);
                            alert('加入精选成功');

                        },
                        function fail(data){
                            console.log('failed');
                            console.log(data);
                        }
                    );
                });
            });
        },
        initRemoveSelectionArticle:function(){
        //    use delegate : )
            jQuery('.action-table')
                .delegate('.remove-selection','click', function(){
                    var url = $(this).attr('url');
                    var selection_article_id = $(this).attr('selection_article_id');
                    $.when(
                        $.ajax(url)
                    ).then(
                        function success(data){
                            console.log('success');
                            console.log(data);
                        },
                        function fail(data){
                            console.log('failed');
                            console.log('data');
                        }
                    );
                });
        }

    };


    var selection = {
        publish2u:function(){
            bootbox.setDefaults({
                className: 'guoku-publish2u batch-selection-modal',
                closeButton: false,
                locale:'zh_CN'
            });

            $('#publish2u').click(function(){
                bootbox.confirm({
                    size: 'small',
                    message: '发布到 U 站 ?',
                    callback: function(result){
                        if (result) {
                            //return;
                            var chklist = $('.usite-chk:checked');
                            if (chklist.length > 0) {
                                //console.log(chklist);
                                var entityIds = new Array(0);
                                chklist.each(function(){
                                    entityIds.push($(this).attr('value'));
                                });
                                $.ajax({
                                    type: 'post',
                                    url: '/management/selection/usite/publish/',
                                    data: {'eids': JSON.stringify(entityIds)},
                                    success: function(res) {
                                        //$(this).prop('checked', false);
                                    }
                                });
                            }
                            //console.log(chklist);
                        }
                    }
                });
            });
        },

        check_all: function(){
            $('#usite-chk-all').click(function(){
                var chklist = $('.usite-chk');
                if ($(this).prop('checked')) {
                    chklist.each(function(){
                        $(this).prop('checked', true);
                    })
                } else {
                    chklist.each(function(){
                        $(this).prop('checked', false);
                    })
                }
            });
        }
    };


    (function init() {
//        console.log($.find());
        entity.removeImage();
        entity.removeBuyLink();
        dashboard.selectedChar();

        comment.remove();

        media.remove();
//        add by An
        article.initAddSelectionArticle();
        article.initRemoveSelectionArticle();


        selection.publish2u();
        selection.check_all();
//        note.post();
    })();

})(jQuery, document, window);
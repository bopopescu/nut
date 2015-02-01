/**
 * Created by edison on 14-9-12.
 */
;(function ($, document, window) {


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
            $('#buylinks').find('.btn-link').on('click', function(){
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
                        buy_link.parent().remove();
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

            if (selection_chart[0]){
                var selection_ctx = selection_chart.get(0).getContext("2d");
                var like_ctx = like_chart.get(0).getContext("2d");
                $.ajax({
                    url:"/management/dashboard/",
                    type: "get",
                    dataType: "json",
                    success : function(res) {
                        var labels = new Array();
                        var d = new Array();
                        var like_total = new Array();
                        $(res).each(function(index){
                            //console.log(row.id)
                            var val = res[index];
                            //console.log(val.selected_total);
                            labels.push(val.pub_date);
                            d.push(parseInt(val.selected_total));
                            like_total.push(parseInt(val.like_total));
                        });
                        //console.log(labels);
                        //console.log(d);
                        //console.log(like_total);
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
                    }
                })
            }
        }
    };

    var comment = {
        remove: function(){
            var comment_list = $("#comment");
            comment_list.find(".btn").on('click', function(){
                console.log("OKOKOKO");
            })
        }
    };

    (function init() {
//        console.log($.find());
        entity.removeImage();
        entity.removeBuyLink();
        dashboard.selectedChar();

        comment.remove();
//        note.post();
    })();
})(jQuery, document, window);
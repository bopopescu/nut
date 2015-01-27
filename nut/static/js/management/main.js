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
            var chart = $('#selectionChart');

            if (chart[0]){
                var ctx = chart.get(0).getContext("2d");
                $.ajax({
                    url:"/management/dashboard/",
                    type: "get",
                    dataType: "json",
                    success : function(res) {
                        var labels = new Array();
                        var d = new Array();
                        $(res).each(function(index){
                            //console.log(row.id)
                            var val = res[index];
                            //console.log(val.selected_total);
                            labels.push(val.pub_date);
                            d.push(parseInt(val.selected_total));
                        });
                        console.log(labels);
                        console.log(d);
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
                        var myLineChart = new Chart(ctx).Line(data);
                    }
                })

            }
        }
    };

    (function init() {
//        console.log($.find());
        entity.removeImage();
        entity.removeBuyLink();
        dashboard.selectedChar();
//        note.post();
    })();
})(jQuery, document, window);
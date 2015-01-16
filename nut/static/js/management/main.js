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

//    var note = {
//        post: function () {
//            var form = $('#EntityNoteModal');
//            console.log(form);
//        }
//    };

    (function init() {
//        console.log($.find());
        entity.removeImage();
        entity.removeBuyLink();
//        note.post();
    })();
})(jQuery, document, window);
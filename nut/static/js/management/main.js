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
        }
    };

    var note = {
        post: function () {
            var form = $('#EntityNoteModal');
            console.log(form);
        }
    };

    (function init() {
//        console.log($.find());
        entity.removeImage();
        note.post();
    })();
})(jQuery, document, window);
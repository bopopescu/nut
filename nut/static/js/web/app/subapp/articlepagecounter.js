define(['jquery', 'libs/Class'], function(jQuery, Class){

    var counterUrl = '/counter/';
    function updateReaderCount(count){
        jQuery('#read_counter').html(count);
    }

    var ArticleCounter = Class.extend({
        init: function(){
            jQuery.when(jQuery.ajax({url:counterUrl}))
                  .then(
                        this.sendSuccess.bind(this),
                        this.sendFail.bind(this)
            );
        },
        sendSuccess: function(data){
            if(data['error'] === 0){
                console.log('success');
                console.log(data['count']);
                updateReaderCount(data['count']);
            }else{
                console.log('error');
                console.log(data['message']);
            }
        },
        sendFail:function(data){
            console.log('fail request');
        }
    });


    return ArticleCounter;

});
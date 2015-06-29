(function(jQuery, window, document){

    var counterUrl = '/counter/';
    function updateReaderCount(count){
        jQuery('#read_counter').html(count);
    }

    jQuery.when(
        jQuery.ajax({
            url:counterUrl
        })
    ).then(
        function success(data){
            //console.log("success");
            if(data['error'] === 0){
                console.log('success');
                console.log(data['count']);
                updateReaderCount(data['count']);
            }else{
                console.log('error');
                console.log(data['message']);
            }

        },
        function fail(data){
        //   handle counter error;
            console.log('fail request');
        }
    );

})(jQuery, window, document);





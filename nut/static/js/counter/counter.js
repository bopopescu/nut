var counterUrl = '/counter/';

jQuery.when(
    jQuery.ajax({
    url:counterUrl
    })
).then(
    function success(data){
        console.log("success");
        console.log(data);
    },
    function fail(data){
        console.log('fail');
        console.log(data);
    }

);


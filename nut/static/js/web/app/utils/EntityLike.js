define(['libs/Class','jquery','fastdom'], function(Class,jQuery,fastdom){

    var AppEntityLike = Class.extend({
        init: function(){
            console.log('app entity like functions');
            console.log(jQuery);
            console.log(fastdom);


        }
    });

    return AppEntityLike;
});
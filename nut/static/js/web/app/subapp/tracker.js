


define(['libs/Class'], function(Class){
    //singleton for tracker
    var instance = null ;
    var Tracker = Class.extend({
        init: function(){
            console.log('tracker init');
            if (!instance){
                instance = this;
            }
        }
    });
    new Tracker();
    return instance;
});
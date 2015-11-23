// singleton instance few.
define(['libs/Class'], function (Class) {
    //singleton for tracker

    var Tracker = Class.extend({
        init: function () {
            console.log('tracker init');
            if (!instance) {
                instance = this;
            }
        }
    });
    var instance =  new Tracker();
    return instance;
});
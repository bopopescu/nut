// singleton instance few.
var instance = null;

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
    instance = instance || new Tracker();
    return instance;
});
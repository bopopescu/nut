// singleton instance few.
define(['libs/Class'], function (Class) {
    //singleton for tracker

    var Tracker = Class.extend({
        init: function (tracker_list) {
            tracker_list.map(function(item){
                  var selector = item.selector;
                   var event = item.event;

                  $(selector).on(event, function(event){
                      var target = event.currentTarget;
                      var lable = $(target).attr(item.label);
                      // 闭包
                     _hmt.push('_trackEvent', '')
                  });
            });
        }
    });
    return Tracker;
});
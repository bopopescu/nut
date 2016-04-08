define(['libs/Class'], function (Class) {
    var Tracker = Class.extend({
        init: function (tracker_list) {
            tracker_list.map(function(ele){
                  var wrapper = ele.wrapper;
                  var selector = ele.selector;
                  var trigger = ele.trigger;
                  $(wrapper).on(trigger, selector, function(event){
                      return (function() {
                              var target = event.currentTarget;
                              console.log(target);
                              var category = ele.category;
                              var action = ele.action;
                              var opt_label = $(target).attr(ele.label) || $(target).parent().attr(ele.label);
                              var opt_value = $(target).attr(ele.value) || $(target).parent().attr(ele.value);
                               //闭包
                             _hmt.push('_trackEvent', category, action, opt_label, opt_value);
                      })();

                  });

            });
        }
    });
    return Tracker;
});
console.log('outside define');

define(['libs/Class'],function(){

    var singletonInstance = (function(){

        var objClass = Class.extend({
            init: function(){
                this.foo = 'far';
                this.bar = 'boo';
            }
        });

    })();

    return singletonInstance;

});
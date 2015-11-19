define(function(){
    var io={
        clearUserInputString: function(str){
            str = str.replace(/(\s+)/mg,' ');
            str = str.replace(/([><:$*&%])/mg, '');
            return str.trim();
        },
    };

    return io;
});
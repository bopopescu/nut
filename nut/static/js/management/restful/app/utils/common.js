define(function(require){
    var commonTools = {
        formatTime : function(timeStr){
             var fmt_string = "YYYY-MM-DD HH:mm";
             return moment(timeStr,fmt_string).format(fmt_string);
        }
    }
    return commonTools;
});
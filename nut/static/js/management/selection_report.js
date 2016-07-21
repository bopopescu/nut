var Selection_Report = Class.extend({
    init: function(){
        var that = this;

        var getUrlParameter = function getUrlParameter(sParam) {
            var sPageURL = decodeURIComponent(window.location.search.substring(1)),
                sURLVariables = sPageURL.split('&'),
                sParameterName,
                i;
        
            for (i = 0; i < sURLVariables.length; i++) {
                sParameterName = sURLVariables[i].split('=');
        
                if (sParameterName[0] === sParam) {
                    return sParameterName[1] === undefined ? true : sParameterName[1];
                }
            }
                };

        $('#submit').click(function(){
                var status = getUrlParameter('status') || 'None';
                var start_date = $('#datetimepicker1').data('date') || $('#start_date').val() || '';
                var end_date = $('#datetimepicker2').data('date') || $('#end_date').val() || '';
                var path = window.location.pathname;

                window.location = path + '?status=' + status + '&start_date=' + start_date +
                    '&end_date=' + end_date;

        });
    }

});



(function($, window, document){
    $(function(){
         var selection_report = new Selection_Report();
    });
})(jQuery, window, document);


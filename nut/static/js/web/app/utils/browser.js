define([], function () {
    //all helper function for browser operation here,
    //
    var browser = {
        getQueryStrings: function () {
            var assoc = {};
            var decode = function (s) {
                return decodeURIComponent(s.replace(/\+/g, " "));
            };
            var queryString = location.search.substring(1);
            var keyValues = queryString.split('&');

            //for(var i in keyValues) {
            for (var i = 0, len = keyValues.length; i < len; i++) {
                var key = keyValues[i].split('=');
                if (key.length > 1) {
                    assoc[decode(key[0])] = decode(key[1]);
                }
            }
            return assoc;
        }
    };

    return browser

});
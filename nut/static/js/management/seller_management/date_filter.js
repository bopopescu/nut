

var DateFilterHandler = Class.extend({

    queryStringToParams : function(qs) {
            if (!qs) return {};
            var kvp, k, v, ls, params = {}, decode = decodeURIComponent;
            var kvps = qs.split('&');
            for (var i = 0, l = kvps.length; i < l; i++) {
                var param = kvps[i];
                kvp = param.split('='), k = kvp[0], v = kvp[1] || true;
                k = decode(k), v = decode(v), ls = params[k];
                if (_.isArray(ls)) ls.push(v);
                else if (ls) params[k] = [ls, v];
                else params[k] = v;
            }
            return params;
        },

    paramToQueryString: function(param){
            var qs = '?';
            var paramStringList =[]
            var encode = encodeURIComponent;
            for(var key in param){

                var str = encode(key)+'='+encode(param[key]) ;
                paramStringList.push(str);
            }
            return qs+ paramStringList.join('&');
        },

    get_origin_params: function () {
        var queryString = location.href.split('?')[1];
        if(!!!queryString){
            return {}
        }else{
            return this.queryStringToParams(queryString);
        }
    },
    get_start_date: function () {
        return $('#start_date').val();
    },
    get_end_date: function () {
        return $('#end_date').val();
    },
    generate_url: function (params) {
        return location.protocol + '//'
             + location.host
             + location.pathname
             + this.paramToQueryString(params);
    },
    handle_filter_button : function(event){
        var params =  this.get_origin_params();
        if(this.get_start_date()){
            params['start_date'] = this.get_start_date();
        }
        if(this.get_end_date()){
            params['end_date'] = this.get_end_date();
        }
        delete params['page'];
        var new_url = this.generate_url(params);
        window.location.href = new_url;
    },
    init_filter_button: function () {
        $('#date_filter_button').on('click', this.handle_filter_button.bind(this));
    },
    render_initial_date: function () {
        var params = this.get_origin_params();
        if(params['start_date']){
            $('#start_date').val(params['start_date']);
        }
        if(params['end_date']){
            $('#end_date').val(params['end_date']);
        }
    },
    init: function(){
        this.render_initial_date();
        this.init_filter_button();
    }
});


$(function(){
    var date_handler = new DateFilterHandler();
});
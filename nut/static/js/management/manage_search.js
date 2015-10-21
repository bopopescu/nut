console.log('in manage_search.js');

function queryStringToParams(qs) {
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
        }



function paramToQueryString(param){
            var qs = '?';
            var paramStringList =[]
            var encode = encodeURIComponent;
            for(var key in param){

                var str = encode(key)+'='+encode(param[key]) ;
                paramStringList.push(str);
            }
            return qs+ paramStringList.join('&');
        }

function handleSearch(e){
    console.log(location);
    var path = location.pathname
    var queryString = location.href.split('?')[1];
    var params = queryStringToParams(queryString);
    console.log(params);
    var filterfield = $(e.target).attr('data-search-field');
    var filtervalue = $(e.target).val();
    console.log('field:' + filterfield + ' value:' + filtervalue);
    params['filterfield'] = filterfield;
    params['filtervalue'] = filtervalue;
    window.location.href =  location.protocol + '//' + location.host + location.pathname  + paramToQueryString(params);

}

$('.guoku_search_input').change(handleSearch);
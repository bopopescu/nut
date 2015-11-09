define(['libs/Class', 'jquery'], function(Class, jQuery){
    var $= jQuery;

    var AjaxLoader = Class.extend({
        init:function(options){
            this.loading = false ;
            this.try_count=5;
            this.loading_indicator = document.getElementById('main_loading_indicator');
            this.attach();
        },
        attach: function(){
            this.scrollHandler =this._handleScroll.bind(this);
            $(window).scroll(this.scrollHandler);
        },

        detach: function(){
            $(window).off('scroll', this.scrollHandler);
        },
        loadNextBatch:function(){
            jQuery.when(
                    this.beginLoad()
            ).then(
                    this.loadSuccess.bind(this),
                    this.loadFail.bind(this)
            );
        },
        loadPrevBatch:function(){
            console.log('not implement');
        },
        _handleScroll: function(){
            if (this._shouldLoad()){
                this.loadNextBatch();
            }else{
                return ;
            }
        },
        _shouldLoad: function(){
            if (this.loading) {
                return false;
            }
            var loading_indicator  = this.loading_indicator;
                if (loading_indicator){
                    var position = loading_indicator.getBoundingClientRect();
                    //console.log(position.top + ' :   '+ window.innerHeight);
                    return (position.top > 0
                          && (position.top+100) <= (window.innerHeight || document.documentElement.clientHeight));
                }else{
                    return false;
                }
        },

        getRequestUrl: function(){
            return this.request_url;
        },

        getData: function(){
            throw new Error('not implemented');
            return null;
        },

        beginLoad: function(){
            this.loading = true;
            var _url = this.getRequestUrl();
            var _data = this.getData();
            return $.ajax({
                url : _url ,
                data : _data,
                method: 'GET'
            });
        //    return a promise , like an ajax() here

        },
        loadSuccess: function(data){
            console.log(data);
            this.loading = false;

        },
        loadFail: function(data){
            //console.log(data);
            // ajax call fail , maybe later
            console.log('loading failed ');
            this.try_count--;
            if (this.try_count <= 0){
                this.detach();
            }
            this.loading = false;
        }
    });

    return AjaxLoader;
});
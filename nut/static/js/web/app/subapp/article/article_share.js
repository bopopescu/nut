define(['jquery', 'libs/Class','underscore','bootbox'], function(
    $, Class,_,bootbox
){

    var ArticleShareApp= Class.extend({
        init: function(){
             //console.log('hello rose!');
            this.weibo_share_service_url = 'http://service.weibo.com/share/share.php';

            this.shareTitle = '我是图文分享对应的动态标题啦。';
            this.sharePic = '';

            this.weiboShareOptions = {
                url: this.getShareUrl(),
                title: this.shareTitle,
                type:'6',
                count:'0',
                appkey:'1459383851',
                ralateUid:'2179686555',
                language:'zh_cn',
                pic: this.sharePic,
                rnd : new Date().valueOf()
            };

            this.setupShareTrigger();

        },

        getShareUrl: function(){
            return location.href.replace(/m\.guoku\.com/, 'www.guoku.com');
        },

        setupShareTrigger: function(){

            $('.article-share .share-btn-weibo').each(this.setupWeiboShareBtn.bind(this));
            $('.article-sidebar-wrapper .sidebar_weibo_share_btn').each(this.setupWeiboShareBtn.bind(this));

        },

        makeUrlQueryString : function(options){
            var paramList = [];
            for (var key in options){
                paramList.push(key+'='+encodeURIComponent(options[key]));
            }
            return  '?' + paramList.join('&');
        },

        setupWeiboShareBtn: function(index,ele){
            var options = _.clone(this.weiboShareOptions);
                options.title = this.getSellerShareTitle(ele);
                options.pic = this.getSellerSharePic(ele);

                ele.href = this.weibo_share_service_url + this.makeUrlQueryString(options);
        },

         getSellerShareTitle: function(ele){

            return $(ele).attr('data_article_title');
        },
        getSellerSharePic: function(ele){

            return $(ele).attr('data_article_cover');
        }

    });

    return ArticleShareApp;
});
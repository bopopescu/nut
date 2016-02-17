define(['jquery', 'libs/Class','underscore','bootbox'], function(
    $, Class,_,bootbox
){

    var ArticleShareApp= Class.extend({
        init: function(){
             //console.log('hello rose!');
            this.weibo_share_service_url = 'http://service.weibo.com/share/share.php';
            this.qq_share_service_url = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey';
            this.share_weixin_modal_content = $('#share_weixin_modal_content').html();

            this.shareTitle = '真实的图文记录，帮助你更高效地做出消费决策，养成正向的消费价值观。';
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

             this.qqShareOptions ={
                url: this.getShareUrl(),
                showcount: 0 ,
                desc: this.shareTitle,
                summary: '果库精选图文概要',
                title: '#果库精选图文标题#',
                site: '果库网',
                pics: this.sharePic
            };

            this.setupShareTrigger();

        },

        getShareUrl: function(){
            return location.href.replace(/m\.guoku\.com/, 'www.guoku.com');
        },

        showWeixinShareDialog: function(){
            bootbox.hideAll();
            bootbox.dialog({
                title: '分享 精选图文 微信 modal title',
                onEscape: true,
                backdrop:true,
                closeButton: true,
                animate: true,
                className: 'article-share-wx-dialog',
                message: this.share_weixin_modal_content,

            });
        },

        setupShareTrigger: function(){

            $('.article-share .share-btn-weibo').each(this.setupWeiboShareBtn.bind(this));
            $('.article-share .share-btn-qq').each(this.setupQQShareBtn.bind(this));

            $('.article-sidebar-wrapper .sidebar_weibo_share_btn').each(this.setupWeiboShareBtn.bind(this));
            $('.article-sidebar-wrapper .sidebar_qq_share_btn').each(this.setupQQShareBtn.bind(this));
            $('.article-sidebar-wrapper .sidebar_weixin_share_btn').each(this.setupWeixinShareSellerBtn.bind(this));

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
                options.title = this.getShareTitle(ele);
                options.pic = this.getSharePic(ele);

                ele.href = this.weibo_share_service_url + this.makeUrlQueryString(options);
        },

        setupQQShareBtn: function(index,ele){
            var options = _.clone(this.qqShareOptions);
                options.showCount = 0;
                options.desc = this.getShareTitle(ele);
                options.summary = '#果库精选图文';
                options.title =  this.shareTitle;
                options.site = '果库网';
                options.pics = this.getSharePic(ele);

                ele.href = this.qq_share_service_url + this.makeUrlQueryString(options);

        },

        setupWeixinShareSellerBtn: function(index, ele){
                $(ele).click(this.showWeixinShareDialog.bind(this));
        },

         getShareTitle: function(ele){

            return $(ele).attr('data_article_title');
        },
        getSharePic: function(ele){

            return $(ele).attr('data_article_cover');
        }

    });

    return ArticleShareApp;
});
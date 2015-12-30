define(['libs/Class', 'jquery', 'underscore','bootbox'], function(Class,$,_,bootbox){

    //  http://open.weibo.com/blog/%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E2%80%93-%E7%8E%A9%E8%BD%AC%E6%96%B0%E6%B5%AA%E5%BE%AE%E5%8D%9A%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE
    //  http://connect.qq.com/intro/share/

    var ShareHanlder = Class.extend({
        init: function(){

            this.weibo_share_service_url = 'http://service.weibo.com/share/share.php';
            this.QQ_share_service_url = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey';
            this.share_modal_content = $('#share_modal_content').html();
            this.share_weixin_modal_content = $('#share_weixin_modal_content').html();

            this.weiboShareOptions = {
                url: location.href,
                type:'6',
                count:'0',
                appkey:'1459383851',
                ralateUid:'2179686555',
                language:'zh_cn',
                rnd : new Date().valueOf(),
            };

            this.weixinShareOptions ={

            }
            this.setupShareTrigger();
            this.setupShareBox();

        },
        setupShareBox: function(){
            $('.seller-cross-screen .share-btn').click(this.showShareDialog.bind(this));
        },

        showShareDialog: function(){
            bootbox.hideAll();
            bootbox.dialog({
                title: '分享 整页 modal. title',
                onEscape: true,
                backdrop:true,
                closeButton: true,
                animate: true,
                className: 'seller-share-dialog',
                message:this.share_modal_content,
            });
        },

        showWeixinShareDialog: function(){
            bootbox.hideAll();
            bootbox.dialog({
                title: '分享 卖家 微信 modal title',
                onEscape: true,
                backdrop:true,
                closeButton: true,
                animate: true,
                className: 'seller-share-wx-dialog',
                message: this.share_weixin_modal_content,

            });
        },
        setupShareTrigger: function(){

            //$('.seller-cross-screen .share-btn')
            //    .each(this.setupWeiboSharePageBtn.bind(this));

            $('.sellers-share .share-btn-wb')
                .each(this.setupWeiboShareSellerBtn.bind(this));

            $('.sellers-share .share-btn-wx')
                .each(this.setupWeixinShareSellerBtn.bind(this));

            $('.sellers-share .share-btn-qq')
                .each(this.setupQQShareSellerBtn.bind(this));

        },

        makeUrlQueryString : function(options){
            var paramList = [];
            for (var key in options){
                paramList.push(key+'='+encodeURIComponent(options[key]));
            }
            return  '?' + paramList.join('&');
        },

        setupWeiboSharePageBtn: function(index,ele){
            var options = _.clone(this.weiboShareOptions);
                options.title = 'this is page sharing title';
                options.pic = 'http://static.guoku.com/static/v4/6f848cd0324e89b80d3c2c776a9d29c5ebee4005/images/gklogo2015.png';
            ele.href = this.weibo_share_service_url + this.makeUrlQueryString(options);
            return;
        },
        setupWeiboShareSellerBtn: function(index,ele){
            var options = _.clone(this.weiboShareOptions);
                options.title = this.getSellerShareTitle(ele);
                options.pic = this.getSellerSharePic(ele);

                ele.href = this.weibo_share_service_url + this.makeUrlQueryString(options);
        },

        setupWeixinShareSellerBtn: function(index, ele){
                $(ele).click(this.showWeixinShareDialog.bind(this));
        },
        setupQQShareSellerBtn: function(index,ele){
            var options = _.clone(this.weiboShareOptions);
                options.showCount = 0;
                options.desc = 'wx desc';
                options.summary = 'qq 分享 summary';
                options.title =  'QQ 分享 title';
                options.site = '果库网';
                options.pics = 'QQ分享图片.jpg';

                ele.href = this.QQ_share_service_url + this.makeUrlQueryString(options);

        },
        getSellerShareTitle: function(ele){
            return 'test title';
        },
        getSellerSharePic: function(ele){
            return 'test pic';
        }

    });
    return ShareHanlder
});

define(['libs/Class', 'jquery', 'underscore','bootbox'], function(Class,$,_,bootbox){

    //  http://open.weibo.com/blog/%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E2%80%93-%E7%8E%A9%E8%BD%AC%E6%96%B0%E6%B5%AA%E5%BE%AE%E5%8D%9A%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE
    //  http://connect.qq.com/intro/share/

    var ShareHanlder = Class.extend({
        init: function(){

            this.weibo_share_service_url = 'http://service.weibo.com/share/share.php';
            this.qq_share_service_url = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey';
            this.share_modal_content = $('#share_modal_content').html();
            this.share_weixin_modal_content = $('#share_weixin_modal_content').html();

            this.shareTitle = '#果库2015年度最受欢迎淘宝店铺100家# 过去这一年，在发现最有趣、最实用 #果库好商品# 的同时，果库君筛选出 #最受欢迎淘宝店铺#，充满剁手智慧的百家经验谈，想说的都在这里...'
            this.sharePic = share_pic;

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
                summary: '最受欢迎淘宝店铺100家',
                title: '#果库2015年度消费报告#',
                site: '果库网',
                pics: this.sharePic
            };

            this.weixinShareOptions ={

            };

            this.section_dic  = {
                '1': '衣衫配饰',
                '2': '文艺漫游',
                '3': '美味佳肴',
                '4': '生活榜样'
            }

            this.setupShareTrigger();
            this.setupShareBox();
            this.setupPageShareLinks();

        },

        getShareUrl: function(){
            return location.href.replace(/m\.guoku\.com/, 'www.guoku.com');
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
                className: 'page-share-dialog',
                message:this.share_modal_content,
            });


            this.setupPageShareLinks();

        },

        setupPageShareLinks: function(){
            $('.pg-weibo-share-btn,.sidebar_weibo_share_btn').attr({href:this.getPageWeiboShareUrl()});
            $('.pg-qq-share-btn,.sidebar_qq_share_btn').attr({href:this.getPageQQShareUrl()})

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

            $('.sidebar_weixin_share_btn')
                .each(this.setupWeixinShareSellerBtn.bind(this));

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

        getPageWeiboShareUrl: function(){
            var options = _.clone(this.weiboShareOptions);
                options.pic = this.sharePic;
                return this.weibo_share_service_url + this.makeUrlQueryString(options);
        },
        getPageQQShareUrl: function(){
            var options = _.clone(this.qqShareOptions);
            return  this.qq_share_service_url + this.makeUrlQueryString(options);

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
                options.desc = this.getSellerShareTitle(ele);
                options.summary = '#果库2015年度消费报告';
                options.title =  this.shareTitle;
                options.site = '果库网';
                options.pics = this.getSellerSharePic(ele);

                ele.href = this.qq_share_service_url + this.makeUrlQueryString(options);

        },
        getSellerShareTitle: function(ele){
            var shop_title = $(ele).attr('data_shop_title');
            var shop_section = this.getSectionNameFromNumberString($(ele).attr('data_shop_section'));
            var shop_desc = $(ele).attr('data_shop_desc');
            var title = '「'+ shop_title+ '」'+'入选 '
                        + '＃果库2015年度最受欢迎淘宝店铺100家＃ 之'
                        + shop_section + '篇：'
                        + shop_desc
                        + ' 还有99家精彩店铺等你来发现。'
                        + '';

            //var title = '「'+ shop_title+ '」'+'入选了2015果库'+shop_section + '！果库年度消费报告，最受欢迎的淘宝店铺都在这里。';
            return title ;
        },
        getSellerSharePic: function(ele){
            return $(ele).attr('data_shop_pic');
        },
        getSectionNameFromNumberString : function(number_string){
                return this.section_dic[number_string];
        },


    });
    return ShareHanlder
});

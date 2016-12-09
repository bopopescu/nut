define(['libs/Class', 'jquery', 'underscore','bootbox','subapp/yearseller/share'], function(Class,$,_,bootbox,ShareHandler){

    //  http://open.weibo.com/blog/%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E2%80%93-%E7%8E%A9%E8%BD%AC%E6%96%B0%E6%B5%AA%E5%BE%AE%E5%8D%9A%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE
    //  http://connect.qq.com/intro/share/

    var ShareHanlder = ShareHandler.extend({
        init: function(){
            this.weibo_share_service_url = 'http://service.weibo.com/share/share.php';
            this.qq_share_service_url = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey';
            this.share_modal_content = $('#share_modal_content').html();
            this.share_weixin_modal_content = $('#share_weixin_modal_content').html();

            this.shareTitle = '#果库2016年度最受欢迎淘宝店铺100家# 过去这一年，在发现最有趣、最实用 #果库好商品# 的同时，果库君筛选出 #最受欢迎淘宝店铺#，充满剁手智慧的百家经验谈，想说的都在这里...';
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
                title: '#果库2016年度消费报告#',
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
            };

            this.setupShareTrigger();
            this.setupShareBox();
            this.setupPageShareLinks();

        },

        setupQQShareSellerBtn: function(index,ele){
            var options = _.clone(this.weiboShareOptions);
                options.showCount = 0;
                options.desc = this.getSellerShareTitle(ele);
                options.summary = '#果库2016年度消费报告';
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
                        + '＃果库2016年度最受欢迎淘宝店铺100家＃ 之'
                        + shop_section + '篇：'
                        + shop_desc
                        + ' 还有 99 家店铺等你来发现。'
                        + '';

            return title ;
        }
    });
    return ShareHanlder
});

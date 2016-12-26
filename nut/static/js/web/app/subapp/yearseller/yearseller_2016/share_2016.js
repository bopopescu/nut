define(['libs/Class', 'jquery', 'underscore','bootbox','subapp/yearseller/share'], function(Class,$,_,bootbox,ShareHandler){

    //  http://open.weibo.com/blog/%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E2%80%93-%E7%8E%A9%E8%BD%AC%E6%96%B0%E6%B5%AA%E5%BE%AE%E5%8D%9A%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE
    //  http://connect.qq.com/intro/share/

    var ShareHanlder = ShareHandler.extend({
        init: function(){
            this.weibo_share_service_url = 'http://service.weibo.com/share/share.php';
            this.qq_share_service_url = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey';
            this.share_modal_content = $('#share_modal_content').html();
            this.share_weixin_modal_content = $('#share_weixin_modal_content').html();

            this.shareTitle = '#果库2016年度消费报告# 生活的改变可以在「消费」里找到答案。过去一年，我们讨论过多少买买买的话题，哪些人始终为生活方式发声，而那些最值得剁手的淘宝好店，果库君可是精挑细选了 100 家！';
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
                summary: '果库2016年度消费报告',
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
            //var shop_section = this.getSectionNameFromNumberString($(ele).attr('data_shop_section'));
            var shop_desc = $(ele).attr('data_shop_desc');
            var title = '「'+ shop_desc+ '」'+'你我都爱的'
                        +'「'+ shop_title+ '」'
                        + '成功入选 #果库2016年度消费报告# 之 #好店100# 啦。'
                        + '';
            return title ;
        }
    });
    return ShareHanlder
});

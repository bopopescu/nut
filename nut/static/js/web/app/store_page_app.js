require([
        'jquery',
        'subapp/topmenu',
        'subapp/store/store_banner',
        'subapp/store/annual_report',
        'subapp/tracker'
    ],
    function (
              jQuery,
              Menu,
              StoreBanner,
              AnnualReport,
              Tracker
    ){
        var menu = new Menu();
        var store_banner = new StoreBanner();
        var annual_report = new AnnualReport();
        var tracker_list = [
            {
                selector : '#index-banners .banner-image-cell a',
                trigger: 'click',
                category: 'store-banner',
                action: 'article-detail',
                label: 'data-banner-title',
                value: 'data-banner'
            }, {
                selector: '#selection_article_list .hot-section-item a',
                trigger: 'click',
                category: 'article-rec',
                action: 'user-detail',
                label: 'data-rec-title',
                value: 'data-rec'
            }, {
                selector: '#top_article_tags_container .top-article-tag a',
                trigger: 'click',
                category: 'category',
                action: 'category_detail',
                label: 'data-stye-title',
                value: 'data-style'
            }, {
                selector: '.select-result-wrapper .result-item-wrapper a',
                trigger: 'click',
                category: 'good-stores',
                action: 'store-detail',
                label: 'data-seller-title',
                value: 'data-seller'

            }, {
                selector: '.consumption-report-item',
                trigger: 'click',
                category: 'store',
                action: 'consumption-report',
                label: 'data-report-title',
                value: 'data-report'
            }
        ];

        var tracker = new Tracker(tracker_list);
});


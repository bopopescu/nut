define(['component/ajaxloader', 'utils/browser', 'libs/fastdom'

], function (AjaxLoader, browser, fastdom) {

    var ArticleLoader = AjaxLoader.extend({
        request_url: '/articles/',
        init: function () {
            this._super();
            this.current_page = this.getInitPageNum();
            $('.next-button').click(this.goNext.bind(this));
            $('.prev-button').click(this.goPrev.bind(this));

        },
        goNext: function () {

            this.gotoPage(this.current_page + 1);
        },
        goPrev: function () {
            this.gotoPage(this.current_page - 5);
        },

        gotoPage: function (pageNum) {
            var path = window.location.pathname;
            var host = window.location.host;
            var protocol = window.location.protocol;
            var refresh_time = this.getRefreshTime();
            var newUrl = protocol + '//' + host + path + '?page=' + pageNum + '&t=' + refresh_time;
            window.location.href = newUrl;
        },

        getInitPageNum: function () {
            var queryDics = browser.getQueryStrings();
            return parseInt(queryDics['page']) || 1;
        },

        getData: function () {
            return {
                refresh_time: this.getRefreshTime(),
                page: this.current_page + 1,
            }
        },

        loadSuccess: function (data) {
            var that = this;
            if (data['errors'] === 0) {

                fastdom.defer(30, function () {
                    $(data['html']).appendTo($('#selection_article_list'));
                    if (data['has_next_page'] === false) {
                        that.handleLastPage();
                    }

                    that.current_page++;
                    if (that.current_page % 3 == 0) {
                        $(that.loading_indicator).hide();

                        if (that.current_page > 5) {
                            that.showPrevButton();
                        }
                        if (data['has_next_page'] === true) {
                            that.showNextButton();
                        }
                    } else {
                        that.hideLoadButton();
                    }
                    that.loading = false;
                });
            } else {
                //TODO: handle fail load
            }

            return;

        },
        showPrevButton: function () {
            $('.prev-button').show();
        },
        showNextButton: function () {
            $('.next-button').show();
        },

        hideNextButton: function () {
            $('.next-button').hide();
        },
        hideLoadButton: function () {
            $('.prev-button').hide();
            $('.next-button').hide();
        },
        handleLastPage: function () {
            this.detach();
            this.hideNextButton();
        },
        getRefreshTime: function () {
            return $('#selection_article_list').attr('refresh-time');
        },

        _shouldLoad: function () {
            var page_condition = (this.current_page > 0) && (this.current_page % 3 != 0);
            return page_condition && this._super();
        },
    });

    return ArticleLoader;
});
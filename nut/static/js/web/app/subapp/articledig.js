define(['libs/Class', 'subapp/account', 'jquery', 'fastdom'],
    function (Class, AccountApp, $, fastdom) {

        var AppArticleDig = Class.extend({
            init: function () {
                $('.dig-action').on('click', this.handleDig.bind(this));
            },
            handleDig: function (e) {
                var $digEle = $(e.currentTarget);
                var $counter = $digEle.parent().find('.dig-count');
                    articleId = $digEle
            }
        });


    });
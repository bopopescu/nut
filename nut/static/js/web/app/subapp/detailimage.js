define(['libs/Class'], function () {
    var EntityImageHandler = Class.extend({
        init: function () {
            $('.other-pic-list img')
                .on('click', this.handleThumbImg.bind(this))
                .on('mouseover', this.handleThumbImg.bind(this));
        },
        handleThumbImg: function (event) {

            var newSrc = $(event.currentTarget)
                .prop('src')
                .replace(/images\/\d+\//i, 'images/310/')
                .replace('_128x128','_310x310');
            var oldSrc = $('.detail-pic-left #buy-btn-img img').prop('src');
            if (newSrc !== oldSrc) {
                $('.detail-pic-left #buy-btn-img img').prop('src', newSrc);
            }
        }
    });

    return EntityImageHandler;
});
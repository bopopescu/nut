define(['libs/Class','jquery','bootstrap'],function(Class, $){
    var  Paginator = Class.extend({
        init: function () {
            this._super();
            this.current_page = this.getInitPageNum();
            $('.next-button').click(this.goNext.bind(this));
            $('.prev-button').click(this.goPrev.bind(this));

        },
    });

    return Paginator
});

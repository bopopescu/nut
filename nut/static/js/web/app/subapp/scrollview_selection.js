define(['jquery','libs/Class','libs/fastdom','masonry'], function($,Class,fastdom,masonry){
    var ScrollEntity = Class.extend({
        init: function () {
            this.$selection = $('#selection');
            this.shouldLoad = true;
            this.setupLoadWatcher();
        },
        setupLoadWatcher: function () {
            if (!this.$selection[0]) return;
            $(window).scroll(this.onScroll.bind(this));
            this.masonry_page();
        },

        masonry_page: function () {

            this.$selection;
            this.$selection.masonry({
                itemSelector: '.grid-item',
                columnWidth: '.grid-sizer',
                percentPosition: true
            })
        },

        onScroll: function () {
            if (this.read) {
                fastdom.clear(this.read)
            }
            this.read = fastdom.read(this.doRead.bind(this));

            if (this.write) {
                fastdom.clear(this.write);
            }
            this.write = fastdom.write(this.doWrite.bind(this));
        },

        doWrite: function () {
            var that = this;
            this.shouldLoad = this.isOverScrolled;

            if (!this.shouldLoad) {
                this.doClear();
                return;
            } else {
                this.loading = true;

                var aQuery = window.location.href.split('?');
                var url = aQuery[0];
                var p = 1, c = 0;
                if (aQuery.length > 1) {
                    var param = aQuery[1].split('&');
                    var param_p;
                    if (param.length > 1) {
                        param_p = param[0].split('=');
                        p = parseInt(param_p[1]);
                    }
                }
                var time = this.$selection.attr('data-refresh');
                var data = {
                    'p': p + this.counter,
                    'page': p + this.counter,
                    't': time
                };
                if (c !== 0) {
                    data['c'] = c;
                }
                fastdom.defer(30, function () {
                    $.when($.ajax({
                        url: url,
                        method: "GET",
                        data: data,
                        dataType: 'json'

                    })).then(
                        that.loadSuccess.bind(that),
                        that.loadFail.bind(that)
                    );
                });
            }
        },

        loadSuccess: function (res) {
            this.attachNewSelections($(res.data), res.status);
        },

        loadFail: function (data) {
            console.log(data)
        },

        attachNewSelections: function (elemList, status) {
            var that = this;
            fastdom.defer(function () {
                that.$selection.append(elemList);
            });
            fastdom.defer(function () {
                that.counter++;
                that.doClear();
                that.loading = false;
            });
        }
    });
    return ScrollEntity;
});


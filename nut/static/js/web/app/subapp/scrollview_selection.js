define(['jquery','libs/Class','libs/fastdom','masonry','jquery_bridget'],
    function($,Class,fastdom,Masonry){

        var ScrollEntity = Class.extend({
            init: function () {
                this.$selection = $('#selection');
                this.shouldLoad = true;
                this.initialize();
            },

            initialize : function () {
                $.bridget('masonry', Masonry);
                this.$selection.masonry({
                    isFitWidth:true,
                })
            }
        });
    return ScrollEntity;
});


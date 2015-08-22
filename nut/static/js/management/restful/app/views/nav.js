define(function(require){
    var navView = Backbone.View.extend({
        initialize: function(){
            console.log('in nav view');
            this.buttons = $('.nav_btn');

        },

        events :{
            'click .nav_btn': 'nav'
        },

        nav : function(event){
//            console.log(event.currentTarget);

            var viewTo = $(event.currentTarget).attr("data-vin");
            var viewFrom = $('.nav_btn.active').attr('data-vin');

            this.$('.nav_btn').removeClass('active');
            $(event.currentTarget).addClass('active');

            APP.nav(viewFrom ,viewTo , "slid");


        }


    });
    return navView;
});
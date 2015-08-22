define(function(require){
    var configTpl  = $('#id-config-view-template').html();
    var ConfigView = Backbone.View.extend({
        className : 'grid-cell',
        events: {
            'click .btn-config' : 'enter',
            'click .back-btn' : 'leave'
        },
        initialize : function(){
            this.template = _.template(configTpl);

        },
        viewDidAppear: function(){

        },
        viewWillAppear: function(){

        },
        enter : function(){
            fastdom.write(this.beginEnter, this);
        },
        leave: function(){
            fastdom.write(this.beginLeave, this);
        },
        beginEnter: function(){
            APP.disableNav();
            this.el.classList.remove('leaving');
            this.el.classList.add('entering');

        },
        beginLeave: function(){
            APP.enableNav();
            var that = this;

            var onAnimationEnd = function(){
                console.log('left');
                that.el.classList.remove('leaving');
                that.el.removeEventListener('webkitAnimationEnd', onAnimationEnd, false);
                that.el.removeEventListener('animationend',       onAnimationEnd);

            }


            this.el.addEventListener('webkitAnimationEnd', onAnimationEnd, false);
            this.el.addEventListener('animationend',       onAnimationEnd);

            this.el.classList.remove('entering');
            this.el.classList.add('leaving');


        },

        render : function(){
            this.el.innerHTML = this.template();
            return this;
        }

    });

    return ConfigView;

});
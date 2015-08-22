define(function(require){
    var authorTpl  = $('#id-author-view-template').html();
    var AuthorView = Backbone.View.extend({
        className : 'grid-cell',
        events: {
            'click .btn-author' : 'enter',
            'click .back-btn' : 'leave'
        },
        initialize : function(){
            this.template = _.template(authorTpl);

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

    return AuthorView;

});
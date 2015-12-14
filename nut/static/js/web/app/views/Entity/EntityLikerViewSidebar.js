define(['views/base/ListView'],function(
    ListView
){


  var EntityLikerViewSidebar = ListView.extend({

        render: function(){
            var res = ListView.prototype.render.apply(this);
            this.displayCounter();
            return res;
        },
        displayCounter: function(){
            this.$el.find('.liker-counter').html(this.likerCount);
        },


  });

  return EntityLikerViewSidebar;

});
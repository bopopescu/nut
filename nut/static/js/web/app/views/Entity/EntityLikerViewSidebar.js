define(['views/base/ListView'],function(
    ListView
){
  var EntityLikerViewSidebar = ListView.extend({

        render: function(){
            var res = ListView.prototype.render.apply(this);
            this.displayCounter();
            return res;
        },
        displayCounter: function(likerCount){
            this.$el.find('.liker-counter').html(likerCount);
        },
        setLikesCount: function(likerCount){
            this.displayCounter(likerCount);
        }
  });
  return EntityLikerViewSidebar;
});
define(['views/base/ListView'],function(
    ListView
){



  var   EntityLikerViewMobile = ListView.extend({

      setLikesCount: function(likeCount){
          this.$el.find('.liker-counter').html(likeCount);
      },

  });

  return EntityLikerViewMobile;

});
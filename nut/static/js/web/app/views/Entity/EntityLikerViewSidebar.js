define(['views/base/ListView'],function(
    ListView
){


  var EntityLikerViewSidebar = ListView.extend({

        initialize: function(){
        },
        render: function(){
            var res = ListView.prototype.render.apply(this);
            this.displayCounter();
            return res;
        },
        displayCounter: function(){

        }

  });

  return EntityLikerViewSidebar;

});
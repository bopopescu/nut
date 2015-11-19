define(['libs/Class', 'jquery'], function(){

    var PokeManager = Class.extend({
        init:function(){
            this.setupPokeEvents();
        },
        setupPokeEvents: function(ele){
            var that = this;
            var ele = ele || document.body;
            var pokeButtons = $(ele).find('.poke[data-note]');
            pokeButtons.each(function(index, pokeLink){
                $(pokeLink).on('click', that.doPoke )
            });
        },
        handleNoteEle: function(ele){
            this.setupPokeEvents(ele);
        },
        doPoke: function(event){
            console.log(event.currentTarget);
            console.log(this);
        }
    });
    return  PokeManager;
});
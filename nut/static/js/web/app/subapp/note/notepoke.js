define(['libs/Class',
        'jquery',
        'subapp/account'],
    function(
        Class,
        $,
        AccountApp
){
        var PokeManager = Class.extend({
        init:function(){
            this.accountApp = new AccountApp();
            this.setupPokeEvents();
        },
            setupPokeEvents: function(ele){
            var that = this;
            var ele = ele || document.body;
            var $pokeButtons = $(ele).find('.poke[data-note]');

            $pokeButtons.on('click', this.doPoke.bind(this));
        },
        handleNoteEle: function(ele){
            this.setupPokeEvents(ele);
        },
        doPoke: function(event){

            var $poke = $(event.currentTarget);
            var note_id =$poke.attr('data-note');
            var $counter = $poke.find('span.poke-count');
            var $poker_icon = $poke.find('i');

            var url  = '/note/' + note_id + '/poke/';

            $.when(
                $.ajax({
                    method: 'POST',
                    dataType: 'json',
                    url : url
                })
            ).then(
                    this.pokeSuccess.bind(this),
                    this.pokeFail.bind(this)
                );

        },
        pokeSuccess:function(data){
            var result = parseInt(data.result);
            var poked_note_id = data.note_id;

            var $poke = $('.poke[data-note="'+ poked_note_id +'"]');
            var $count = $poke.find('span.poke-count');
            var numberCount  = parseInt($count.html()) || 0 ;
            var $poke_icon = $poke.find('i.fa');


            if(result === 1){// poke , Not unpoke
                numberCount++;
                $poke_icon.addClass('fa-thumbs-up');
                $poke_icon.removeClass('fa-thumbs-o-up');

                if(numberCount === 1){
                    $('<span class="poke-count">' + numberCount + '</span>').appendTo($poke);

                }else{
                    $count.html(numberCount);

                }
                $count.show();

            }else if(result === 0){// unpoke

                numberCount--;
                $poke_icon.addClass('fa-thumbs-o-up');
                $poke_icon.removeClass('fa-thumbs-up');

                if (numberCount <= 0){
                    $poke.find('span').remove();
                }else{
                    $count.html(numberCount);
                }

            }else{
                var html = $(data);
                this.accountApp.modalSignIn(html);
            }

        },
        pokeFail:function(data){
            var html = data.responseText;
                this.accountApp.modalSignIn(html);
            }
        });

         return  PokeManager;
    });






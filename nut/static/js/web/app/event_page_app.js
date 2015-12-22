require(['jquery',
          'subapp/topmenu',
          'subapp/gotop',
          'subapp/event/event_entity_loader',
          'bootstrap',
          'snowFall'
    ],
    function($,Menu,GoTop,EventEntityLoader, snowFall){

        var menu = new Menu();
        var gotop = new GoTop();
        var eventEntityLoader = new EventEntityLoader();
        window.setInterval(snow, 10000);
        //snow();
        function snow(){
            if (/20151225/.test(location.pathname)){
                 $(document).snowfall('clear');
                 $(document).snowfall({shadow : false, round : true,  minSize: 5, maxSize:8,flakeCount : 180});
            }

        }

    });
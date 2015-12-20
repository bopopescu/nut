require(['jquery',
          'subapp/topmenu',
          'subapp/gotop',
          'subapp/event/event_entity_loader',
          'bootstrap'
    ],
    function($,Menu,GoTop,EventEntityLoader){

        var menu = new Menu();
        var gotop = new GoTop();
        var eventEntityLoader = new EventEntityLoader();

    });
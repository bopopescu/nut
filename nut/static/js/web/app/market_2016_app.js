require([
        'jquery',
        'subapp/market/show_modal',
        'subapp/market/device_orientation'
    ],
    function($,
             ShowModal,
             DeviceOrientation
    ){
        var show_modal = new ShowModal();
        var device_orientation = new DeviceOrientation();
    });

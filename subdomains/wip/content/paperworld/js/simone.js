$(document).ready(function() {
    var flashvars  = {};
    var params     = {
        scale: "noscale",
        wmode: "gpu",
        menu : "false",
    };
    var attributes = {};

    swfobject.embedSWF("swf/main.swf", "flash-panel", "800", "400", "10.0.0", false, flashvars, params, attributes);
});

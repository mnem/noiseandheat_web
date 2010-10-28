$(document).ready(function() {
    var flashvars  = {};
    var params     = {
        scale: "noscale",
        wmode: "gpu",
        menu : "false"
    };
    var attributes = {};

    swfobject.embedSWF("swf/index.swf", "flash-panel", "800", "600", "10.1.0", false, flashvars, params, attributes);
});

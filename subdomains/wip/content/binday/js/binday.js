var g_binaryString = "";

function binaryGroupToString(group) {
    var value = 0;
    
    for(var i = 0; i < group.length; i++) {
        if(group.charAt(i) == "1") {
            value = value | (1 << ((group.length-1) - i));
        }
    }
    
    return value;
}

function stringFromBinaryString(binary) {
    var message = "";
    var group = "";
    
    for(var i = 0; i < binary.length; i++) {
        if((binary.charAt(i) != "0" && binary.charAt(i) != "1" && group.length > 0) || group.length == 32) {
            message += String.fromCharCode(binaryGroupToString(group));
            group = "";
        } else if (binary.charAt(i) == "0" || binary.charAt(i) == "1"){
            group += binary.charAt(i);
        }
    }
    
    if(group.length > 0) {
        message += String.fromCharCode(binaryGroupToString(group));
    }
    
    return message;
}

function valueToBinaryString(value) {
    var binary = ""
    
    for(var i = 0; i < 32; i++) {
        if((value & (0x80000000 >>> i)) != 0) {
            binary += "1";
        } else {
            binary += "0";
        }
    }
    
    while(binary.length > 0 && (binary.charAt(0) == "0")) {
        binary = binary.substr(1);
    }
    
    return binary;
}

function stringToBinaryString(message) {
    var binary = "";
    
    for(var i = 0; i < message.length; i++) {
        if(binary.length > 0) {
            binary += " ";
        }
        binary += valueToBinaryString(message.charCodeAt(i));
    }
    
    return binary;
}

function messageIsProbablyBinary(message) {
    var bits = 0;
    for(var i = 0; i < message.length; i++) {
        var character = message.charAt(i);
        if(character == "0" || character == "1") {
            bits += 1;
        }
    }
    
    var percentageBits = bits / message.length;
    if(percentageBits > 0.25) {
        return true;
    } else {
        return false;
    }
}

function messageChanged() {
    message = $("#message").val();
    if(messageIsProbablyBinary(message)) {
        $("#binary-label").html("Translation");
        $("#binary").val(stringFromBinaryString(message));
        $("#binary").change();
    } else {
        $("#binary-label").html("Binary");
        g_binaryString = stringToBinaryString(message);
        if(g_binaryString.length > 0) {
            $("#binary").val(g_binaryString + "#binday");
        } else {
            $("#binary").val(g_binaryString);
        }
        $("#binary").change();
    }
}

function canTweet() {
    var length = $("#binary").val().length;
    var message = $("#message").val();
    
    if(length > 140 || length <= 0) {
        return false;
    }
    if(messageIsProbablyBinary(message)) {
        return false;
    }
    
    return true;
}

function binaryChanged() {
    var length = $("#binary").val().length;
    
    $("#characters-left").html(140 - length);
    
    // Adjust label colour
    $("#characters-left").removeClass("chars-ok chars-careful chars-you-were-only-supposed-to-blow-the-bloody-doors-off")
    if(length >= 130) {
        $("#characters-left").addClass("chars-you-were-only-supposed-to-blow-the-bloody-doors-off")
    } else if(length >= 120) {
        $("#characters-left").addClass("chars-careful")
    } else {
        $("#characters-left").addClass("chars-ok")
    }
    
    if(canTweet()) {
        $("#tweet-button").button("option", "disabled", false);
    } else {
        $("#tweet-button").button("option", "disabled", true);
    }
}

function tweetIt() {
    if(canTweet()){
        var url = "http://twitter.com/?status=" + encodeURI(g_binaryString) + "%23binday";
        window.location = url;
    }
}

$(document).ready(function() {
    $("#message").keypress(messageChanged);
    $("#message").keydown(messageChanged);
    $("#message").keyup(messageChanged);

    $("#binary").change(binaryChanged);

    $("#tweet-button").button({disabled:true});
    $("#tweet-button").click(tweetIt);
    
    $("#message").focus();
});

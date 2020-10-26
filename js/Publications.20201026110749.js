(function(d){var h=[];d.loadImages=function(a,e){"string"==typeof a&&(a=[a]);for(var f=a.length,g=0,b=0;b<f;b++){var c=document.createElement("img");c.onload=function(){g++;g==f&&d.isFunction(e)&&e()};c.src=a[b];h.push(c)}}})(window.jQuery);
$.fn.hasAttr = function(name) { var attr = $(this).attr(name); return typeof attr !== typeof undefined && attr !== false; };


$(document).ready(function() {
r=function(){dpi=window.devicePixelRatio;$('.js30').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js31').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js32').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js33').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js34').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js35').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js36').attr('src', (dpi>1) ? 'images/button_over-264.png' : 'images/button_over-132.png');
$('.js37').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js38').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');};
if(!window.HTMLPictureElement){r();}
(function(){$('a[href^="#"]:not(.allowConsent,.noConsent,.denyConsent,.removeConsent)').each(function(i,e){$(e).click(function(){var t=e.hash.length>1?$('[name="'+e.hash.slice(1)+'"]').offset().top:0;return $("html, body").animate({scrollTop:t},400),!1})})})();

});
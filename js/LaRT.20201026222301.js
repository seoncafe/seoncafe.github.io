(function(d){var h=[];d.loadImages=function(a,e){"string"==typeof a&&(a=[a]);for(var f=a.length,g=0,b=0;b<f;b++){var c=document.createElement("img");c.onload=function(){g++;g==f&&d.isFunction(e)&&e()};c.src=a[b];h.push(c)}}})(window.jQuery);
$.fn.hasAttr = function(name) { var attr = $(this).attr(name); return typeof attr !== typeof undefined && attr !== false; };


$(document).ready(function() {
r=function(){dpi=window.devicePixelRatio;$('.js61').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js62').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js63').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js64').attr('src', (dpi>1) ? 'images/button_over-264.png' : 'images/button_over-132.png');
$('.js65').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js66').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js67').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js68').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js69').attr('src', (dpi>1) ? 'images/button_normal-264.png' : 'images/button_normal-132.png');
$('.js71').attr('src', (dpi>1) ? 'images/poster-1184-2.jpg' : 'images/poster-592-1.jpg');};
if(!window.HTMLPictureElement){r();}
(function(){$('a[href^="#"]:not(.allowConsent,.noConsent,.denyConsent,.removeConsent)').each(function(i,e){$(e).click(function(){var t=e.hash.length>1?$('[name="'+e.hash.slice(1)+'"]').offset().top:0;return $("html, body").animate({scrollTop:t},400),!1})})})();
$('.js72').click(function(e) {
e.preventDefault();
$('.js70').html("<video class=\"video\" loop controls autoplay class=\"videoinline\"><source src=\"video/t1tau3_cub111_ani.mp4\" type=\"video/mp4\"></video>");
});

});
(function(d){var h=[];d.loadImages=function(a,e){"string"==typeof a&&(a=[a]);for(var f=a.length,g=0,b=0;b<f;b++){var c=document.createElement("img");c.onload=function(){g++;g==f&&d.isFunction(e)&&e()};c.src=a[b];h.push(c)}}})(window.jQuery);
var wl;

!function(){if("Promise"in window){var e,t,r=document,n=function(){return r.createElement("link")},o=new Set,a=n(),s=a.relList&&a.relList.supports&&a.relList.supports("prefetch"),i=location.href.replace(/#[^#]+$/,"");o.add(i);var c=function(e){var t=location,r="http:",n="https:";if(e&&e.href&&e.origin==t.origin&&[r,n].includes(e.protocol)&&(e.protocol!=r||t.protocol!=n)){var o=e.pathname;if(!(e.hash&&o+e.search==t.pathname+t.search||"?preload=no"==e.search.substr(-11)||".html"!=o.substr(-5)&&".html"!=o.substr(-5)&&"/"!=o.substr(-1)))return!0}},u=function(e){var t=e.replace(/#[^#]+$/,"");if(!o.has(t)){if(s){var a=n();a.rel="prefetch",a.href=t,r.head.appendChild(a)}else{var i=new XMLHttpRequest;i.open("GET",t,i.withCredentials=!0),i.send()}o.add(t)}},p=function(e){return e.target.closest("a")},f=function(t){var r=t.relatedTarget;r&&p(t)==r.closest("a")||e&&(clearTimeout(e),e=void 0)},l={capture:!0,passive:!0};r.addEventListener("touchstart",function(e){t=performance.now();var r=p(e);c(r)&&u(r.href)},l),r.addEventListener("mouseover",function(r){if(!(performance.now()-t<1200)){var n=p(r);c(n)&&(n.addEventListener("mouseout",f,{passive:!0}),e=setTimeout(function(){u(n.href),e=void 0},80))}},l)}}();

$(function(){
r=function(){dpi=window.devicePixelRatio;var e=document.querySelector('.js61');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js62');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js63');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js64');e.setAttribute('src',(dpi>1)?'images/button_over-264-1.png':'images/button_over-132-1.png');
var e=document.querySelector('.js65');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js66');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js67');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js68');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js69');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.js70');e.setAttribute('src',(dpi>1)?'images/poster-1184-4.jpg':'images/poster-592-3.jpg');};
if(!window.HTMLPictureElement){r();}
(function(){$('a[href^="#"]:not(.allowConsent,.noConsent,.denyConsent,.removeConsent)').each(function(i,e){$(e).click(function(){var t=e.hash.length>1?$('[name="'+e.hash.slice(1)+'"]').offset().top:0;return $("html, body").animate({scrollTop:t},400),!1})})})();
$('.js71').click(function(e) {
e.preventDefault();
$('.js72').html("<video class=\"video1\" loop controls autoplay class=\"videoinline\"><source src=\"video/t1tau3_cub111_ani.mp4\" type=\"video/mp4\"></video>");
});

});
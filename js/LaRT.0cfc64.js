(function(d){var h=[];d.loadImages=function(a,e){"string"==typeof a&&(a=[a]);for(var f=a.length,g=0,b=0;b<f;b++){var c=document.createElement("img");c.onload=function(){g++;g==f&&d.isFunction(e)&&e()};c.src=a[b];h.push(c)}}})(window.jQuery);
var wl;

!function(){if("Promise"in window&&void 0!==window.performance){var e,t,r=document,n=function(){return r.createElement("link")},o=new Set,a=n(),i=a.relList&&a.relList.supports&&a.relList.supports("prefetch"),s=location.href.replace(/#[^#]+$/,"");o.add(s);var c=function(e){var t=location,r="http:",n="https:";if(e&&e.href&&e.origin==t.origin&&[r,n].includes(e.protocol)&&(e.protocol!=r||t.protocol!=n)){var o=e.pathname;if(!(e.hash&&o+e.search==t.pathname+t.search||"?preload=no"==e.search.substr(-11)||".html"!=o.substr(-5)&&".html"!=o.substr(-5)&&"/"!=o.substr(-1)))return!0}},u=function(e){var t=e.replace(/#[^#]+$/,"");if(!o.has(t)){if(i){var a=n();a.rel="prefetch",a.href=t,r.head.appendChild(a)}else{var s=new XMLHttpRequest;s.open("GET",t,s.withCredentials=!0),s.send()}o.add(t)}},p=function(e){return e.target.closest("a")},f=function(t){var r=t.relatedTarget;r&&p(t)==r.closest("a")||e&&(clearTimeout(e),e=void 0)},d={capture:!0,passive:!0};r.addEventListener("touchstart",function(e){t=performance.now();var r=p(e);c(r)&&u(r.href)},d),r.addEventListener("mouseover",function(r){if(!(performance.now()-t<1200)){var n=p(r);c(n)&&(n.addEventListener("mouseout",f,{passive:!0}),e=setTimeout(function(){u(n.href),e=void 0},80))}},d)}}();

$(function(){
r=function(){dpi=window.devicePixelRatio;var e=document.querySelector('.un61');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un62');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un63');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un64');e.setAttribute('src',(dpi>1)?'images/button_over-264-1.png':'images/button_over-132-1.png');
var e=document.querySelector('.un65');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un66');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un67');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un68');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un69');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un70');e.setAttribute('src',(dpi>1)?'images/poster-1184-4.jpg':'images/poster-592-3.jpg');};
if(!window.HTMLPictureElement){r();}
!function(){var e=document.querySelectorAll('a[href^="#"]');[].forEach.call(e,function(e){e.addEventListener("click",function(t){var o=0;if(e.hash.length>1){var n=parseFloat(getComputedStyle(document.body).getPropertyValue("zoom"));n||(n=1);var r=document.querySelectorAll('[name="'+e.hash.slice(1)+'"]')[0];if(!r)return;var l=/chrome/i.test(navigator.userAgent);o=l?r.getBoundingClientRect().top*n+pageYOffset:(r.getBoundingClientRect().top+pageYOffset)*n}if("scrollBehavior"in document.documentElement.style)scroll({top:o,left:0,behavior:"smooth"});else if("requestAnimationFrame"in window){var a=pageYOffset,i=null;requestAnimationFrame(function e(t){i||(i=t);var n=t-i;scrollTo(0,a<o?(o-a)*n/400+a:a-(a-o)*n/400),n<400?requestAnimationFrame(e):scrollTo(0,o)})}else scrollTo(0,o);t.preventDefault()},!1)})}();
$('.un71').click(function(e) {
e.preventDefault();
$('.un72').html("<video class=\"video1\" loop controls autoplay class=\"videoinline\"><source src=\"video/t1tau3_cub111_ani.mp4\" type=\"video/mp4\"></video>");
});
if(location.hash){var e=location.hash.replace("#",""),o=function(){var t=document.querySelectorAll('[name="'+e+'"]')[0];t&&t.scrollIntoView(),"0px"===window.getComputedStyle(document.body).getPropertyValue("min-width")&&setTimeout(o,100)};o()}

});
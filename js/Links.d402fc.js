(function(d){var h=[];d.loadImages=function(a,e){"string"==typeof a&&(a=[a]);for(var f=a.length,g=0,b=0;b<f;b++){var c=document.createElement("img");c.onload=function(){g++;g==f&&d.isFunction(e)&&e()};c.src=a[b];h.push(c)}}})(window.jQuery);
var wl;

!function(){if("Promise"in window&&void 0!==window.performance){var e,t,r=document,n=function(){return r.createElement("link")},o=new Set,a=n(),i=a.relList&&a.relList.supports&&a.relList.supports("prefetch"),s=location.href.replace(/#[^#]+$/,"");o.add(s);var c=function(e){var t=location,r="http:",n="https:";if(e&&e.href&&e.origin==t.origin&&[r,n].includes(e.protocol)&&(e.protocol!=r||t.protocol!=n)){var o=e.pathname;if(!(e.hash&&o+e.search==t.pathname+t.search||"?preload=no"==e.search.substr(-11)||".html"!=o.substr(-5)&&".html"!=o.substr(-5)&&"/"!=o.substr(-1)))return!0}},u=function(e){var t=e.replace(/#[^#]+$/,"");if(!o.has(t)){if(i){var a=n();a.rel="prefetch",a.href=t,r.head.appendChild(a)}else{var s=new XMLHttpRequest;s.open("GET",t,s.withCredentials=!0),s.send()}o.add(t)}},p=function(e){return e.target.closest("a")},f=function(t){var r=t.relatedTarget;r&&p(t)==r.closest("a")||e&&(clearTimeout(e),e=void 0)},d={capture:!0,passive:!0};r.addEventListener("touchstart",function(e){t=performance.now();var r=p(e);c(r)&&u(r.href)},d),r.addEventListener("mouseover",function(r){if(!(performance.now()-t<1200)){var n=p(r);c(n)&&(n.addEventListener("mouseout",f,{passive:!0}),e=setTimeout(function(){u(n.href),e=void 0},80))}},d)}}();

$(function(){
r=function(){dpi=window.devicePixelRatio;var e=document.querySelector('.un82');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un83');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un84');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un85');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un86');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un87');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un88');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');
var e=document.querySelector('.un89');e.setAttribute('src',(dpi>1)?'images/button_over-264-1.png':'images/button_over-132-1.png');
var e=document.querySelector('.un90');e.setAttribute('src',(dpi>1)?'images/button_normal-264-1.png':'images/button_normal-132-1.png');};
if(!window.HTMLPictureElement){r();}
!function(){var e=document.querySelectorAll('a[href^="#"]:not(.allowConsent,.noConsent,.denyConsent,.removeConsent)');[].forEach.call(e,function(e){e.addEventListener("click",function(o){var t=0;if(e.hash.length>1){var n=parseFloat(getComputedStyle(document.body).getPropertyValue("zoom"));n||(n=1);var l=document.querySelectorAll('[name="'+e.hash.slice(1)+'"]')[0];t=(l.getBoundingClientRect().top+pageYOffset)*n}if("scrollBehavior"in document.documentElement.style)scroll({top:t,left:0,behavior:"smooth"});else if("requestAnimationFrame"in window){var r=pageYOffset,a=null;requestAnimationFrame(function e(o){a||(a=o);var n=o-a;scrollTo(0,r<t?(t-r)*n/400+r:r-(r-t)*n/400),n<400?requestAnimationFrame(e):scrollTo(0,t)})}else scrollTo(0,t);o.preventDefault()},!1)})}();
if(location.hash){var e=location.hash.replace("#",""),o=function(){var t=document.querySelectorAll('[name="'+e+'"]')[0];t&&t.scrollIntoView(),"complete"!=document.readyState&&setTimeout(o,100)};o()}

});
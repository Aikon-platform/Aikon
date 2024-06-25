var recordList=function(){"use strict";function t(){}function e(t){return t()}function n(){return Object.create(null)}function o(t){t.forEach(e)}function l(t){return"function"==typeof t}function c(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}let i,s;function r(t,e){return i||(i=document.createElement("a")),i.href=e,t===i.href}function a(t,e){t.appendChild(e)}function u(t,e,n){t.insertBefore(e,n||null)}function d(t){t.parentNode&&t.parentNode.removeChild(t)}function f(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function p(t){return document.createElement(t)}function m(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function g(t){return document.createTextNode(t)}function h(){return g(" ")}function b(){return g("")}function $(t,e,n,o){return t.addEventListener(e,n,o),()=>t.removeEventListener(e,n,o)}function v(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function y(t,e){e=""+e,t.data!==e&&(t.data=e)}function k(t,e,n){t.classList[n?"add":"remove"](e)}function w(t){s=t}function x(){const t=function(){if(!s)throw new Error("Function called outside component initialization");return s}();return(e,n,{cancelable:o=!1}={})=>{const l=t.$$.callbacks[e];if(l){const c=function(t,e,{bubbles:n=!1,cancelable:o=!1}={}){const l=document.createEvent("CustomEvent");return l.initCustomEvent(t,n,o,e),l}(e,n,{cancelable:o});return l.slice().forEach((e=>{e.call(t,c)})),!c.defaultPrevented}return!0}}const L=[],S=[];let A=[];const _=[],E=Promise.resolve();let N=!1;function O(t){A.push(t)}const j=new Set;let C=0;function P(){if(0!==C)return;const t=s;do{try{for(;C<L.length;){const t=L[C];C++,w(t),z(t.$$)}}catch(t){throw L.length=0,C=0,t}for(w(null),L.length=0,C=0;S.length;)S.pop()();for(let t=0;t<A.length;t+=1){const e=A[t];j.has(e)||(j.add(e),e())}A.length=0}while(L.length);for(;_.length;)_.pop()();N=!1,j.clear(),w(t)}function z(t){if(null!==t.fragment){t.update(),o(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(O)}}const T=new Set;let M;function V(){M={r:0,c:[],p:M}}function R(){M.r||o(M.c),M=M.p}function I(t,e){t&&t.i&&(T.delete(t),t.i(e))}function H(t,e,n,o){if(t&&t.o){if(T.has(t))return;T.add(t),M.c.push((()=>{T.delete(t),o&&(n&&t.d(1),o())})),t.o(e)}else o&&o()}function B(t,e){H(t,1,1,(()=>{e.delete(t.key)}))}function q(t){t&&t.c()}function J(t,n,c,i){const{fragment:s,after_update:r}=t.$$;s&&s.m(n,c),i||O((()=>{const n=t.$$.on_mount.map(e).filter(l);t.$$.on_destroy?t.$$.on_destroy.push(...n):o(n),t.$$.on_mount=[]})),r.forEach(O)}function D(t,e){const n=t.$$;null!==n.fragment&&(!function(t){const e=[],n=[];A.forEach((o=>-1===t.indexOf(o)?e.push(o):n.push(o))),n.forEach((t=>t())),A=e}(n.after_update),o(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function U(t,e){-1===t.$$.dirty[0]&&(L.push(t),N||(N=!0,E.then(P)),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}function F(e,l,c,i,r,a,u,f=[-1]){const p=s;w(e);const m=e.$$={fragment:null,ctx:[],props:a,update:t,not_equal:r,bound:n(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(l.context||(p?p.$$.context:[])),callbacks:n(),dirty:f,skip_bound:!1,root:l.target||p.$$.root};u&&u(m.root);let g=!1;if(m.ctx=c?c(e,l.props||{},((t,n,...o)=>{const l=o.length?o[0]:n;return m.ctx&&r(m.ctx[t],m.ctx[t]=l)&&(!m.skip_bound&&m.bound[t]&&m.bound[t](l),g&&U(e,t)),n})):[],m.update(),g=!0,o(m.before_update),m.fragment=!!i&&i(m.ctx),l.target){if(l.hydrate){const t=function(t){return Array.from(t.childNodes)}(l.target);m.fragment&&m.fragment.l(t),t.forEach(d)}else m.fragment&&m.fragment.c();l.intro&&I(e.$$.fragment),J(e,l.target,l.anchor,l.customElement),P()}w(p)}class G{$destroy(){D(this,1),this.$destroy=t}$on(e,n){if(!l(n))return t;const o=this.$$.callbacks[e]||(this.$$.callbacks[e]=[]);return o.push(n),()=>{const t=o.indexOf(n);-1!==t&&o.splice(t,1)}}$set(t){var e;this.$$set&&(e=t,0!==Object.keys(e).length)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}function K(t=null,e="full",n="full"){if(!t)return"https://via.placeholder.com/96x96?text=No+Image";if((t=t.split("_")).length<3)return"https://via.placeholder.com/96x96?text=No+Image";const o=t[t.length-1].includes(",")?t.pop().replace(".jpg",""):e,l=t.join("_").replace(".jpg","");return`${CANTALOUPE_APP_URL??"http://localhost:8182"}/iiif/2/${l}.jpg/${o}/${n}/0/default.jpg`}function Q(t,e,n){const o=t.slice();return o[6]=e[n][0],o[7]=e[n][1],o}function W(t,e,n){const o=t.slice();return o[10]=e[n],o}function X(t){let e;return{c(){e=p("span"),e.innerHTML='<span class="icon has-text-success"><i class="fas fa-check-circle"></i></span> \n                                <span style="margin-left: -0.5rem">Public</span>',v(e,"class","pl-3 icon-text is-size-7 is-center has-text-weight-normal")},m(t,n){u(t,e,n)},d(t){t&&d(e)}}}function Y(t){let e,n,o,l,c=t[0].hasOwnProperty("iiif"),i=t[0].buttons.includes("regions"),s=t[0].buttons.includes("similarity"),r=t[0].buttons.includes("vectorization"),f=c&&Z(t),m=i&&et(t),g=s&&nt(t),b=r&&ot(t);return{c(){e=p("p"),f&&f.c(),n=h(),m&&m.c(),o=h(),g&&g.c(),l=h(),b&&b.c(),v(e,"class","subtitle is-6 mb-0 ml-2 pt-2")},m(t,c){u(t,e,c),f&&f.m(e,null),a(e,n),m&&m.m(e,null),a(e,o),g&&g.m(e,null),a(e,l),b&&b.m(e,null)},p(t,a){1&a&&(c=t[0].hasOwnProperty("iiif")),c?f?f.p(t,a):(f=Z(t),f.c(),f.m(e,n)):f&&(f.d(1),f=null),1&a&&(i=t[0].buttons.includes("regions")),i?m?m.p(t,a):(m=et(t),m.c(),m.m(e,o)):m&&(m.d(1),m=null),1&a&&(s=t[0].buttons.includes("similarity")),s?g?g.p(t,a):(g=nt(t),g.c(),g.m(e,l)):g&&(g.d(1),g=null),1&a&&(r=t[0].buttons.includes("vectorization")),r?b?b.p(t,a):(b=ot(t),b.c(),b.m(e,null)):b&&(b.d(1),b=null)},d(t){t&&d(e),f&&f.d(),m&&m.d(),g&&g.d(),b&&b.d()}}}function Z(t){let e,n=t[0].iiif,o=[];for(let e=0;e<n.length;e+=1)o[e]=tt(W(t,n,e));return{c(){for(let t=0;t<o.length;t+=1)o[t].c();e=b()},m(t,n){for(let e=0;e<o.length;e+=1)o[e]&&o[e].m(t,n);u(t,e,n)},p(t,l){if(1&l){let c;for(n=t[0].iiif,c=0;c<n.length;c+=1){const i=W(t,n,c);o[c]?o[c].p(i,l):(o[c]=tt(i),o[c].c(),o[c].m(e.parentNode,e))}for(;c<o.length;c+=1)o[c].d(1);o.length=n.length}},d(t){f(o,t),t&&d(e)}}}function tt(t){let e,n=t[10]+"";return{c(){e=p("span"),v(e,"class","tag logo mt-1")},m(t,o){u(t,e,o),e.innerHTML=n},p(t,o){1&o&&n!==(n=t[10]+"")&&(e.innerHTML=n)},d(t){t&&d(e)}}}function et(t){let e,n,o,l;return{c(){e=p("a"),n=p("span"),v(n,"class","iconify"),v(n,"data-icon","entypo:documents"),v(e,"href",o=t[0].url+"regions/"),v(e,"class","button is-small is-rounded is-link px-2"),v(e,"title",l="en"===t[1]?"Show extracted regions":"Afficher les zones d'images")},m(t,o){u(t,e,o),a(e,n)},p(t,n){1&n&&o!==(o=t[0].url+"regions/")&&v(e,"href",o),2&n&&l!==(l="en"===t[1]?"Show extracted regions":"Afficher les zones d'images")&&v(e,"title",l)},d(t){t&&d(e)}}}function nt(t){let e,n,o,l;return{c(){e=p("a"),n=p("span"),v(n,"class","iconify"),v(n,"data-icon","octicon:mirror-16"),v(e,"href",o=t[0].url+"similarity/"),v(e,"class","button is-small is-rounded is-link px-2"),v(e,"title",l="en"===t[1]?"Show similarity":"Afficher les similarités")},m(t,o){u(t,e,o),a(e,n)},p(t,n){1&n&&o!==(o=t[0].url+"similarity/")&&v(e,"href",o),2&n&&l!==(l="en"===t[1]?"Show similarity":"Afficher les similarités")&&v(e,"title",l)},d(t){t&&d(e)}}}function ot(t){let e,n,o,l;return{c(){e=p("a"),n=p("span"),v(n,"class","iconify"),v(n,"data-icon","arcticons:geogebra-geometry"),v(e,"href",o=t[0].url+"vectorization/"),v(e,"class","button is-small is-rounded is-link px-2"),v(e,"title",l="en"===t[1]?"Show vectorizations":"Afficher les vectorisations")},m(t,o){u(t,e,o),a(e,n)},p(t,n){1&n&&o!==(o=t[0].url+"vectorization/")&&v(e,"href",o),2&n&&l!==(l="en"===t[1]?"Show vectorizations":"Afficher les vectorisations")&&v(e,"title",l)},d(t){t&&d(e)}}}function lt(t){let e,n,o=t[2]?"Retirer de":"Ajouter à la";return{c(){e=g(o),n=g(" sélection")},m(t,o){u(t,e,o),u(t,n,o)},p(t,n){4&n&&o!==(o=t[2]?"Retirer de":"Ajouter à la")&&y(e,o)},d(t){t&&d(e),t&&d(n)}}}function ct(t){let e,n,o=t[2]?"Remove from":"Add to";return{c(){e=g(o),n=g(" set")},m(t,o){u(t,e,o),u(t,n,o)},p(t,n){4&n&&o!==(o=t[2]?"Remove from":"Add to")&&y(e,o)},d(t){t&&d(e),t&&d(n)}}}function it(t){let e;return{c(){e=m("path"),v(e,"fill","currentColor"),v(e,"d","M0 48C0 21.5 21.5 0 48 0l0 48V441.4l130.1-92.9c8.3-6 19.6-6 27.9 0L336 441.4V48H48V0H336c26.5 0 48 21.5 48 48V488c0 9-5 17.2-13 21.3s-17.6 3.4-24.9-1.8L192 397.5 37.9 507.5c-7.3 5.2-16.9 5.9-24.9 1.8S0 497 0 488V48z")},m(t,n){u(t,e,n)},d(t){t&&d(e)}}}function st(t){let e;return{c(){e=m("path"),v(e,"fill","currentColor"),v(e,"d","M0 48V487.7C0 501.1 10.9 512 24.3 512c5 0 9.9-1.5 14-4.4L192 400 345.7 507.6c4.1 2.9 9 4.4 14 4.4c13.4 0 24.3-10.9 24.3-24.3V48c0-26.5-21.5-48-48-48H48C21.5 0 0 21.5 0 48z")},m(t,n){u(t,e,n)},d(t){t&&d(e)}}}function rt(t){let e,n,o,l,c,i,s,r=t[6]+"",f=t[7]+"";return{c(){e=p("tr"),n=p("th"),o=g(r),l=h(),c=p("td"),i=g(f),s=h(),v(n,"class","is-narrow is-3")},m(t,r){u(t,e,r),a(e,n),a(n,o),a(e,l),a(e,c),a(c,i),a(e,s)},p(t,e){1&e&&r!==(r=t[6]+"")&&y(o,r),1&e&&f!==(f=t[7]+"")&&y(i,f)},d(t){t&&d(e)}}}function at(e){let n,o,l,c,i,s,b,k,w,x,L,S,A,_,E,N,O,j,C,P,z,T,M,V,R,I,H,B,q,J,D,U,F,G,W,Z,tt,et,nt,ot=e[0].type+"",at=e[0].id+"",ut=e[0].title+"",dt=e[0].user+"",ft=e[0].updated_at+"",pt=e[0].is_public&&X(),mt=0!==e[0].buttons.length&&Y(e);function gt(t,e){return"en"===t[1]?ct:lt}let ht=gt(e),bt=ht(e);function $t(t,e){return t[2]?st:it}let vt=$t(e),yt=vt(e),kt=Object.entries(e[0].metadata),wt=[];for(let t=0;t<kt.length;t+=1)wt[t]=rt(Q(e,kt,t));return{c(){n=p("div"),o=p("div"),l=p("div"),c=p("div"),i=p("div"),s=p("figure"),b=p("img"),w=h(),x=p("div"),L=p("a"),S=p("span"),A=g(ot),_=g(" #"),E=g(at),N=h(),O=g(ut),j=h(),pt&&pt.c(),P=h(),z=p("p"),T=g(dt),M=h(),V=p("span"),R=g(ft),I=h(),mt&&mt.c(),H=h(),B=p("div"),q=p("button"),bt.c(),J=h(),D=m("svg"),yt.c(),F=h(),G=p("div"),W=p("table"),Z=p("tbody");for(let t=0;t<wt.length;t+=1)wt[t].c();r(b.src,k=K(e[0].img,"full","250,"))||v(b,"src",k),v(b,"alt","Record illustration"),v(s,"class","card image is-96x96 svelte-xqp9nk"),v(i,"class","media-left"),v(S,"class","tag px-2 py-1 mb-1 is-dark is-rounded"),v(L,"href",C=e[0].url),v(L,"class","title is-4 hoverable pt-2 svelte-xqp9nk"),v(V,"class","tag p-1 mb-1"),v(z,"class","subtitle is-6 mb-0 ml-2 pt-2"),v(x,"class","media-content"),v(D,"xmlns","http://www.w3.org/2000/svg"),v(D,"viewBox","0 0 384 512"),v(D,"class","svelte-xqp9nk"),v(q,"class",U="button "+(e[2]?"is-inverted":"")),v(B,"class","media-right"),v(c,"class","media"),v(W,"class","table pl-2 is-fullwidth"),v(G,"class","content"),v(l,"class","card-content"),v(o,"id",tt="block-"+e[0].id),v(o,"class","card"),v(n,"class","block")},m(t,r){u(t,n,r),a(n,o),a(o,l),a(l,c),a(c,i),a(i,s),a(s,b),a(c,w),a(c,x),a(x,L),a(L,S),a(S,A),a(S,_),a(S,E),a(L,N),a(L,O),a(L,j),pt&&pt.m(L,null),a(x,P),a(x,z),a(z,T),a(z,M),a(z,V),a(V,R),a(x,I),mt&&mt.m(x,null),a(c,H),a(c,B),a(B,q),bt.m(q,null),a(q,J),a(q,D),yt.m(D,null),a(l,F),a(l,G),a(G,W),a(W,Z);for(let t=0;t<wt.length;t+=1)wt[t]&&wt[t].m(Z,null);et||(nt=$(q,"click",e[4]),et=!0)},p(t,[e]){if(1&e&&!r(b.src,k=K(t[0].img,"full","250,"))&&v(b,"src",k),1&e&&ot!==(ot=t[0].type+"")&&y(A,ot),1&e&&at!==(at=t[0].id+"")&&y(E,at),1&e&&ut!==(ut=t[0].title+"")&&y(O,ut),t[0].is_public?pt||(pt=X(),pt.c(),pt.m(L,null)):pt&&(pt.d(1),pt=null),1&e&&C!==(C=t[0].url)&&v(L,"href",C),1&e&&dt!==(dt=t[0].user+"")&&y(T,dt),1&e&&ft!==(ft=t[0].updated_at+"")&&y(R,ft),0!==t[0].buttons.length?mt?mt.p(t,e):(mt=Y(t),mt.c(),mt.m(x,null)):mt&&(mt.d(1),mt=null),ht===(ht=gt(t))&&bt?bt.p(t,e):(bt.d(1),bt=ht(t),bt&&(bt.c(),bt.m(q,J))),vt!==(vt=$t(t))&&(yt.d(1),yt=vt(t),yt&&(yt.c(),yt.m(D,null))),4&e&&U!==(U="button "+(t[2]?"is-inverted":""))&&v(q,"class",U),1&e){let n;for(kt=Object.entries(t[0].metadata),n=0;n<kt.length;n+=1){const o=Q(t,kt,n);wt[n]?wt[n].p(o,e):(wt[n]=rt(o),wt[n].c(),wt[n].m(Z,null))}for(;n<wt.length;n+=1)wt[n].d(1);wt.length=kt.length}1&e&&tt!==(tt="block-"+t[0].id)&&v(o,"id",tt)},i:t,o:t,d(t){t&&d(n),pt&&pt.d(),mt&&mt.d(),bt.d(),yt.d(),f(wt,t),et=!1,nt()}}}function ut(t,e,n){let{block:o}=e,{appLang:l}=e,{isSelected:c=!1}=e;const i=x();function s(){i("toggleSelection",{block:o})}return t.$$set=t=>{"block"in t&&n(0,o=t.block),"appLang"in t&&n(1,l=t.appLang),"isSelected"in t&&n(2,c=t.isSelected)},[o,l,c,s,()=>s()]}class dt extends G{constructor(t){super(),F(this,t,ut,at,c,{block:0,appLang:1,isSelected:2})}}function ft(t){localStorage.setItem("documentSet",JSON.stringify(t))}function pt(e){let n,o,l,c,i,s,r,f,m,b,$="en"===e[3]?"Selection":"Sélection";return{c(){n=p("div"),o=p("button"),l=p("span"),c=p("i"),i=h(),s=g($),r=g("\n            ("),f=p("span"),m=g(e[2]),b=g(")"),v(c,"class","fa-solid fa-book-bookmark"),v(f,"id","selection-count"),v(f,"class","svelte-1ifntk3"),v(l,"class","svelte-1ifntk3"),v(o,"id","set-btn"),v(o,"class","button px-5 py-4 is-link js-modal-trigger svelte-1ifntk3"),v(o,"data-target","selection-modal"),k(o,"add-animation",e[0]),k(o,"remove-animation",e[1]),v(n,"class","set-container svelte-1ifntk3")},m(t,e){u(t,n,e),a(n,o),a(o,l),a(l,c),a(l,i),a(l,s),a(l,r),a(l,f),a(f,m),a(l,b)},p(t,[e]){8&e&&$!==($="en"===t[3]?"Selection":"Sélection")&&y(s,$),4&e&&y(m,t[2]),1&e&&k(o,"add-animation",t[0]),2&e&&k(o,"remove-animation",t[1])},i:t,o:t,d(t){t&&d(n)}}}function mt(t,e,n){let{addAnimation:o=!1}=e,{removeAnimation:l=!1}=e,{selectionLength:c=0}=e,{appLang:i="en"}=e;return t.$$set=t=>{"addAnimation"in t&&n(0,o=t.addAnimation),"removeAnimation"in t&&n(1,l=t.removeAnimation),"selectionLength"in t&&n(2,c=t.selectionLength),"appLang"in t&&n(3,i=t.appLang)},[o,l,c,i]}class gt extends G{constructor(t){super(),F(this,t,mt,pt,c,{addAnimation:0,removeAnimation:1,selectionLength:2,appLang:3})}}function ht(e){let n,l,c,i,s,r,f,m,b,k,w,x="en"===e[0]?"Clear selection":"Vider la sélection",L="en"===e[0]?"Save selection":"Sauvegarder la sélection";return{c(){n=p("footer"),l=p("div"),c=p("button"),i=g(x),s=h(),r=p("button"),f=p("i"),m=h(),b=g(L),v(c,"class","button is-link is-light"),v(f,"class","fa-solid fa-floppy-disk"),v(r,"class","button is-link"),v(l,"class","buttons"),v(n,"class","modal-card-foot is-center")},m(t,o){u(t,n,o),a(n,l),a(l,c),a(c,i),a(l,s),a(l,r),a(r,f),a(r,m),a(r,b),k||(w=[$(c,"click",e[2]),$(r,"click",e[3])],k=!0)},p(t,[e]){1&e&&x!==(x="en"===t[0]?"Clear selection":"Vider la sélection")&&y(i,x),1&e&&L!==(L="en"===t[0]?"Save selection":"Sauvegarder la sélection")&&y(b,L)},i:t,o:t,d(t){t&&d(n),k=!1,o(w)}}}function bt(t,e,n){const o=x();function l(t="save"){o("commitSelection",{updateType:t})}let{appLang:c="en"}=e;return t.$$set=t=>{"appLang"in t&&n(0,c=t.appLang)},[c,l,()=>l("clear"),()=>l("save")]}class $t extends G{constructor(t){super(),F(this,t,bt,ht,c,{appLang:0})}}function vt(t,e,n){const o=t.slice();return o[14]=e[n][0],o[15]=e[n][1],o}function yt(t,e,n){const o=t.slice();return o[18]=e[n][0],o[19]=e[n][1],o}function kt(t,e,n){const o=t.slice();return o[22]=e[n],o}function wt(t){let e,n,l=[],c=new Map,i=t[0];const s=t=>t[22].id;for(let e=0;e<i.length;e+=1){let n=kt(t,i,e),o=s(n);c.set(o,l[e]=Lt(o,n))}let r=null;return i.length||(r=xt(t)),{c(){e=p("div");for(let t=0;t<l.length;t+=1)l[t].c();r&&r.c()},m(t,o){u(t,e,o);for(let t=0;t<l.length;t+=1)l[t]&&l[t].m(e,null);r&&r.m(e,null),n=!0},p(t,n){1035&n&&(i=t[0],V(),l=function(t,e,n,l,c,i,s,r,a,u,d,f){let p=t.length,m=i.length,g=p;const h={};for(;g--;)h[t[g].key]=g;const b=[],$=new Map,v=new Map,y=[];for(g=m;g--;){const t=f(c,i,g),o=n(t);let r=s.get(o);r?l&&y.push((()=>r.p(t,e))):(r=u(o,t),r.c()),$.set(o,b[g]=r),o in h&&v.set(o,Math.abs(g-h[o]))}const k=new Set,w=new Set;function x(t){I(t,1),t.m(r,d),s.set(t.key,t),d=t.first,m--}for(;p&&m;){const e=b[m-1],n=t[p-1],o=e.key,l=n.key;e===n?(d=e.first,p--,m--):$.has(l)?!s.has(o)||k.has(o)?x(e):w.has(l)?p--:v.get(o)>v.get(l)?(w.add(o),x(e)):(k.add(l),p--):(a(n,s),p--)}for(;p--;){const e=t[p];$.has(e.key)||a(e,s)}for(;m;)x(b[m-1]);return o(y),b}(l,n,s,1,t,i,c,e,B,Lt,null,kt),R(),!i.length&&r?r.p(t,n):i.length?r&&(r.d(1),r=null):(r=xt(t),r.c(),r.m(e,null)))},i(t){if(!n){for(let t=0;t<i.length;t+=1)I(l[t]);n=!0}},o(t){for(let t=0;t<l.length;t+=1)H(l[t]);n=!1},d(t){t&&d(e);for(let t=0;t<l.length;t+=1)l[t].d();r&&r.d()}}}function xt(t){let e,n,o="en"===t[1]?"No records found":"Aucun document trouvé";return{c(){e=p("p"),n=g(o)},m(t,o){u(t,e,o),a(e,n)},p(t,e){2&e&&o!==(o="en"===t[1]?"No records found":"Aucun document trouvé")&&y(n,o)},d(t){t&&d(e)}}}function Lt(t,e){let n,o,l;return o=new dt({props:{block:e[22],appLang:e[1],isSelected:e[3](e[22])}}),o.$on("toggleSelection",e[10]),{key:t,first:null,c(){n=b(),q(o.$$.fragment),this.first=n},m(t,e){u(t,n,e),J(o,t,e),l=!0},p(t,n){e=t;const l={};1&n&&(l.block=e[22]),2&n&&(l.appLang=e[1]),9&n&&(l.isSelected=e[3](e[22])),o.$set(l)},i(t){l||(I(o.$$.fragment,t),l=!0)},o(t){H(o.$$.fragment,t),l=!1},d(t){t&&d(n),D(o,t)}}}function St(t){let e,n,o,l,c="en"===t[1]?"No documents in selection":"Aucun document sélectionné";return{c(){e=p("tr"),n=p("td"),o=g(c),l=h()},m(t,c){u(t,e,c),a(e,n),a(n,o),a(e,l)},p(t,e){2&e&&c!==(c="en"===t[1]?"No documents in selection":"Aucun document sélectionné")&&y(o,c)},d(t){t&&d(e)}}}function At(t){let e,n,o,l,c="en"===t[1]?"No documents in selection":"Aucun document sélectionné";return{c(){e=p("tr"),n=p("td"),o=g(c),l=h()},m(t,c){u(t,e,c),a(e,n),a(n,o),a(e,l)},p(t,e){2&e&&c!==(c="en"===t[1]?"No documents in selection":"Aucun document sélectionné")&&y(o,c)},d(t){t&&d(e)}}}function _t(t){let e,n,o,l,c,i,s,r,f,m,b,k,w,x,L,S,A=t[18]+"",_=t[19].title+"";function E(){return t[12](t[18],t[14])}return{c(){e=p("tr"),n=p("th"),o=p("span"),l=g("#"),c=g(A),i=h(),s=p("td"),r=p("a"),f=g(_),b=h(),k=p("td"),w=p("button"),x=h(),v(o,"class","tag px-2 py-1 mb-1 is-dark is-rounded"),v(n,"class","is-narrow is-3"),v(r,"href",m=t[19].url),v(r,"target","_blank"),v(w,"class","delete"),v(w,"aria-label","close"),v(k,"class","is-narrow")},m(t,d){u(t,e,d),a(e,n),a(n,o),a(o,l),a(o,c),a(e,i),a(e,s),a(s,r),a(r,f),a(e,b),a(e,k),a(k,w),a(e,x),L||(S=$(w,"click",E),L=!0)},p(e,n){t=e,4&n&&A!==(A=t[18]+"")&&y(c,A),4&n&&_!==(_=t[19].title+"")&&y(f,_),4&n&&m!==(m=t[19].url)&&v(r,"href",m)},d(t){t&&d(e),L=!1,S()}}}function Et(t){let e,n,o,l,c,i,s=t[14]+"",r=Object.entries(t[15]),m=[];for(let e=0;e<r.length;e+=1)m[e]=_t(yt(t,r,e));let b=null;return r.length||(b=At(t)),{c(){e=p("h3"),n=g(s),o=h(),l=p("table"),c=p("tbody");for(let t=0;t<m.length;t+=1)m[t].c();b&&b.c(),i=h(),v(l,"class","table pl-2 is-fullwidth")},m(t,s){u(t,e,s),a(e,n),u(t,o,s),u(t,l,s),a(l,c);for(let t=0;t<m.length;t+=1)m[t]&&m[t].m(c,null);b&&b.m(c,null),a(l,i)},p(t,e){if(4&e&&s!==(s=t[14]+"")&&y(n,s),646&e){let n;for(r=Object.entries(t[15]),n=0;n<r.length;n+=1){const o=yt(t,r,n);m[n]?m[n].p(o,e):(m[n]=_t(o),m[n].c(),m[n].m(c,null))}for(;n<m.length;n+=1)m[n].d(1);m.length=r.length,!r.length&&b?b.p(t,e):r.length?b&&(b.d(1),b=null):(b=At(t),b.c(),b.m(c,null))}},d(t){t&&d(e),t&&d(o),t&&d(l),f(m,t),b&&b.d()}}}function Nt(t){let e,n,o,l,c,i,s,r,m,b,$,k,w,x,L,S,A,_,E,N,O,j,C,P="en"===t[1]?"Selected documents":"Documents sélectionnés";e=new gt({props:{addAnimation:t[4],removeAnimation:t[5],selectionLength:t[6],appLang:t[1]}});let z=0!==t[0].length&&wt(t),T=t[7](t[2]),M=[];for(let e=0;e<T.length;e+=1)M[e]=Et(vt(t,T,e));let B=null;return T.length||(B=St(t)),j=new $t({props:{appLang:t[1]}}),j.$on("commitSelection",t[8]),{c(){q(e.$$.fragment),n=h(),z&&z.c(),o=h(),l=p("div"),c=p("div"),i=h(),s=p("div"),r=p("div"),m=p("div"),b=p("i"),$=h(),k=g(P),w=g("\n                ("),x=p("span"),L=g(t[6]),S=g(")"),A=h(),_=p("button"),E=h(),N=p("section");for(let t=0;t<M.length;t+=1)M[t].c();B&&B.c(),O=h(),q(j.$$.fragment),v(c,"class","modal-background"),v(b,"class","fa-solid fa-book-bookmark"),v(x,"id","selection-count"),v(m,"class","title is-4 mb-0 media-content"),v(_,"class","delete media-left"),v(_,"aria-label","close"),v(r,"class","modal-card-head media mb-0"),v(N,"class","modal-card-body"),v(s,"class","modal-content"),v(l,"id","selection-modal"),v(l,"class","modal fade"),v(l,"tabindex","-1"),v(l,"aria-labelledby","selection-modal-label"),v(l,"aria-hidden","true")},m(t,d){J(e,t,d),u(t,n,d),z&&z.m(t,d),u(t,o,d),u(t,l,d),a(l,c),a(l,i),a(l,s),a(s,r),a(r,m),a(m,b),a(m,$),a(m,k),a(m,w),a(m,x),a(x,L),a(m,S),a(r,A),a(r,_),a(s,E),a(s,N);for(let t=0;t<M.length;t+=1)M[t]&&M[t].m(N,null);B&&B.m(N,null),a(s,O),J(j,s,null),C=!0},p(t,[n]){const l={};if(16&n&&(l.addAnimation=t[4]),32&n&&(l.removeAnimation=t[5]),64&n&&(l.selectionLength=t[6]),2&n&&(l.appLang=t[1]),e.$set(l),0!==t[0].length?z?(z.p(t,n),1&n&&I(z,1)):(z=wt(t),z.c(),I(z,1),z.m(o.parentNode,o)):z&&(V(),H(z,1,1,(()=>{z=null})),R()),(!C||2&n)&&P!==(P="en"===t[1]?"Selected documents":"Documents sélectionnés")&&y(k,P),(!C||64&n)&&y(L,t[6]),646&n){let e;for(T=t[7](t[2]),e=0;e<T.length;e+=1){const o=vt(t,T,e);M[e]?M[e].p(o,n):(M[e]=Et(o),M[e].c(),M[e].m(N,null))}for(;e<M.length;e+=1)M[e].d(1);M.length=T.length,!T.length&&B?B.p(t,n):T.length?B&&(B.d(1),B=null):(B=St(t),B.c(),B.m(N,null))}const c={};2&n&&(c.appLang=t[1]),j.$set(c)},i(t){C||(I(e.$$.fragment,t),I(z),I(j.$$.fragment,t),C=!0)},o(t){H(e.$$.fragment,t),H(z),H(j.$$.fragment,t),C=!1},d(t){D(e,t),t&&d(n),z&&z.d(t),t&&d(o),t&&d(l),f(M,t),B&&B.d(),D(j)}}}function Ot(t,e,n){let o,l,c,i;const s="Regions";let{records:r=[]}=e,{appLang:a="en"}=e,u=JSON.parse(localStorage.getItem("documentSet"))??{};const d=t=>Object.entries(t).filter((([t,e])=>t!==s));function f(t,e){n(2,u=function(t,e,n){const{[e]:o,...l}=t[n];return t[n]=l,ft(t),t}(u,t,e)),n(5,l=!0),setTimeout((()=>n(5,l=!1)),300)}function p(t){n(2,u=function(t,e){return t.hasOwnProperty(e.type)||(t[e.type]=[]),t[e.type]={...t[e.type],[e.id]:e},ft(t),t}(u,t)),n(4,o=!0),setTimeout((()=>n(4,o=!1)),300)}return t.$$set=t=>{"records"in t&&n(0,r=t.records),"appLang"in t&&n(1,a=t.appLang)},t.$$.update=()=>{4&t.$$.dirty&&n(6,c=d(u).reduce(((t,[e,n])=>t+Object.keys(n).length),0)),4&t.$$.dirty&&n(3,i=t=>u[t.type]?.hasOwnProperty(t.id))},n(4,o=!1),n(5,l=!1),[r,a,u,i,o,l,c,d,function(t){const{updateType:e}=t.detail;"clear"===e?n(2,u=function(t,e){return e.map((e=>!t.hasOwnProperty(e)||delete t[e])),ft(t),t}(u,Object.keys(u).filter((t=>t!==s)))):"save"===e&&n(2,u=function(t){return console.log(t),t}(u))},f,function(t){const{block:e}=t.detail;i(e)?f(e.id,e.type):p(e)},s,(t,e)=>f(t,e)]}const jt=(Ct="record-data",document.getElementById(Ct)?JSON.parse(document.getElementById(Ct).textContent):[]);var Ct;APP_LANG;return new class extends G{constructor(t){super(),F(this,t,Ot,Nt,c,{regionsType:11,records:0,appLang:1})}get regionsType(){return this.$$.ctx[11]}}({target:document.getElementById("record-list"),props:{records:jt,regionsType:"Regions"}})}();
//# sourceMappingURL=recordList.js.map

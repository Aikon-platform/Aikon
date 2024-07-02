var recordList=function(){"use strict";function t(){}function e(t){return t()}function n(){return Object.create(null)}function l(t){t.forEach(e)}function o(t){return"function"==typeof t}function c(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}let r,s;function i(t,e){return r||(r=document.createElement("a")),r.href=e,t===r.href}function a(t,e){t.appendChild(e)}function u(t,e,n){t.insertBefore(e,n||null)}function d(t){t.parentNode&&t.parentNode.removeChild(t)}function f(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function p(t){return document.createElement(t)}function m(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function g(t){return document.createTextNode(t)}function h(){return g(" ")}function b(){return g("")}function $(t,e,n,l){return t.addEventListener(e,n,l),()=>t.removeEventListener(e,n,l)}function y(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function v(t,e){e=""+e,t.data!==e&&(t.data=e)}function k(t){s=t}function x(){const t=function(){if(!s)throw new Error("Function called outside component initialization");return s}();return(e,n,{cancelable:l=!1}={})=>{const o=t.$$.callbacks[e];if(o){const c=function(t,e,{bubbles:n=!1,cancelable:l=!1}={}){const o=document.createEvent("CustomEvent");return o.initCustomEvent(t,n,l,e),o}(e,n,{cancelable:l});return o.slice().forEach((e=>{e.call(t,c)})),!c.defaultPrevented}return!0}}const w=[],L=[];let S=[];const _=[],A=Promise.resolve();let E=!1;function N(t){S.push(t)}const O=new Set;let j=0;function z(){if(0!==j)return;const t=s;do{try{for(;j<w.length;){const t=w[j];j++,k(t),C(t.$$)}}catch(t){throw w.length=0,j=0,t}for(k(null),w.length=0,j=0;L.length;)L.pop()();for(let t=0;t<S.length;t+=1){const e=S[t];O.has(e)||(O.add(e),e())}S.length=0}while(w.length);for(;_.length;)_.pop()();E=!1,O.clear(),k(t)}function C(t){if(null!==t.fragment){t.update(),l(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(N)}}const P=new Set;let M;function T(){M={r:0,c:[],p:M}}function V(){M.r||l(M.c),M=M.p}function I(t,e){t&&t.i&&(P.delete(t),t.i(e))}function R(t,e,n,l){if(t&&t.o){if(P.has(t))return;P.add(t),M.c.push((()=>{P.delete(t),l&&(n&&t.d(1),l())})),t.o(e)}else l&&l()}function B(t,e){R(t,1,1,(()=>{e.delete(t.key)}))}function H(t){t&&t.c()}function q(t,n,c,r){const{fragment:s,after_update:i}=t.$$;s&&s.m(n,c),r||N((()=>{const n=t.$$.on_mount.map(e).filter(o);t.$$.on_destroy?t.$$.on_destroy.push(...n):l(n),t.$$.on_mount=[]})),i.forEach(N)}function J(t,e){const n=t.$$;null!==n.fragment&&(!function(t){const e=[],n=[];S.forEach((l=>-1===t.indexOf(l)?e.push(l):n.push(l))),n.forEach((t=>t())),S=e}(n.after_update),l(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function D(t,e){-1===t.$$.dirty[0]&&(w.push(t),E||(E=!0,A.then(z)),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}function U(e,o,c,r,i,a,u,f=[-1]){const p=s;k(e);const m=e.$$={fragment:null,ctx:[],props:a,update:t,not_equal:i,bound:n(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(o.context||(p?p.$$.context:[])),callbacks:n(),dirty:f,skip_bound:!1,root:o.target||p.$$.root};u&&u(m.root);let g=!1;if(m.ctx=c?c(e,o.props||{},((t,n,...l)=>{const o=l.length?l[0]:n;return m.ctx&&i(m.ctx[t],m.ctx[t]=o)&&(!m.skip_bound&&m.bound[t]&&m.bound[t](o),g&&D(e,t)),n})):[],m.update(),g=!0,l(m.before_update),m.fragment=!!r&&r(m.ctx),o.target){if(o.hydrate){const t=function(t){return Array.from(t.childNodes)}(o.target);m.fragment&&m.fragment.l(t),t.forEach(d)}else m.fragment&&m.fragment.c();o.intro&&I(e.$$.fragment),q(e,o.target,o.anchor,o.customElement),z()}k(p)}class X{$destroy(){J(this,1),this.$destroy=t}$on(e,n){if(!o(n))return t;const l=this.$$.callbacks[e]||(this.$$.callbacks[e]=[]);return l.push(n),()=>{const t=l.indexOf(n);-1!==t&&l.splice(t,1)}}$set(t){var e;this.$$set&&(e=t,0!==Object.keys(e).length)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}function Y(t=null,e="full",n="full"){if(!t)return"https://via.placeholder.com/96x96?text=No+Image";if((t=t.split("_")).length<3)return"https://via.placeholder.com/96x96?text=No+Image";const l=t[t.length-1].includes(",")?t.pop().replace(".jpg",""):e,o=t.join("_").replace(".jpg","");return`${CANTALOUPE_APP_URL??"http://localhost:8182"}/iiif/2/${o}.jpg/${l}/${n}/0/default.jpg`}function F(t,e,n){const l=t.slice();return l[6]=e[n][0],l[7]=e[n][1],l}function G(t,e,n){const l=t.slice();return l[10]=e[n],l}function K(t){let e;return{c(){e=p("span"),e.innerHTML='<span class="icon has-text-success"><i class="fas fa-check-circle"></i></span> \n                                <span style="margin-left: -0.5rem">Public</span>',y(e,"class","pl-3 icon-text is-size-7 is-center has-text-weight-normal")},m(t,n){u(t,e,n)},d(t){t&&d(e)}}}function Q(t){let e,n,l,o,c=t[0].hasOwnProperty("iiif"),r=t[0].buttons.includes("regions"),s=t[0].buttons.includes("similarity"),i=t[0].buttons.includes("vectorization"),f=c&&W(t),m=r&&tt(t),g=s&&et(t),b=i&&nt(t);return{c(){e=p("p"),f&&f.c(),n=h(),m&&m.c(),l=h(),g&&g.c(),o=h(),b&&b.c(),y(e,"class","subtitle is-6 mb-0 ml-2 pt-2")},m(t,c){u(t,e,c),f&&f.m(e,null),a(e,n),m&&m.m(e,null),a(e,l),g&&g.m(e,null),a(e,o),b&&b.m(e,null)},p(t,a){1&a&&(c=t[0].hasOwnProperty("iiif")),c?f?f.p(t,a):(f=W(t),f.c(),f.m(e,n)):f&&(f.d(1),f=null),1&a&&(r=t[0].buttons.includes("regions")),r?m?m.p(t,a):(m=tt(t),m.c(),m.m(e,l)):m&&(m.d(1),m=null),1&a&&(s=t[0].buttons.includes("similarity")),s?g?g.p(t,a):(g=et(t),g.c(),g.m(e,o)):g&&(g.d(1),g=null),1&a&&(i=t[0].buttons.includes("vectorization")),i?b?b.p(t,a):(b=nt(t),b.c(),b.m(e,null)):b&&(b.d(1),b=null)},d(t){t&&d(e),f&&f.d(),m&&m.d(),g&&g.d(),b&&b.d()}}}function W(t){let e,n=t[0].iiif,l=[];for(let e=0;e<n.length;e+=1)l[e]=Z(G(t,n,e));return{c(){for(let t=0;t<l.length;t+=1)l[t].c();e=b()},m(t,n){for(let e=0;e<l.length;e+=1)l[e]&&l[e].m(t,n);u(t,e,n)},p(t,o){if(1&o){let c;for(n=t[0].iiif,c=0;c<n.length;c+=1){const r=G(t,n,c);l[c]?l[c].p(r,o):(l[c]=Z(r),l[c].c(),l[c].m(e.parentNode,e))}for(;c<l.length;c+=1)l[c].d(1);l.length=n.length}},d(t){f(l,t),t&&d(e)}}}function Z(t){let e,n=t[10]+"";return{c(){e=p("span"),y(e,"class","tag logo mt-1")},m(t,l){u(t,e,l),e.innerHTML=n},p(t,l){1&l&&n!==(n=t[10]+"")&&(e.innerHTML=n)},d(t){t&&d(e)}}}function tt(t){let e,n,l,o;return{c(){e=p("a"),n=p("span"),y(n,"class","iconify"),y(n,"data-icon","entypo:documents"),y(e,"href",l=t[0].url+"regions/"),y(e,"class","button is-small is-rounded is-link px-2"),y(e,"title",o="en"===t[1]?"Show extracted regions":"Afficher les zones d'images")},m(t,l){u(t,e,l),a(e,n)},p(t,n){1&n&&l!==(l=t[0].url+"regions/")&&y(e,"href",l),2&n&&o!==(o="en"===t[1]?"Show extracted regions":"Afficher les zones d'images")&&y(e,"title",o)},d(t){t&&d(e)}}}function et(t){let e,n,l,o;return{c(){e=p("a"),n=p("span"),y(n,"class","iconify"),y(n,"data-icon","octicon:mirror-16"),y(e,"href",l=t[0].url+"similarity/"),y(e,"class","button is-small is-rounded is-link px-2"),y(e,"title",o="en"===t[1]?"Show similarity":"Afficher les similarités")},m(t,l){u(t,e,l),a(e,n)},p(t,n){1&n&&l!==(l=t[0].url+"similarity/")&&y(e,"href",l),2&n&&o!==(o="en"===t[1]?"Show similarity":"Afficher les similarités")&&y(e,"title",o)},d(t){t&&d(e)}}}function nt(t){let e,n,l,o;return{c(){e=p("a"),n=p("span"),y(n,"class","iconify"),y(n,"data-icon","arcticons:geogebra-geometry"),y(e,"href",l=t[0].url+"vectorization/"),y(e,"class","button is-small is-rounded is-link px-2"),y(e,"title",o="en"===t[1]?"Show vectorizations":"Afficher les vectorisations")},m(t,l){u(t,e,l),a(e,n)},p(t,n){1&n&&l!==(l=t[0].url+"vectorization/")&&y(e,"href",l),2&n&&o!==(o="en"===t[1]?"Show vectorizations":"Afficher les vectorisations")&&y(e,"title",o)},d(t){t&&d(e)}}}function lt(t){let e,n,l=t[2]?"Retirer de":"Ajouter à la";return{c(){e=g(l),n=g(" sélection")},m(t,l){u(t,e,l),u(t,n,l)},p(t,n){4&n&&l!==(l=t[2]?"Retirer de":"Ajouter à la")&&v(e,l)},d(t){t&&d(e),t&&d(n)}}}function ot(t){let e,n,l=t[2]?"Remove from":"Add to";return{c(){e=g(l),n=g(" set")},m(t,l){u(t,e,l),u(t,n,l)},p(t,n){4&n&&l!==(l=t[2]?"Remove from":"Add to")&&v(e,l)},d(t){t&&d(e),t&&d(n)}}}function ct(t){let e;return{c(){e=m("path"),y(e,"fill","currentColor"),y(e,"d","M0 48C0 21.5 21.5 0 48 0l0 48V441.4l130.1-92.9c8.3-6 19.6-6 27.9 0L336 441.4V48H48V0H336c26.5 0 48 21.5 48 48V488c0 9-5 17.2-13 21.3s-17.6 3.4-24.9-1.8L192 397.5 37.9 507.5c-7.3 5.2-16.9 5.9-24.9 1.8S0 497 0 488V48z")},m(t,n){u(t,e,n)},d(t){t&&d(e)}}}function rt(t){let e;return{c(){e=m("path"),y(e,"fill","currentColor"),y(e,"d","M0 48V487.7C0 501.1 10.9 512 24.3 512c5 0 9.9-1.5 14-4.4L192 400 345.7 507.6c4.1 2.9 9 4.4 14 4.4c13.4 0 24.3-10.9 24.3-24.3V48c0-26.5-21.5-48-48-48H48C21.5 0 0 21.5 0 48z")},m(t,n){u(t,e,n)},d(t){t&&d(e)}}}function st(t){let e,n,l,o,c,r,s,i=t[6]+"",f=t[7]+"";return{c(){e=p("tr"),n=p("th"),l=g(i),o=h(),c=p("td"),r=g(f),s=h(),y(n,"class","is-narrow is-3")},m(t,i){u(t,e,i),a(e,n),a(n,l),a(e,o),a(e,c),a(c,r),a(e,s)},p(t,e){1&e&&i!==(i=t[6]+"")&&v(l,i),1&e&&f!==(f=t[7]+"")&&v(r,f)},d(t){t&&d(e)}}}function it(e){let n,l,o,c,r,s,b,k,x,w,L,S,_,A,E,N,O,j,z,C,P,M,T,V,I,R,B,H,q,J,D,U,X,G,W,Z,tt,et,nt,it=e[0].type+"",at=e[0].id+"",ut=e[0].title+"",dt=e[0].user+"",ft=e[0].updated_at+"",pt=e[0].is_public&&K(),mt=0!==e[0].buttons.length&&Q(e);function gt(t,e){return"en"===t[1]?ot:lt}let ht=gt(e),bt=ht(e);function $t(t,e){return t[2]?rt:ct}let yt=$t(e),vt=yt(e),kt=Object.entries(e[0].metadata),xt=[];for(let t=0;t<kt.length;t+=1)xt[t]=st(F(e,kt,t));return{c(){n=p("div"),l=p("div"),o=p("div"),c=p("div"),r=p("div"),s=p("figure"),b=p("img"),x=h(),w=p("div"),L=p("a"),S=p("span"),_=g(it),A=g(" #"),E=g(at),N=h(),O=g(ut),j=h(),pt&&pt.c(),C=h(),P=p("p"),M=g(dt),T=h(),V=p("span"),I=g(ft),R=h(),mt&&mt.c(),B=h(),H=p("div"),q=p("button"),bt.c(),J=h(),D=m("svg"),vt.c(),X=h(),G=p("div"),W=p("table"),Z=p("tbody");for(let t=0;t<xt.length;t+=1)xt[t].c();i(b.src,k=Y(e[0].img,"full","250,"))||y(b,"src",k),y(b,"alt","Record illustration"),y(s,"class","card image is-96x96 svelte-xqp9nk"),y(r,"class","media-left"),y(S,"class","tag px-2 py-1 mb-1 is-dark is-rounded"),y(L,"href",z=e[0].url),y(L,"class","title is-4 hoverable pt-2 svelte-xqp9nk"),y(V,"class","tag p-1 mb-1"),y(P,"class","subtitle is-6 mb-0 ml-2 pt-2"),y(w,"class","media-content"),y(D,"xmlns","http://www.w3.org/2000/svg"),y(D,"viewBox","0 0 384 512"),y(D,"class","svelte-xqp9nk"),y(q,"class",U="button "+(e[2]?"is-inverted":"")),y(H,"class","media-right"),y(c,"class","media"),y(W,"class","table pl-2 is-fullwidth"),y(G,"class","content"),y(o,"class","card-content"),y(l,"id",tt="block-"+e[0].id),y(l,"class","card"),y(n,"class","block")},m(t,i){u(t,n,i),a(n,l),a(l,o),a(o,c),a(c,r),a(r,s),a(s,b),a(c,x),a(c,w),a(w,L),a(L,S),a(S,_),a(S,A),a(S,E),a(L,N),a(L,O),a(L,j),pt&&pt.m(L,null),a(w,C),a(w,P),a(P,M),a(P,T),a(P,V),a(V,I),a(w,R),mt&&mt.m(w,null),a(c,B),a(c,H),a(H,q),bt.m(q,null),a(q,J),a(q,D),vt.m(D,null),a(o,X),a(o,G),a(G,W),a(W,Z);for(let t=0;t<xt.length;t+=1)xt[t]&&xt[t].m(Z,null);et||(nt=$(q,"click",e[4]),et=!0)},p(t,[e]){if(1&e&&!i(b.src,k=Y(t[0].img,"full","250,"))&&y(b,"src",k),1&e&&it!==(it=t[0].type+"")&&v(_,it),1&e&&at!==(at=t[0].id+"")&&v(E,at),1&e&&ut!==(ut=t[0].title+"")&&v(O,ut),t[0].is_public?pt||(pt=K(),pt.c(),pt.m(L,null)):pt&&(pt.d(1),pt=null),1&e&&z!==(z=t[0].url)&&y(L,"href",z),1&e&&dt!==(dt=t[0].user+"")&&v(M,dt),1&e&&ft!==(ft=t[0].updated_at+"")&&v(I,ft),0!==t[0].buttons.length?mt?mt.p(t,e):(mt=Q(t),mt.c(),mt.m(w,null)):mt&&(mt.d(1),mt=null),ht===(ht=gt(t))&&bt?bt.p(t,e):(bt.d(1),bt=ht(t),bt&&(bt.c(),bt.m(q,J))),yt!==(yt=$t(t))&&(vt.d(1),vt=yt(t),vt&&(vt.c(),vt.m(D,null))),4&e&&U!==(U="button "+(t[2]?"is-inverted":""))&&y(q,"class",U),1&e){let n;for(kt=Object.entries(t[0].metadata),n=0;n<kt.length;n+=1){const l=F(t,kt,n);xt[n]?xt[n].p(l,e):(xt[n]=st(l),xt[n].c(),xt[n].m(Z,null))}for(;n<xt.length;n+=1)xt[n].d(1);xt.length=kt.length}1&e&&tt!==(tt="block-"+t[0].id)&&y(l,"id",tt)},i:t,o:t,d(t){t&&d(n),pt&&pt.d(),mt&&mt.d(),bt.d(),vt.d(),f(xt,t),et=!1,nt()}}}function at(t,e,n){let{block:l}=e,{appLang:o}=e,{isSelected:c=!1}=e;const r=x();function s(){r("toggleSelection",{block:l})}return t.$$set=t=>{"block"in t&&n(0,l=t.block),"appLang"in t&&n(1,o=t.appLang),"isSelected"in t&&n(2,c=t.isSelected)},[l,o,c,s,()=>s()]}class ut extends X{constructor(t){super(),U(this,t,at,it,c,{block:0,appLang:1,isSelected:2})}}function dt(t){localStorage.setItem("documentSet",JSON.stringify(t))}function ft(e){let n,l,o,c,r,s,i,f,m,b="en"===e[1]?"Selection":"Sélection";return{c(){n=p("div"),l=p("button"),o=p("span"),c=p("i"),r=h(),s=g(b),i=g("\n            ("),f=g(e[0]),m=g(")"),y(c,"class","fa-solid fa-book-bookmark"),y(o,"id","btn-content"),y(l,"id","set-btn"),y(l,"class","button px-5 py-4 is-link js-modal-trigger svelte-hs48f9"),y(l,"data-target","selection-modal"),y(n,"class","set-container svelte-hs48f9")},m(t,e){u(t,n,e),a(n,l),a(l,o),a(o,c),a(o,r),a(o,s),a(o,i),a(o,f),a(o,m)},p(t,[e]){2&e&&b!==(b="en"===t[1]?"Selection":"Sélection")&&v(s,b),1&e&&v(f,t[0])},i:t,o:t,d(t){t&&d(n)}}}function pt(t,e,n){let{selectionLength:l=0}=e,{appLang:o="en"}=e,c=l;return t.$$set=t=>{"selectionLength"in t&&n(0,l=t.selectionLength),"appLang"in t&&n(1,o=t.appLang)},t.$$.update=()=>{if(5&t.$$.dirty&&l!==c){const t=l>c;n(2,c=l);const e=document.getElementById("btn-content");e&&e.animate([{transform:t?"translateY(-7px)":"translateX(-5px)"},{transform:t?"translateY(7px)":"translateX(5px)"},{transform:"translate(0)"}],{duration:300,easing:"cubic-bezier(0.65, 0, 0.35, 1)"})}},[l,o,c]}class mt extends X{constructor(t){super(),U(this,t,pt,ft,c,{selectionLength:0,appLang:1})}}function gt(e){let n,o,c,r,s,i,f,m,b,k,x,w="en"===e[0]?"Clear selection":"Vider la sélection",L="en"===e[0]?"Save selection":"Sauvegarder la sélection";return{c(){n=p("footer"),o=p("div"),c=p("button"),r=g(w),s=h(),i=p("button"),f=p("i"),m=h(),b=g(L),y(c,"class","button is-link is-light"),y(f,"class","fa-solid fa-floppy-disk"),y(i,"class","button is-link"),y(o,"class","buttons"),y(n,"class","modal-card-foot is-center")},m(t,l){u(t,n,l),a(n,o),a(o,c),a(c,r),a(o,s),a(o,i),a(i,f),a(i,m),a(i,b),k||(x=[$(c,"click",e[2]),$(i,"click",e[3])],k=!0)},p(t,[e]){1&e&&w!==(w="en"===t[0]?"Clear selection":"Vider la sélection")&&v(r,w),1&e&&L!==(L="en"===t[0]?"Save selection":"Sauvegarder la sélection")&&v(b,L)},i:t,o:t,d(t){t&&d(n),k=!1,l(x)}}}function ht(t,e,n){const l=x();function o(t="save"){l("commitSelection",{updateType:t})}let{appLang:c="en"}=e;return t.$$set=t=>{"appLang"in t&&n(0,c=t.appLang)},[c,o,()=>o("clear"),()=>o("save")]}class bt extends X{constructor(t){super(),U(this,t,ht,gt,c,{appLang:0})}}function $t(t,e,n){const l=t.slice();return l[12]=e[n][0],l[13]=e[n][1],l}function yt(t,e,n){const l=t.slice();return l[16]=e[n][0],l[17]=e[n][1],l}function vt(t,e,n){const l=t.slice();return l[20]=e[n],l}function kt(t){let e,n,o=[],c=new Map,r=t[0];const s=t=>t[20].id;for(let e=0;e<r.length;e+=1){let n=vt(t,r,e),l=s(n);c.set(l,o[e]=wt(l,n))}let i=null;return r.length||(i=xt(t)),{c(){e=p("div");for(let t=0;t<o.length;t+=1)o[t].c();i&&i.c()},m(t,l){u(t,e,l);for(let t=0;t<o.length;t+=1)o[t]&&o[t].m(e,null);i&&i.m(e,null),n=!0},p(t,n){267&n&&(r=t[0],T(),o=function(t,e,n,o,c,r,s,i,a,u,d,f){let p=t.length,m=r.length,g=p;const h={};for(;g--;)h[t[g].key]=g;const b=[],$=new Map,y=new Map,v=[];for(g=m;g--;){const t=f(c,r,g),l=n(t);let i=s.get(l);i?o&&v.push((()=>i.p(t,e))):(i=u(l,t),i.c()),$.set(l,b[g]=i),l in h&&y.set(l,Math.abs(g-h[l]))}const k=new Set,x=new Set;function w(t){I(t,1),t.m(i,d),s.set(t.key,t),d=t.first,m--}for(;p&&m;){const e=b[m-1],n=t[p-1],l=e.key,o=n.key;e===n?(d=e.first,p--,m--):$.has(o)?!s.has(l)||k.has(l)?w(e):x.has(o)?p--:y.get(l)>y.get(o)?(x.add(l),w(e)):(k.add(o),p--):(a(n,s),p--)}for(;p--;){const e=t[p];$.has(e.key)||a(e,s)}for(;m;)w(b[m-1]);return l(v),b}(o,n,s,1,t,r,c,e,B,wt,null,vt),V(),!r.length&&i?i.p(t,n):r.length?i&&(i.d(1),i=null):(i=xt(t),i.c(),i.m(e,null)))},i(t){if(!n){for(let t=0;t<r.length;t+=1)I(o[t]);n=!0}},o(t){for(let t=0;t<o.length;t+=1)R(o[t]);n=!1},d(t){t&&d(e);for(let t=0;t<o.length;t+=1)o[t].d();i&&i.d()}}}function xt(t){let e,n,l="en"===t[1]?"No records found":"Aucun document trouvé";return{c(){e=p("p"),n=g(l)},m(t,l){u(t,e,l),a(e,n)},p(t,e){2&e&&l!==(l="en"===t[1]?"No records found":"Aucun document trouvé")&&v(n,l)},d(t){t&&d(e)}}}function wt(t,e){let n,l,o;return l=new ut({props:{block:e[20],appLang:e[1],isSelected:e[3](e[20])}}),l.$on("toggleSelection",e[8]),{key:t,first:null,c(){n=b(),H(l.$$.fragment),this.first=n},m(t,e){u(t,n,e),q(l,t,e),o=!0},p(t,n){e=t;const o={};1&n&&(o.block=e[20]),2&n&&(o.appLang=e[1]),9&n&&(o.isSelected=e[3](e[20])),l.$set(o)},i(t){o||(I(l.$$.fragment,t),o=!0)},o(t){R(l.$$.fragment,t),o=!1},d(t){t&&d(n),J(l,t)}}}function Lt(t){let e,n,l,o,c="en"===t[1]?"No documents in selection":"Aucun document sélectionné";return{c(){e=p("tr"),n=p("td"),l=g(c),o=h()},m(t,c){u(t,e,c),a(e,n),a(n,l),a(e,o)},p(t,e){2&e&&c!==(c="en"===t[1]?"No documents in selection":"Aucun document sélectionné")&&v(l,c)},d(t){t&&d(e)}}}function St(t){let e,n,l,o,c="en"===t[1]?"No documents in selection":"Aucun document sélectionné";return{c(){e=p("tr"),n=p("td"),l=g(c),o=h()},m(t,c){u(t,e,c),a(e,n),a(n,l),a(e,o)},p(t,e){2&e&&c!==(c="en"===t[1]?"No documents in selection":"Aucun document sélectionné")&&v(l,c)},d(t){t&&d(e)}}}function _t(t){let e,n,l,o,c,r,s,i,f,m,b,k,x,w,L,S,_=t[16]+"",A=t[17].title+"";function E(){return t[10](t[16],t[12])}return{c(){e=p("tr"),n=p("th"),l=p("span"),o=g("#"),c=g(_),r=h(),s=p("td"),i=p("a"),f=g(A),b=h(),k=p("td"),x=p("button"),w=h(),y(l,"class","tag px-2 py-1 mb-1 is-dark is-rounded"),y(n,"class","is-narrow is-3"),y(i,"href",m=t[17].url),y(i,"target","_blank"),y(x,"class","delete"),y(x,"aria-label","close"),y(k,"class","is-narrow")},m(t,d){u(t,e,d),a(e,n),a(n,l),a(l,o),a(l,c),a(e,r),a(e,s),a(s,i),a(i,f),a(e,b),a(e,k),a(k,x),a(e,w),L||(S=$(x,"click",E),L=!0)},p(e,n){t=e,4&n&&_!==(_=t[16]+"")&&v(c,_),4&n&&A!==(A=t[17].title+"")&&v(f,A),4&n&&m!==(m=t[17].url)&&y(i,"href",m)},d(t){t&&d(e),L=!1,S()}}}function At(t){let e,n,l,o,c,r,s=t[12]+"",i=Object.entries(t[13]),m=[];for(let e=0;e<i.length;e+=1)m[e]=_t(yt(t,i,e));let b=null;return i.length||(b=St(t)),{c(){e=p("h3"),n=g(s),l=h(),o=p("table"),c=p("tbody");for(let t=0;t<m.length;t+=1)m[t].c();b&&b.c(),r=h(),y(o,"class","table pl-2 is-fullwidth")},m(t,s){u(t,e,s),a(e,n),u(t,l,s),u(t,o,s),a(o,c);for(let t=0;t<m.length;t+=1)m[t]&&m[t].m(c,null);b&&b.m(c,null),a(o,r)},p(t,e){if(4&e&&s!==(s=t[12]+"")&&v(n,s),166&e){let n;for(i=Object.entries(t[13]),n=0;n<i.length;n+=1){const l=yt(t,i,n);m[n]?m[n].p(l,e):(m[n]=_t(l),m[n].c(),m[n].m(c,null))}for(;n<m.length;n+=1)m[n].d(1);m.length=i.length,!i.length&&b?b.p(t,e):i.length?b&&(b.d(1),b=null):(b=St(t),b.c(),b.m(c,null))}},d(t){t&&d(e),t&&d(l),t&&d(o),f(m,t),b&&b.d()}}}function Et(t){let e,n,l,o,c,r,s,i,m,b,$,k,x,w,L,S,_,A,E,N,O,j,z="en"===t[1]?"Selected documents":"Documents sélectionnés";e=new mt({props:{selectionLength:t[4],appLang:t[1]}});let C=0!==t[0].length&&kt(t),P=t[5](t[2]),M=[];for(let e=0;e<P.length;e+=1)M[e]=At($t(t,P,e));let B=null;return P.length||(B=Lt(t)),O=new bt({props:{appLang:t[1]}}),O.$on("commitSelection",t[6]),{c(){H(e.$$.fragment),n=h(),C&&C.c(),l=h(),o=p("div"),c=p("div"),r=h(),s=p("div"),i=p("div"),m=p("div"),b=p("i"),$=h(),k=g(z),x=g("\n                ("),w=g(t[4]),L=g(")"),S=h(),_=p("button"),A=h(),E=p("section");for(let t=0;t<M.length;t+=1)M[t].c();B&&B.c(),N=h(),H(O.$$.fragment),y(c,"class","modal-background"),y(b,"class","fa-solid fa-book-bookmark"),y(m,"class","title is-4 mb-0 media-content"),y(_,"class","delete media-left"),y(_,"aria-label","close"),y(i,"class","modal-card-head media mb-0"),y(E,"class","modal-card-body"),y(s,"class","modal-content"),y(o,"id","selection-modal"),y(o,"class","modal fade"),y(o,"tabindex","-1"),y(o,"aria-labelledby","selection-modal-label"),y(o,"aria-hidden","true")},m(t,d){q(e,t,d),u(t,n,d),C&&C.m(t,d),u(t,l,d),u(t,o,d),a(o,c),a(o,r),a(o,s),a(s,i),a(i,m),a(m,b),a(m,$),a(m,k),a(m,x),a(m,w),a(m,L),a(i,S),a(i,_),a(s,A),a(s,E);for(let t=0;t<M.length;t+=1)M[t]&&M[t].m(E,null);B&&B.m(E,null),a(s,N),q(O,s,null),j=!0},p(t,[n]){const o={};if(16&n&&(o.selectionLength=t[4]),2&n&&(o.appLang=t[1]),e.$set(o),0!==t[0].length?C?(C.p(t,n),1&n&&I(C,1)):(C=kt(t),C.c(),I(C,1),C.m(l.parentNode,l)):C&&(T(),R(C,1,1,(()=>{C=null})),V()),(!j||2&n)&&z!==(z="en"===t[1]?"Selected documents":"Documents sélectionnés")&&v(k,z),(!j||16&n)&&v(w,t[4]),166&n){let e;for(P=t[5](t[2]),e=0;e<P.length;e+=1){const l=$t(t,P,e);M[e]?M[e].p(l,n):(M[e]=At(l),M[e].c(),M[e].m(E,null))}for(;e<M.length;e+=1)M[e].d(1);M.length=P.length,!P.length&&B?B.p(t,n):P.length?B&&(B.d(1),B=null):(B=Lt(t),B.c(),B.m(E,null))}const c={};2&n&&(c.appLang=t[1]),O.$set(c)},i(t){j||(I(e.$$.fragment,t),I(C),I(O.$$.fragment,t),j=!0)},o(t){R(e.$$.fragment,t),R(C),R(O.$$.fragment,t),j=!1},d(t){J(e,t),t&&d(n),C&&C.d(t),t&&d(l),t&&d(o),f(M,t),B&&B.d(),J(O)}}}function Nt(t,e,n){let l,o;const c="Regions";let{records:r=[]}=e,{appLang:s="en"}=e,i=JSON.parse(localStorage.getItem("documentSet"))??{};const a=t=>Object.entries(t).filter((([t,e])=>t!==c));function u(t,e){n(2,i=function(t,e,n){console.log("coucou");const{[e]:l,...o}=t[n];return t[n]=o,dt(t),t}(i,t,e))}function d(t){n(2,i=function(t,e){return t.hasOwnProperty(e.type)||(t[e.type]=[]),t[e.type]={...t[e.type],[e.id]:e},dt(t),t}(i,t))}return t.$$set=t=>{"records"in t&&n(0,r=t.records),"appLang"in t&&n(1,s=t.appLang)},t.$$.update=()=>{4&t.$$.dirty&&n(4,l=a(i).reduce(((t,[e,n])=>t+Object.keys(n).length),0)),4&t.$$.dirty&&n(3,o=t=>i[t.type]?.hasOwnProperty(t.id))},[r,s,i,o,l,a,function(t){const{updateType:e}=t.detail;"clear"===e?n(2,i=function(t,e){return e.map((e=>!t.hasOwnProperty(e)||delete t[e])),dt(t),t}(i,Object.keys(i).filter((t=>t!==c)))):"save"===e&&n(2,i=function(t){return console.log(t),t}(i))},u,function(t){const{block:e}=t.detail;o(e)?u(e.id,e.type):d(e)},c,(t,e)=>u(t,e)]}const Ot=(jt="record-data",document.getElementById(jt)?JSON.parse(document.getElementById(jt).textContent):[]);var jt;APP_LANG;return new class extends X{constructor(t){super(),U(this,t,Nt,Et,c,{regionsType:9,records:0,appLang:1})}get regionsType(){return this.$$.ctx[9]}}({target:document.getElementById("record-list"),props:{records:Ot,regionsType:"Regions"}})}();
//# sourceMappingURL=recordList.js.map

"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9136],{27957:function(e,t,n){n.d(t,{Gm:function(){return C},Kn:function(){return b},L8:function(){return y},O3:function(){return f},Qs:function(){return _},Yc:function(){return g},bQ:function(){return m},dY:function(){return v},iR:function(){return w},ou:function(){return x},u0:function(){return h}});var a=n(91014),r=n(89992),o=n(88075),i=n(65490),l=n(49793),s=n(26821),u=n(10751),c=n.n(u),d=n(7653),p=n(69602);let f=function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},{activeOrganization:t}=(0,o.t)(),{defer:n}=e,a=(0,p.U)(),i=null==t?void 0:t.uuid;return(0,r.WE)("/api/organizations/".concat(i,"/projects"),{queryKey:[l.gi,{orgUuid:i}],enabled:!n&&!!(t&&a),staleTime:0,select:e=>e.filter(e=>!e.archived_at)})},m=()=>{let{data:e,isLoading:t}=f();return{data:null==e?void 0:e.filter(e=>e.is_starred),isLoading:t}},h=()=>{let{data:e,isLoading:t}=(0,a.QR)(),{data:n,isLoading:r}=f();return(0,d.useMemo)(()=>{if(t||r)return{data:n,isLoading:!0};if(!n||!e)return{data:n,isLoading:!1};let a=n.map(t=>({...t,lastConversation:null==e?void 0:e.find(e=>e.project_uuid===t.uuid)})).filter(e=>e.lastConversation).sort((e,t)=>new Date(t.lastConversation.created_at).getTime()-new Date(e.lastConversation.created_at).getTime()),o=null==n?void 0:n.filter(e=>!a.find(t=>t.uuid===e.uuid));return{data:[...a,...o],isLoading:!1}},[n,e,t,r])},g=e=>{let{activeOrganization:t}=(0,o.t)(),n=null==t?void 0:t.uuid;return(0,r.WE)("/api/organizations/".concat(n,"/projects/").concat(e),{queryKey:[l.$T,{orgUuid:n,projectUuid:e}],enabled:!!(t&&e),staleTime:0,meta:{noToast:e=>e instanceof i.Hx&&404===e.statusCode}})},_=()=>{let{activeOrganization:e}=(0,o.t)(),t=null==e?void 0:e.uuid,n=(0,s.useQueryClient)();return(0,r.uC)(()=>"/api/organizations/".concat(t,"/projects"),"POST",{onSuccess:()=>{n.invalidateQueries({queryKey:[l.gi,{orgUuid:t}]}),n.invalidateQueries({queryKey:[l.n$,{orgUuid:t}]})}})},v=e=>{let{activeOrganization:t}=(0,o.t)(),n=null==t?void 0:t.uuid,a=C();return(0,r.Ne)(()=>"/api/organizations/".concat(n,"/projects/").concat(e),"PUT",(e,t)=>t?{...t,...e}:void 0,{onSuccess:()=>{a(e)},queryKey:[l.$T,{orgUuid:n,projectUuid:e}]})},y=e=>{let{activeOrganization:t}=(0,o.t)(),n=null==t?void 0:t.uuid,a=C();return(0,r.uC)(()=>"/api/organizations/".concat(n,"/projects/").concat(e),"DELETE",{onSuccess:()=>{a(e)}})},w=e=>{let{activeOrganization:t}=(0,o.t)(),n=null==t?void 0:t.uuid;return(0,r.WE)("/api/organizations/".concat(n,"/projects/").concat(e,"/conversations"),{queryKey:[l.lx,{orgUuid:n,projectUuid:e}],enabled:!!t,staleTime:0,select:e=>c()(e,e=>new Date(e.updated_at)).reverse()})},x=function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},{activeOrganization:t}=(0,o.t)(),{defer:n}=e,a=null==t?void 0:t.uuid;return(0,r.WE)("/api/organizations/".concat(a,"/top_projects"),{queryKey:[l.n$,{orgUuid:a}],enabled:!n&&!!t,staleTime:0})},b=()=>{var e,t;let n=f(),a=null===(t=n.data)||void 0===t?void 0:null===(e=t.find(e=>e.is_starter_project))||void 0===e?void 0:e.uuid;return{...n,data:a}},C=()=>{let{activeOrganization:e}=(0,o.t)(),t=null==e?void 0:e.uuid,n=(0,s.useQueryClient)();return e=>{n.invalidateQueries({queryKey:[l.$T,{orgUuid:t,projectUuid:e}]}),n.invalidateQueries({queryKey:[l.gi,{orgUuid:t}]}),n.invalidateQueries({queryKey:[l.n$,{orgUuid:t}]}),n.invalidateQueries({queryKey:[l.lx,{orgUuid:t,projectUuid:e}]})}}},69602:function(e,t,n){n.d(t,{U:function(){return r}});var a=n(88075);let r=()=>{let e=(0,a.ZJ)();return(0,a.Cf)()||e}},98635:function(e,t,n){n.d(t,{Ch:function(){return T},Qe:function(){return k},Qt:function(){return N},Vn:function(){return L},kR:function(){return M},kS:function(){return P},sE:function(){return O}});var a=n(85565),r=n(27573),o=n(49456),i=n(27920),l=n(23489),s=n(21468),u=n(89992),c=n(88075),d=n(24658),p=n(82880),f=n(17886),m=n(65490),h=n(71854),g=n(44846),_=n(36222),v=n(95166),y=n(27222),w=n(13623),x=n(7653),b=n(34016);function C(){let e=(0,a._)(["\n  relative\n  grid\n  place-content-center\n  aspect-square\n  rounded-xl\n  cursor-pointer\n  transition\n  [fieldset:not(:disabled)_&]:hover:bg-bg-400\n  [fieldset:disabled_&]:opacity-50\n  [fieldset:disabled_&]:pointer-events-none\n  focus-within:ring\n  inline-flex\n  items-center\n  justify-center\n  relative\n  shrink-0\n  ring-offset-2\n  ring-offset-bg-300\n  ring-accent-main-100\n  focus-visible:outline-none\n  focus-visible:ring-1\n  disabled:pointer-events-none\n  disabled:opacity-50\n  disabled:shadow-none\n  disabled:drop-shadow-none\n  bg-[radial-gradient(ellipse,_var(--tw-gradient-stops))]\n  from-bg-500/10\n  from-50%\n  to-bg-500/30\n  border-0.5\n  border-border-400\n  font-medium\n  font-styrene\n  text-text-100/90\n  transition-colors\n  active:bg-bg-500/50\n  hover:text-text-000\n  hover:bg-bg-500/60\n"]);return C=function(){return e},e}let k=20,j=e=>{let t=e.webkitRelativePath;return t&&t.length?t:e.name},S=e=>e.replace(/\0/g,""),T=e=>{e.extracted_content=S(e.extracted_content),e.file_name=S(e.file_name),e.file_type=S(e.file_type)},E=(e,t)=>({file_name:j(e),file_type:e.type,file_size:e.size,extracted_content:t});function P(e){let{syncSourceCount:t,files:n,setFiles:a,numExistingConversationFiles:s,attachments:u,setAttachments:c,numExistingConversationAttachments:p,detectSameAttachment:m,selectedModel:h,blobFileUploadsEnabled:g}=e,{addError:w}=(0,d.e)(),b=(0,i.wN)(null);return function(e){let{syncSourceCount:t,onUploadComplete:n,existingAttachments:a,existingFiles:i,numExistingConversationAttachments:s,numExistingConversationFiles:u,selectedModel:c,blobFileUploadsEnabled:d}=e,{modelConfig:p}=(0,l.V)(c),m=p.image_in,[h,g,w,b]=function(e){let{syncSourceCount:t,onUploadComplete:n,existingAttachments:a,existingFiles:r,numExistingConversationFiles:i,selectedModel:s,blobFileUploadsEnabled:u}=e,{modelConfig:c}=(0,l.V)(s),d=c.image_in,p=U()&&c.pdf_in,{isUploading:f,setIsUploading:m,handleError:h,handleUpload:g}=L({imagesEnabled:d,blobFileUploadsEnabled:u,onUploadComplete:n,rasterizePdfUploadsEnabled:p}),v=(0,x.useCallback)(e=>{let{newUploads:n=[],numNewPotentialAttachments:l=0,showError:s=!0}=e,{attachmentUploads:c,imageUploads:f,rasterizedDocumentUploads:m,outOfContextFileUploads:g}=(0,o.Jw)(n,{imagesEnabled:d,blobFileUploadsEnabled:u,rasterizePdfUploadsEnabled:p});return l+c.length+f.length+m.length+g.length+a.length+r.length+t>k?(s&&h("You can add at most ".concat((0,_.M0)(k,"attachment")," to a message. Please select fewer attachments.")),!1):!(f.length+m.length+r.length+i>100)||(s&&h("You can add at most ".concat((0,_.M0)(100,"file")," to a chat. ").concat(i<100?"Please select fewer files.":"Please consider starting a new chat.")),!1)},[d,u,a,r,t,i,h,p]);return[f,m,v,(0,x.useCallback)(async e=>{v({newUploads:e})&&await g(e)},[g,v])]}({syncSourceCount:t,onUploadComplete:n,existingFiles:i,existingAttachments:a,numExistingConversationFiles:u,numExistingConversationAttachments:s,selectedModel:c,blobFileUploadsEnabled:d}),C=function(e){let{handleUpload:t}=e,n=(0,x.useRef)({ready:0,total:0}),a=(0,x.useCallback)(()=>{n.current={ready:0,total:0}},[]),r=(0,x.useCallback)(e=>{n.current.ready+=1,n.current.total===n.current.ready&&t(e)},[t]),o=(0,x.useCallback)((e,t)=>{let a=e.length;for(let i=0;i<a;i++){let a=e[i];a.isFile?(n.current.total+=1,a.file(e=>{t.push(e),r(t)})):a.isDirectory&&a.createReader().readEntries(e=>{o(e,t)})}},[r]);return(0,x.useCallback)(e=>{var t;e.preventDefault(),a();let n=null===(t=e.dataTransfer)||void 0===t?void 0:t.items;if(!n)return;let r=[];for(let e=0;e<(null==n?void 0:n.length);e++){let t=n[e].webkitGetAsEntry();t&&r.push(t)}o(r,[])},[o,a])}({handleUpload:b}),j=(0,x.useCallback)(async e=>{await b(Array.from(e))},[b]),S=(0,x.useCallback)(async e=>{let t=e.target.files;t&&await b(Array.from(t)),e.target.value=""},[b]),T=m?"Upload docs or images to Claude\n(Max ".concat(k,", 30mb each)"):"Add content (".concat(k," max, 30mb each)\nAccepts pdf, txt, csv, etc."),E={type:"file",accept:(0,o.tB)({imagesEnabled:m,outOfContextFilesEnabled:d}).join(","),onChange:e=>{S(e)},multiple:!0,"aria-label":"Upload files"};return[h,g,w,C,j,b,(0,r.jsx)(f.u,{className:"text-center",tooltipContent:T,children:(0,r.jsxs)(Q,{children:[(0,r.jsx)("input",{"data-testid":"file-upload",className:"absolute inset-0 -z-10 overflow-hidden rounded-xl opacity-0",...E}),h?(0,r.jsx)(v.U,{className:"animate-spin",size:18}):(0,r.jsx)(y.p,{size:18,weight:"light"})]})},"upload-tooltip"),E]}({syncSourceCount:t,onUploadComplete:(0,x.useCallback)(async(e,t)=>{m&&e.find(e=>m(e.extracted_content))&&w("The same attachment was already added earlier. Claude sees the full conversation when replying, so there’s no need to re-upload."),c(t=>[...t,...e]),a(e=>[...e,...t])},[c,m,w,a]),existingAttachments:u,existingFiles:n,numExistingConversationAttachments:p,numExistingConversationFiles:s,selectedModel:null!=h?h:b,blobFileUploadsEnabled:g})}let D=async(e,t,n)=>{let a=new Image;if(a.src=URL.createObjectURL(e),await new Promise(e=>{a.onload=e,setTimeout(e,250)}),!a.width||!a.height||"image/png"!==e.type&&a.width<=t&&a.height<=n)return e;let r=a.width/a.height,o=a.width,i=a.height;a.width>t&&(i=(o=t)/r),i>n&&(o=(i=n)*r);let l=document.createElement("canvas");l.style.display="none",document.body.appendChild(l);let s=l.getContext("2d");if(!s||!s.imageSmoothingQuality)return document.body.removeChild(l),e;s.imageSmoothingQuality="high",l.width=o,l.height=i,s.drawImage(a,0,0,o,i);let u=await new Promise(e=>{l.toBlob(t=>e(t),"image/webp",.85)});return(document.body.removeChild(l),u)?new File([u],e.name,{type:"image/webp"}):e},O=()=>{let{value:e}=(0,g.F)("use_canvas_resize");return(0,x.useCallback)(async t=>e?await D(t,2e3,2e3):t,[e])},N=()=>{let e=R(),t=M();return async(n,a,r)=>{try{return await t(n,a,r)}catch(t){e(t,(0,o.Wr)(n)?"image":"file")}}},z=e=>{let t=R(),n=M(),a=(0,u.OJ)();return async(r,o)=>{let i={};try{i.file=await n(r,o)}catch(n){n instanceof m.Hx&&"document_too_many_pages"===n.errorCode?i.attachment=await F(a,r,o,e):t(n,"document")}return i}},M=()=>{let e=(0,u.OJ)();return async(t,n,a)=>{let r=new FormData;r.append("file",t);let o=a?"/api/organizations/".concat(n,"/projects/").concat(a,"/upload"):"/api/".concat(n,"/upload"),i=await e(o,{method:"POST",body:r}),l=await i.json();if(i.ok)return l;throw(0,m.fT)(i.status,l,"File upload failed",i.headers)}},I=async(e,t,n,a)=>{let r;let o=new FormData;o.append("file",t);try{r=await e("/api/organizations/".concat(n,"/convert_document"),{method:"POST",body:o})}catch(e){return(0,w.Tb)(e),a("One or more file uploads have failed. Please try again.")}if(429===r.status)return a("Too many file upload attempts. Please wait and try again later.");if(413===r.status)return a("Uploaded file is too large. Try uploading a smaller part of the document, or copy/pasting an excerpt from the file.");if(!r.ok)return a("Text extraction failed for one of the uploaded files. Please try again.");let i=await r.json();return i&&0!==Object.keys(i).length&&i.extracted_content?(i.file_name=j(t),i):a("Text extraction failed for one of the uploaded files. Please try again.")},L=e=>{var t;let{imagesEnabled:n,blobFileUploadsEnabled:a,rasterizePdfUploadsEnabled:r,onUploadComplete:i,onError:l,projectUuid:p}=e,{activeOrganization:f}=(0,c.t)(),m=null!==(t=null==f?void 0:f.uuid)&&void 0!==t?t:"",[g,v]=(0,x.useState)(!1),{addError:y}=(0,d.e)(),w=(0,x.useCallback)(e=>{v(!1),y(e),l&&l()},[y,l,v]),b=O(),C=N(),k=z(w),j=(0,u.OJ)(),S=(0,s.z$)(),T=(0,x.useCallback)(async(e,t)=>{let{attachmentUploads:l,imageUploads:s,rasterizedDocumentUploads:u,unsupportedUploads:c,tooLargeUploads:d,outOfContextFileUploads:f}=(0,o.Jw)(e,{imagesEnabled:n,blobFileUploadsEnabled:a,rasterizePdfUploadsEnabled:r}),g=c.map(e=>(0,o.mD)(e.name));if(g.length>0)return w("Files of the following ".concat((0,_._6)(g.length,"format")," are not supported: ").concat([...new Set(g)].join(", "),"."));if(d.length>0)return S.track({event_key:"file_upload_too_large",large_files:d.map(e=>({file_type:e.type,file_size:e.size}))}),w("You may not upload files larger than 30mb.");v(!0);let y=[],x=0,T=(e,n)=>{if(void 0===t)return!0;let a=new Blob([n]).size/h.r6;return!((x+=a)>t)||(w("Failed to upload file ".concat(e,". Project knowledge exceeds maximum. Remove files to continue.")),!1)};for(let e of l){let t=await F(j,e,m,w);if(!(t&&T(e.name,t.extracted_content)))return;await i([t],[])}for(let e of s){let t=await b(e),n=await C(t,m);n&&y.push(n)}for(let e of u){let{file:t,attachment:n}=await k(e,m);if(t&&y.push(t),n){if(!T(e.name,n.extracted_content))return;await i([n],[])}}for(let e of f){let t=await C(e,m,p);t&&y.push(t)}await i([],y),v(!1)},[a,j,i,n,w,C,k,m,b,S,r,p]);return{isUploading:g,setIsUploading:v,handleError:w,handleUpload:T}},Q=p.q.label(C()),F=async(e,t,n,a)=>{if(!(0,o.dF)(t))try{let e=await (0,o.CL)(t);return E(t,e)}catch(e){}let r=await I(e,t,n,a);if(r)return T(r),r},R=()=>{let{addError:e}=(0,d.e)();return(0,x.useCallback)((t,n)=>{if(t instanceof m.Hx){if("rate_limit_error"===t.type){e((0,r.jsxs)("p",{children:["You've reached your limit for ",n," uploads. Please try again later.",(0,r.jsx)(b.o,{})]}));return}if("document_password_protected"===t.errorCode){e((0,r.jsx)("p",{children:"The document you uploaded is password protected. Please remove the password and try again."}));return}}if(t instanceof m.Hx&&"Image is too large"===t.message){e((0,r.jsxs)("p",{children:["Image is too large."," ",(0,r.jsx)("a",{href:"https://support.anthropic.com/en/articles/9002500-what-kinds-of-images-can-i-upload-to-claude-ai",target:"_blank",rel:"noopener noreferrer",className:"underline hover:text-accent-main-100",children:"Learn more"})]}));return}e((0,r.jsxs)("p",{children:["Your ",n," upload failed. Please try again."]}))},[e])},U=()=>{let{value:e}=(0,g.F)("janus_claude-ai");return e}},34016:function(e,t,n){n.d(t,{o:function(){return s}});var a=n(27573),r=n(51571),o=n(88075),i=n(87659);let l=()=>{let e=(0,r.Z)(),{websiteBaseUrl:t}=(0,r.m)();return e?(0,a.jsxs)(a.Fragment,{children:[" ","Or consider"," ",(0,a.jsx)("a",{href:"/upgrade/pro",className:"font-bold underline",rel:"noreferrer",children:"upgrading to Claude Pro"}),"."]}):(0,a.jsxs)(a.Fragment,{children:[" ","Or"," ",(0,a.jsx)(i.default,{href:"".concat(t,"/contact-sales"),className:"font-bold underline",children:"contact sales"})," ","if you would be interested in upgrading to a paid version of Claude."]})};function s(){let e=(0,o.w7)(),t=(0,o.uh)();return e&&!t?(0,a.jsx)(l,{}):null}},49456:function(e,t,n){n.d(t,{CL:function(){return P},Jw:function(){return S},MR:function(){return _},Wr:function(){return C},dF:function(){return T},eh:function(){return D},mD:function(){return x},tB:function(){return v},wI:function(){return c}});var a=n(88075),r=n(17299),o=n(44846),i=n(42443);let l=[".DS_Store"],s=["jpg","jpeg","png","gif","webp"],u=["image/jpeg","image/png","image/gif","image/webp"],c={"image/jpeg":"jpg","image/png":"png","image/gif":"gif","image/webp":"webp"},d=["bmp","ico","tiff","tif","psd","raw","cr2","nef","orf","sr2","mobi","jp2","jpx","jpm","mj2","svg","svgz","ai","eps","ps","indd","heic","mp4","mov","avi","mkv","wmv","flv","webm","mpeg","mpg","m4v","3gp","ogv","ogg","rm","rmvb","asf","amv","mpe","m1v","m2v","svi","3g2","roq","nsv","f4v","f4p","f4a","f4b","qt","hdmov","divx","div","m2ts","mts","vob","mp3","wav","wma","aac","flac","alac","aiff","ogg","opus","m4a","amr","awb","wmv","ra","rm","mid","midi","mka","ttf","otf","woff","woff2","eot","sfnt","ttc","suit","zip"],p=["xls","xlsx","xlsb","xlm","xlsm","xlt","xltm","xltx","ods"],f=["txt","py","ipynb","js","jsx","html","css","java","cs","php","c","cc","cpp","cxx","cts","h","hh","hpp","rs","R","Rmd","swift","go","rb","kt","kts","ts","tsx","m","mm","mts","scala","rs","dart","lua","pl","pm","t","sh","bash","zsh","csv","log","ini","cfg","config","json","proto","yaml","yml","toml","lua","sql","bat","md","coffee","tex","latex","gd","gdshader","tres","tscn"],m=["docx","rtf","epub","odt","odp","pdf"],h=["application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/rtf","application/epub+zip","application/vnd.oasis.opendocument.text","application/vnd.oasis.opendocument.presentation","application/pdf"],g=["csv"],_=3e7,v=e=>{let{imagesEnabled:t=!1,outOfContextFilesEnabled:n=!1}=e;return[".pdf",".doc",".docx",".rtf",".epub",".odt",".odp",".pptx",...w(),...t?y():[],...n?p.map(e=>".".concat(e)):[]]},y=()=>s.map(e=>".".concat(e)),w=()=>f.map(e=>".".concat(e)),x=e=>e.split(".").pop().toLowerCase(),b=(e,t)=>{let{imagesEnabled:n=!1,blobFileUploadsEnabled:a=!1}=t,r=x(e.name);return!!(!n&&(s.includes(r)||u.includes(e.type)))||(a?d.includes(r):[...d,...p].includes(r))},C=e=>{let t=x(e.name);return s.includes(t)||u.includes(e.type)},k=e=>[...g,...p].includes(x(e.name)),j=e=>!!l.includes(e.name),S=(e,t)=>{let{imagesEnabled:n=!1,blobFileUploadsEnabled:a=!1,rasterizePdfUploadsEnabled:r}=t,o=[],i=[],l=[],s=[],u=[],c=[];return e.filter(e=>!j(e)).forEach(e=>{let t=n&&C(e);b(e,{imagesEnabled:n,blobFileUploadsEnabled:a})?u.push(e):e.size>_?c.push(e):a&&k(e)?l.push(e):r&&("pdf"===x(e.name)||"application/pdf"===e.type)?s.push(e):T(e)?o.push(e):t?i.push(e):o.push(e)}),{attachmentUploads:o,imageUploads:i,rasterizedDocumentUploads:s,unsupportedUploads:u,tooLargeUploads:c,outOfContextFileUploads:l}},T=e=>{let t=x(e.name);return m.includes(t)||h.includes(e.type)},E=e=>{let t=new Uint8Array(e);if(t.length>=4){if(239===t[0]&&187===t[1]&&191===t[2])return"utf-8";if(254===t[0]&&255===t[1]||255===t[0]&&254===t[1])return"utf-16";if(0===t[0]&&0===t[1]&&254===t[2]&&255===t[3]||255===t[0]&&254===t[1]&&0===t[2]&&0===t[3])return"utf-32"}let n=!0,a=Math.min(t.length-1,1e3);for(let e=0;e<a;e+=2)if(0===t[e]&&0===t[e+1]||0!==t[e]&&0!==t[e+1]){n=!1;break}if(n)return"utf-16";let r=!0,o=!1;for(let e=0;e<t.length;e++){let n=t[e];if(n>127){if(o=!0,(224&n)==192){if(e+1>=t.length||(192&t[e+1])!=128){r=!1;break}e+=1}else if((240&n)==224){if(e+2>=t.length||(192&t[e+1])!=128||(192&t[e+2])!=128){r=!1;break}e+=2}else if((248&n)==240){if(e+3>=t.length||(192&t[e+1])!=128||(192&t[e+2])!=128||(192&t[e+3])!=128){r=!1;break}e+=3}else{r=!1;break}}}if(r&&o)return"utf-8";let i=(e=>{let t={ascii:0,nonAscii:0,cyrillic:0,latin1:0,control:0,total:Math.min(e.length,4e3)};for(let n=0;n<t.total;n++){let a=e[n];a<32?t.control++:a<127?t.ascii++:a>127&&(t.nonAscii++,(a>=192&&a<=255||a>=168&&a<=183)&&t.cyrillic++,(a>=128&&a<=159||a>=160&&a<=255)&&t.latin1++)}return t})(t),l=i.cyrillic/i.total*100,s=i.latin1/i.total*100,u=i.ascii/i.total*100;if(i.nonAscii>0){if(l>.3)return"windows-1251";if(s>i.control/i.total*100)return"windows-1252"}return u>90&&i.control/i.total<.1?"ascii":"utf-8"},P=async e=>{let t=await e.arrayBuffer(),n=E(t);try{return new TextDecoder(n,{fatal:!0}).decode(t)}catch(e){if("utf-8"!==n)return new TextDecoder("utf-8",{fatal:!0}).decode(t)}throw Error("Failed to decode file as plain text")};function D(){var e;let{value:t}=(0,o.F)("ooc_attachments"),{account:n}=(0,a.t)(),l=(0,r.T)(),s=null!==(e=null!=l?l:null==n?void 0:n.settings)&&void 0!==e?e:{},{value:u}=(0,i.h)(s);return!!t&&u}},42443:function(e,t,n){n.d(t,{h:function(){return o}});var a=n(44846),r=n(48644);function o(e){let t=function(){let{layer:e}=(0,r.useLayer)("frontend");return e.get("analysis_tool_experiment_enabled",!1)}(),{value:n}=(0,a.F)("rely_on_analysis_flag"),{value:o}=(0,a.F)("analysis_tool_launch_ga");if(n){var i;return{value:null!==(i=null==e?void 0:e.enabled_artifacts_attachments)&&void 0!==i?i:o,source:"flag"}}return{value:(null==e?void 0:e.enabled_artifacts_attachments)||t,source:"experiment"}}},27920:function(e,t,n){n.d(t,{hH:function(){return F},wN:function(){return A},Qk:function(){return W},pV:function(){return R},lE:function(){return U}});var a,r,o,i,l=n(27573),s=n(91014),u=n(34016),c=n(21468),d=n(51571),p=n(88075),f=n(24658),m=n(65490),h=n(71854),g=n(6734),_=n(36222),v=n(49793),y=n(71994),w=n(13623),x=n(26821),b=n(2560),C=n(82177),k=n(87659),j=n(67754),S=n(7653),T=n(48644);class E{_getBlockCharCount(e){if("text"===e.type||"text_with_citations"===e.type)return e.text.length;if("tool_use"===e.type){var t;return(null===(t=e.partial_json)||void 0===t?void 0:t.length)||0}return e.type,0}_maybeConvertMessageEventToContentBlock(e){let t=this.completionsToSmooth[this.completionsToSmooth.length-1];switch(e.type){case"content_block_delta":if("text_delta"===e.delta.type){if(t&&"text_with_citations"===t.type)return{type:"text_with_citations",text:e.delta.text,citations:[]};return{type:"text",text:e.delta.text}}if("input_json_delta"===e.delta.type){if(t&&"tool_use"===t.type)return{type:"tool_use",id:"",name:"",partial_json:e.delta.partial_json};if(t&&"tool_result"===t.type)return{type:"tool_result",tool_use_id:"",name:"",is_error:!1,content:[{type:"text",text:e.delta.partial_json}]}}if("citations_delta"===e.delta.type)return{type:"text_with_citations",text:"",citations:[e.delta.citation]};break;case"content_block_start":return e.content_block}}_set_raw_completion(e){0===this.start&&(this.start=Date.now());let t=this._maybeConvertMessageEventToContentBlock(e);t&&(e=>{if(0===this.completionsToSmooth.length){this.completionsToSmooth.push(e);return}let t=this.completionsToSmooth[this.completionsToSmooth.length-1];if(t.type!==e.type||"tool_use"===e.type&&e.id||"tool_result"===e.type&&e.tool_use_id){this.completionsToSmooth.push(e);return}switch(e.type){case"text":"text"===t.type&&(t.text+=e.text);break;case"text_with_citations":"text_with_citations"===t.type&&(t.text+=e.text,t.citations=[...t.citations,...e.citations]);break;case"tool_use":if("tool_use"===t.type){var n,a;t.partial_json=(null!==(n=t.partial_json)&&void 0!==n?n:"")+(null!==(a=e.partial_json)&&void 0!==a?a:"")}break;case"tool_result":"tool_result"===t.type&&(t.content=e.content)}})(t),this.model_done="message_stop"===e.type;let n=this.completionsToSmooth.reduce((e,t)=>e+this._getBlockCharCount(t),0);this.totalCompletionLength=n,this.arrivals.push([(Date.now()-this.start)/1e3,n])}_get_smoothed_completion(){if(0===this.start)return[];let e=(Date.now()-this.start)/1e3,t=this.arrivals[this.arrivals.length-1][1]+(this.model_done?100:0),n=.9*e-.3,a=this.arrivals.filter(e=>e[0]<n).map(e=>e[1]),r=a[a.length-1],o=function(e,t,n){let a=arguments.length>3&&void 0!==arguments[3]?arguments[3]:.01;if(t===n)return t;let r=e(t),o=e(n);if(t>=n)throw Error("Lower x is greater than upper x");if(r>a)throw Error("Lower f is greater than zero");if(o<-a)throw Error("Upper f is less than zero");for(;r<-a;){let a=(t+n)/2,i=e(a);i<=0?(t=a,r=i):(n=a,o=i)}return t}(n=>{let a=(n-this.x)/(e-this.t),o=1/(e-this.t);return 2*this.gamma*o*(a-this.v)-1/(n-r)+1/(t-n)},r,t),i=(o-this.x)/(e-this.t);this.v=this.alpha*this.v+(1-this.alpha)*i,this.smoothed_completion_is_unchanged=this.x>=this.totalCompletionLength,this.x=Math.max(o,this.x),this.t=e,this.smoother_done=this.model_done&&this.x>=this.totalCompletionLength,this.stats.push({t:e,x:o,v:i,min_chars:r,max_chars:t});let l=(e,t)=>{if("tool_result"===e.type)return e;if("text"===e.type||"text_with_citations"===e.type)return{...e,text:e.text.slice(0,t)};if("tool_use"===e.type){var n;return{...e,partial_json:null===(n=e.partial_json)||void 0===n?void 0:n.slice(0,t)}}return e},s=0,u=[];for(let e of this.completionsToSmooth){let t=this._getBlockCharCount(e);if(s+t<this.x)u.push(e),s+=t;else{let t=l(e,this.x-s);u.push(t);break}}return u}getTextCompletion(){let e=this.completionsToSmooth.find(e=>"text"===e.type||"text_with_citations"===e.type);return e&&e.text||""}onMessage(e){this._set_raw_completion(e)}async task(e,t){for(;!this.smoother_done&&!t.aborted;){let t=this._get_smoothed_completion();this.smoothed_completion_is_unchanged||e(t),await new Promise(e=>setTimeout(e,10))}}constructor(){this.alpha=.99,this.gamma=1e-5,this.v=100,this.x=0,this.t=0,this.arrivals=[[-9999,0]],this.start=0,this.completionsToSmooth=[],this.totalCompletionLength=0,this.model_done=!1,this.smoother_done=!1,this.smoothed_completion_is_unchanged=!1,this.stats=[]}}var P=n(80523);(a=o||(o={}))[a.APPEND_MESSAGE_WITH_COMPLETION=1]="APPEND_MESSAGE_WITH_COMPLETION",a[a.RETRY_MESSAGE_WITH_COMPLETION=2]="RETRY_MESSAGE_WITH_COMPLETION",(r=i||(i={})).Ping="ping",r.Completion="completion",r.Error="error",r.ContentBlockDelta="content_block_delta",r.ContentBlockStart="content_block_start",r.ContentBlockStop="content_block_stop",r.MessageDelta="message_delta",r.MessageStart="message_start",r.MessageStop="message_stop",r.MessageLimit="message_limit";let D=["close_file","create_file","delete_file","draw_svg","file_search","open_file","repl","str_replace","update_file"];async function O(e){let{frontendPrivateApiUrl:t,endpoint:n,orgUuid:a,conversationUuid:r,body:o,onCompletion:i,onInvokeTool:l,abortController:s,completion:u,getTools:c}=e,d=new E,p=d.task(i,s.signal),f=null,h=null,g=JSON.stringify({...u,...o,text:void 0,rendering_mode:"messages",organization_uuid:void 0,conversation_uuid:void 0}),_="",v="",y="",x=0,b=(0,P.L)(function(e,t,n,a){let r;if(void 0===n||void 0===a)throw Error("Missing org uuid or conversation uuid");switch(t){case 1:r="completion";break;case 2:r="retry_completion";break;default:throw Error("Invalid endpoint")}return"".concat(e,"/api/organizations/").concat(n,"/chat_conversations/").concat(a,"/").concat(r)}(t,n,a,r),{method:"POST",credentials:"include",headers:{"Content-Type":"application/json",Accept:"text/event-stream"},body:g,openWhenHidden:!0,signal:s.signal,async onopen(e){var t;if(!e.ok||!(null===(t=e.headers.get("content-type"))||void 0===t?void 0:t.includes(P.a))){let t=await e.text(),n={};try{n=JSON.parse(t)}catch(e){}throw(0,m.fT)(e.status,n,"Failed to fetch",e.headers)}},onmessage(e){var t,n;switch(e.event){case"ping":default:return;case"error":throw(0,m.fT)(0,JSON.parse(e.data),"Streaming error: 22");case"completion":{let n=JSON.parse(e.data);if(void 0===n.completion)throw Error("Unexpected message received when streaming: ".concat(e.data));let a={type:"content_block_delta",index:0,delta:{type:"text_delta",text:n.completion}};f=n.stop_reason,h=null!==(t=n.messageLimit)&&void 0!==t?t:null,d.onMessage(a);break}case"content_block_start":{let t=JSON.parse(e.data);x=t.index,"tool_use"===t.content_block.type&&(v=t.content_block.name,y=t.content_block.id),d.onMessage(t);break}case"content_block_delta":{let t=JSON.parse(e.data);if(t.index!==x)throw Error("Content block index did not match the expected index");(null===(n=t.delta)||void 0===n?void 0:n.type)==="input_json_delta"&&(D.includes(v)||c().some(e=>e.name===v))&&(_+=t.delta.partial_json),d.onMessage(t);break}case"content_block_stop":{if(!v)break;let t=JSON.parse(e.data);if(t.index!==x)throw Error("Content block index did not match the expected index");d.onMessage(t),l(r,v,y,_),_="",v="",y="";break}case"message_delta":case"message_start":case"message_stop":case"message_limit":{let t=JSON.parse(e.data);"message_stop"===t.type&&(f="message_stop"),"message_limit"===t.type&&(h=t.message_limit),d.onMessage(t)}}},onclose(){d.model_done=!0},onerror(e){throw e instanceof m.Hx&&529===e.statusCode||(0,w.Tb)(e),d.model_done=!0,d.smoother_done=!0,e}});return await Promise.all([b,p]),{stopReason:f,messageLimitResult:h}}var N=n(52212),z=n(3982),M=n(46777),I=n(33267),L=n(44768);let Q=(0,S.createContext)([null,null]);function F(e){let{children:t}=e,n=(0,S.useState)({});return(0,l.jsx)(Q.Provider,{value:n,children:t})}function R(e,t,n){let{onIncrementalCompletion:a,onStartAppend:r,onStreamCompleted:i}=(0,L.p)(),l=B({conversationUUID:e,endpoint:o.APPEND_MESSAGE_WITH_COMPLETION,onIncrementalCompletion:a,onStreamCompleted:i,onInvokeTool:t,getTools:n}),{runStream:s}=l,u=(0,S.useCallback)(async t=>{let{prompt:n,attachments:a,files:o,syncSources:i,rethrowErrors:l=!1,modelOverride:u,parent_message_uuid:c,personalized_style:d}=t;await r(e,e=>{if(!e)throw Error("Conversation tree must be provided for tree append");let t=(0,N.HX)(e),r=[{uuid:N.wZ,content:[{type:"text",text:n}],created_at:new Date().toISOString(),sender:"human",attachments:a,files:o,files_v2:o,sync_sources:i,index:t+1,parent_message_uuid:null!=c?c:N.QC},{uuid:N.FC,content:[],created_at:new Date().toISOString(),sender:"assistant",attachments:[],files:[],files_v2:[],sync_sources:[],index:t+2,parent_message_uuid:N.wZ}];return(0,N.vv)(e,r)}),await s({prompt:n,attachments:a,files:o,syncSources:i,rethrowErrors:l,modelOverride:u,parent_message_uuid:c,personalized_style:d})},[s,r,e]);return{...l,runStream:u}}function U(e,t,n,a){let{onIncrementalCompletion:r,onStreamCompleted:i,onStartAppend:l}=(0,L.p)(),s=B({conversationUUID:e,endpoint:o.RETRY_MESSAGE_WITH_COMPLETION,onIncrementalCompletion:r,onInvokeTool:t,onStreamCompleted:i,getTools:n}),{runStream:u}=s,c=(0,S.useCallback)(async t=>{await l(e,e=>{let n=[{uuid:N.FC,content:[],created_at:new Date().toISOString(),sender:"assistant",attachments:[],files:[],files_v2:[],sync_sources:[],parent_message_uuid:t,selectedOption:0,index:(0,N.HX)(e)+1}];return(0,N.vv)(e,n)}),await u({prompt:"",attachments:[],files:[],syncSources:[],parent_message_uuid:t,personalized_style:a})},[e,u,l,a]);return{...s,runStream:c}}let q="incomplete_stream",A=e=>{var t,n;let a=H(e),{config:r}=(0,T.useExperiment)("tepui_default_on_claude_free"),o=null==r?void 0:null===(t=r.get("console_default_model_override",null))||void 0===t?void 0:t.model,{layer:i}=(0,T.useLayer)("frontend"),l=null===(n=i.get("console_default_model_override",null))||void 0===n?void 0:n.model,{config:s}=(0,T.useConfig)("console_default_model"),u=s.get("model",null);return a||o||l||u||"claude-2.1"},H=e=>{let{data:t}=(0,s.Rq)(e||""),n=(0,j.useSearchParams)(),a=null==n?void 0:n.get("model");return(null==t?void 0:t.model)?null==t?void 0:t.model:a||void 0},J={value:null},W=()=>{let e=(0,x.useQueryClient)();return{failedStreamRetryData:(0,b.useQuery)({queryKey:[v.sf],queryFn:()=>J.value,initialData:null}).data||null,setFailedStreamRetryData:(0,S.useCallback)(t=>{J.value=t,e.setQueryData([v.sf],t)},[e])}};function B(e){var t;let{conversationUUID:n,endpoint:a,getTools:r,onIncrementalCompletion:o,onInvokeTool:i,onStreamCompleted:v}=e,{frontendPrivateApiUrl:x}=(0,d.m)(),{activeOrganization:b}=(0,p.t)(),T=null==b?void 0:b.uuid,{context:E,clearContext:P,setContext:D}=function(e){let[t,n]=(0,S.useContext)(Q),[a,r]=(0,S.useState)(),o=(0,S.useCallback)(()=>{n?n(t=>{let n={...t};return delete n[e],n}):r(void 0)},[e,n]),i=(0,S.useCallback)(t=>{n?n(n=>({...n,[e]:t})):r(t)},[e,n]);return{context:t?t[e]:a,clearContext:o,setContext:i}}(n),N=(0,j.useSearchParams)(),L=null==N?void 0:N.get("t"),F=null!==(t=H(n))&&void 0!==t?t:"",R=null==N?void 0:N.get("max_tokens"),U=(0,I.n)(),{addError:A,clearToast:J}=(0,f.e)(),B=(0,S.useMemo)(y.H,[]),Y=(0,s.$H)("push",B),{setFailedStreamRetryData:K}=W(),G=(0,S.useCallback)(async e=>{await (null==v?void 0:v(n,e)),P()},[v,n,P]),$=(0,S.useCallback)((e,t,a)=>{if(e===q)return A((0,l.jsxs)("p",{children:["Claude’s response was interrupted. Please check your network connection or"," ",(0,l.jsx)(k.default,{href:"https://support.anthropic.com/en/articles/9015913-how-to-get-support",className:"underline",children:"contact support"})," ","if the issue persists."]}));if(!(e instanceof m.Hx))return A("We couldn’t connect to Claude. Please check your network connection and try again.");if("rate_limit_error"===e.type){if(e.message.includes("{")&&T)try{let t=JSON.parse(e.message);U(t,T,n)}catch(e){}return A((0,l.jsxs)("p",{children:["You've reached the limit for Claude messages at this time. Please wait before trying again. ",(0,l.jsx)(u.o,{})]}))}if("not_found_error"===e.type)return A((0,l.jsx)("p",{children:"Claude model version not found."}));if("billing_error"===e.type)return A((0,l.jsxs)("p",{children:["We had an unexpected billing error, please"," ",(0,l.jsx)("a",{className:"underline",href:"https://support.anthropic.com/en/articles/9015913-how-can-i-contact-support",target:"_blank",rel:"noreferrer",children:"contact support."})," "]}));if("overloaded_error"===e.type)return A((0,l.jsxs)("p",{children:["Due to unexpected capacity constraints, Claude is unable to respond to your message. Please try again soon.",(0,l.jsx)(u.o,{})]}));if("exceeded_max_uploads_per_message"===e.errorCode){A("Your message will exceed the maximum number of files allowed per message. Consider removing some of your file or adding files over several messages.");return}if("exceeded_max_image_limit_per_chat"===e.errorCode){let e=A((0,l.jsxs)("p",{children:["Your message will exceed the"," ",(0,l.jsx)("a",{className:"underline",target:"_blank",rel:"noreferrer",href:h._R,children:"maximum image count"})," ","for this chat.",a>0?(0,l.jsxs)(l.Fragment,{children:[" ","Try uploading ",(0,_._6)(a,"document")," ","with fewer pages, removing images,"]}):" Try removing images"," ",(0,l.jsx)("a",{href:"#",className:"underline",onClick:t=>{t.preventDefault(),Y(),J(e)},children:"or starting a new conversation."}),(0,l.jsx)(u.o,{})]}));return}if("invalid_request_error"===e.type&&413===e.statusCode){let e=A((0,l.jsxs)("p",{children:["Your message will exceed the"," ",(0,l.jsx)("a",{className:"underline",target:"_blank",rel:"noreferrer",href:h.jC,children:"length limit"})," ","for this chat.",t>0?" Try attaching fewer or smaller files":" Try shortening your message"," ",(0,l.jsx)("a",{href:"#",className:"underline",onClick:t=>{t.preventDefault(),Y(),J(e)},children:"or starting a new conversation."}),(0,l.jsx)(u.o,{})]}));return}return"invalid_request_error"===e.type&&"read_only_mode"===e.extra.code?A((0,l.jsx)("p",{children:"Due to capacity constraints, chatting with Claude is currently not available. Please try again in a little while."})):A(e)},[A,T,U,n,Y,J]),V=(0,c.z$)(),Z=function(){let{height:e,width:t}=(0,z.iP)(),n=[];return n.length?n.join("\n"):null}(),X=(0,S.useCallback)(async e=>{let{prompt:t,attachments:l,files:s,syncSources:u,rethrowErrors:c=!1,modelOverride:d,parent_message_uuid:p,personalized_style:f}=e;if(E)return;if(!b)throw Error("Cannot stream without an organization");let m=new AbortController;D({controller:m}),K(null);let h={prompt:t,parent_message_uuid:p,timezone:C.ou.local().zoneName||void 0,personalized_styles:f?[f]:void 0},_=(0,M.l)();(_||Z)&&(h.custom_system_prompt=[_,Z].filter(Boolean).join("\n")),F&&"string"==typeof F&&(h.model=F),d&&(h.model=d),"string"==typeof L&&(h.temperature=parseInt(L)),R&&"string"==typeof R&&(h.max_tokens_to_sample=parseInt(R));let v=r();v.length&&(h.tools=v);let y=[],k=null,j=null,S=null;try{k=(S=await O({frontendPrivateApiUrl:x,endpoint:a,orgUuid:b.uuid,conversationUuid:n,body:{organization_uuid:b.uuid,conversation_uuid:n,text:t,attachments:l,files:s.map(e=>e.file_uuid),sync_sources:u.map(e=>e.uuid)},onCompletion:e=>{o(n,e),y=e},onInvokeTool:i,abortController:m,completion:h,getTools:r})).stopReason,j=S.messageLimitResult}catch(e){if(K({prompt:t,attachments:l,files:s}),$(e,l.length+s.length,s.filter(e=>"document"===e.file_kind).length),(0,w.Tb)(e),c||(0,g.yG)())throw e}finally{S&&!k&&(o(n,y),$(q,l.length+s.length,s.filter(e=>"document"===e.file_kind).length),V.track({event_key:"sse_interrupted"}),(0,w.uT)("sse_interrupted"),await new Promise(e=>setTimeout(e,3e4))),await G(j)}return y},[E,b,D,K,Z,F,L,R,r,x,a,n,i,o,$,G,V]),ee=(0,S.useCallback)(()=>{E&&(E.controller.abort(),G(null))},[E,G]);return{runStream:X,isStreaming:!!E,abortStream:ee}}},46777:function(e,t,n){n.d(t,{h:function(){return o},l:function(){return i}});var a=n(7653);let r="customSystemPrompt",o=()=>{let[e,t]=(0,a.useState)(()=>"undefined"==typeof localStorage?"":localStorage.getItem(r)||"");return(0,a.useEffect)(()=>{localStorage.setItem(r,e)},[e]),{customSystemPrompt:e,setCustomSystemPrompt:t}},i=()=>"undefined"==typeof localStorage?"":localStorage.getItem(r)},23489:function(e,t,n){n.d(t,{V:function(){return s},u:function(){return u}});var a=n(89992),r=n(88075),o=n(49793),i=n(48644);let l={image_in:!1,pdf_in:!1},s=e=>{let{activeOrganization:t}=(0,r.t)(),n=null==t?void 0:t.uuid,{data:i,isLoading:s,isPlaceholderData:u}=(0,a.WE)("/api/organizations/".concat(n,"/model_configs/").concat(e),{queryKey:[o.Qn,n,e],enabled:!!n,staleTime:3e5,meta:{noToast:!0}}),c=!u&&i||l;return"claude-3-5-haiku-20241022"===e&&(c={image_in:!0,pdf_in:!1}),{isLoading:s,modelConfig:c}},u=()=>{let{config:e}=(0,i.useConfig)("claude_ai_models"),t=e.get("models",[]),n=t.filter(e=>!e.inactive),a=n.filter(e=>!e.overflow),r=n.filter(e=>e.overflow);return{allModelOptions:t,activeModelOptions:n,mainModels:a,overflowModels:r}}},33267:function(e,t,n){n.d(t,{I:function(){return u},n:function(){return s}});var a=n(89992),r=n(88075),o=n(49793),i=n(26821),l=n(7653);let s=()=>{let e=(0,i.useQueryClient)();return(0,l.useCallback)((t,n,a)=>{"within_limit"!==t.type&&(t.conversationUUID=a),e.setQueryData([o.aY],e=>e?{...e,messageLimits:{...e.messageLimits,[n]:t}}:e)},[e])},u=e=>{let{activeOrganization:t}=(0,r.t)(),n=null==t?void 0:t.uuid,o=s(),i={type:"within_limit"};return(0,a.uC)(()=>"/api/organizations/".concat(n,"/reset_rate_limits"),"POST",{onSuccess:()=>{o(i,n,e||"")},meta:{noToast:!0}})}},44768:function(e,t,n){n.d(t,{p:function(){return u}});var a=n(88075),r=n(49793),o=n(26821),i=n(7653),l=n(52212),s=n(33267);let u=()=>{let e=(0,o.useQueryClient)(),{activeOrganization:t}=(0,a.t)(),n=null==t?void 0:t.uuid,u=(0,i.useRef)(),c=(0,s.n)(),d=(0,i.useCallback)(async(t,a)=>{let o=[r.I8,{orgUUID:n},{uuid:t}],i=e.getQueryData(o);if(!i)throw Error("Conversation tree must be provided for append");let l=a(i);u.current=l,await e.cancelQueries({queryKey:o}),e.setQueryData(o,u.current)},[e,n]),p=(0,i.useCallback)((t,a)=>{0!==a.length&&e.setQueryData([r.I8,{orgUUID:n},{uuid:t}],()=>{let e=u.current;if(!e)throw Error("Conversation tree must be provided for incremental completion");if(!e.current_leaf_message_uuid)throw Error("Couldn't figure out where to put completion");let t=e.messageByUuid.get(e.current_leaf_message_uuid);if(!t)throw Error("New assistant message not found");return t.content=a,{...e,created_at:new Date().toISOString()}})},[e,n]);return{onStartAppend:d,onStreamCompleted:(0,i.useCallback)(async(t,a)=>{let o=[r.I8,{orgUUID:n},{uuid:t}];u.current=void 0,a?(e.setQueryData([r.tv,{orgUUID:n}],e=>{if(!e)return;let n=e.find(e=>e.uuid===t);return n?[{...n,updated_at:new Date().toISOString()},...e.filter(e=>e.uuid!==t)]:e}),await e.invalidateQueries({queryKey:o})):e.invalidateQueries({queryKey:o}),a&&n&&c(a,n,t)},[e,c,n]),onIncrementalCompletion:p,changeDisplayedConversationPath:(0,i.useCallback)((t,a,o,i)=>{e.setQueryData([r.I8,{orgUUID:n},{uuid:t}],e=>{if(!e)throw Error("Conversation tree must be provided for changeDisplayedConversationPath");let t=(0,l.mj)(e,a,o);return t.current_leaf_message_uuid&&i&&i(t.current_leaf_message_uuid),t})},[e,n])}}},82880:function(e,t,n){n.d(t,{q:function(){return i}});var a=n(57908),r=n(7653);function o(e){return function(t){for(var n=arguments.length,o=Array(n>1?n-1:0),i=1;i<n;i++)o[i-1]=arguments[i];let l=t.map(e=>e.replace(/\n/g,"").trim()),s=r.forwardRef((t,n)=>{let{className:i,...s}=t,u=o.map(e=>"function"==typeof e?e(t):e);return r.createElement(e,{...s,ref:n,className:(0,a.Z)(l,u,"string"==typeof i?i:"")})});return s.displayName="string"==typeof e?e:e.displayName,s}}function i(e){return o(e)}i.a=o("a"),i.aside=o("aside"),i.button=o("button"),i.main=o("main"),i.div=o("div"),i.form=o("form"),i.nav=o("nav"),i.fieldset=o("fieldset"),i.header=o("header"),i.h1=o("h1"),i.h2=o("h2"),i.h3=o("h3"),i.h4=o("h4"),i.h5=o("h5"),i.th=o("th"),i.td=o("td"),i.input=o("input"),i.label=o("label"),i.p=o("p"),i.section=o("section"),i.span=o("span"),i.li=o("li")},6734:function(e,t,n){n.d(t,{cm:function(){return r},yG:function(){return a}}),n(68571);let a=()=>!1,r=()=>!1},36222:function(e,t,n){n.d(t,{M0:function(){return r},_6:function(){return a}});let a=(e,t,n)=>1===e?t:n||t+"s",r=function(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"s",r=a(e,t,t+n);return"".concat(e," ").concat(r)}}}]);
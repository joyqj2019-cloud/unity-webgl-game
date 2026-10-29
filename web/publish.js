"use strict";
(function(){
 const url=new URL(window.location.href);
 // Uses the existing diagnostic OFF option; the tested mouse-spike fix remains active.
 if(!url.searchParams.has("lookDiagnostics")){url.searchParams.set("lookDiagnostics","off");history.replaceState(null,"",url);}
 const canvas=document.getElementById("unity-canvas"),start=document.getElementById("start-game"),loading=document.getElementById("unity-loading-container"),status=document.getElementById("load-status"),playStatus=document.getElementById("play-status");
 let instance=null,started=false;
 function banner(message){const box=document.getElementById("unity-warning");box.style.display="block";const row=document.createElement("p");row.textContent=message;box.appendChild(row);}
 start.addEventListener("click",function(){
  if(started)return;started=true;document.getElementById("start-panel").hidden=true;loading.hidden=false;
  const script=document.createElement("script");script.src="Build/Site.loader.js";
  script.onerror=function(){banner("The game loader could not be downloaded. Please reload and try again.");};
  script.onload=function(){
   const config={arguments:[],dataUrl:"Build/Site.data.unityweb",frameworkUrl:"Build/Site.framework.js.unityweb",codeUrl:"Build/Site.wasm.unityweb",streamingAssetsUrl:"StreamingAssets",fullscreenElementID:"unity-fullscreen-container",companyName:"DefaultCompany",productName:"My project 1",productVersion:"0.1.0",showBanner:function(message,type){if(type==="error")banner(message);else console.warn(message);}};
   createUnityInstance(canvas,config,function(progress){const percent=Math.round(progress*100);document.getElementById("unity-progress-bar-full").style.width=percent+"%";status.textContent="Loading… "+percent+"%";}).then(function(game){instance=game;loading.hidden=true;document.getElementById("fullscreen").disabled=false;playStatus.textContent="Ready — click inside the game to capture the mouse. Esc releases it.";}).catch(function(error){loading.hidden=true;banner(String(error));});
  };
  document.body.appendChild(script);
 });
 canvas.addEventListener("click",function(){canvas.focus();});
 document.getElementById("fullscreen").addEventListener("click",function(){if(instance)instance.SetFullscreen(1);});
})();
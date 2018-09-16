(function(){

if (window.location.protocol !== "https:" ) {
  document.body.innerHTML = 'Must be https.';
  return;
}

const ENDPOINT = "/api"
  
navigator.getUserMedia  = navigator.getUserMedia ||
                          navigator.webkitGetUserMedia ||
                          navigator.mozGetUserMedia ||
                          navigator.msGetUserMedia;

if ( !navigator.getUserMedia ) { return false; }
  
  var width = 0, height = 0;
  
  var canvas = document.createElement('canvas'),
      ctx = canvas.getContext('2d');
  document.body.appendChild(canvas);
  
  var video = document.createElement('video'),
      track;
  video.setAttribute('autoplay',true);
  
  window.vid = video;
  
  function getWebcam(){ 
    navigator.getUserMedia({ video: true, audio: false }, function(stream) {
      video.src = window.URL.createObjectURL(stream);
      track = stream.getTracks()[0];
    }, function(e) {
      console.error('Rejected!', e);
    });
  }

  function getMetaData(data, callback) {
    // I'll fix!
    // var formdata = new FormData();
    // formdata.append('file', data);

    debugger
    var xhr = new XMLHttpRequest();


    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200) {
            var metadata = JSON.parse(this.responseText);
            callback(metadata);
        }
        
        // end of state change: it can be after some time (async)
    };

    // xhr.open('POST', ENDPOINT, true);
    xhr.open('POST', ENDPOINT, true);
    // xhr.setRequestHeader('Content-Type', '');
    xhr.send(data);
  }

  function snap() {
    let data = canvas.toDataURL("image/png");
    getMetaData(data, (metadata)=>{
        // TODO(Anthony)
        // Render bounding box and text to canvas
        console.log(metadata);
    });
  }
  
  getWebcam();
  
  var rotation = 0,
      loopFrame,
      centerX,
      centerY,
      twoPI = Math.PI * 2;
  
  function loop(){
    
    loopFrame = requestAnimationFrame(loop);
    
    // Track points near bounding box from 1 frame to another.
    // ^ Find lib?


    //ctx.clearRect(0, 0, width, height);
    
    // ctx.globalAlpha = 0.005;
    // ctx.fillStyle = "#FFF";
    // ctx.fillRect(0, 0, width, height);
    
    ctx.save();
    
    
    // ctx.beginPath();
    // ctx.arc( centerX, centerY, 140, 0, twoPI , false);
    // //ctx.rect(0, 0, width/2, height/2);
    // ctx.closePath();
    // ctx.clip();
    
    //ctx.fillStyle = "#FFF";
    //ctx.fillRect(0, 0, width, height);
    
    // ctx.translate( centerX, centerY );
    // rotation += 0.005;
    // rotation = rotation > 360 ? 0 : rotation;
    // ctx.rotate(rotation);
    // ctx.translate( -centerX, -centerY );
    
    ctx.globalAlpha = 0.1;
    ctx.drawImage(video, 0, 0, width, height);
    
    ctx.restore();

  }
  
  function startLoop(){ 
    loopFrame = loopFrame || requestAnimationFrame(loop);
  }
  
  video.addEventListener('loadedmetadata',function(){
    width = canvas.width = video.videoWidth;
    height = canvas.height = video.videoHeight;
    centerX = width / 2;
    centerY = height / 2;
    startLoop();
  });
  
  canvas.addEventListener('click',function(){
    /*
    if ( track ) {
      if ( track.stop ) { track.stop(); }
      track = null;
    } else {
    */
    snap();
    //}
  });
  
  
})()

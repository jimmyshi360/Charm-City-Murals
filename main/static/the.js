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

const constraints = {
    advanced: [{
        facingMode: "environment"
    }]
};

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
    navigator.getUserMedia({ video: constraints, audio: false }, function(stream) {
      video.src = window.URL.createObjectURL(stream);
      track = stream.getTracks()[0];
    }, function(e) {
      console.error('Rejected!', e);
    });
  }

  function getMetaData(data, callback) {
    console.log(data)
    var data = data.replace('data:image/png;base64,', '');

    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    // formData.append("file", data);
    formData.append("testing", "Hello");
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
    // xhr.setRequestHeader('Content-Type', 'multipart/form-data');
    // xhr.send({"thing":"Hello"});
    xhr.send(data);
  }

var bb1 = 0
var bb2 = 0
var bb3 = 0
var bb4 = 0
var clicked = false;
 function writingText(text,posData){
ctx.font = "30px Arial";
ctx.fillText(text,posData-20,50);

  }


  function drawBoundingBox(metadata){
	bb1 = metadata['bounding_box'][0]
	bb2 = metadata['bounding_box'][1]
	bb3 = metadata['bounding_box'][2]
	bb4 = metadata['bounding_box'][3]
	
	ctx.strokeStyle = "#7CFC00";
	ctx.lineWidth = 5;
	ctx.beginPath();
	ctx.moveTo(bb1[0],bb1[1]);
	ctx.lineTo(bb2[0],bb2[1]);
	ctx.lineTo(bb3[0],bb3[1]);
	ctx.lineTo(bb4[0],bb4[1]);
	ctx.lineTo(bb1[0],bb1[1]);
	ctx.stroke();	


   }


  var prevData = null;
  function snap() {
    if(clicked){
        return;
    }
    clicked = true;
    let data = canvas.toDataURL("image/png");
    let fn = (metadata)=>{
        // TODO(Anthony)
        // Render bounding box and text to canvas
        console.log(metadata);
        if(metadata['has_mural']){
	        drawBoundingBox(metadata);
            //writingText('Here is a mural',metadata);
                        
        }
        let dataTmp = canvas.toDataURL("image/png");
        getMetaData(dataTmp, fn);

    };
    getMetaData(data, fn)
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
	
    ctx.strokeStyle = "#7CFC00";
	ctx.lineWidth = 5;
	ctx.beginPath();
	ctx.moveTo(bb1[0],bb1[1]);
	ctx.lineTo(bb2[0],bb2[1]);
	ctx.lineTo(bb3[0],bb3[1]);
	ctx.lineTo(bb4[0],bb4[1]);
	ctx.lineTo(bb1[0],bb1[1]);
	ctx.stroke();	

    writingText('Here is a mural',bb1[1]);

    
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

  let resize = function () {

      // Our canvas must cover full height of screen
      // regardless of the resolution
      let height = window.innerHeight;

      // So we need to calculate the proper scaled width
      // that should work well with every resolution
      let ratio = canvas.width/canvas.height;
      let width = height * ratio;

      canvas.style.width = width+'px';
      canvas.style.height = height+'px';
  }
  resize();
  window.addEventListener('resize', resize, true);
  document.body.webkitRequestFullScreen();
  
})()

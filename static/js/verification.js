var startTime=document.getElementById("countdown").dataset.timeId;

var x=setInterval(function(){
  var now=new Date().getTime();
  var remaining=60000-(now-startTime);

  document.getElementById("countdown").innerHTML=Math.floor(remaining/1000);
  
  if(remaining<=0) {
    clearInterval(x);
    document.getElementById("countdown").remove();
    document.getElementById("send_again").href="again";
  }
}, 1000);

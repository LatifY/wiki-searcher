document.body.style.zoom = "125%" 

var theme = document.getElementById("theme");
var isDark = false;

if (sessionStorage.getItem("mode") == "dark") {
  darkmode();
} else {
  lightmode();
}

theme.addEventListener("click", function() {
  if(isDark){
    lightmode();
  }
  else{
    darkmode();
  }
  location.reload();
});

function darkmode() {
  document.getElementById("html").style.filter = "invert(0)";
  
  //no themes
  var nothemes = document.getElementsByClassName("no-theme");
  for (let i = 0; i < nothemes.length; i++){
    nothemes[i].style.filter = "invert(0)";
  }

  isDark = true;
  sessionStorage.setItem("mode", "dark");
}



function lightmode() {
  document.getElementById("html").style.filter = "invert(1)";

  //no themes
  var nothemes = document.getElementsByClassName("no-theme");
  for (let i = 0; i < nothemes.length; i++){
    nothemes[i].style.filter = "invert(1)";
  }

  isDark = false;
  sessionStorage.setItem("mode", "light");
}

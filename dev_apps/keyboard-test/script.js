window.addEventListener("keydown", function() {
  dump("[keyboard test app][window] got keydown!\n");
});

var txt = document.getElementById('txt');

function focusCB(x) {
  dump("~~~~~~ background: " + x.style.backgroundColor + "\n");
  if (x.style.backgroundColor == "yellow") {
    x.style.backgroundColor = "white";
  } else {
    x.style.backgroundColor = "yellow";
  }
}

txt.addEventListener('focus', function(){focusCB(document.body)});

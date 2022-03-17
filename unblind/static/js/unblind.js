function deleteOnClick(clicked_id, x_str) {
  //console.log(clicked_id);
  url = window.location.href;
  if (x_str == "xss") {
      u = url + "/xss/" + clicked_id
      fetch(u, {
          method: "DELETE"
        }).then(() => {
          window.location.reload();        
        });
  }
  else{
  }    
}

function copy_clipboard(clicked_id) {
  var copyText = document.getElementById(clicked_id);
  navigator.clipboard.writeText(copyText.textContent);
}
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

function send_cmd(clicked_id) {
  u = "http://127.0.0.1:5000/unblind/cmd/" + clicked_id;
  cmd = document.getElementById("cmd");
  j = {
    c: cmd.value
  };
  fetch(u, {
    method: "POST",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(j)
  });
}

function copy_clipboard(clicked_id) {
  var copyText = document.getElementById(clicked_id);
  navigator.clipboard.writeText(copyText.textContent);
}

function get_info() {
  //console.log(window.location.href)
  //console.log(document.cookie)
  //console.log(window.navigator.userAgent)
  //console.log(window.clientInformation)
}
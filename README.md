# printerest


For generating a new Heroku app, use:
```$ heroku create```

For an already existing Heroku app, add a remote to the local repository `printerest` with:
```$ heroku git:remote -a printerest```

On Ubuntu, if heroku was installed with snap, you might need to replace `heroku` with `/snap/bin/heroku` on the preceeding commands.

Deploy the code to heroku site with:
```$ git push heroku master```

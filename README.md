<div align="center">
    <h1> AigenML - Aigen's Machine Learning Repository </h1>
</div>


## Run flask server

```
python server.py
```

#### Database commands 

````
flask --app server db init
flask --app server db migrate -m "Migrate message"
flask --app server db upgrade
````

#### How to run the uWSGI server

````
uwsgi --socket 0.0.0.0:5001 --protocol=http -w wsgi:app
````
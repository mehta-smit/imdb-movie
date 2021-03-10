# Setup imdb-movie
## Required Setups to run the services

#### Create Virtualenv
- [x] ```virtualenv ~/virt/imdb-movie -p python3.9```

#### Activate Virtualenv
- [x] ```source ~/virt/imdb-movie/bin/activate```

#### Install Required PIP Packages
- [x] ```pip install -U -r requirements.txt```

#### Setup Database using alembic
- [x] ```./run_with_env.sh env/developer.env flask db init```
- [x] ```./run_with_env.sh env/developer.env flask db migrate```
- [x] ```./run_with_env.sh env/developer.env flask db upgrade```

## Run API & Worker

#### Flask API Command :-
> ```./run_with_env.sh env/developer.env python app.py```

#### Gunicorn Command :-
> ```./run_with_env.sh env/developer.env exec gunicorn app:flask_app --bind=0.0.0.0:5000 --log-level=INFO```

### Ready to spare this.!!!

#### Access this Mini-IMDB on below internet address
[imdb-movie API Server Link](http://3.128.136.86:5000)

#### Access the imdb-movie API Documentation using below links
[Swagger API Documentation Link](http://3.128.136.86:5000/swagger-ui/)
[Swagger API Documentation JSON File](http://3.128.136.86:5000/swagger/)

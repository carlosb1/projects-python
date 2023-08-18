REQUERIMENTS
============
Install docker and docker compose (https://www.docker.com)

EXECUTION
=========
for the execution, It should be simple.. To apply: 
```
   $ docker-compose build . # in the project folder
   $ docker-compose up # to run
```
Anyway, it is possible to set up all the different docker images. For example, it is possible to execute the backend image with docker via Dockerfile:
```
   $ docker build .
   $ docker run
```
but It would be necessary to have started a database (mongodb) and a redis service.
Some ways to start mongodb and redis via console:
```
 docker run -d -p 27017:27017 -v /home/carlosb/data:/data/db mongo
 docker run -d -p 6379:6379 redis
```
    
COMMENTS
========

The objective of this demo is the creation of a minimal example of a w app to remove silence from videos. 

The applied stack of technology is:
* Vue.js (2.x) with node.js as frontend
* bootstrap (4) for css design.
* flask as backend service 
* Redis + Celery as queue batch processor
* pydub and ffmpeg-python for the management of videos 
* Mongodb as database
* gunicorn to manage multithread requests
* docker and docker-compose to set up images

The main idea for the web app is the creation of a pipeline with a queue of background processes... It seems a good scalable solution because it permits to decouple heavy processes (need more cpus and resources) from our API REST backend and from our frontend. In this simple demo, it works together but  with the current design, It would not be a problem to split it in another service with Celery. There are other good options, for example work with external webserveless but for this demo, it seems the most simple  / clean way. 

The REST Service is very simple, I thought to split in more classes (following some Model-View-Controller or a Clean Architecture) but It didn't seem necessary. I had the same problem with testing... I would like to apply the pyramid test pattern with unit, functional and integration tests, but I figured out that the REST service is only updating our DB and call a batch process, It doesn't have enough business classes to add these tests..

**developer:** carlos.baezruiz@gmail.com 



Possible improvements:
* Add complexity in the video module, It would be possible to permit change parameters or add more manipulations in the videos in order to set up  a pipelone..
* Wavenet to process noises. The Wavenet neural network is used for a lot of audio tasks, it is a recursive neural network which can be modified for different audio tasks...It could be useful to add more tasks. 
* NGINX. In order to set up this, in a real use case, gunicorn works to add paralellization but I would be recommended to add a proxy as NGINX in the docker-compose

DIRECTORIES
===========
```
.
├── backend			-> backend code. Python implementation
│   ├── app.py			-> REST implementation
│   ├── docker.cfg		-> Configuration to use docker
│   ├── Dockerfile		-> Docker file configuration	
│   ├── factory_responses.py	-> Factory pattern to create http responses
│   ├── filters.py		-> Filters for video pipeline... 
│   ├── ini.cfg			-> Default configuration for backend
│   ├── Pipfile			-> Dependencies
│   ├── run.sh			-> script to autorun backend gunicorn + celery + flask
│   ├── start_celery.py		-> script to start celery
│   ├── tasks.py		-> Code for celery tasks
│   ├── utils.py		-> Different functions without an important responsability role
│   └── videos_database		-> Output folder for videos
├── docker-compose.yml		-> Docker compose configuration
├── frontend			-> Frontend code. Vue + node impl.
│   ├── build			-> Build configuration files
│   ├── config			-> Configuration files
│   ├── Dockerfile		-> Docker file configuration
│   ├── index.html		-> Initial index.html 
│   ├── package.json		-> Dependencies
│   ├── src			-> Vue source code
│   └── static			-> static location
└── README.md			-> Readme file

```

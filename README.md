#The battle of hashtags

###Stack
- Django 1.9.1 running on Python 2.7
- PostgreSQL
- Celery with RabbitMQ as a broker

###Requirements
- Docker (developed with 1.9.1)
- Docker compose (developed with 1.5.2)
  
###Admin credentials
- username: admin
- password: password
- url: /admin

###Installation
First, run the containers:
```
docker-compose up
```

Then find IP of your docker machine
```
docker-machine ip default
```

and navigate to `http://DOCKER_IP:8000` (i.e. `http://192.168.99.100:8000`).

###Functionality
All CRUD operations are performed within the Django admin interface (/admin).

####Endpoints
There is a simple frontend that exposes all endpoints (both JSON and battle details template).

Battle details with all its hashtags and the current winner are accessible at `/battle/BATTLE_ID`.

Similar JSON endpoint is accessible at `/api/battle/BATTLE_ID`.

###Victory definition
Hashtags that have more tweets are likely to have more typos, which is why I've added additional victory definition. It takes a ratio of the number of typos to the number of words for a specific hashtag. The lowest ratio wins, what is much fairer.

JSON endpoint and the frontend shows both winners (according to the specificaion + by ratio).

###Notes
- Editing a battle will terminate any tasks running for that battle (if any) and it will schedule a new task.
- Twitter error code 420 means that Twitter has rate-limitted the app. In this case, please try again in 10 minutes.
- Hashtags with 0 tweets can't win (which is why current winner might say `null`).

###Future improvements
 - Implement tests.
 - Improve reliability of the worker (i.e. when the worker restarts or shuts down during execution).
 - Improve Twitter stream task termination.
 - Use celery with BROKER_USE_SSL and SSL certs.
 - Find a better dictionary for the spell checker. Currently words like `iPhone` and `http` are considered to have typos.
 - Can't run multiple battle in parallel due to Twitter's rate limitting. One way of solving this is sharing a single stream for all battles.
 - Handle a tie (i.e. when both hashtags have same number of typos and same ratios).
 - Set DEBUG to False (left it out to make errors observable).

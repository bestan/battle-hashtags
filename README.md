#The battle of hashtags

###Stack
- Django 1.9.1 running on Python 2.7
- PostgreSQL
- Celery with RabbitMQ as a broker

###Requirements
- Docker (developed with 1.8.3)
- Docker compose (developed with 1.4.2)
  
###Admin credentials
- username: admin
- password: password
- url: /admin

###Installation
First, run the container:
```
docker-compose build && docker-compose up
```

Then find IP of your docker machine
```
docker-machine ip default
```

and navigate to http://DOCKER_IP:8000 (i.e. http://192.168.99.100:8000).

###Functionality
All CRUD operations are performed within the Django admin interface (/admin).

####Endpoints
There is a simple frontend that exposes all endpoints (both JSON and battle details template).

Battle details with all its hashtags and the current winner are accessible at /battle/BATTLE_ID.

Similar JSON endpoint is accessible at /api/battle/BATTLE_ID.

###Victory definition
Hashtags that have more tweets are likely to have more typos, which is why I've added additional victory definition. It takes a ratio of the number of typos to the number of words for a specific hashtag. The lowest ratio wins, what is much fairer.

JSON endpoint and the frontend shows both winners (according to the specificaion + by ratio).

###Notes
- Editing a battle will terminate any tasks running the battle (if any), and it will also re-schedule it.
- Twitter error code 420 means that Twitter has rate-limitted the app. In this case, please try again in 10 minutes.
- Hashtags with 0 tweets can't be a winner (which is why Current winner might say `null`).

###Future improvements
 - Use celery with BROKER_USE_SSL with SSL certs.
 - Setting DEBUG to False (left it out to make errors observable).
 - Better dictionary for the spell checker. Currently it thinks that words iPhone and http all have typos.
 - Can't run multiple battle in parallel due to Twitter's rate limitting. One way of solving this is sharing one stream for all battles.
 - Handle a tie (i.e. when both hashtags have same number of typos and same ratios).
 - Improve battle task termination.

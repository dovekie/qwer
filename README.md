# qwer
A small API that makes with queues

To set up:
Install and run RabbitMQ on localhost

Set up a virtualenv and ```pip install -r requirements.txt```

run ```python/qwer_listener.py```

run ```python/qwer.py```

A web server will then be running on 127.0.0.1:5000

To see all jobs:
```GET /job/```

To see a particular job:
```GET /job/<job id>```

To add a job:
```POST /job/ with form data 'location'=<url>``` where url is a fully-speced URL, e.g. http://www.google.com

To delete a job:
```DELETE /job/<job id>```

To add a job to the queue of jobs to be run:
```GET /run/<job id>```


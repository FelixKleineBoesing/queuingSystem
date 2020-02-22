# CapPlan Backend

### Prerequisites

- docker and docker-compose

### Setup

```
docker-compose up --build
```

### Overview

The backend is primarly divided into two services. One is the api that receives requests from the frontend. The api 
puts the tasks that are described in the request onto a redis queue where an instance of the worker service takes a
task, calculates it and puts the result therefore an another channel for the api to return the result if the request 
is synchron. Otherwise it puts it onto a channel for the frontend.

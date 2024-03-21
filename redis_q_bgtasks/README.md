# REDIS-QUEUE WITH FASTAPI

This is a simple example of how to use Redis as a queue with FastAPI.

## CREATE THE REDIS QUEUE

```bash
pip install rq
```

## create the queue

```python
from fastapi import FastAPI
from rq import Queue
from redis import Redis

app = FastAPI()
redis_conn = Redis(host="localhost", port=6379) #  db=0
task_queue = Queue("task_queue", connection=redis_conn) # creating a task q with the name task_queue
```

## create a job

- a number printing machine

`job.py`

```python
def print_number(low, high):
    print("----job processing started----")
    for i in range(low, high):
        print(i)
    print("===job processing completed===")
```

## create a post route to add a job to the queue

```python
from job import print_number
from pydantic import BaseModel

class job(BaseModel):
    low: int
    high: int

@app.post("/add_task")
def post_job(job: job):
    task_queue.enqueue(print_number(job.low, job.high))
    return {"message": "Task added to the queue"}
```

## start the worker to consume the job

```bash
rq worker task_queue
```

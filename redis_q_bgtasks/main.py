from fastapi import FastAPI
from rq import Queue
from redis import Redis

from pydantic import BaseModel

from job import print_number

app = FastAPI()
redis_conn = Redis(host="localhost", port=6379) #  db=0
task_queue = Queue("task_queue", connection=redis_conn) # creating a task q with the name task_queue


class job(BaseModel):
    low: int
    high: int

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/add_task")
def post_job(job: job):
    job_instance = task_queue.enqueue(print_number, job.low, job.high)
    """
    jb_instance = task_queue.enqueue(print_number, job.low, job.high)
    print(jb_instance.id)
    """
    return {
        "status": "success",
        "job_id:": job_instance.id
    }
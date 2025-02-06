from locust import TaskSet, constant, task, HttpUser
import random


class MyHTTPCat(TaskSet):

    @task
    def get_status(self):
        response = self.client.get("/200")
        print("Get Status of 200")

    @task
    def get_random_status(self):
        status_codes = [100, 101, 102, 200, 201, 202, 203, 204, 205, 206, 207, 208]
        random_url = "/" + str(random.choice(status_codes))
        res = self.client.get(random_url)
        print("Random http status " + random_url)



class MyLoadTest(HttpUser):
    host = "https://http.cat"
    tasks = [MyHTTPCat]
    wait_time = constant(1)

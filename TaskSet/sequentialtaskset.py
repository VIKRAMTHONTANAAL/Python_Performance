from locust import SequentialTaskSet, HttpUser, constant, task

class MySequentialTaskSet(SequentialTaskSet):

    @task
    def get_status(self):
        self.client.get("/200")
        print("Status of 200")

    @task
    def get_500_status(self):
        self.client.get("/500")
        print("Status of 500")

class MyLoadTest(HttpUser):
    host = "https://http.cat"
    tasks = [MySequentialTaskSet ]
    wait_time = constant(1)
    
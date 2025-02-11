from locust import HttpUser, task, constant

class HelloWorld(HttpUser):
    wait_time = constant(1)
    host = "https://petstore.octoperf.com"

    @task
    def test(self):
        self.client.get("/")
    
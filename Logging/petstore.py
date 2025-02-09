from locust import HttpUser, SequentialTaskSet, task, constant
import logging

class PetStore(SequentialTaskSet):

    @task
    def home_page(self):
        with self.client.get("/", catch_response=True, name="TOO_Homepage") as response: 
            if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds()< 2.0:
                response.success()
                logging.info("Home page load success")
            else: 
                response.failure("Home page took too long")
                logging.error("Home page did not load successfully")
        
class LoadTest(HttpUser):
    host  = "https://petstore.octoperf.com"
    wait_time= constant(1)
    tasks = [PetStore]

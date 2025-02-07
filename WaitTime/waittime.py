from locust import User, task, constant, between, constant_pacing
import time

class MyUser(User):

    #wait_time= constant(1)
    #wait_time = between(2, 5)
    wait_time = constant_pacing(5)

    @task
    def launch(self):
        time.sleep(8)
        print("constant pacing ")
from locust import HttpUser, task, constant, SequentialTaskSet

class MyTestOne(SequentialTaskSet):

    wait_time= constant(1)

    def on_start(self):
        self.client.get("/", name=self.on_start.__name__)
        print("Starting")

    @task
    def browse_product(self):
        self.client.get("/product/OLJCESPC7Z", name=self.browse_product.__name__)
        print("Browse Product")

    @task
    def cart_page(self):
        self.client.get("/cart", name=self.browse_product.__name__)
        print("Cart page")

    def on_stop(self):
        self.client.get("/", name=self.on_stop.__name__)
        print("Stopping")

class LoadTest(HttpUser):
    host = "https://onlineboutique.dev"
    tasks = [MyTestOne]
    wait_time = constant(1)

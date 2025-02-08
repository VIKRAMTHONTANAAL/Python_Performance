from locust import TaskSet, constant, task, HttpUser

class MyNonSequentialClass(TaskSet):

    def on_start(self):
        self.client.get("/", name=self.on_start.__name__)
        print("Start")

    @task
    def browse_product_1(self):
        self.client.get("/product/OLJCESPC7Z", name=self.browse_product_1.__name__)
        print("Browse product 1")

    @task
    def browse_product_2(self):
        self.client.get("/product/OLJCESPC7Z2", name=self.browse_product_2.__name__)
        print("Browse product 2")

    @task
    def  cart_page(self):
        self.client.get("/cart", name=self.cart_page.__name__)
        print("Cart Page")

    def on_stop(self):
        self.client.get("/", name=self.on_stop.__name__)
        print("Stop")

class LoadTest(HttpUser):
    host="https://onlineboutique.dev"
    # wait_time = constant(1)
    tasks = [MyNonSequentialClass]
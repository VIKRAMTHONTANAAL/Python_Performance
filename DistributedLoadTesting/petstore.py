from locust import HttpUser, SequentialTaskSet, task, constant
import re
import random

class PetStore(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.jsession = ""
        self.random_product = ""

    @task
    def home_page(self):
        with self.client.get("", catch_response=True, name="TOO_Homepage") as response:
            if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds() < 2.0:
                response.success() 
            else: 
                response.failure("home page took too long and/or text check has failed")

    @task
    def enter_store(self):
        products = ['Fish', 'Dogs', 'Cats', 'Reptiles', 'Birds']
        with self.client.get("/actions/Catalog.action", catch_response = True, name ="T10_enterstore") as response:
            for product in products:
                if product in response.text:
                    response.success()
                else: 
                    response.failure("Products check failed")
                    break

            try:
                jsession = re.search(r"jsessionid=(.+?)\?", response.text)
                self.jsession=jsession.group(1)
            except AttributeError:
                self.jsession = ""

    @task
    def signin_page(self):
        self.client.cookies.clear()
        url = "/actions/Account.action;jsessionid="+ self.jsession+"?signonForm="
        with self.client.get(url, catch_response=True,name="T20_SignInPage") as response:
            if "Please enter your username and password" in response.text:
                response.success()
            else: 
                response.failure("Sign in page check failed")

    @task
    def login(self):
        self.client.cookies.clear()
        url = "/actions/Account.action"
        data = {
            "username": "j2ee",
            "password": "j2ee",
            "signon": "Login"
        }

        with self.client.post(url, name="T30_Signin", data=data, catch_response=True) as response:
            if "Welcome ABC!" in response.text:
                response.success()
                try: 
                    random_product = re.findall(r"Catalog.action\?viewCategory=&categoryId=(.?)\"", response.text)
                    self.random_product= random.choice(random_product)
                except AttributeError:
                    self.random_product = ""
            else:
                response.failure("Sign in failed")

    @task
    def random_product_page(self):
        url="/actions/Catalog.action?viewCategory=&categoryId=" + self.random_product
        name = "T40_"+ self.random_product+ "_Page"
        with self.client.get(url, name=name, catch_response= True) as response:
            if self.random_product in response.text:
                response.success()
            else: 
                response.failure("Product page not loaded")

    @task
    def sign_out(self):
        with self.client.get("/acitons/Account.action?signoff=", name="T50_Signoff", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Log off failed")
        self.client.cookies.clear()

class LoadTest(HttpUser):
    wait_time=constant(1)
    tasks = [PetStore]
    host = "https://petstore.octoperf.com/"
                             


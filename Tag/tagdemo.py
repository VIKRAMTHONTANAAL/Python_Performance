from locust import tag, HttpUser,  task, constant , SequentialTaskSet

class MyScript(SequentialTaskSet):

    @task
    @tag('get', 'xml')
    def get_xml(self):
        result = self.client.get("/xml", name="XML")
        print(result)

    @task
    @tag('get', 'json')
    def get_json(self):
        expected_response = "Wake up to WonderWidgets"

        with self.client.get("/json", catch_response = True, name="JSON") as response: 
            result = True if expected_response in response else False
            print(self.get_json.__name__, result)
            response.success()

    @task
    @tag('get', 'robots')
    def get_robots(self):
        expected_response = "*"
        result = "Fail"
        with self.client.get("/robots.txt", catch_response=True, name="Robots") as response:
            if expected_response in response.text:
                result = "Success"
                response.failure("Not a failure")
        print(self.get_robots.__name__, result)

    @task
    @tag('get')
    def get_failure(self):
        expected_response = 404
        with self.client.get("/status/404", catch_response= True, name="HTTP 404") as response:
            if response.status_code == expected_response:
                response.failure("got 404")
            else: 
                response.success()

    @task
    @tag('post')
    def post_json(self):
        expected_response = 200
        with self.client.post("/post", catch_response= True, name="Post") as response:
            if response.status_code == expected_response:
                response.success()
            else: 
                response.failure("Post failed")

class MyLoadTest(HttpUser):
    host = "https://httpbin.org"
    wait_time = constant(1)
    tasks = [MyScript]

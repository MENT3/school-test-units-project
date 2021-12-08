from locust import HttpUser, task, between
from locust.user import wait_time
from requests.models import cookiejar_from_dict

class WebsiteTestUser(HttpUser):
    wait_time = between(0.5, 3.0)
    auth_email = 'john@simplylift.co'
    auth_cookies = dict(
        session="eyJjbHViX3NsdWciOiJzaW1wbHktbGlmdCJ9.YbBiPg.FXW4U3NcB89D4IrupImk8aSoWhk"
    )

    def on_start(self):
        """" on_start is called when the TaskSet is starting """
        pass

    def on_stop(self):
        """" on_stop is called when the TaskSet is stopping """
        pass

    @task(1)
    def index(self):
        self.client.get('http://localhost:5000')

    @task(2)
    def dashboard(self):
        self.client.get('http://localhost:5000/dashboard')

    @task(3)
    def book(self):
        self.client.get('http://localhost:5000/book/fall-classic/simply-lift',
            cookies=self.auth_cookies)

    @task(4)
    def show_summary(self):
        self.client.post('http://localhost:5000/showSummary', {
            'email': self.euth_email
        })

    @task(5)
    def purchase_places(self):
        self.client.post('http://localhost:5000/purchasePlaces', {
            'club_slug': 'simply-lift',
            'competition_slug': 'spring-festival',
            'places': '1'
        }, cookies=self.auth_cookies)

    @task(6)
    def reset_data(self):
        self.client.get('http://localhost:5000/reset-data')

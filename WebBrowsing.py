import requests
import json


class UrlOpener:
    def __init__(self, session: requests.Session):
        self.session = session

    def open_url(self, url, query_string, headers):
        self.session.headers.update(headers)
        response = self.session.get(url, params=query_string)
        response.raise_for_status()
        return json.loads(response.text)

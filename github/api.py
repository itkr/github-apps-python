import json
import requests
from json.decoder import JSONDecodeError


class REST(object):
    # https://developer.github.com/v3/
    BASE_URL = 'https://api.github.com'

    def __init__(self, headers: dict, **kwargs):
        self.headers = headers
        self.base_url = self.BASE_URL.format(**kwargs)

    def list(self) -> dict:
        response = requests.get(self.base_url, headers=self.headers)
        return json.loads(response.text)

    def create(self, **request_body) -> dict:
        response = requests.post(
            self.base_url, json.dumps(request_body), headers=self.headers)
        try:
            return json.loads(response.text)
        except JSONDecodeError:
            # TODO: Projectのcreateでエラー。ここの例外処理をなくす
            return {}


class Issue(REST):
    # https://developer.github.com/v3/issues
    BASE_URL = 'https://api.github.com/repos/{owner}/{repo}/issues'


class IssueComment(REST):
    # https://developer.github.com/v3/issues/comments
    BASE_URL = 'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'


class Installation(REST):
    # https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-an-installation
    BASE_URL = 'https://api.github.com/app/installations'

    def get_token(self, installation_id: int) -> str:
        url = '{}/{}/access_tokens'.format(self.base_url, str(installation_id))
        response = requests.post(url, headers=self.headers)
        return json.loads(response.text).get('token')


class ProjectCard(REST):
    # https://developer.github.com/v3/projects/cards
    BASE_URL = "https://api.github.com/projects/columns/{column_id}/cards"

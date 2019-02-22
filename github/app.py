import jwt
from datetime import datetime, timedelta

from .api import Installation, Issue, ProjectCard


class GitHubApp(object):

    def __init__(self, pem: str, app_id: int, installation_id: int):
        self._pem = pem
        self._app_id = app_id
        self._token = self.installations().get_token(installation_id)

    @property
    def _token_header(self) -> dict:
        return {
            'Authorization': 'token {}'.format(self._token),
            # project API で必要だった
            'Accept': 'application/vnd.github.inertia-preview+json',
        }

    @property
    def _jwt_header(self) -> dict:
        return {
            'Authorization': 'Bearer {}'.format(self._generate_jwt()),
            'Accept': 'application/vnd.github.machine-man-preview+json',
        }

    def _generate_jwt(self) -> str:
        utcnow = datetime.utcnow()
        alg = 'RS256'
        payload = {
            'typ': 'JWT',
            'alg': alg,
            'iat': utcnow,
            'exp': utcnow + timedelta(seconds=30),
            'iss': self._app_id,
        }
        return jwt.encode(payload, self._pem, algorithm=alg).decode('utf-8')

    def installations(self) -> Installation:
        return Installation(self._jwt_header)

    def issues(self, owner: str, repo: str) -> Issue:
        return Issue(self._token_header, owner=owner, repo=repo)

    def project_cards(self, column_id):
        return ProjectCard(self._token_header, column_id=column_id)
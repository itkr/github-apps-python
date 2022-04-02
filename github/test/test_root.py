import os
import unittest
import yaml

from nose.tools import eq_

from github.app import GitHubApp


class TestRoot(unittest.TestCase):

    def setUp(self):
        try:
            path = os.path.join(os.path.dirname(__file__), 'env.yaml')
            with open(path) as f:
                os.environ.update(yaml.load(f))
        except FileNotFoundError as e:
            print('aaa')
            pass

        envs = {
            'GITHUB_APP_ID': int,
            'GITHUB_APP_INSTALLATION_ID': int,
            'GITHUB_APP_PEM': str,
            'GITHUB_ORGANIZATION_NAME': str,
            'GITHUB_REPOSITORY_NAME': str,
            'GITHUB_REPOSITORY_PROJECT_COLUMN_ID': str,
        }
        for env_name, env_type in envs.items():
            setattr(self, env_name, env_type(os.getenv(env_name)))

    def tearDown(self):
        pass

    def test_root(self):

        app = GitHubApp(
            self.GITHUB_APP_PEM,
            self.GITHUB_APP_ID,
            self.GITHUB_APP_INSTALLATION_ID)
        issues = app.issues(
            self.GITHUB_ORGANIZATION_NAME,
            self.GITHUB_REPOSITORY_NAME)
        eq_(int, type(len(issues.list())))

        eq_(1, 1)


if __name__ == '__main__':
    unittest.main()

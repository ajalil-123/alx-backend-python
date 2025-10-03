#!/usr/bin/env python3
"""Module function that inherits from unittest.TestCase"""

import unittest
import requests
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for the GithubOrgClient class.
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"repos_url": "dummy_url"})
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        Parameters:
            - org_name: The organization name.
        """
        client = GithubOrgClient(org_name)

        # Access org property
        result = client.org

        # Assert that get_json is called once with the expected args
        mock_get_json.assert_called_once_with(client.ORG_URL.format(
            org=org_name))

        # Assert that the result is a dictionary
        self.assertIsInstance(result, dict)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test the GithubOrgClient._public_repos_url property.

        This method mocks the GithubOrgClient.org method and tests
        that the result of _public_repos_url is the expected one based
        on the mocked payload.
        """
        # Known payload to be returned by the mocked org method
        mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/example/repos"
        }
        client = GithubOrgClient("example")

        result = client._public_repos_url

        expected_url = "https://api.github.com/orgs/example/repos"

        self.assertEqual(result, expected_url)

    @patch('client.get_json', return_value={"repos": [
        {"name": "repo1"}, {"name": "repo2"}]})
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test GithubOrgClient.public_repos.

        This method mocks get_json and _public_repos_url to test that the list
        of repos is what you expect from the chosen payload. It also tests
        that the mocked property and the mocked get_json were called once.
        """
        mock_public_repos_url.return_value = ("https://api.github.com/orgs/example/repos")
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("example")
        result = client.public_repos()
        expected_result = ["repo1", "repo2"]
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/example/repos"
        )
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({'license': {}}, 'my_license', False),
        ({}, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test GithubOrgClient.has_license.

        This method parametrizes the test with different inputs to
        test the has_license method with various scenarios.
        """
        # Call the has_license method
        result = GithubOrgClient.has_license(repo, license_key)

        # Assert that the result matches the expected value
        self.assertEqual(result, expected_result)


@parameterized_class(
        ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
        [(TEST_PAYLOAD[0])]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test case for the GithubOrgClient class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method to mock requests.get and provide fixtures.
            - org_payload: Fixture for organization payload.
            - repos_payload: Fixture for repositories payload.
            - expected_repos: Fixture for expected repositories.
            - apache2_repos: Fixture for repositories with Apache2 license.
        """
        cls.get_patcher = patch('requests.get')

        # Start the patcher and set side_effect for requests.get(url).json()
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
                Mock(json=lambda: cls.org_payload),
                Mock(json=lambda: cls.repos_payload),
                Mock(json=lambda: cls.expected_repos),
                Mock(json=lambda: cls.apache2_repos),
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method to stop the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """
        Test the GithubOrgClient.public_repos method in an integration test.
        """
        client = GithubOrgClient("Safaricom")
        # Call the public_repos method
        result = client.public_repos()

        # Assert that the result matches the expected_repos fixture
        self.assertEqual(result, self.expected_repos)

    def test_public_repos(self):
        """
        Test the public_repos method without specifying a license
        """
        client = GithubOrgClient("Safaricom")
        with patch('client.get_json', side_effect=[self.org_payload, self.repos_payload, self.expected_repos]):
            result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the public_repos method with a specified license
        """
        client = GithubOrgClient("Safaricom")
        with patch('client.get_json', side_effect=[self.org_payload, self.repos_payload, self.apache2_repos]):
            result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
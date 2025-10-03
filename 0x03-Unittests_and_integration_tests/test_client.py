#!/usr/bin/env python3
"""Unittests and Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"repos_url": "dummy_url"})
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        client = GithubOrgClient(org_name)
        result = client.org

        # Ensure get_json was called with correct URL
        mock_get_json.assert_called_once_with(
            client.ORG_URL.format(org=org_name)
        )
        # Ensure result is a dict
        self.assertIsInstance(result, dict)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property."""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/example/repos"
        }
        client = GithubOrgClient("example")
        result = client._public_repos_url
        self.assertEqual(
            result,
            "https://api.github.com/orgs/example/repos"
        )

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test the public_repos method."""
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/example/repos"
        )
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        client = GithubOrgClient("example")
        result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/example/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({'license': {}}, 'my_license', False),
        ({}, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test has_license with multiple scenarios."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


# ---------------- Integration Tests ---------------- #

@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [TEST_PAYLOAD[0]]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class.
    """

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and set side_effect for JSON responses."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if "orgs" in url and "repos" not in url:
                return Mock(json=lambda: cls.org_payload)
            elif "repos" in url:
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos."""
        client = GithubOrgClient("example")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license."""
        client = GithubOrgClient("example")

        result = client.public_repos(license="apache-2.0")
        expected = [repo["name"] for repo in self.repos_payload
                    if repo.get("license", {}).get("key") == "apache-2.0"]

        self.assertEqual(result, expected)
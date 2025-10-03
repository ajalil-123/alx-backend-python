#!/usr/bin/env python3
"""Module function that inherits from unittest.TestCase"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    This class uses parameterized.expand to allow
    multiple sets of inputs and their corresponding
    expected results
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Test the access_nested_map function with various inputs.

        Parameters:
            - nested_map: A nested map.
            - path: A sequence of keys representing a path to the value.
            - expected_result: The expected result when accessing the
            nested map.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises a KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """
    class TestGetJson that checks that the output of get_json
    is equal to the test_payload.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that utils.get_json returns the expected result using mocked
        HTTP calls

        Parameters:
            - test_url: The URL to test.
            - test_payload: The expected JSON payload.
        """
        # Mock the response of requests.get
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert that the mocked get method was called exactly once
        # with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert that the output of get_json is equal to test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test case for the memoize decorator.
    """
    class TestClass:
        """
        Test class containing methods to demonstrate memoization.
        """
        def a_method(self):
            """
            A method returning a constant value (42).
            """
            return 42

        @memoize
        def a_property(self):
            """
            A memoized property that calls the a_method.
            """
            return self.a_method()

    @patch('test_utils.TestMemoize.TestClass.a_method')
    def test_memoize(self, mock_a_method):
        """
        Test the memoize decorator by mocking a_method and
        checking the behavior of a_property.
        """
        mock_a_method.return_value = 42
        test_obj = self.TestClass()
        # Access a_property multiple times
        result1 = test_obj.a_property
        result2 = test_obj.a_property

        # Assert that a_method is called only once
        self.assertEqual(mock_a_method.call_count, 1)

        # Assert that the results are correct
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)

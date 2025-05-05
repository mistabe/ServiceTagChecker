import ipaddress
import json
import unittest
from datetime import datetime
from unittest.mock import mock_open, patch

from servicetags import (
    is_in_prefix,
    jsonfiledate,
    loadjson,
    resolve_ip,
    validate_ipaddress,
)


class TestServiceTagParser(unittest.TestCase):

    @patch("builtins.print")
    def test_jsonfiledate(self, mock_print):
        jsonfiledate()
        mock_print.assert_called_with("Service Tags published on:", "February 03, 2025")

    @patch("builtins.open", new_callable=mock_open, read_data='{"values": []}')
    def test_loadjson(self, mock_file):
        expected_output = {"values": []}
        self.assertEqual(loadjson(), expected_output)
        mock_file.assert_called_with(
            "ServiceTags_Public_20250303.json", mode="r", encoding="us-ascii"
        )

    @patch("sys.exit")
    @patch("builtins.print")
    def test_validate_ipaddress_valid(self, mock_print, mock_exit):
        validate_ipaddress("192.168.1.1")
        mock_print.assert_called_with("The address", "192.168.1.1", "is valid")
        mock_exit.assert_not_called()

    @patch("sys.exit")
    @patch("builtins.print")
    def test_validate_ipaddress_invalid(self, mock_print, mock_exit):
        validate_ipaddress("999.999.999.999")
        mock_print.assert_called_with("The address", "999.999.999.999", "is invalid")
        mock_exit.assert_called_once_with(1)

    def test_is_in_prefix_match(self):
        result = is_in_prefix("192.168.1.1", "192.168.1.0/24")
        self.assertEqual(result, "192.168.1.1")

    def test_is_in_prefix_no_match(self):
        result = is_in_prefix("10.0.0.1", "192.168.1.0/24")
        self.assertIsNone(result)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"values": [{"name": "TestTag", "properties": {"addressPrefixes": ["192.168.1.0/24"]}}]}',
    )
    @patch("builtins.print")
    def test_resolve_ip_match(self, mock_print, mock_file):
        result = resolve_ip("192.168.1.1")
        self.assertIn("in the ServiceTag: TestTag", result)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"values": [{"name": "TestTag", "properties": {"addressPrefixes": ["10.0.0.0/24"]}}]}',
    )
    @patch("builtins.print")
    def test_resolve_ip_no_match(self, mock_print, mock_file):
        result = resolve_ip("192.168.1.1")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
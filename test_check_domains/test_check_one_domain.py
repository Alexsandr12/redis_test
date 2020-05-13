import unittest
from unittest.mock import patch
from check_domains import check_one_domain


class TestCheckOneDomain(unittest.TestCase):
    def setUp(self) -> None:
        redis_conn_patcher = patch("check_domains.redis_conn")
        self.redis_conn_mock = redis_conn_patcher.start()
        self.addCleanup(redis_conn_patcher.stop)

        get_whois_patcher = patch("check_domains._get_whois")
        self.get_whois_mock = get_whois_patcher.start()
        self.addCleanup(get_whois_patcher.stop)

    def test_check_data_true(self) -> None:
        self.redis_conn_mock.get.return_value = b'True'
        
        result = check_one_domain('')

        self.assertTrue(result)

    def test_check_data_false(self) -> None:
        self.redis_conn_mock.get.return_value = b'False'

        result = check_one_domain('')

        self.assertFalse(result)

    def test_check_data_none(self) -> None:
        self.redis_conn_mock.get.return_value = None

        self.get_whois_mock.return_value = "created:"

        result = check_one_domain('')

        self.assertTrue(result)

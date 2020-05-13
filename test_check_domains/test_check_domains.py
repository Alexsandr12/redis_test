import unittest
from unittest.mock import patch
from check_domains import check_domains


class TestCheckDomains(unittest.TestCase):
    def setUp(self) -> None:
        redis_conn_patcher = patch("check_domains.redis_conn")
        self.redis_conn_mock = redis_conn_patcher.start()
        self.addCleanup(redis_conn_patcher.stop)

    def test_dict_dnames(self) -> None:
        self.redis_conn_mock.get.return_value = b'True'

        result = check_domains(['reg.ru', 'kavo.ru'])

        self.assertDictEqual(result, {'reg.ru': True, 'kavo.ru': True})

    def test_dict_dnames(self) -> None:
        self.redis_conn_mock.get.return_value = b'False'

        result = check_domains(['reg.ru', 'kavo.ru'])

        self.assertDictEqual(result, {'reg.ru': False, 'kavo.ru': False})
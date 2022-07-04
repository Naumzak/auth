import unittest
from unittest import main
from unittest.mock import MagicMock, patch, Mock

import testApp.views
from testApp.only_for_test import func_one, func_two
from testApp.my_funcs import upadate_minidescription, list_to_dict
from django.test import RequestFactory, TestCase


class TestMyFunc(unittest.TestCase):
    def test_upadate_minidescription_1(self):
        self.assertEqual(upadate_minidescription('test text'), 'test text')

    def test_upadate_minidescription_2(self):
        self.assertEqual(upadate_minidescription('test text default second test text'), 'second test text')

    def test_list_to_dict_1(self):
        value = ['ProductDimensions:24.5x32.5x3.5inches', 'ItemWeight:3pounds',
                 'ShippingWeight:3.2pounds(Viewshippingratesandpolicies)',
                 'DomesticShipping:ItemcanbeshippedwithinU.S.',
                 'InternationalShipping:ThisitemcanbeshippedtoselectcountriesoutsideoftheU.S.LearnMore',
                 'ASIN:B004K4IBGM', 'Itemmodelnumber:TOP3847', 'Manufacturerrecommendedage:4-18years']
        finish_value = ['24.5x32.5x3.5inches', '3pounds', '3.2pounds(Viewshippingratesandpolicies)',
                        'ItemcanbeshippedwithinU.S.', 'ThisitemcanbeshippedtoselectcountriesoutsideoftheU.S.LearnMore',
                        '4-18years']

        self.assertEqual(list_to_dict(value), finish_value)


mocked_func_one_1 = Mock(return_value=2)
mocked_func_one_2 = Mock(return_value='a')


class TestMock(unittest.TestCase):
    @patch('testApp.only_for_test.func_one', mocked_func_one_1)
    def test_func_two_1(self):
        self.assertEqual(func_two(2), 8)

    @patch('testApp.only_for_test.func_one', mocked_func_one_2)
    def test_func_two_2(self):
        with self.assertRaises(TypeError) as ex:
            func_two('a')


def db_mock(*args, **kwargs):
    return [{'test': 123}]


def total_price_mock(*args, **kwargs):
    return 1000


def authenticate_true_mock(*args, **kwargs):
    return True


def authenticate_none_mock(*args, **kwargs):
    return None


def login_mock(*args, **kwargs):
    return True


class ViewsTest(TestCase):
    def test_user_admin(self):
        response = self.client.get('/user_admin')
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    @patch('testApp.views.login', login_mock)
    @patch('testApp.views.authenticate', authenticate_true_mock)
    def test_login_post_1(self):
        response = self.client.post('/login', {'username': "test_name", "password": "test_password"})
        self.assertEqual(response.status_code, 200)

    @patch('testApp.views.authenticate', authenticate_none_mock)
    def test_login_post_2(self):
        response = self.client.post('/login', {'username': "test_name", "password": "test_password"})
        self.assertEqual(response.status_code, 200)

    @patch('testApp.views.dbconnect.get_data', db_mock)
    def test_search(self):
        response = self.client.get('/search/1')
        self.assertEqual(response.status_code, 200)

    @patch('testApp.views.dbconnect.get_data', db_mock)
    @patch('testApp.views.made_basket.total_price', total_price_mock)
    def test_category(self):
        response = self.client.get('/category/test_category_name/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    main()

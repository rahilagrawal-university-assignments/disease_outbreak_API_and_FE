import requests
import unittest
import json

baseUrl = 'http://bearhouse-disease.azurewebsites.net/disease'
# baseUrl = 'http://127.0.0.1:5000/disease'


class TestStringMethods(unittest.TestCase):

    # Error Cases

    def test_no_paramater(self):
        response = requests.get(url=f'{baseUrl}')
        self.assertEqual(response.status_code, 404)

    def test_date_range_incorrect(self):
        response = requests.get(url=f'{baseUrl}?start_date=2018-05-25&end_date=2018-05-20')
        self.assertEqual(response.status_code, 404)

    def test_date_range_only(self):
        response = requests.get(url=f'{baseUrl}?start_date=2018-05-01&end_date=2018-05-20')
        self.assertEqual(response.status_code, 404)

    # Success Scenarios

    def test_location(self):
        response = requests.get(url=f'{baseUrl}?location=Australia')
        self.assertEqual(type(response.json()), type([]), "Is a List")
        self.assertGreaterEqual(len(response.json()), 0, "Length is greater or equal to 0")
        self.assertEqual(response.status_code, 200, "Status Code is 200")

    def test_disease(self):
        response = requests.get(url=f'{baseUrl}?disease=Ebola')
        self.assertEqual(type(response.json()), type([]), "Is a List")
        self.assertGreaterEqual(len(response.json()), 0, "Length is greater or equal to 0")
        self.assertEqual(response.status_code, 200, "Status Code is 200")

    def test_location_and_disease(self):
        response = requests.get(url=f'{baseUrl}?location=Australia&disease=Ebola')
        self.assertEqual(type(response.json()), type([]), "Is a List")
        self.assertGreaterEqual(len(response.json()), 0, "Length is greater or equal to 0")
        self.assertEqual(response.status_code, 200, "Status Code is 200")

    def test_date_range_disease(self):
        response = requests.get(url=f'{baseUrl}?disease=Ebola&start_date=2018-05-01&end_date=2018-05-30')
        self.assertEqual(type(response.json()), type([]), "Is a List")
        self.assertGreaterEqual(len(response.json()), 0, "Length is greater or equal to 0")
        self.assertEqual(response.status_code, 200, "Status Code is 200")

    def test_date_range_location(self):
        response = requests.get(url=f'{baseUrl}?location=Australia&start_date=2018-05-01&end_date=2018-05-30')
        self.assertEqual(type(response.json()), type([]), "Is a List")
        self.assertGreaterEqual(len(response.json()), 0, "Length is greater or equal to 0")
        self.assertEqual(response.status_code, 200, "Status Code is 200")

    def test_date_range_disease_and_location(self):
        response = requests.get(
            url=f'{baseUrl}?location=Australia&disease=Ebola&start_date=2018-05-01&end_date=2018-05-30')
        self.assertEqual(type(response.json()), type([]), "Is a List")
        self.assertGreaterEqual(len(response.json()), 0, "Length is greater or equal to 0")
        self.assertEqual(response.status_code, 200, "Status Code is 200")


if __name__ == '__main__':
    unittest.main()

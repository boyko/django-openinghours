from rest_framework.test import APITestCase
from openinghours.formats import parse_rules
from openinghours.models import Rule
from django.urls import reverse
from rest_framework import status
from django_dynamic_fixture import G


class TestModel(APITestCase):
    @classmethod
    def setUp(cls):
        cls.facebook_data = {'mon_1_open': '08:30', 'tue_1_open': '08:30',
                             'mon_2_open': '22:10', 'mon_2_close': '22:45',
                             'sun_1_open': '08:30', 'sat_1_close': '22:00',
                             'sun_1_close': '22:00', 'sat_1_open': '08:30', 'wed_1_open': '08:30',
                             'thu_1_open': '08:30',
                             'mon_1_close': '22:00', 'thu_1_close': '22:00', 'tue_1_close': '22:00',
                             'wed_1_close': '22:00',
                             'fri_1_close': '22:00', 'fri_1_open': '08:30'}

    def test_facebook_parser(self):
        parsed_rules = parse_rules(self.facebook_data)

        self.assertTrue({'open': '08:30', 'nr': '1', 'day': 'fri', 'close': '22:00'} in parsed_rules)
        self.assertTrue({'open': '08:30', 'day': 'mon', 'close': '22:00', 'nr': '1'} in parsed_rules)
        self.assertTrue({'open': '22:10', 'day': 'mon', 'close': '22:45', 'nr': '2'} in parsed_rules)

    def test_create_instances_from_facebook_data(self):
        Rule.objects.create_from_facebook_data(self.facebook_data)
        assert False

    def test_create_rule_from_raw_data(self):
        raw_data = {'open': '22:10', 'day': 'mon', 'close': '22:45', 'nr': '2'}
        rule = Rule.objects.create(**raw_data)
        rule.save()


class TestOpeningHoursApi(APITestCase):
    @classmethod
    def setUp(cls):
        cls.rule1 = G(Rule, day='mon', open='8:30', close='22:30')
        pass

    def list_url(self):
        return reverse('rule-list')

    def detail_url(self, id):
        return reverse('rule-detail', id)

    def test_get_object(self):
        pass

    def test_get_list(self):
        resp = self.client.get(self.list_url())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_post_object(self):
        resp = self.client.post(self.list_url(), data={
            'day': 'mon', 'nr': 1, 'open': '7:30', 'close': '10:01'
        })

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_malformed(self):
        resp_malformed_time = self.client.post(self.list_url(), data={
            'day': 'mon', 'nr': 1, 'open': 'abc', 'close': '11'
        })

        self.assertEqual(resp_malformed_time.status_code, status.HTTP_400_BAD_REQUEST)

        resp_malformed_range = self.client.post(self.list_url(), data={
            'day': 'mon', 'nr': 1, 'open': '23:12', 'close': '9:00'
        })

        self.assertEqual(resp_malformed_range.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_day(self):
        resp = self.client.post(self.list_url(), data={
            'day': 'XXX', 'nr': 1, 'open': '23:12', 'close': '9:00'
        })

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_bulk(self):
        data = [
            {'day': 'mon', 'nr': 1, 'open': '8:30', 'close': '19:00'},
            {'day': 'tue', 'nr': 1, 'open': '8:30', 'close': '19:00'},
        ]

        resp = self.client.post(self.list_url(), data=data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        assert False

    def test_put_bulk(self):
        assert False

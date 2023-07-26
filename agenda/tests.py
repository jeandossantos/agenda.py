from rest_framework.test import APITestCase, APIClient
from rest_framework import HTTP_HEADER_ENCODING
import json
from datetime import datetime, timedelta, timezone
import base64

from agenda.models import Agendamento
from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth
import requests
from requests.auth import HTTPBasicAuth


class TestListagemAgendamento(APITestCase):

    def setUp(self) -> None:
        self.username = "test-list"
        self.email = "test-list@gmail.com"
        self.password = "94198380"
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email)

    def test_list_vazia(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(
            f'/api/agendamentos/?username={self.username}',
        ).json()

        self.assertEqual(response, [])

    def test_list_not_empty(self):

        request_data = {
            "data_horario": datetime(2023, 12, 26, tzinfo=timezone.utc),
            "nome_cliente": "Diego Fernandes",
            "email_cliente": "diego3g@hotmail.com",
            "telefone_cliente": "70809040",
            "prestador": self.user
        }

        Agendamento(**request_data).save()

        self.client.login(username=self.username, password=self.password)

        response = self.client.get(
            'http://localhost:8000/api/agendamentos/?username=' + self.username, format='json')

        data_length = len(json.loads(response.content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_length, 1)


class TestCreateAgendamento(APITestCase):
    def setUp(self) -> None:
        self.username = "test-list"
        self.email = "test-list@gmail.com"
        self.password = "94198380"
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email)

    def test_create_agendamento(self):
        current_date = datetime.now()
        data_horario = datetime(current_date.year + 1,
                                2, 10, 13, 30, tzinfo=timezone.utc).isoformat()

        request_data = {
            "data_horario": data_horario,
            "nome_cliente": "Diego Fernandes",
            "email_cliente": "diego3g@hotmail.com",
            "telefone_cliente": "70809040",
            "prestador": self.username
        }

        response = self.client.post('/api/agendamentos/', request_data)

        print(response.json())
        self.assertEqual(response.status_code, 201)

        obj_from_db = Agendamento.objects.get()

        self.assertDictEqual(
            {
                "data_horario": obj_from_db.data_horario.isoformat(),
                "nome_cliente": obj_from_db.nome_cliente,
                "email_cliente": obj_from_db.email_cliente,
                "telefone_cliente": obj_from_db.telefone_cliente,
                "prestador": obj_from_db.prestador.username
            },
            request_data
        )

    def test_not_create_agendamento(self):
        response = self.client.post('/api/agendamentos/', {})

        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data, {
                'data_horario': ['This field is required.'],
                'nome_cliente': ['This field is required.'],
                'email_cliente': ['This field is required.'],
                'telefone_cliente': ['This field is required.'],
                'prestador': ['This field is required.']
            })


class classTestGetHorarios(APITestCase):
    def return_empty_list_if_date_is_holiday(self):
        response = self.client.get(
            '/api/horarios/?data=2023-12-25'
        )

        self.assertEqual(response.data, [])

    def return_available_days_if_is_not_a_holiday(self):
        response = self.client.get(
            '/api/horarios/?data=2028-12-20'
        )

        self.assertEqual(response.data[0], datetime(
            2028, 12, 20, 9, tzinfo=timezone.utc))
        self.assertEqual(
            response.data[-1], datetime(2028, 12, 20, 18, tzinfo=timezone.utc))

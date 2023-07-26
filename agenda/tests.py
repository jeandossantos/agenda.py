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

        current_date = datetime.utcnow()
        data_horario = timedelta(days=3) + current_date

        request_data = {
            "data_horario": data_horario.isoformat(),
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

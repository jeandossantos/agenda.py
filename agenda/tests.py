from unittest import mock
from rest_framework.test import APITestCase
import json
from datetime import datetime, timezone

from agenda.models import Agendamento
from django.contrib.auth.models import User


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

    def test_not_create_agendamento_with_passed_date(self):
        data_horario = datetime(2020, 2, 10, 13, 30, tzinfo=timezone.utc)

        request_data = {
            "data_horario": data_horario.isoformat(),
            "nome_cliente": "Diego Fernandes",
            "email_cliente": "diego3g@hotmail.com",
            "telefone_cliente": "70809040",
            "prestador": self.username
        }

        response = self.client.post('/api/agendamentos/', request_data)

        assert response.status_code == 400
        assert response.json() == {
            "data_horario": [
                "Agendamento não pode ser feito no passado!"
            ]
        }


class TestGetHorarios(APITestCase):
    @mock.patch('agenda.libs.brasil_api.is_feriado', return_value=True)
    def test_return_empty_list_if_date_is_holiday(self, _):
        response = self.client.get(
            '/api/horarios/?data=2023-12-20'
        )

        self.assertEqual(response.data, [])

    @mock.patch('agenda.libs.brasil_api.is_feriado', return_value=False)
    def test_return_available_days_if_is_not_a_holiday(self, _):
        response = self.client.get(
            '/api/horarios/?data=2028-12-20'
        )

        self.assertEqual(response.data[0], datetime(
            2028, 12, 20, 9, tzinfo=timezone.utc))
        self.assertEqual(
            response.data[-1], datetime(2028, 12, 20, 18, tzinfo=timezone.utc))

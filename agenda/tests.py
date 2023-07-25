from rest_framework.test import APITestCase

import json
from datetime import datetime, timedelta, timezone

from agenda.models import Agendamento


class TestListagemAgendamento(APITestCase):
    def test_list_vazia(self):
        response = self.client.get('/api/agendamentos/').json()

        self.assertEqual(response, [])

    def test_list_not_empty(self):
        current_date = datetime.now()
        data_horiario = timedelta(days=3) + current_date

        request_data = {
            "data_horario": data_horiario.isoformat(),
            "nome_cliente": "Diego Fernandes",
            "email_cliente": "diego3g@hotmail.com",
            "telefone_cliente": "70809040"
        }

        agendamento = self.client.post(
            '/api/agendamentos/', request_data)

        self.assertEqual(agendamento.status_code, 201)

        response = self.client.get('/api/agendamentos/')

        data_length = len(json.loads(response.content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_length, 1)


class TestCreateAgendamento(APITestCase):
    def test_create_agendamento(self):
        current_date = datetime.now()
        data_horario = timedelta(days=3) + current_date

        request_data = {
            "data_horario": data_horario.isoformat(),
            "nome_cliente": "Diego Fernandes",
            "email_cliente": "diego3g@hotmail.com",
            "telefone_cliente": "70809040"
        }

        response = self.client.post('/api/agendamentos/', request_data)

        self.assertEqual(response.status_code, 201)

        obj_from_db = Agendamento.objects.get()

        request_data["data_horario"] = datetime(
            data_horario.year, data_horario.month, data_horario.day,
            data_horario.hour, data_horario.minute, data_horario.second, data_horario.microsecond, tzinfo=timezone.utc
        ).isoformat()

        self.assertDictEqual(
            {
                "data_horario": obj_from_db.data_horario.isoformat(),
                "nome_cliente": obj_from_db.nome_cliente,
                "email_cliente": obj_from_db.email_cliente,
                "telefone_cliente": obj_from_db.telefone_cliente
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
                'prestador': ''
            })

from datetime import date
import requests as request
from django.conf import settings
import logging


def is_feriado(data: date) -> bool:
    """Verifica se o dia informado é um feriado."""
    logging.info(f"fazendo requisição para brasil_api com data {data}")

    if settings.TESTING == True:
        logging.info(f"requisição não feita: TESTING=TRUE {data}")
        if data.day == 25 and data.month == 12:
            logging.error('Algum erro ocorreu ao acessar Brasil API.')
            return False

        return False

    ano = data.year
    URL = "https://brasilapi.com.br/api/feriados/v1/{0}".format(ano)

    response = request.get(URL)

    if response.status_code != 200:
        raise ValueError('Não foi possível consultar os feriados.')

    feriados = response.json()

    for feriado in feriados:
        data_feriado = date.fromisoformat(feriado["date"])

        if data == data_feriado:
            return True

    return False

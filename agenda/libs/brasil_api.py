from datetime import date
import requests as request
from django.conf import settings


def is_feriado(data: date) -> bool:
    """Verifica se o dia informado é um feriado."""

    if settings.TESTING == True:
        if data.day == 25 and data.month == 12:
            return True

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

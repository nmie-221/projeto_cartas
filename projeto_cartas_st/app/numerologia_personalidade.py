from datetime import date
from typing import Tuple

def sum_date_components(birth_date: date) -> int:
    """Soma dia + mês + ano (ex.: 16/04/2001 -> 16 + 4 + 2001 = 2021)."""
    return birth_date.day + birth_date.month + birth_date.year

def digit_sum(n: int) -> int:
    """Soma os dígitos de um inteiro (ex.: 2021 -> 2+0+2+1 = 5)."""
    return sum(int(d) for d in str(abs(int(n))))

def reduce_to_limit(n: int, limit: int = 22) -> int:
    """
    Reduz somando os dígitos repetidamente até que o resultado seja <= limit.
    Ex.: se > 22, reduz novamente.
    """
    r = digit_sum(n)
    while r > limit:
        r = digit_sum(r)
    return r

def calcula_personalidade(birth_date: date) -> Tuple[int, int]:
    """
    Retorna (raw_sum, reduced_value) onde:
    raw_sum = dia + mês + ano
    reduced_value = redução por dígitos até <= 22
    """
    raw = sum_date_components(birth_date)
    reduced = reduce_to_limit(raw, limit=22)
    return raw, reduced

def calcula_alma(birth_date: date) -> Tuple[int, int, int]:
    """
    Usa calcula_personalidade e calcula o 'número final' da personalidade.
    Retorna (raw_sum, reduced_value, final_single_digit).
    - Se reduced_value < 10 -> final = reduced_value
    - Se >= 10 -> reduz somando os dígitos repetidamente até obter um dígito (<10).
    Ex.: raw=2021, reduced=14 -> final=1+4=5
    """
    raw, reduced = calcula_personalidade(birth_date)
    final = reduced
    while final >= 10:
        final = digit_sum(final)
    return raw, reduced, final

def calcula_fator_oculto(birth_date: date) -> Tuple[int, int]:
    """
    Calcula o Fator Oculto somando TODOS os dígitos da data (ddmmaaaa).
    Ex.: 16/04/2001 -> digits "16042001" -> 1+6+0+4+2+0+0+1 = 14
    Se o resultado for > 22, reduz somando os dígitos até <= 22.
    Retorna (raw_digit_sum, reduced_value).
    """
    s = birth_date.strftime("%d%m%Y")  # garante zeros à esquerda
    raw = sum(int(ch) for ch in s if ch.isdigit())
    reduced = reduce_to_limit(raw, limit=22) if raw > 22 else raw
    return raw, reduced

def calcula_energia_ano(day: int, month: int, year: int) -> Tuple[int, int]:
    """
    Calcula o Fator Oculto somando TODOS os dígitos (ddmmaaaa) com ano passado como parâmetro.
    Ex.: day=16, month=4, year=2001 -> digits "16042001" -> 1+6+0+4+2+0+0+1 = 14
    Se o resultado for > 22, reduz somando os dígitos até <= 22.
    Retorna (raw_digit_sum, reduced_value).
    """
    s = f"{day:02d}{month:02d}{year:04d}"  # formata com zeros à esquerda
    raw = sum(int(ch) for ch in s if ch.isdigit())
    reduced = reduce_to_limit(raw, limit=22) if raw > 22 else raw
    return raw, reduced

import socket
from typing import List, Dict

import redis

from config import TIMEOUT, PORT, WHOIS_SERVER, EXPIRED_RECORD

redis_conn = redis.Redis()


def _get_whois(dname: str) -> str:
    """Получаем whois доменов с ответственного whois-сервера.

    Args:
        dname: имя домена.

    Returns:
        str: информация whois о домене.
    """
    response = bytes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        sock.connect((WHOIS_SERVER, PORT))
        sock.send(f"{dname}\r\n".encode())
        while True:
            try:
                data = sock.recv(4096)
            except socket.timeout:
                raise Exception

            if data:
                response += data
            else:
                break

    return response.decode("utf-8", "replace")


def _check_availability(dname: str) -> bool:
    """Парсим полученный whois домена.

    Args:
        dname: имя домена.

    Returns:
        bool: Доступность домена. Если домен зарегистрирован, возвращаем True, если нет - False.
    """
    whois_text = _get_whois(dname)
    if "created:" in whois_text:
        return True
    else:
        return False


def check_one_domain(dname: str) -> bool:
    """Проверка доступности одного домена.

    Args:
        dname: имя домена.

    Returns:
        bool: Доступность домена. Если домен зарегистрирован, возвращаем True, если нет - False.
    """
    domain_availability = redis_conn.get(dname)
    print()
    print(domain_availability)
    print()
    if domain_availability is None:
        domain_availability = _check_availability(dname)
        redis_conn.setex(dname, EXPIRED_RECORD, str(domain_availability))
        return domain_availability
    else:
        if domain_availability.decode("utf-8", "replace") == "True":
            return True

        return False


def check_domains(dnames: List[str]) -> Dict[str, bool]:
    """Проверка доступности нескольких доменов.

    Args:
        dnames: список доменов.

    Returns:
        dict: домены и их доступность.
    """
    dict_dnames_availability = {}
    for dname in dnames:
        domain_availability = check_one_domain(dname)
        dict_dnames_availability[dname] = domain_availability
    print(dict_dnames_availability)
    return dict_dnames_availability

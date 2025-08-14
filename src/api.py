import requests
from typing import List, Dict


def fetch_json(url: str, params: dict = {}) -> dict:
    """Вспомогательная функция для GET-запроса к API hh.ru"""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_employers(employer_ids: List[int]) -> List[Dict]:
    """
    Получает информацию о работодателях по их ID
    :param employer_ids: список ID работодателей на hh.ru
    :return: список словарей с данными работодателей
    """
    employers = []
    for eid in employer_ids:
        url = f"https://api.hh.ru/employers/{eid}"
        try:
            data = fetch_json(url)
            employers.append(data)
        except requests.RequestException as e:
            print(f"[!] Ошибка при получении работодателя {eid}: {e}")
    return employers


def get_vacancies(employer_id: int) -> List[Dict]:
    """
    Получает список всех вакансий работодателя
    :param employer_id: ID работодателя на hh.ru
    :return: список словарей с данными вакансий
    """
    url = "https://api.hh.ru/vacancies"
    vacancies = []
    page = 0
    pages = 1  # заранее устанавливаем значение для входа в цикл

    while page < pages:
        params = {
            "employer_id": employer_id,
            "page": page,
            "per_page": 100
        }
        try:
            data = fetch_json(url, params)
            vacancies.extend(data.get("items", []))
            pages = data.get("pages", 1)
            page += 1
        except requests.RequestException as e:
            print(f"[!] Ошибка при получении вакансий {employer_id}: {e}")
            break

    return vacancies

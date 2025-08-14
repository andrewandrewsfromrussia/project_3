import os
import psycopg2
from typing import List, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс для работы с БД hh_db"""

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Список компаний и количество вакансий у каждой"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.id)
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.employer_id
                GROUP BY c.name
                ORDER BY COUNT(v.id) DESC
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Все вакансии: компания, название, зп от, зп до, ссылка"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name, v.salary_from, v.salary_to, v.vacancy_url
                FROM vacancies v
                JOIN companies c ON v.employer_id = c.id
                ORDER BY c.name
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Средняя зарплата (если указана)"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            result = cur.fetchone()
            return result[0] if result and result[0] is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], Optional[int]]]:
        """Вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name, v.salary_from, v.salary_to
                FROM vacancies v
                JOIN companies c ON v.employer_id = c.id
                WHERE (salary_from + salary_to)/2.0 > %s
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, str]]:
        """Вакансии, содержащие ключевое слово в названии"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name, v.vacancy_url
                FROM vacancies v
                JOIN companies c ON v.employer_id = c.id
                WHERE LOWER(v.name) LIKE %s
            """, (f"%{keyword.lower()}%",))
            return cur.fetchall()

    def close(self):
        """Закрыть подключение"""
        self.conn.close()

from psycopg2 import connect, Error
from dotenv import load_dotenv
from os import getenv
import sys

load_dotenv(dotenv_path="config/.env")

db_user = getenv("DB_USER")
db_name = getenv("DB_NAME")
db_pass = getenv("PASSWORD")
db_host = getenv("DB_HOST")
db_port = getenv("DB_PORT")

def insert_student(regno: str, name: str, age: int, marks: float, cgpa: float, grade: str) -> tuple[bool, str]:
    try:
        conn = connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()
        try:
            cur.execute(
                '''INSERT INTO student1
                (regno, name, age, marks, cgpa, grade)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (regno, name, age, marks, cgpa, grade)
            )
            conn.commit()
            return True, "Student added successfully!"
        except Error as e:
            conn.rollback()
            print(f"Database error: {e}", file=sys.stderr)
            return False, "Error inserting data into database!"
        finally:
            cur.close()
    except Error as e:
        return False, "Database connection failed!"
    finally:
        if conn:
            conn.close()


def delete_student(criteria: dict[str, object]) -> tuple[bool, str]:
    if not criteria:
        return False, "No delete criteria provided."

    try:
        conn = connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()
        try:
            conditions = [f"{key} = %s" for key in criteria]
            values = list(criteria.values())
            query = f"DELETE FROM student1 WHERE {' AND '.join(conditions)}"
            cur.execute(query, values)
            conn.commit()
            if cur.rowcount:
                return True, "Record deleted successfully!"
            return False, "Record not found."
        except Error as e:
            conn.rollback()
            print(f"Database error: {e}", file=sys.stderr)
            return False, "Error deleting record."
        finally:
            cur.close()
    except Error:
        return False, "Database connection failed!"
    finally:
        if conn:
            conn.close()
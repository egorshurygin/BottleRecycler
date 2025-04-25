from sqlite3 import *
from random import *
import os


way = r'C:\Users\shury\PycharmProjects\school_project\BottleRecycler\app\TG\identifier.sqlite'
print(way)


def get_lasts() -> set[int]:
    conn = connect(way)
    cur = conn.cursor()
    print(way)
    cur.execute("SELECT DISPLAY_CODE FROM Codes;")
    a = cur.fetchall()
    lasts = set(map(lambda x: int(x[0][2:]), a))
    conn.commit()
    return lasts


def decode_message_from_display(message: str) -> int:  # количество начисленных баллов
    conn = connect(way)
    cur = conn.cursor()
    cur.execute(f"SELECT POINTS FROM Codes WHERE DISPLAY_CODE == '{message}';")
    try:
        a = cur.fetchall()[0]
    except IndexError:
        return int(-1e100)
    cur.execute(f"DELETE FROM Codes WHERE DISPLAY_CODE == '{message}';")
    conn.commit()
    return a[0]


def encode_in_message_on_display(points: int) -> str:
    lasts = get_lasts()
    conn = connect(way)
    cur = conn.cursor()
    s = 'abcdefghijklmnopqrstuvwxyz'
    series = s[randrange(len(s))]
    number = list(set(i for i in range(1000000, 10000000)) - lasts)
    shuffle(number)
    number = number[0]
    code = f'{series}-{number}'
    cur.execute(
        f"INSERT INTO Codes (DISPLAY_CODE, POINTS) VALUES ('{code}', {points});")
    conn.commit()
    return code


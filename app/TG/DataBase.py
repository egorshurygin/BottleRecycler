from sqlite3 import *
from random import *
import os
from app.TG.CodeFromDisplay import way
from app.TG.TG_BOT import agree, agree2, bot


genered_CardID = set()
print(way)


def get_balance_by_telegram_id(tg_id):
    conn = connect(way)
    cur = conn.cursor()
    cur.execute(f"SELECT BALANCE FROM Bottle WHERE TELEGRAM_ID == {tg_id};")
    balance = cur.fetchone()[0]
    conn.commit()
    return balance


def make_new_line_in_database(tg_id):
    global genered_CardID
    conn = connect(way)
    cur = conn.cursor()
    new_CardID = list(set(i for i in range(100000, 1000000)) - genered_CardID)
    rand_pref = list(set(i for i in range(100000, 1000000)))
    shuffle(rand_pref)
    shuffle(new_CardID)
    new_CardID = new_CardID[0]
    print(new_CardID, tg_id)
    # try:
    cur.execute(f"INSERT INTO Bottle (TELEGRAM_ID, CARD_ID) VALUES({tg_id}, {rand_pref[0] * 10 ** 6 + new_CardID});")
    genered_CardID.add(new_CardID)
    # except IntegrityError:
    #    pass
    conn.commit()


def add_to_balance_in_database(tg_id, points):
    conn = connect(way)
    cur = conn.cursor()
    balance = get_balance_by_telegram_id(tg_id) + points
    cur.execute(f"UPDATE Bottle SET BALANCE = {balance} WHERE TELEGRAM_ID == {tg_id};")
    conn.commit()


def get_card_number(tg_id):
    conn = connect(way)
    cur = conn.cursor()
    cur.execute(f"SELECT CARD_ID FROM Bottle WHERE TELEGRAM_ID == {tg_id};")
    card = cur.fetchone()[0]
    conn.commit()
    return card


def get_balance_by_card_id(card_id: str) -> int:
    conn = connect(way)
    cur = conn.cursor()
    cur.execute(f"SELECT BALANCE FROM Bottle WHERE CARD_ID == {card_id};")
    a = cur.fetchone()
    try:
        a = int(a[0])
    except TypeError:
        a = "CardError"
    conn.commit()
    return a


def get_telegram_id_by_card_id(card_id: str) -> int:
    conn = connect(way)
    cur = conn.cursor()
    cur.execute(f"SELECT TELEGRAM_ID FROM Bottle WHERE CARD_ID == {card_id};")
    telegram_id = cur.fetchone()[0]
    conn.commit()
    return telegram_id


def change_balance_by_card_id(card_id, summ):
    conn = connect(way)
    cur = conn.cursor()
    cur.execute(f"SELECT BALANCE FROM Bottle WHERE CARD_ID == {card_id};")
    summ = int(summ)
    try:
        balance = int(cur.fetchone()[0])
    except TypeError:
        return "CardError"
    if balance < summ:
        return "LowBalanceError"
    tg_id = get_telegram_id_by_card_id(card_id)
    mess = f"From your account will be deducted {summ} points."
    #is_confirmed = agree(tg_id, mess)
    # while len(is_confirmed) < 3:
    #    t = ""
    #if not is_confirmed[1]:
    agree(tg_id, mess)
    # return "AgreementError"
    cur.execute(f"UPDATE Bottle SET BALANCE = {balance - summ} WHERE CARD_ID = {card_id};")
    conn.commit()
    return "OK"



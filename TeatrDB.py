# --------------------------------------------------------
# pip install mysql-connector-python
#
import config
import mysql.connector
from mysql.connector import errorcode
import KlientDef
import ImprezaDef
import BiletDef

PUSTY_KLIENT = 1


def init():
    mydb = init_database()
    cursor1 = mydb.cursor()
    init_tabele(cursor1)


def init_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=config.DATABASE_USER,
            password=config.DATABASE_USER_PASSWD,
            database=config.TEATR_DATABASE_NAME,
            buffered=True,
        )
    except  Exception as ex:
        if ex.errno == errorcode.ER_BAD_DB_ERROR:
            print("Brak bazy danych. Zakładam nową.")
            mydb = mysql.connector.connect(
                host="localhost",
                user=config.DATABASE_USER,
                password=config.DATABASE_USER_PASSWD,
                buffered=True,
            )
            create_database(mydb.cursor())


        else:
            print("Bląd inicjalizacji bazy danych:", ex)

    return mydb


def create_database(cursor):
    try:
        print("DB:", cursor)
        sql_txt = "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(config.TEATR_DATABASE_NAME)
        cursor.execute(sql_txt)

    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


TABELA_KLIENT = "klienci"
TABELA_IMPREZ = "imprezy"
TABELA_BILETOW = "bilety"

TABLES = {}
TABLES['klienci'] = (
    "CREATE TABLE `klienci` ("
    "  `klient_no` int(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,"
    "  `name` varchar(60) NOT NULL,"
    "  `forname` varchar(60) NOT NULL,"
    "  `city` varchar(60),"
    "  `street` varchar(60),"
    "  `email`  varchar(60),"
    "  `phone`  varchar(20),"
    "  PRIMARY KEY (`klient_no`)"
    ") ENGINE=InnoDB")

TABLES['imprezy'] = (
    "CREATE TABLE `imprezy` ("
    "  `impreza_no` int(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,"
    "  `nazwa` varchar(60) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `sala` varchar(16) NOT NULL,"
    "  `cena_a` float,"
    "  `cena_b` float,"
    "  `cena_c` float,"
    "  `cena_d` float,"
    "  PRIMARY KEY (`impreza_no`), UNIQUE KEY `nazwa` (`nazwa`)"
    ") ENGINE=InnoDB")

TABLES['bilety'] = (
    "CREATE TABLE `bilety` ("
    "  `bilet_no` int(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,"
    "  `kategoria` varchar(8),"
    "  `rzad` int(11),"
    "  `miejsce` int(11),"
    "  `cena` float,"
    "  `impreza_no` int(11) NOT NULL,"
    "  `klient_no` int(11),"
    "  PRIMARY KEY (`bilet_no`),"
    "  CONSTRAINT fk_impreza FOREIGN KEY (impreza_no) REFERENCES imprezy(impreza_no),"
    "  CONSTRAINT fk_klient FOREIGN KEY (klient_no) REFERENCES klienci(klient_no)"
    ") ENGINE=InnoDB")


# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html


def init_tabele(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Dodaje tabele {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    # dodanie pustego klienta
    klient = KlientDef.Klient()
    if not load_klient(PUSTY_KLIENT, klient):
        klient.imie = 'NULL'
        add_klient(klient)


def init_db():
    mydb = init_database()
    if mydb is not None:
        my_cursor = mydb.cursor()
        init_tabele(my_cursor)
        init_database()
        init_tabele()
        return True
    return False


# ---- tablica klienci ---------

def add_klient(klient):
    db1 = init_database()
    cursor1 = db1.cursor()

    sql = f'INSERT INTO {TABELA_KLIENT} (name, forname, city, street, email, phone) VALUES (%s, %s, %s, %s, %s, %s)'
    val = klient.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()

    cursor1.execute(f"SELECT klient_no FROM {TABELA_KLIENT} WHERE klient_no=LAST_INSERT_ID()")
    myresult = cursor1.fetchall()
    klient.id = myresult[0][0]
    # print('impreza.id=',impreza.id)


def update_klient(klient):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'UPDATE {TABELA_KLIENT} SET name=%s, forname=%s, city=%s, street=%s, email=%s, phone=%s  WHERE klient_no = {klient.id}'
    val = klient.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()
    return cursor1.rowcount == 1


def load_klient(klient_id, klient_obiekt):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT * FROM {TABELA_KLIENT} WHERE klient_no = {klient_id}'
    cursor1.execute(sql)
    myresult = cursor1.fetchall()
    if len(myresult) == 1:
        klient_obiekt.laduj_z_tablicy(myresult[0])
        # print(klient_obiekt)
        return True
    else:
        return False


def delete_klient(klient_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'DELETE FROM {TABELA_KLIENT} WHERE klient_no = {klient_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


def load_klints():
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TABELA_KLIENT} WHERE klient_no<>{PUSTY_KLIENT}")
    myresult = cursor1.fetchall()
    return myresult


# ---- tablica impreza ---------

def add_impreza(impreza):
    db1 = init_database()
    cursor1 = db1.cursor()

    sql = f'INSERT INTO {TABELA_IMPREZ} (nazwa, date, sala, cena_a, cena_b,cena_c,cena_d) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    val = impreza.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()

    cursor1.execute(f"SELECT impreza_no FROM {TABELA_IMPREZ} WHERE impreza_no=LAST_INSERT_ID()")
    myresult = cursor1.fetchall()
    impreza.id = myresult[0][0]
    # print('impreza.id=',impreza.id)


def load_imprezy():
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TABELA_IMPREZ}")
    myresult = cursor1.fetchall()
    return myresult


def update_impreza(impreza):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'UPDATE {TABELA_IMPREZ} SET nazwa=%s, date=%s, sala=%s, cena_a=%s, cena_b=%s,cena_c=%s,cena_d=%s  WHERE impreza_no = {impreza.id}'
    val = impreza.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()
    return cursor1.rowcount == 1


def load_impreza(impreza_id, impreza_obiekt):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT * FROM {TABELA_IMPREZ} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    myresult = cursor1.fetchall()
    if len(myresult) == 1:
        impreza_obiekt.laduj_z_tablicy(myresult[0])
        return True
    else:
        return False


def usun_impreza(impreza_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'DELETE FROM {TABELA_IMPREZ} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


# ---- tablica biletow ---------

def dodaj_bilet(bilet):
    db1 = init_database()
    cursor1 = db1.cursor()
    val = bilet.daj_jako_tablica()
    sql = f'INSERT INTO {TABELA_BILETOW} (kategoria, rzad, miejsce, cena, impreza_no, klient_no) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor1.execute(sql, val)
    db1.commit()


def podmien_bilet(bilet):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'UPDATE {TABELA_BILETOW} SET kategoria=%s, rzad=%s, miejsce=%s, cena=%s, impreza_no=%s, klient_no=%s  WHERE bilet_no = {bilet.id}'
    val = bilet.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()
    return cursor1.rowcount == 1


def usun_bilet(bilet_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'DELETE FROM {TABELA_BILETOW} WHERE bilet_no = {bilet_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


def usun_bilety_z_imprezy(impreza_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'DELETE FROM {TABELA_BILETOW} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


def policz_bilety_z_imprezy(impreza_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT COUNT(*) FROM {TABELA_BILETOW} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    myresult = cursor1.fetchall()
    return myresult[0][0]


def policz_bilety_z_imprezy_dla_kategorii(impreza_id, wszystkie):
    db1 = init_database()
    cursor1 = db1.cursor()

    kategorie = ('A', 'B', 'C', 'D')
    wynik = []
    for k in kategorie:
        if wszystkie:
            sql = f'SELECT COUNT(*) FROM {TABELA_BILETOW} WHERE impreza_no = {impreza_id} AND kategoria = "{k}"'
        else:
            sql = f'SELECT COUNT(*) FROM {TABELA_BILETOW} WHERE impreza_no = {impreza_id} AND kategoria = "{k}" AND klient_no = {PUSTY_KLIENT}'
        cursor1.execute(sql)
        db1.commit()
        myresult = cursor1.fetchall()
        n = myresult[0][0]
        wynik.append([k, n])
    print(wynik)
    return wynik


# ---Test----------------------------------

def _test():
    print("\n\n------Teatr-------")

    mydb = init_database()
    my_cursor = mydb.cursor()

    sql = f"DROP TABLE  IF EXISTS {TABELA_KLIENT}, {TABELA_IMPREZ}, {TABELA_BILETOW}"
    my_cursor.execute(sql)

    init_tabele(my_cursor)

    klient = KlientDef.Klient()
    klient.imie = 'Adam'
    klient.nazwisko = 'Nowak'
    klient.email = 'adam@wp.pl'
    add_klient(klient)

    impreza = ImprezaDef.Impreza()
    impreza.nazwa = 'TSA1'
    impreza.setDateAsStr = '1.1.2026'
    impreza.sala = "Głowna"
    impreza.cena = [10, 9, 8, 4]
    add_impreza(impreza)
    impreza.nazwa = 'TSA2'
    impreza.setDateAsStr = '1.1.2026'
    impreza.sala = "Głowna"
    impreza.cena = [10, 9, 8, 4]
    add_impreza(impreza)

    bilet = BiletDef.Bilet()
    bilet.kategoria = 'A'
    bilet.rzad = 1
    bilet.miejsce = 2
    bilet.cena = 24
    bilet.impreza_id = 1
    bilet.klient_id = 1
    dodaj_bilet(bilet)

    bilet.kategoria = 'A'
    bilet.rzad = 1
    bilet.miejsce = 3
    bilet.cena = 24
    bilet.impreza_id = 1
    bilet.klient_id = 1
    dodaj_bilet(bilet)

    bilet.kategoria = 'A'
    bilet.rzad = 1
    bilet.miejsce = 3
    bilet.cena = 24
    bilet.impreza_id = 1
    bilet.klient_id = 1
    dodaj_bilet(bilet)


if __name__ == "__main__":
    _test()

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


TB_KLIENT = "klienci"
TB_IMPREZA = "imprezy"
TB_BILET = "bilety"

TABLES = {} #słownik
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
    # dodanie pustego klienta - sztuczka
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

    sql = f'INSERT INTO {TB_KLIENT} (name, forname, city, street, email, phone) VALUES (%s, %s, %s, %s, %s, %s)'
    val = klient.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()

    cursor1.execute(f"SELECT klient_no FROM {TB_KLIENT} WHERE klient_no=LAST_INSERT_ID()")
    myresult = cursor1.fetchall()
    klient.id = myresult[0][0]
    # print('impreza.id=',impreza.id)


def update_klient(klient):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'UPDATE {TB_KLIENT} SET name=%s, forname=%s, city=%s, street=%s, email=%s, phone=%s  WHERE klient_no = {klient.id}'
    val = klient.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()
    return cursor1.rowcount == 1


def load_klient(klient_id, klient_obiekt):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT * FROM {TB_KLIENT} WHERE klient_no = {klient_id}'
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
    sql = f'DELETE FROM {TB_KLIENT} WHERE klient_no = {klient_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


def load_klints():
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TB_KLIENT} WHERE klient_no<>{PUSTY_KLIENT}")
    myresult = cursor1.fetchall()
    return myresult


def load_klients_human_mode():
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TB_KLIENT} WHERE klient_no<>{PUSTY_KLIENT}")
    myresult = cursor1.fetchall()
    lista_czytelna = []
    for k in myresult:
        lista_czytelna.append(f'{k[1]} {k[2]}')
    return lista_czytelna


def get_klient_id_by_human_name(name):
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TB_KLIENT} WHERE klient_no<>{PUSTY_KLIENT}")
    myresult = cursor1.fetchall()
    lista_czytelna = []
    for k in myresult:
        item_name = f'{k[1]} {k[2]}'
        if item_name == name:
            return int(k[0])
    return -1


# ---- tablica impreza ---------

def add_impreza(impreza):
    db1 = init_database()
    cursor1 = db1.cursor()

    sql = f'INSERT INTO {TB_IMPREZA} (nazwa, date, sala, cena_a, cena_b,cena_c,cena_d) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    val = impreza.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()

    cursor1.execute(f"SELECT impreza_no FROM {TB_IMPREZA} WHERE impreza_no=LAST_INSERT_ID()")
    myresult = cursor1.fetchall()
    impreza.id = myresult[0][0]
    # print('impreza.id=',impreza.id)


def load_imprezy():
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TB_IMPREZA}")
    myresult = cursor1.fetchall()
    return myresult


def update_impreza(impreza):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'UPDATE {TB_IMPREZA} SET nazwa=%s, date=%s, sala=%s, cena_a=%s, cena_b=%s,cena_c=%s,cena_d=%s  WHERE impreza_no = {impreza.id}'
    val = impreza.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()
    return cursor1.rowcount == 1


def load_impreza(impreza_id, impreza_obiekt):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT * FROM {TB_IMPREZA} WHERE impreza_no = {impreza_id}'
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
    sql = f'DELETE FROM {TB_IMPREZA} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


# ---- tablica biletow ---------

def dodaj_bilet(bilet):
    db1 = init_database()
    cursor1 = db1.cursor()
    val = bilet.daj_jako_tablica()
    sql = f'INSERT INTO {TB_BILET} (kategoria, rzad, miejsce, cena, impreza_no, klient_no) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor1.execute(sql, val)
    db1.commit()


def podmien_bilet(bilet):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'UPDATE {TB_BILET} SET kategoria=%s, rzad=%s, miejsce=%s, cena=%s, impreza_no=%s, klient_no=%s  WHERE bilet_no = {bilet.id}'
    val = bilet.daj_jako_tablica()
    cursor1.execute(sql, val)
    db1.commit()
    return cursor1.rowcount == 1


def usun_bilet(bilet_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'DELETE FROM {TB_BILET} WHERE bilet_no = {bilet_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


def usun_bilety_z_imprezy(impreza_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'DELETE FROM {TB_BILET} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    return cursor1.rowcount == 1


def policz_bilety_z_imprezy(impreza_id, wszystkie):
    db1 = init_database()
    cursor1 = db1.cursor()
    if wszystkie:
        sql = f'SELECT COUNT(*) FROM {TB_BILET} WHERE impreza_no = {impreza_id}'
    else:
        sql = f'SELECT COUNT(*) FROM {TB_BILET} WHERE impreza_no = {impreza_id} and klient_no = {PUSTY_KLIENT}'
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
            sql = f'SELECT COUNT(*) FROM {TB_BILET} WHERE impreza_no = {impreza_id} AND kategoria = "{k}"'
        else:
            sql = f'SELECT COUNT(*) FROM {TB_BILET} WHERE impreza_no = {impreza_id} AND kategoria = "{k}" AND klient_no = {PUSTY_KLIENT}'
        cursor1.execute(sql)
        db1.commit()
        myresult = cursor1.fetchall()
        n = myresult[0][0]
        wynik.append([k, n])
    print(wynik)
    return wynik


def load_bilety_dla_imprezy(impreza_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT * FROM {TB_BILET} WHERE impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    myresult = cursor1.fetchall()
    lista_biletow = []
    for item in myresult:
        bilet = BiletDef.Bilet()
        bilet.laduj_z_tablicy(item)
        lista_biletow.append(bilet)
    return lista_biletow


def load_bilety_dla_imprezy_ex(impreza_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT {TB_BILET}.kategoria, {TB_BILET}.rzad, {TB_BILET}.miejsce, {TB_BILET}.cena, {TB_KLIENT}.name, {TB_KLIENT}.forname FROM {TB_BILET}' \
          f' INNER JOIN {TB_KLIENT} ON {TB_BILET}.klient_no = {TB_KLIENT}.klient_no WHERE {TB_BILET}.impreza_no = {impreza_id}'
    cursor1.execute(sql)
    db1.commit()
    myresult = cursor1.fetchall()
    return myresult


#    bilety_header = ['lp', 'Impreza', "Data", 'Miejsce', 'Cena']
def load_bilety_dla_klienta(klient_id):
    db1 = init_database()
    cursor1 = db1.cursor()
    sql = f'SELECT {TB_IMPREZA}.nazwa, {TB_IMPREZA}.date, {TB_BILET}.kategoria, {TB_BILET}.rzad, {TB_BILET}.miejsce, {TB_BILET}.cena FROM {TB_BILET}' \
          f' INNER JOIN {TB_IMPREZA} ON {TB_BILET}.impreza_no = {TB_IMPREZA}.impreza_no WHERE {TB_BILET}.klient_no = {klient_id}'
    cursor1.execute(sql)
    db1.commit()
    myresult = cursor1.fetchall()
    result = []
    cnt = 0
    for x in myresult:
        cnt += 1
        miejsce_ex = f'{x[2]}R{x[3]}M{x[4]}'
        result.append([cnt, x[0], x[1], miejsce_ex, x[5]])

    return result


def execute_zakup(zakup):
    db1 = init_database()
    cursor1 = db1.cursor()
    for x in zakup.lista:
        rzad = x[0]
        miejsce = x[1]
        sql = f'UPDATE {TB_BILET} SET klient_no={zakup.klient_id}  WHERE impreza_no = {zakup.impreza_id} AND rzad = {rzad} AND miejsce= {miejsce}'
        cursor1.execute(sql)
        db1.commit()
        if cursor1.rowcount != 1:
            return False;
    return True;


# ---Test----------------------------------

def _test():
    print("\n\n------Teatr-------")

    mydb = init_database()
    my_cursor = mydb.cursor()

    sql = f"DROP TABLE  IF EXISTS {TB_KLIENT}, {TB_IMPREZA}, {TB_BILET}"
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


def _test2():
    tickets = load_bilety_dla_imprezy_ex(4)
    for t in tickets:
        print(t)


def _test3():
    tickets = load_bilety_dla_klienta(2)
    for t in tickets:
        print(t)


if __name__ == "__main__":
    _test3()

import mysql.connector
import random
dbconfig = {'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
    'user': 'ich1',
    'password': 'password',   #ich1_password_ilovedbs
    'database': 'sakila'}

dbconfig_requests = {'host': 'mysql.itcareerhub.de',
    'user': 'ich1',
    'password': 'ich1_password_ilovedbs',
    'database': 'project_220424_ptm_Kutuzova'}


def connect_to_db(config):
    connect = mysql.connector.connect(**config)
    return connect

def disconnect_from_db(conn):
    conn.close()


def insert_request(current_request):
    cursor_requests.execute("INSERT INTO requests_statistic (request) VALUES (%s)", (current_request,))
    connection_requests.commit()


def menu_and_choosing():
    print('''        МЕНЮ ПОИСКА:
        * Для выбора фильма по жанрам введите: "C"    
        * Для поиска фильмов по году его выхода на экраны введите: "Y" 
        * Для выбора фильма по жанрам и году выхода введите: "CY"
        * Для поиска фильмов по имени и/или фамилии актера введите: "A" 
        * Для поиска по ключевому слову: "W" 
        * Для вывода топ-5 самых популярных запросов пользователей введите "TOP"
        * Для выхода введите: "STOP" ''')
    choosing = input('Поле для ввода:   ').strip().upper()
    return choosing


def categorie_search(cursor_r):
    print("Выбран поиск по жанрам фильма")
    request_categories = 'SELECT category_id, name FROM category'
    cursor_r.execute(request_categories)
    # insert_request(request)
    categories = cursor_r.fetchall()
    print('+-------+----------------------+')
    print("| {:^5} | {:^20} |".format('ID', 'ЖАНР'))
    print('+-------+----------------------+')

    for id, name in categories:
        print("| {:^5} | {:^20} |".format(id, name))
    print('+-------+----------------------+')

    print()
    ID_choos = input("Введите ID интересующей категории/жанра: ")
    # name_choos = ID_choos
    # print(f'Вы выбрали жанры в категории {name_choos}')
    request_categ = '''SELECT film.title, film.release_year, film.description FROM film 
            JOIN film_category ON film.film_id = film_category.film_id 
            JOIN category ON film_category.category_id = category.category_id 
            WHERE category.category_id={}'''.format(ID_choos)
    cursor_r.execute(request_categ)
    insert_request(request_categ)
    all_categories_request = cursor_r.fetchall()
    return all_categories_request


def year_search(cursor_r):
    print('Выбран поиск по году выхода фильма')
    year_choosing = int(input('Введите год выхода интересующих фильмов: '))
    request_year = '''SELECT film.title, film.release_year, film.description FROM film 
            WHERE film.release_year=('{}')'''.format(year_choosing)
    cursor_r.execute(request_year)
    insert_request(request_year)
    res = cursor_films.fetchall()
    print()
    return res


def category_and_year(cursor_r):
    print("Выбран поиск по жанрам фильма и году выхода на экраны")
    request_categories = 'SELECT category_id, name FROM category'
    cursor_r.execute(request_categories)
    categories = cursor_r.fetchall()
    print('+-------+----------------------+')
    print("| {:^5} | {:^20} |".format('ID', 'ЖАНР'))
    print('+-------+----------------------+')

    for id, name in categories:
        print("| {:^5} | {:^20} |".format(id, name))
    print('+-------+----------------------+')

    print()
    ID_choos = input("Введите ID интересующей категории/жанра: ")
    year_choosing = int(input('Введите год выхода интересующих фильмов: '))

    request_categ = '''SELECT film.title, film.release_year, film.description FROM film 
                JOIN film_category ON film.film_id = film_category.film_id 
                JOIN category ON film_category.category_id = category.category_id 
                WHERE category.category_id={} and film.release_year = {}'''.format(ID_choos, year_choosing)
    cursor_r.execute(request_categ)
    insert_request(request_categ)
    all_categories_request = cursor_r.fetchall()
    return all_categories_request


def all_or_random_print(result_request):
    if result_request:
        answer = input('''Введите цифру "10" для вывода десяти случайных фильмов из подборки, 
любое другое значение пиведет к выводу всех результатов:  ''').strip()
        print()
        if answer == '10':
            res_10 = random.choices(result_request, k=10)  # выбор 10 случайных фильмов из подборки
            print('| {:^30} | {:^10} | {:^130} |'.format('НАЗВАНИЕ ФИЛЬМА', 'ГОД ВЫХОДА', 'ОПИСАНИЕ'))
            for title, year, describtion in res_10:
                print('| {:^30} | {:^10} | {:<130} |'.format(title, year, describtion))
        else:
            print('| {:^30} | {:^10} | {:^130} |'.format('НАЗВАНИЕ ФИЛЬМА', 'ГОД ВЫХОДА', 'ОПИСАНИЕ'))
            for title, year, describtion in result_request:
                print('| {:^30} | {:^10} | {:<130} |'.format(title, year, describtion))
        print()
    else:
        print('Поиск не дал результатов. Попробуйте еще раз.')
        print()

def actor_search(cursor_read):
    res_act = input('Вы выбрали поиск по актерам. Хотите просмотреть список актеров? Y/N: ').upper()
    if res_act == 'Y':
        request_actors = 'SELECT first_name, last_name FROM actor'
        cursor_films.execute(request_actors)
        actors = cursor_films.fetchall()
        print("Список актеров: ")
        for firstname, lastname in actors:
            print(firstname, lastname)

    # if res == 'N'
    print()
    print('Вы выбрали поиск по актерам. Если Вы не знаете имя или фамилию, для пропуска нажмите Enter')
    choosing_actor_firstname = input("Введите имя актера/актрисы: ").upper()
    choosing_actor_lastname = input("Введите фамилию актера/актрисы: ").upper()
    print()
    if choosing_actor_firstname != '' and choosing_actor_lastname != '':
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                    JOIN film_actor ON actor.actor_id=film_actor.actor_id
                    JOIN film ON film.film_id=film_actor.film_id
                    WHERE actor.first_name=('{}') and 
                    actor.last_name=('{}')'''.format(choosing_actor_firstname, choosing_actor_lastname)
        # print(request)
    elif choosing_actor_firstname != '' and choosing_actor_lastname == '':
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                                JOIN film ON film.film_id=film_actor.film_id
                                WHERE actor.first_name=('{}') '''.format(choosing_actor_firstname)
    elif choosing_actor_firstname == '' and choosing_actor_lastname != '':
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                                JOIN film ON film.film_id=film_actor.film_id
                                WHERE actor.last_name=('{}')'''.format(choosing_actor_lastname)
    else:
        print('Данные введены некорректно. Попробуйте снова')
    cursor_read.execute(request_a)
    insert_request(request_a)
    films = cursor_films.fetchall()
    return films, choosing_actor_firstname, choosing_actor_lastname


def actors_print(request_fetchall, firstname, lastname):
    if request_fetchall:
        print(f"Фильмы с {firstname} {lastname}:")
        all_or_random_print(request_fetchall)
    else:
        print(f'Актера {firstname}, {lastname} нет в базе данных')
    print()


def key_word_search(cursor_read):
    print('Выбран поиск по ключевому слову')
    while True:
        key_word = input('Введите слово для поиска (не менее трех символов): ').strip()
        if len(key_word) < 3:
            print('Длина ключевого слова должна быть не менее трех символов')

        else:
            request = '''SELECT film.title, film.release_year, film.description FROM film WHERE (title like '%{}%') 
            or (description like "%{}%")'''.format(key_word, key_word)
            cursor_read.execute(request)
            insert_request(request)
            films = cursor_read.fetchall()
            return films


connection_films = connect_to_db(dbconfig)
cursor_films = connection_films.cursor()

connection_requests = connect_to_db(dbconfig_requests)
cursor_requests = connection_requests.cursor()

print('Добро пожаловать в сервис кинопоиска! Ввод осуществляется латинскими буквами.')
while True:
    user_choosing = menu_and_choosing()

    if user_choosing == 'C':
        res_categories = categorie_search(cursor_films)
        all_or_random_print(res_categories)

    elif user_choosing == 'Y':
        res_years = year_search(cursor_films)
        all_or_random_print(res_years)

    elif user_choosing == 'CY':
        result_CY = category_and_year(cursor_films)
        all_or_random_print(result_CY)

    elif user_choosing == 'A':
        actors = actor_search(cursor_films)
        actors_print(*actors)

    elif user_choosing == 'W':
        key_word_res = key_word_search(cursor_films)
        all_or_random_print(key_word_res)

    elif user_choosing == 'TOP':

        request = '''SELECT request, count(request) as count 
        FROM requests_statistic GROUP BY request ORDER BY count DESC LIMIT 5'''
        cursor_requests.execute(request)
        statistic = cursor_requests.fetchall()
        for request, count in statistic:
            print(f'{request} - {count}')

    elif user_choosing == 'STOP':
        print('Спасибо за использование сервиса по поиску кинофильмов. До новых встреч!')
        break
    else:
        print('Такой команды не существует. Попробуй еще раз.')
        print()

cursor_films.close()
disconnect_from_db(connection_films)

cursor_requests.close()
disconnect_from_db(connection_requests)

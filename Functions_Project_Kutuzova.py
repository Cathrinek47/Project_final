import mysql.connector


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


#Функция для записи запосов в БД - сбор статистики по запросам
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
    length = len(categories)        #Определяем количество возможных категорий

    while True:
        try:
            id_choosing = int(input("Введите ID интересующей категории/жанра: "))
            if id_choosing not in range(1, length):
                print(f'Некорректный ввод данных. Ожидается целое число от 1 до {length}')
            else:
                break
        except ValueError:
                print(f'Некорректный ввод данных. Ожидается целое число от 1 до {length}')
        except TypeError:
                print(f'Некорректный ввод данных. Ожидается целое число от 1 до {length}')
    # finally:
    return id_choosing


def category_request(cursor_r, id):
    request_categ = '''SELECT film.title, film.release_year, film.description FROM film 
        JOIN film_category ON film.film_id = film_category.film_id 
        JOIN category ON film_category.category_id = category.category_id 
        WHERE category.category_id={} 
        ORDER BY film.title'''.format(id)
    cursor_r.execute(request_categ)
    insert_request(request_categ)
    all_categories_request = cursor_r.fetchall()
    return all_categories_request


def year_search():

    try:
        while True:
            year_choosing = int(input('Введите год выхода интересующих фильмов: '))
            if len(f'{year_choosing}') != 4:
                print("Год дожлен состоять из четырех символов.")
            else:
                break
        return year_choosing
    except ValueError:
        print('Некореректный ввод данных. Ожидается целое число')
    except TypeError:
        print('Некореректный ввод данных. Ожидается целое число')

def year_request(year_from_user, cursor_r):
    request_year = '''SELECT film.title, film.release_year, film.description FROM film 
                    WHERE film.release_year=('{}')'''.format(year_from_user)
    cursor_r.execute(request_year)
    insert_request(request_year)
    res = cursor_films.fetchall()
    print()
    return res


def category_and_year(category, year, cursor_r):

    request_categ = '''SELECT film.title, film.release_year, film.description FROM film 
                JOIN film_category ON film.film_id = film_category.film_id 
                JOIN category ON film_category.category_id = category.category_id 
                WHERE category.category_id={} and film.release_year = {}
                ORDER BY film.title'''.format(category, year)
    cursor_r.execute(request_categ)
    insert_request(request_categ)
    all_categories_request = cursor_r.fetchall()
    return all_categories_request


def all_or_random_print(result_request):
    head_table = '''+--------------------------------+------------+-------------------------------------------------------------------------------------------------------------------------------+'''
    if result_request:
        if len(result_request) <= 10:
            print(f'Поиск выдал {len(result_request)} результатов.')
            print(head_table + '\n| {:^30} | {:^10} | {:^125} |'.format('НАЗВАНИЕ ФИЛЬМА', 'ГОД ВЫХОДА', 'ОПИСАНИЕ'))
            print(head_table)
            for title, year, describtion in result_request:
                print('| {:^30} | {:^10} | {:<125} |'.format(title, year, describtion))
            print(head_table)
            print()
        else:
            try:
                answer = int(input(f'''Поиск выдал {len(result_request)} результатов. Cколько результатов вывести на экран?
    По умолчанию выводится 10 результатов.            
    Введите число: '''))
                print()
                print(head_table)
                print('| {:^30} | {:^10} | {:^125} |'.format('НАЗВАНИЕ ФИЛЬМА', 'ГОД ВЫХОДА', 'ОПИСАНИЕ'))
                print(head_table)
                for title, year, describtion in result_request[:abs(answer)]:
                    print('| {:^30} | {:^10} | {:<125} |'.format(title, year, describtion))
                print(head_table)
                print()
            except:
                print()
                print(head_table)
                print('| {:^30} | {:^10} | {:^125} |'.format('НАЗВАНИЕ ФИЛЬМА', 'ГОД ВЫХОДА', 'ОПИСАНИЕ'))
                print(head_table)
                for title, year, describtion in result_request[:10]:
                    print('| {:^30} | {:^10} | {:<125} |'.format(title, year, describtion))
                print(head_table)
                print()

    else:
        print('Поиск не дал результатов. Попробуйте еще раз.')
        print()

def actor_search(cursor_read):
    res_act = input('Вы выбрали поиск по актерам. Если хотите просмотреть список актеров нажмите "Y": ').upper()
    if res_act == 'Y':
        request_actors = 'SELECT first_name, last_name FROM actor ORDER BY last_name'
        cursor_films.execute(request_actors)
        actors = cursor_films.fetchall()
        print("Список актеров: ")
        for firstname, lastname in actors:
            print(firstname, lastname)

    # if res == 'N'
    print()
    print('Вы выбрали поиск по актерам. Если Вы не знаете имя или фамилию, для пропуска нажмите Enter')
    choosing_actor_firstname = input("Введите имя актера/актрисы: ").strip().upper()
    choosing_actor_lastname = input("Введите фамилию актера/актрисы: ").strip().upper()
    print()
    if choosing_actor_firstname != '' and choosing_actor_lastname != '':
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                    JOIN film_actor ON actor.actor_id=film_actor.actor_id
                    JOIN film ON film.film_id=film_actor.film_id
                    WHERE actor.first_name=('{}') and actor.last_name=('{}') 
                    ORDER BY film.release_year'''.format(choosing_actor_firstname, choosing_actor_lastname)
    elif choosing_actor_firstname != '' and choosing_actor_lastname == '':
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                                JOIN film ON film.film_id=film_actor.film_id
                                WHERE actor.first_name=('{}') 
                                ORDER BY film.release_year'''.format(choosing_actor_firstname)
    elif choosing_actor_firstname == '' and choosing_actor_lastname != '':
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                                JOIN film ON film.film_id=film_actor.film_id
                                WHERE actor.last_name=('{}') 
                                ORDER BY film.release_year'''.format(choosing_actor_lastname)
    else:
        print('Имя и фамилия не введены. Будут выведены все фильмы')
        request_a = '''SELECT film.title, film.release_year, film.description FROM actor
                       JOIN film_actor ON actor.actor_id=film_actor.actor_id
                       JOIN film ON film.film_id=film_actor.film_id
                       ORDER BY film.release_year DESC'''

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


def top_search(cursor_r, cursor_w):
    request_popular = '''SELECT ROW_NUMBER() OVER (ORDER BY count DESC) AS "rank", request, count
    FROM (SELECT request, COUNT(request) AS count
    FROM requests_statistic
    GROUP BY request 
    ORDER BY count DESC 
    LIMIT 5) AS subquery'''
    cursor_r.execute(request_popular)
    statistic = cursor_r.fetchall()
    for id, request, count in statistic:
         print(f'{id}           {request} \n Количество запросов - {count}')
    return statistic


def top_req(statistic, cursor_w):
    try:
        id_input = int(input('Введите номер желаемого запроса (1-5): '))
        for id, request, count in statistic:
            if id == id_input:
                cursor_w.execute(request)
                insert_request(request)
                popular_request = cursor_w.fetchall()
                return popular_request
    except ValueError:
        print('Некореректный ввод данных. Ожидается целое число')
    except TypeError:
        print('Некореректный ввод данных. Ожидается целое число')




connection_films = connect_to_db(dbconfig)
cursor_films = connection_films.cursor()

connection_requests = connect_to_db(dbconfig_requests)
cursor_requests = connection_requests.cursor()

print('Добро пожаловать в сервис кинопоиска! Ввод осуществляется латинскими буквами.')
while True:
    user_choosing = menu_and_choosing()

    if user_choosing == 'C':
        print("Выбран поиск по жанрам фильма")
        id_category = categorie_search(cursor_films)
        res_categories = category_request(cursor_films, id_category)
        all_or_random_print(res_categories)

    elif user_choosing == 'Y':
        print('Выбран поиск по году выхода фильма')
        res_years = year_search()
        year_request_result = year_request(res_years, cursor_films)
        all_or_random_print(year_request_result)

    elif user_choosing == 'CY':
        print("Выбран поиск по жанрам фильма и году выхода на экраны")
        id_category = categorie_search(cursor_films)
        res_years = year_search()
        result_CY = category_and_year(id_category, res_years, cursor_films)
        all_or_random_print(result_CY)

    elif user_choosing == 'A':
        actors = actor_search(cursor_films)
        actors_print(*actors)

    elif user_choosing == 'W':
        key_word_res = key_word_search(cursor_films)
        all_or_random_print(key_word_res)

    elif user_choosing == 'TOP':
        top_search_result = top_search(cursor_requests, cursor_films)
        top_res = top_req(top_search_result, cursor_films)
        all_or_random_print(top_res)

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

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


def insert_request(current_request):
    cursor_requests.execute("INSERT INTO requests_statistic (request) VALUES (%s)", (current_request,))
    connection_requests.commit()


connection_films = connect_to_db(dbconfig)
cursor_films = connection_films.cursor()

connection_requests = connect_to_db(dbconfig_requests)
cursor_requests = connection_requests.cursor()

print('Добро пожаловать в сервис кинопоиска! Ввод осуществляется латинскими буквами.')
while True:
    print('''        Меню поиска:
        Для выбора фильма по жанрам введите: "C"    
        Для поиска фильмов по имени и/или фамилии актера введите: "A" 
        Для поиска кинофильмов по году его выхода на экраны введите: "Y" 
        Для поиска по ключевому слову: "W" 
        Для вывода топ-5 самых популярных запросов пользователей введите "TOP"
        Для выхода введите: "STOP" ''')
    user_choosing = input('Поле для ввода:   ').strip().upper()
    if user_choosing == 'C':
        print("Выбран поиск по жанрам фильма")
        request = 'SELECT category_id, name FROM category'
        cursor_films.execute(request)
        # insert_request(request)
        categories = cursor_films.fetchall()
        print("ID   Жанр")
        for id, name in categories:
            print(id, name)
        print()
        ID_choosing = input("Введите ID интересующей категории/жанра: ")
        request = '''SELECT film.title, film.release_year, film.description FROM film 
        JOIN film_category ON film.film_id = film_category.film_id 
        JOIN category ON film_category.category_id = category.category_id 
        WHERE category.category_id={}'''.format(ID_choosing)
        # print(request)
        cursor_films.execute(request)
        insert_request(request)
        res = cursor_films.fetchall()
        for title, year, describtion in res[:10]:
            print(f'Фильм "{title}" - год выхода: {year}\nОписание: {describtion}')
        print()

    elif user_choosing == 'A':
        print()
        res = input('Вы выбрали поиск по актерам. Хотите просмотреть список актеров? Y/N: ').upper()
        if res == 'Y':
            request = 'SELECT first_name, last_name FROM actor'
            cursor_films.execute(request)
            actors = cursor_films.fetchall()
            print("Список актеров: ")
            for firstname, lastname in actors:
                print(firstname, lastname)

        #if res == 'N'
        print('Вы выбрали поиск по актерам. Если Вы не знаете имя или фамилию, для пропуска нажмите Enter')
        choosing_actor_firstname = input("Введите имя актера/актрисы: ").upper()
        choosing_actor_lastname = input("Введите фамилию актера/актрисы: ").upper()
        print()

        if choosing_actor_firstname != '' and choosing_actor_lastname != '':
            request = '''SELECT film.title, film.description FROM actor
                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                JOIN film ON film.film_id=film_actor.film_id
                WHERE actor.first_name=('{}') and 
                actor.last_name=('{}')'''.format(choosing_actor_firstname, choosing_actor_lastname)
            # print(request)

        elif choosing_actor_firstname != '' and choosing_actor_lastname == '':
            request = '''SELECT film.title, film.description FROM actor
                            JOIN film_actor ON actor.actor_id=film_actor.actor_id
                            JOIN film ON film.film_id=film_actor.film_id
                            WHERE actor.first_name=('{}') '''.format(choosing_actor_firstname)

        elif choosing_actor_firstname == '' and choosing_actor_lastname != '':
            request = '''SELECT film.title, film.description FROM actor
                            JOIN film_actor ON actor.actor_id=film_actor.actor_id
                            JOIN film ON film.film_id=film_actor.film_id
                            WHERE actor.last_name=('{}')'''.format(choosing_actor_lastname)

        cursor_films.execute(request)
        insert_request(request)
        films = cursor_films.fetchall()
        if films:
            print(f"Фильмы с {choosing_actor_firstname} {choosing_actor_lastname}:")
            print('Название фильма                       Описание')
            for film, description in films:
                print(f"'{film}'                      {description}")
        else:
            print(f'Актера {choosing_actor_firstname}, {choosing_actor_lastname} нет в базе данных')
        print()
        # else:
        #     print('Ошибка ввода')

    elif user_choosing == 'Y':
        print('Выбран поиск по году выхода фильма')
        year_choosing = int(input('Введите год выхода интересующих фильмов: '))
        request = '''SELECT film.title, film.release_year, film.description FROM film 
        WHERE film.release_year=('{}')'''.format(year_choosing)
        cursor_films.execute(request)
        insert_request(request)
        res = cursor_films.fetchall()
        for title, year, describtion in res:
            print(f'Фильм "{title}" - год выхода: {year}\nОписание: {describtion}')
        print()

    elif user_choosing == 'W':
        print('Выбран поиск по ключевому слову')
        key_word = input('Введите слово для поиска: ')
        request = '''SELECT film.title, film.description FROM film WHERE title like '%{}%' 
        or description like "%{}%"'''.format(key_word,key_word)
        cursor_films.execute(request)
        insert_request(request)
        films = cursor_films.fetchall()
        if films:
            print('Название фильма                       Описание')
            for film, description in films:
                print(f"'{film}'                      {description}")
            print()
        else:
            print(f'Поиск по ключевому слову "{key_word}" не дал результатов')
            print()

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

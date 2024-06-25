import mysql.connector
dbconfig = {'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
    'user': 'ich1',
    'password': 'ich1_password_ilovedbs',
    'database': 'sakila'}


def connect_to_db(config):
    connect = mysql.connector.connect(**config)
    return connect

def disconnect_from_db(conn):
    conn.close()


connection = connect_to_db(dbconfig)
cursor = connection.cursor()


print('Добро пожаловать в сервис кинопоиска! Ввод осуществляется латинскими буквами.')
while True:
    print('''        Для выбора фильма по жанрам введите: "C"    
        Для поиска фильмов по имени и/или фамилии актера введите: "A" 
        Для поиска кинофильмов по году его выхода на экраны введите: "Y" 
        Для поиска по ключевому слову: "W" 
        Для вывода топ-5 самых популярных запросов пользователей введите "TOP"
        Для выхода введите: "STOP" ''')
    user_choosing = input('Поле для ввода:   ').upper()
    if user_choosing == 'C':
        print("Выбран поиск по жанрам фильма")

        cursor.execute('SELECT category_id, name FROM category')
        categories = cursor.fetchall()
        print("ID   Жанр")
        for id, name in categories:
            print(id, name)
        print()
        ID_choosing = int(input("Введите ID интересующей категории/жанра: "))

        cursor.execute('''SELECT film.title, film.release_year, film.description FROM film 
                JOIN film_category ON film.film_id = film_category.film_id 
                JOIN category ON film_category.category_id = category.category_id 
                WHERE category.category_id=(%s)''', (ID_choosing,))
        res = cursor.fetchall()
        for title, year, describtion in res[:10]:
            print(f'Фильм "{title}" - год выхода: {year}\nОписание: {describtion}')


    elif user_choosing == 'A':
        print()
        res = input('Вы выбрали поиск по актерам. Хотите просмотреть список актеров? Y/N: ').upper()
        if res == 'Y':
            cursor.execute('SELECT first_name, last_name FROM actor')
            actors = cursor.fetchall()
            print("Список актеров: ")
            for firstname, lastname in actors:
                print(firstname, lastname)

        elif res == 'N':
            print('Вы выбрали поиск по актерам. Если Вы не знаете имя или фамилию, для пропуска нажмите Enter')
            choosing_actor_firstname = input("Введите имя актера/актрисы: ").upper()
            choosing_actor_lastname = input("Введите фамилию актера/актрисы: ").upper()
            print()

            if choosing_actor_firstname != '' and choosing_actor_lastname != '':
                cursor.execute('''SELECT film.title, film.description FROM actor
                    JOIN film_actor ON actor.actor_id=film_actor.actor_id
                    JOIN film ON film.film_id=film_actor.film_id
                    WHERE actor.first_name=(%s) and actor.last_name=(%s)''', (choosing_actor_firstname, choosing_actor_lastname))

            elif choosing_actor_firstname != '' and choosing_actor_lastname == '':
                cursor.execute('''SELECT film.title, film.description FROM actor
                                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                                JOIN film ON film.film_id=film_actor.film_id
                                WHERE actor.first_name=(%s) ''',
                               (choosing_actor_firstname, ))

            elif choosing_actor_firstname == '' and choosing_actor_lastname != '':
                cursor.execute('''SELECT film.title, film.description FROM actor
                                JOIN film_actor ON actor.actor_id=film_actor.actor_id
                                JOIN film ON film.film_id=film_actor.film_id
                                WHERE actor.last_name=(%s)''',
                               (choosing_actor_lastname,))


            films = cursor.fetchall()
            if films:
                print(f"Фильмы с {choosing_actor_firstname} {choosing_actor_lastname}:")
                print('Название фильма                       Описание')
                for film, description in films:
                    print(f"'{film}'                      {description}")
            else:
                print(f'Актера {choosing_actor_firstname}, {choosing_actor_lastname} нет в базе данных')
        else:
            print('Ошибка ввода')

    elif user_choosing == 'Y':
        print('Выбран поиск по году выхода фильма')
        year_choosing = int(input('Введите год выхода интересующих фильмов: '))
        cursor.execute('''SELECT film.title, film.release_year, film.description FROM film 
                                 WHERE film.release_year=(%s)''', (year_choosing,))
        res = cursor.fetchall()
        for title, year, describtion in res:
            print(f'Фильм "{title}" - год выхода: {year}\nОписание: {describtion}')

    elif user_choosing == 'W':
        print('Выбран поиск по ключевому слову')
        key_word = input('Введите слово для поиска: ')
        request = '''SELECT film.title, film.description FROM film WHERE title like '%{0:<4}%' 
        or description like "%{0:<4}%"'''.format(key_word)
        cursor.execute(request)
        films = cursor.fetchall()
        if films:
            print('Название фильма                       Описание')
            for film, description in films:
                print(f"'{film}'                      {description}")
            print()
        else:
            print(f'Поиск по ключевому слову "{key_word}" не дал результатов')
            print()

    elif user_choosing == 'TOP':
        print('')

    elif user_choosing == 'STOP':
        print('Спасибо за использование сервиса по поиску кинофильмов. До новых встреч!')
        break


cursor.close()
disconnect_from_db(connection)

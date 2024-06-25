import mysql.connector

class MyBD_1:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.get_connection()

    def get_connection(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect({
                'host': self.host,
                'user': self.user,
                'password': self.password,
                'database': self.database
            })
            print('Соединение с БД прошло успешно')
        except mysql.connector.Error as err:
            print(f'Ошибка соединения: \'{err}\'\nРабота программы завершена')

    def execute_query_read(self, query):
        result = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f'Ошибка: \'{err}\' в запросе: {query}')
        finally:
            cursor.close()
        return result


class MyBD_2(MyBD_1):

    def execute_query_write(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            print(f'Ошибка: \'{err}\' в запросе: {query}')
        finally:
            cursor.close()


bd_read = MyBD_1('ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com', 'ich1', 'ich1_password_ilovedbs', 'sakila')
# bd_write = MyBD_2('mysql.itcareerhub.de', 'ich1', 'ich1_password_ilovedbs', 'project_220424_ptm_Kutuzova')




# query = '...'
# criterions = ''
# res = bd_ich.execute_query_read(query)
#
# query_2 = f'...{criterions}...'
# bd_write.execute_query_write(query_2)



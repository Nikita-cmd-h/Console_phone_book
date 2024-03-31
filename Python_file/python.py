import sqlite3

def new_user(user_input):                 #Добавление нового пользователя
  del user_input[0]
  cursor.execute('INSERT INTO Users (telephone, surname, username, middle_name) VALUES (?, ?, ?, ?)',
                 (user_input[0], user_input[1], user_input[2], user_input[3]))

def search_user(user_search):             #Фильтрация БД
  del user_search[0]
  string = f'SELECT id, telephone, surname, username, middle_name FROM Users WHERE {user_search[0]} {user_search[1]} ?'
  cursor.execute(string, (user_search[2],))
  users = cursor.fetchall()
  for user in users:
    print(user)

def editing_user(user_editing):           #Замена данных БД
  del user_editing[0]
  cursor.execute(f'UPDATE Users SET {user_editing[3]} = ? WHERE {user_editing[0]} {user_editing[1]} ?', (user_editing[4], user_editing[2]))

def delete_user(user_del):                #Удаление данных в БД
  del user_del[0]
  cursor.execute(f'DELETE FROM Users WHERE {user_del[0]} {user_del[1]} ?', (user_del[2],))

def table_user():                         #Ввывод БД на экран
    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for user in users:
        print(user)

def help():
  print('''
+===========+====================================================================================================================+=====================+===============================================+
| Название  |                                                         Входные данные/пояснения                                                         |                                               |
+===========+====================================================================================================================+=====================+===============================================+
| I, INSERT |    --telephone      |        --surname         |          --username             |           --middle_name         |                     |     добавляет введённые данные в таблицу      |
|           +---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
|           |     --телефон       |        --фамилия         |             --имя               |            --отчество           |                     |                                               |
+-----------+---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
| S, SELECT | --the search column | --the sign of comparison |       --comparable data         |                                 |                     | фильтрует и выводит на экран даные по запросу |
|           +---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
|           | --поисковая колонка |    --знак сравнения      |        --условные данные        |                                 |                     |                                               |
+-----------+---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
| D, DELETE | --the search column | --the sign of comparison |        --search parameter       |                                 |                     |            удалить данные о номере            |
|           +---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
|           | --поисковая колонка |    --знак сравнения      |       --поисковой парамтр       |                                 |                     |                                               |
+-----------+---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
| U, UPDATE | --the search column | --the sign of comparison |        --search parameter       | --column with replaceable data  |   --replaced data   |         обновляет информацию о человеке       |
|           +---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
|           | --поисковая колонка |    --знак сравнения      |       --поисковой параметр      | --колонка с заменяемыми данными | --заменяемые данные |                                               |
+-----------+---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
| Q, QUIT   |                     |                          |                                 |                                 |                     |                выход из программы             |
+-----------+---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
| H, HELP   |                     |                          |                                 |                                 |                     |       вызывает окно с доступными командами    |
+-----------+---------------------+--------------------------+---------------------------------+---------------------------------+---------------------+-----------------------------------------------+
| T, TABLE  |                     |                          |                                 |                                 |                     |               выводит всю таблицу             |
+===========+=====================+==========================+=================================+=================================+=====================+===============================================+
''')

functional = {
  'INSERT' : new_user,
  'SELECT' : search_user,
  'UPDATE' : editing_user,
  'DELETE' : delete_user,
  'TABLE'  : table_user,
  'HELP'   : help,
  'I' : new_user,
  'S' : search_user,
  'U' : editing_user,
  'D' : delete_user,
  'T' : table_user,
  'H' : help
}

# Создаем подключение к базе данных (файл my_database.db будет создан)
with sqlite3.connect('my_database.db') as connection:
  cursor = connection.cursor()
  # Создаем таблицу Users
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS Users (
  id INTEGER PRIMARY KEY,
  telephone INTEGER NOT NULL,
  surname TEXT NOT NULL,
  username TEXT NOT NULL,
  middle_name TEXT NOT NULL
  )''')

  while True:
    try:
      # Начинаем транзакцию автоматически
      with connection:
        mistake = input("Введите команду(h для инструкции): ")
        input_functional = mistake.split()
        if input_functional[0] == 'Q' or input_functional[0] == 'QUIT':
          break
        elif len(input_functional) == 1:
          functional[input_functional[0]]()
        else:
          functional[input_functional[0]](input_functional)
        print()
    except:
      # Ошибки будут приводить к автоматическому откату транзакции
      print(f"bash: команда {mistake}: не найдена,\nвведите h чтобы посмотреть доступные команды")
      print()

#Закрываем соединение
connection.close()

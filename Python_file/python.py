import sqlite3

def new_user(user_input):
  del user_input[0]
  cursor.execute('INSERT INTO Users (telephone, surname, username, middle_name) VALUES (?, ?, ?, ?)',
                 (user_input[0], user_input[1], user_input[2], user_input[3]))

def search_user(user_search):
  del user_search[0]
  string = f'SELECT id, telephone, surname, username, middle_name FROM Users WHERE {user_search[0]} {user_search[1]} ?'
  cursor.execute(string, (user_search[2],))
  users = cursor.fetchall()
  for user in users:
    print(user)

def editing_user(user_editing):
  del user_editing[0]
  cursor.execute(f'UPDATE Users SET {user_editing[0]} = ? WHERE id = ?', (user_editing[2], user_editing[1]))

def delete_user(user_del):
  del user_del[0]
  cursor.execute(f'DELETE FROM Users WHERE {user_del[0]} = ?', (user_del[1],))

functional = {
  '+' : new_user,
  'S' : search_user,
  'E' : editing_user,
  '-S' : delete_user,
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
        input_functional = input("Введите команду(h для инструкции)").split()
        if input_functional[0] == 'q':
          break
        elif input_functional[0] == 'V':
            # Выбираем всех пользователей
            cursor.execute('SELECT * FROM Users')
            users = cursor.fetchall()
            for user in users:
                print(user)
        elif input_functional[0] == 'C':
            #Сохраняем изменения
            connection.commit()
        else:
          functional[input_functional[0]](input_functional)

    except:
      # Ошибки будут приводить к автоматическому откату транзакции
      pass

#Закрываем соединение
connection.close()
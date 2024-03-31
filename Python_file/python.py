import sqlite3

def new_user():
  # Выполняем операции
  input_user = input("Ведите через пробел данные(телефон, фамилия, имя, отчество): ").split()
  cursor.execute('INSERT INTO Users (telephone, surname, username, middle_name) VALUES (?, ?, ?, ?)',
                 (int(input_user[0]), input_user[1], input_user[2], input_user[3]))

def search_user():
  input_search = input("Введите через пробел, название столбца(id, telephone, surname, username, middle_name) и данные: ").split()
  cursor.execute(f'SELECT id, telephone, surname, username, middle_name FROM Users WHERE {input_search[0]} = ?',
                 (input_search[1],))
  users = cursor.fetchall()
  for user in users:
    print(user)

def editing_user():
  input_search = input("Введите через пробел, название столбца(id, telephone, surname, username, middle_name),\n id того кого хотите заменить в этом столбце и заменяющие данные: ").split()
  cursor.execute(f'UPDATE Users SET {input_search[0]} = ? WHERE id = ?', (input_search[2], input_search[1]))

def delete_user():
  input_delete = input("Введите через пробел, название столбца(id, telephone, surname, username, middle_name) и данные: ").split()
  cursor.execute(f'DELETE FROM Users WHERE {input_delete[0]} = ?', (input_delete[1],))

def viewing():
  # Выбираем всех пользователей
  cursor.execute('SELECT * FROM Users')
  users = cursor.fetchall()

  # Выводим результаты
  for user in users:
    print(user)

def saving():
  #Сохраняем изменения
  connection.commit()

functional = {
  'добавление' : new_user,
  'поиск' : search_user,
  'изменение данных' : editing_user,
  'удаление' : delete_user,
  'просмотр' : viewing,

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
        input_functional = input("Введите что вы хотите сделать (просмотр, сохранение, добавление, поиск, удаление, изменение данных, выход): ")
        if input_functional == 'выход':
          break
        functional[input_functional]()

    except:
      # Ошибки будут приводить к автоматическому откату транзакции
      pass

#Закрываем соединение
connection.close()
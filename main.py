"""
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной

"""
from csv import DictWriter, DictReader
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_data():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Слишком короткое имя")
            last_name = input("Введите фамилию: ")
            if len(last_name) < 5:
                raise NameError("Слишком короткая фамилия")
            phone = input("Введите номер: ")
            if len(phone) != 13:
                raise NameError("Количество цифр должно быть 12. Не забудьте поставить "+" перед номером")
        except NameError as err:
            print(err)
        else:
            flag = True
        return [first_name, last_name, phone]


def create_file(filename):
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)  # получаем содержимое в виде списка словарей, где каждая запись это словарь


def write_file(filename, lst):
    res = read_file(filename)  # сначала читаем файл, он пустой (достали ящик с вещами)
    obj = {'Имя': lst[0], 'Фамилия': lst[1],
           'Телефон': lst[2]}  # создаем словарь, кладем в него список (кладем вещь в ящик)
    res.append(obj)
    standart_write(filename, res)  # filename - ящик, res - шкаф (ящик задвигаем в шкаф)


def row_search(filename):
    name = input("Введите фамилию, имя или номер телефона: ")
    res = read_file(filename)
    for row in res:
        if name == row['Фамилия'] or name == row['Имя'] or name == row['Телефон']:
            return row
    return ("Запись не найдена")


def delete_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    res.pop(row_number - 1)  # удаляем элемент по индексу
    standart_write(filename, res)


def standart_write(filename, res):
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(res)


def change_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    data = get_data()  # вызываем функцию get_data - запрашиваем ввод данных
    res[row_number - 1]["Имя"] = data[0]  # берем нужную вещь из ящика по индексу, обращаемся в словаре по ключу "Имя"
    #                                     и кладем новое значение
    res[row_number - 1]["Фамилия"] = data[1]
    res[row_number - 1]["Телефон"] = data[2]
    standart_write(filename, res)


def copy_row(filename, filename_new):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    res_new = read_file(filename_new)
    if (row_number < 1) or (row_number > len(res)):
        print ("Такой строки не существует. Введите другую")
    else:
        row_content = res[row_number-1]
        res_new.append(row_content)
        standart_write(filename_new, res_new)

def check_not_exists(filename):
    if not exists(filename):
        print("Файл не существует. Создайте его.")

filename = 'phone.csv'
filename_new = ('phone_new.csv')

def main():
    while True:
        command = input("Введите команду: ")
        if command == "q":
            break
        elif command == "w":
            check_not_exists(filename)
            write_file(filename, get_data())
        elif command == 'r':
            check_not_exists(filename)
            print(read_file(filename))
        elif command == 'f':
            check_not_exists(filename)
            print(row_search(filename))
        elif command == 'd':
            check_not_exists(filename)
            delete_row(filename)
        elif command == 'c':
            check_not_exists(filename)
            change_row(filename)
        elif command == 'co':
            if not exists(filename_new):
                create_file(filename_new)
                continue
            copy_row(filename, filename_new)


main()

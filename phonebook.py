import os
import re


def validate_phone(phone_type, phone):
    # Проверяет введеный номер на коректность

    if re.match(r'^\+7\d{10}$', phone) or phone == '':
        return phone
    else:
        print(f"Некорректный формат номера телефона. Введите номер снова.")
        return validate_phone(phone_type, input(f"Введите {phone_type} номер телефона: "))


def validate_fio(name_type, name):
    # Проверяет введеный ФИО на коректность
    if name.isalpha():
        return name
    else:
        print(f"Используются недопустимые символы")
        return validate_fio(name_type, input(f"Введите {name_type}: "))


def add_contact():
    # Добавляет новый контакт в телефонную книгу
    last_name = validate_fio("Фамилию", input("Введите фамилию: ").capitalize())
    first_name = validate_fio("Имя", input("Введите имя: ").capitalize())
    patronymic = validate_fio("Отчество", input("Введите отчество: ").capitalize())
    organization = input("Введите название организации: ")
    work_phone = validate_phone("рабочий", input("Введите рабочий телефон: "))
    personal_phone = validate_phone("личный", input("Введите личный телефон: "))

    with open("contacts.txt", "a") as f:
        f.write(f"{last_name},{first_name},{patronymic},{organization},{work_phone},{personal_phone}\n")

    print("Контакт  добавлен!")


def edit_contact():
    # Редактирует уже имеющийся контакт
    # Вывод пронумерованного списка контактов
    contact_list = read_contacts()
    print("Список контактов:")
    for i, contact in enumerate(contact_list):
        print(f"{i + 1}. {contact}")

    # Запрос порядкового номера контакта для редактирования
    choice = int(input("Выберите номер контакта, который хотите редактировать: "))
    if choice <= 0 or choice > len(contact_list):
        print("Некорректный выбор!")
        return

    contact = contact_list[choice - 1].split(',')
    # Запрос отредактированый данных

    last_name = validate_fio("Фамилию", input("Введите фамилию: ").capitalize())
    first_name = validate_fio("Имя", input("Введите имя: ").capitalize())
    patronymic = validate_fio("Отчество", input("Введите отчество: ").capitalize())
    organization = input("Введите название организации: ")
    work_phone = validate_phone("рабочий", input("Введите рабочий телефон: "))
    personal_phone = validate_phone("личный", input("Введите личный телефон: "))

    contact[0] = last_name
    contact[1] = first_name
    contact[2] = patronymic
    contact[3] = organization
    contact[4] = work_phone
    contact[5] = personal_phone

    contact_list[choice - 1] = ','.join(contact)

    with open("contacts.txt", "w") as f:
        f.write('\n'.join(contact_list))

    print("Контакт успешно изменен!")


def search_contacts():
    # Поиск контакта по одному из параметров
    contact_list = read_contacts()

    search_term = input("Введите поисковый запрос: ")

    found_contacts = []
    for contact in contact_list:
        if search_term.lower() in contact.lower():
            found_contacts.append(contact)

    if len(found_contacts) == 0:
        print("Контакты не найдены.")
    else:
        print("Найденные контакты:")
        for contact in found_contacts:
            print(contact)


def read_contacts():
    # Загрузка контактов из файла
    contact_list = []
    if os.path.isfile("contacts.txt"):
        with open("contacts.txt", "r") as f:
            contact_list = f.readlines()
    return contact_list


def display_contacts(page_size=5):
    # Постраничный вывод контактов(по умолчанию 5)
    contact_list = read_contacts()

    if len(contact_list) == 0:
        print("Справочник пуст.")
        return

    page = 1
    while True:
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        page_contacts = contact_list[start_index:end_index]

        print("Список контактов:")
        for contact in page_contacts:
            print(contact)

        # Возможность перехода на следующую страницу появляется при наличии невыведеных контактов
        if end_index < len(contact_list):
            print("1 - Следующая страница")
        # Возможность перехода на предыдущую страницу появляется работает аналогично
        if page > 1:
            print("2 - Предыдущая страница")
        print("3 - Выход")

        choice = input("Выберите действие: ")
        if choice == '1':
            if end_index < len(contact_list):
                page += 1
            else:
                print("Это последняя страница.")
        elif choice == '2':
            if page > 1:
                page -= 1
            else:
                print("Это первая страница.")
        elif choice == '3':
            break
        else:
            print("Некорректный выбор!")


def main():
    # Вывод меню для взаимодействия пользователя с телефонной книгой
    while True:
        print("==========================")
        print("Телефонный справочник")
        print("==========================")
        print("1 - Вывести контакты")
        print("2 - Добавить контакт")
        print("3 - Редактировать контакт")
        print("4 - Поиск контактов")
        print("5 - Выход")
        print("==========================")

        choice = input("Выберите действие: ")
        if choice == '1':
            display_contacts()
        elif choice == '2':
            add_contact()
        elif choice == '3':
            edit_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            break
        else:
            print("Некорректный выбор!")


if __name__ == "__main__":
    main()

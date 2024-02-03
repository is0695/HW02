import re
import csv
import datetime


def logger(path):

    def __logger(old_function):
        def new_function(*args, **kwargs):
            date = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            with open(f'{path}', 'a', encoding="utf-8") as log_file:
                log_file.write(
                    f'{date} функция: {old_function.__name__} аргументы: {args} {kwargs} результат: {result}\n')
            return result

        return new_function

    return __logger


@logger("log_4.log")
def last_first_surname(contacts_list):
    '''Второй цикл для того чтобы не терять столбец, в случае, когда неполные ФИО'''
    for contact in contacts_list:
        temp = ' '.join(contact[:3])
        temp = temp.split()
        for i in range(len(temp)):
            contact[i] = temp[i]
    return fix_phone_number(contacts_list)


@logger("log_3.log")
def fix_phone_number(contacts_list):
    pattern = r"(8|\+7)\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*[\(доб.\s]*(\d{4})*\)*"
    repl_extra = r"+7(\2)\3-\4-\5 доб.\6"
    repl = r"+7(\2)\3-\4-\5"
    for contact in contacts_list:
        if "доб" in contact[5]:
            contact[5] = re.sub(pattern, repl_extra, contact[5])
        else:
            contact[5] = re.sub(pattern, repl, contact[5])
    return fix_doubles(contacts_list)


@logger("log_2.log")
def fix_doubles(contacts_list):
    temp_dict = {}
    for contact in contacts_list:
        key = contact[0] + ' ' + contact[1]
        if key in temp_dict:
            for i in range(7):
                if not temp_dict[key][i]:
                    temp_dict[key][i] = contact[i]
        else:
            temp_dict[key] = contact
    return dict_to_list(temp_dict)


@logger("log_1.log")
def dict_to_list(temp_dict):
    contact_list = []
    for value in temp_dict.values():
        contact_list.append(value)
    return contact_list


def fix_phonebook(contacts_list):
    return last_first_surname(contacts_list)


def main():
    with open(r"phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # TODO 1: выполните пункты 1-3 ДЗ

    contacts_list = fix_phonebook(contacts_list)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open(r"phonebook.csv", "w",  encoding="utf-8", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
    #   # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    main()

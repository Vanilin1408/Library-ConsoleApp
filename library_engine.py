import json
import hashlib


class Library:
    def __init__(self, data_path: str):
        self.__data_path: str = data_path

    def __read_data(self) -> dict:
        """ Метод чтения данных из json файла """
        try:
            with open(self.__data_path, "r", encoding="utf-8") as file:
                if len(file.read()) == 0:
                    return {}
                else:
                    file.seek(0)    # Указатель в начало
                    return json.load(file)
        except FileNotFoundError:
            print("Ошибка чтения, файл не найден.")
            return {}

    def __write_data(self, data: dict) -> None:
        """ Метод записи новых данных в json файл """
        try:
            with open(self.__data_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            print("Ошибка записи, файл не найден.")
        return

    def __generate_unique_id(self, key: str) -> str:
        """ Метод для создания уникальных идентификаторов на основе ключа (строке с информацией о книге).
            Возвращает хеш (уникальный id) преданной строки ограниченного размера (для единства) """
        return hashlib.md5(key.encode()).hexdigest()[:10]

    def add_update_book(self, title: str, author: str, year: str) -> None:
        """ Метод добавления новых/обновления имеющихся данных книг """
        key: str = f"{author.lower()}-{title.lower()}-{year}"
        unique_id: str = self.__generate_unique_id(key)
        curr_data: dict = self.__read_data()

        if unique_id not in curr_data.keys():
            curr_data[unique_id] = {
                    'title': title,
                    'author': author,
                    'year': year,
                    'count': 1,
                    'status': 'в наличии'
            }

            self.__write_data(curr_data)
            print(f"Книга успешно добавлена c id: {unique_id}.")
        else:
            curr_data[unique_id].update({
                'count': curr_data[unique_id]['count'] + 1,
                'status': 'в наличии'
            })
            print(f"Книга c id: {unique_id} успешно обновлена.")

        self.__write_data(curr_data)
        return

    def borrow_book(self, unique_id: str) -> None:
        """ Метод обработки "заимствования" книги в библиотеке, то есть обновление количества,
            статуса книги по уникальному идентификатору """
        curr_data: dict = self.__read_data()

        if unique_id not in curr_data.keys():
            print(f"Книги с идентификатором {unique_id} не существует. Выдача невозможна.")
        elif curr_data[unique_id]['count'] == 0:
            print(f"Запрашиваемой книги '{curr_data[unique_id]['title']}' автора {curr_data[unique_id]['author']}"
                  f" {curr_data[unique_id]['year']} года выпуска нет в наличии. Выдача невозможна.")
        else:
            curr_data[unique_id].update({
                'count': curr_data[unique_id]['count'] - 1
            })

            if curr_data[unique_id]['count'] == 0:
                curr_data[unique_id].update({
                    'status': 'нет в наличии'
                })
            print(f"Запрашиваемая книга '{curr_data[unique_id]['title']}' автора {curr_data[unique_id]['author']}"
                  f" {curr_data[unique_id]['year']} года выпуска успешно выдана.")

            self.__write_data(curr_data)
        return

    def delete_book_by_id(self, unique_id: str) -> None:
        """ Метод полного удаления книги из базы по уникальному идентификатору """
        curr_data: dict = self.__read_data()

        if unique_id not in curr_data.keys():
            print(f"Книги с идентификатором {unique_id} не существует. Удаление невозможно.")
            return
        else:
            del curr_data[unique_id]
            self.__write_data(curr_data)
            print(f"Удаление книги с идентификатором {unique_id} выполнено.")

    def change_status_by_id(self, unique_id: str, new_status: str) -> None:
        """ Метод ручного изменения статуса книги по id """
        curr_data: dict = self.__read_data()

        if unique_id not in curr_data.keys():
            print(f"Книги с id: {unique_id} не существует. Изменения статуса невозможно.")
            return

        if new_status.lower() == curr_data[unique_id]['status'].lower():
            print(f"Новый статус '{new_status.lower()}' соответствует уже установленному, изменения не произведены.")
        elif new_status.lower() == 'в наличии':
            curr_data[unique_id]['status'] = new_status.lower()
            curr_data[unique_id]['count'] = curr_data[unique_id]['count'] + 1
            print(f"Новый статус '{new_status.lower()}' успешно применен для книги с id '{unique_id}'.")
        elif new_status.lower() == 'нет в наличии':
            curr_data[unique_id]['status'] = new_status.lower()
            curr_data[unique_id]['count'] = 0
            print(f"Новый статус '{new_status.lower()}' успешно применен для книги с id '{unique_id}'.")
        else:
            print(f"Статус '{new_status.lower()}' не поддерживается. "
                  f"Возможные варианты статуса книги: 'в наличии', 'нет в наличии'.")

        self.__write_data(curr_data)
        return

    def find_all_by_keyword(self, keyword: str) -> None:
        """ Находит все книги, включающие ключевое слово и выводит их """
        if keyword is None or len(keyword) == 0:
            print('Ключевое слово должно содержать как минимум 1 символ.')
            return

        curr_data: dict = self.__read_data()
        found_ids: list = []

        for unique_id in curr_data:
            if keyword == unique_id:
                found_ids.append(unique_id)
                continue
            for val in curr_data[unique_id].values():
                if str(val).lower() == keyword.lower():
                    found_ids.append(unique_id)

        if len(found_ids) == 0:
            print(f"По запросу '{keyword}' ничего не найдено.")
        else:
            print(f"По запросу '{keyword}' найдены следующие результаты:")
            print(f"| {'id':^{16}} | {'название':^{30}} | {'автор':^{20}} | "
                  f"{'год':^{10}} | {'кол-во':^{6}} | {'статус':^{15}} |")
            print(f"|{'':{'-'}^{114}}|")
            for key, val in curr_data.items():
                if key in found_ids:
                    print(f"| {key:^{16}} | {val['title']:^{30}} | {val['author']:^{20}} | "
                          f"{val['year']:^{10}} | {val['count']:^{6}} | {val['status']:^{15}} |")
        return

    def print_all_books_info(self) -> None:
        curr_data: dict = self.__read_data()
        # Оформление табличного вида для удобочитаемости
        print(f"| {'id':^{16}} | {'название':^{30}} | {'автор':^{20}} | "
              f"{'год':^{10}} | {'кол-во':^{6}} | {'статус':^{15}} |")
        print(f"|{'':{'-'}^{114}}|")

        for key, val in curr_data.items():
            print(f"| {key:^{16}} | {val['title']:^{30}} | {val['author']:^{20}} | "
                  f"{val['year']:^{10}} | {val['count']:^{6}} | {val['status']:^{15}} |")
        return


if __name__ == '__main__':
    # For testing
    DATA_PATH = './DATA/lib_data.json'
    library = Library(DATA_PATH)

    library.find_all_by_keyword('Mark Twain')
    # library.print_all_books_info()

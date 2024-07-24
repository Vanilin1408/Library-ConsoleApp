from library_engine import Library


class ConsoleApp:
    def __init__(self, library: Library):
        self.status_running = True
        self.__library = library

    def display_main_menu(self):
        print("-" * 30)
        print("Система управления библиотекой")
        print("-" * 30)
        print("1. Добавить/обновить книгу")
        print("2. Обновить статус книги")
        print("3. Выдать книгу")
        print("4. Удалить книгу")
        print("5. Показать все книги")
        print("6. Поиск по ключевому слову")
        print("7. Выход\n")

    def add_book_mode(self) -> None:
        """ Режим добавления книги """
        print("\nДобавление/обновление книги...")
        print("Для отмены введите '0'")

        title: str = input("Введите название книги: ")
        if title == '0':
            print("Отмена операции.\n")
            return

        author: str = input("Введите автора книги: ")
        if author == '0':
            print("Отмена операции.\n")
            return

        year: str = input("Введите год выпуска: ")
        if year == '0':
            print("Отмена операции.\n")
            return

        self.__library.add_update_book(title, author, year)
        print('')
        return

    def update_status_mode(self) -> None:
        """ Режим обновления статуса книги """
        print("\nОбновление статуса книги...")
        print("Для отмены введите '0'")

        uniq_id: str = input("Введите id книги: ")
        if uniq_id == '0':
            print("Отмена операции.\n")
            return

        new_status: str = input("Введите новый статус: ")
        if uniq_id == '0':
            print("Отмена операции.\n")
            return

        self.__library.change_status_by_id(uniq_id, new_status)
        print('')
        return

    def borrow_book_mode(self) -> None:
        """ Режим выдачи книг по id """
        print("\nВыдача книги...")
        print("Для отмены введите '0'")

        uniq_id: str = input("Введите id книги, которая выдается: ")
        if uniq_id == '0':
            print("Отмена операции.\n")
            return

        self.__library.borrow_book(uniq_id)
        print('')
        return

    def delete_book_mode(self) -> None:
        """ Режим полного удаления книг по id """
        print("\nПолное удаление книги...")
        print("Для отмены введите '0'")

        uniq_id: str = input("Введите id книги, которую необходимо удалить: ")
        if uniq_id == '0':
            print("Отмена операции.\n")
            return

        self.__library.delete_book_by_id(uniq_id)
        print('')
        return

    def show_all_books_mode(self) -> None:
        """ Режим отображения всех книг в базе данных """
        print("\nКниги, имеющиеся в базе данных: ")
        self.__library.print_all_books_info()
        print('')
        return

    def find_by_keyword_mode(self) -> None:
        """ Режим поиска по ключевому слову """
        print("\nПоиск книг по ключевому слову...")
        keyword: str = input("Введите ключевое слово для поиска: ")
        self.__library.find_all_by_keyword(keyword)
        print('')
        return

    def exit(self) -> None:
        """ Метод изменения флага состояния приложения, т.е. выход """
        self.status_running = False
        return

    def run(self) -> None:
        """ Метод работы приложения """
        while self.status_running:
            self.display_main_menu()
            choice = input("-> Выберите номер пункта меню: ")

            match choice:
                case '1':
                    self.add_book_mode()
                case '2':
                    self.update_status_mode()
                case '3':
                    self.borrow_book_mode()
                case '4':
                    self.delete_book_mode()
                case '5':
                    self.show_all_books_mode()
                case '6':
                    self.find_by_keyword_mode()
                case '7':
                    self.exit()
                case _:
                    print("Некорректный ввод, необходимо выбрать пункт меню от 1 до 7.")
        return


if __name__ == '__main__':
    console = ConsoleApp(Library('./DATA/lib_data.json'))
    console.run()

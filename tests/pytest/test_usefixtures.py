import pytest

# Использование pytest.mark.usefixtures особенно полезно для выполнения действий,
# которые необходимы перед тестами, но не возвращают результат, например,
# отправка аналитики или настройка окружения

# Фикстура для очистки данных из базы данных
@pytest.fixture
def clear_books_database():
    print("[FIXTURE] Удаляем все данные из базы данных")


# Фикстура для заполнения данных в базу данных
@pytest.fixture
def fill_books_database():
    print("[FIXTURE] Создаем новые данные в базе данных")


@pytest.mark.usefixtures('fill_books_database')
def test_read_all_books_in_library():
    ...


@pytest.mark.usefixtures(
    'clear_books_database',
    'fill_books_database'
)
class TestLibrary:
    def test_read_book_from_library(self):
        ...

    def test_delete_book_from_library(self):
        ...

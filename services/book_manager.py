import logging
from pathlib import Path
from typing import Dict, List, Optional

from .file_handling import prepare_book


logger = logging.getLogger(__name__)

BOOKS_DIR = Path(__file__).parent.parent / 'books'
CALLBACK_PREFIX = 'book:'
MAX_CALLBACK_BYTES = 64


class BookManager:
    def __init__(self, book_folder: str | Path | None = None):
        self.book_folder = Path(book_folder) if book_folder else BOOKS_DIR
        self._books: Dict[str, dict] = {}
        self._load_books()

    def _filename_to_title(self, book_id: str) -> str:
        return book_id.replace('_', ' ')

    def _validate_callback_data(self, book_id: str) -> None:
        callback_data = f'{CALLBACK_PREFIX}{book_id}'
        if len(callback_data.encode('utf-8')) > MAX_CALLBACK_BYTES:
            logger.warning(
                f'Имя файла "{book_id}.txt" слишком длинное для Telegram callback '
                f'({len(callback_data.encode("utf-8"))} байт, лимит {MAX_CALLBACK_BYTES}). '
                'Сократите имя файла.'
            )

    def _load_books(self) -> None:
        if not self.book_folder.exists():
            logger.warning(f'Папка с книгами не найдена: {self.book_folder}')
            return

        txt_files = sorted(self.book_folder.glob('*.txt'))
        logger.debug(f'Найдено .txt файлов: {len(txt_files)}')

        for file_path in txt_files:
            try:
                book_id = file_path.stem
                title = self._filename_to_title(book_id)

                self._validate_callback_data(book_id)

                self._books[book_id] = {
                    'id': book_id,
                    'title': title,
                    'file': str(file_path),
                    'pages': None,
                    'size': file_path.stat().st_size,
                }
                logger.info(
                    f'Загружена книга: {title} (ID: {book_id}, '
                    f'размер: {self._books[book_id]["size"]} байт)'
                )
            except Exception as e:
                logger.error(f'Ошибка при загрузке файла {file_path.name}: {e}')

        if not self._books:
            logger.warning(
                f'Книги не найдены. Добавьте .txt файлы в папку {self.book_folder}/'
            )
        else:
            logger.info(f'Всего загружено книг: {len(self._books)}')

    def get_pages(self, book_id: str) -> dict:
        if not self.book_exists(book_id):
            raise KeyError(f'Книга с ID {book_id} не найдена')
        if self._books[book_id]['pages'] is None:
            self._books[book_id]['pages'] = prepare_book(self.get_book_file(book_id))
        return self._books[book_id]['pages']

    def get_book_title(self, book_id: str) -> str:
        return self._books.get(book_id, {}).get('title', 'Неизвестная книга')

    def get_book_file(self, book_id: str) -> Optional[str]:
        return self._books.get(book_id, {}).get('file')

    def get_all_books(self) -> Dict[str, dict]:
        return self._books.copy()

    def get_books_list(self) -> List[Dict[str, str]]:
        return [
            {'id': book_id, 'title': info['title']}
            for book_id, info in sorted(self._books.items(), key=lambda item: item[1]['title'])
        ]

    def book_exists(self, book_id: str) -> bool:
        return book_id in self._books

    def get_books_count(self) -> int:
        return len(self._books)

    def reload(self) -> None:
        self._books.clear()
        self._load_books()

    def get_book_info(self, book_id: str) -> Optional[dict]:
        return self._books.get(book_id)


book_manager = BookManager()

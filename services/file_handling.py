import re


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    slice_text = text[start:start + page_size]
    cleaned_text = re.sub(r'[!?.,:;]{2}$', '', slice_text)
    match = re.search(r'.*[!?.,:;]', cleaned_text, re.DOTALL)
    page_text = match.group(0) if match else cleaned_text

    return page_text, len(page_text)


def prepare_book(path: str, page_size: int = 650) -> dict[int, str]:
    book = {}
    start = 0
    page_number = 1

    with open(path, encoding='utf-8') as file:
        all_text = file.read().lstrip()

    while start < len(all_text):
        page_text, page_length = _get_part_text(all_text, start, page_size)
        book[page_number] = page_text.lstrip()
        start += page_length
        page_number += 1

    return book
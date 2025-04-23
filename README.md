# PDF Converter

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-lightgrey.svg)

Конвертер PDF в Markdown/Excel с поддержкой математических формул через Mathpix OCR.

## 🔥 Возможности

- Преобразование PDF с математическими формулами в структурированный Markdown
- Конвертация в Excel с разделением на:
  - Часть документа
  - Номер вопроса
  - Текст вопроса
  - Ссылки на изображения
- Поддержка LaTeX-формул через Mathpix API
- Автоматическая обработка изображений

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/pullveryzator/pdf_converter.git
cd pdf_converter
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
cp .env.example .env
```
Заполните `.env` вашими ключами Mathpix:
```ini
MATHPIX_APP_ID=your_app_id
MATHPIX_APP_KEY=your_app_key
```

## 🚀 Использование

### Как REST-сервис (Flask):
```bash
flask run
```
Отправьте POST-запрос с PDF файлом на `/upload`

### Как библиотека:
```python
from pdf_converter import PDFToMarkdownConverter, MarkdownToExcelConverter

# PDF → Markdown
pdf_conv = PDFToMarkdownConverter()
success, pages = pdf_conv.process_pdf_to_markdown("input.pdf", "output.md")

# Markdown → Excel
md_conv = MarkdownToExcelConverter()
success, tasks = md_conv.process_md_to_excel("output.md", "output.xlsx")
```

## 📂 Структура проекта
```
pdf_converter/
├── app.py                # Flask приложение
├── pdf_to_md.py          # Конвертер PDF→Markdown
├── md_to_excel.py        # Конвертер Markdown→Excel
├── templates/            # HTML шаблоны
├── static/               # CSS/JS ресурсы
└── tests/                # Тесты
```

## 🌟 Особенности реализации

- **Гибкая обработка формул**: Поддержка как встроенных (`$E=mc^2$`), так и блочных формул (`$$`)
- **Разделение на части**: Автоматическое определение разделов документа

---

> **Note**  
> Для работы с Mathpix требуется аккаунт на [mathpix.com](https://mathpix.com/)  
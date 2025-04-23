import os
import requests
import time
from typing import Tuple

class PDFToMarkdownConverter:
    def __init__(self, mathpix_id: str, mathpix_key: str):
        """
        Инициализация конвертера PDF в Markdown с использованием Mathpix PDF API
        """
        self.mathpix_id = mathpix_id
        self.mathpix_key = mathpix_key
        self.base_url = "https://api.mathpix.com/v3"

    def _upload_pdf(self, pdf_path: str) -> str:
        """Загрузка PDF файла на сервер Mathpix"""
        with open(pdf_path, 'rb') as f:
            response = requests.post(
                f"{self.base_url}/pdf",
                files={"file": (os.path.basename(pdf_path), f)},
                headers={
                    "app_id": self.mathpix_id,
                    "app_key": self.mathpix_key
                }
            )
        
        if response.status_code == 200:
            return response.json()["pdf_id"]
        else:
            raise Exception(f"PDF upload error: {response.text}")

    def _get_conversion_results(self, pdf_id: str) -> str:
        """Получение результатов конвертации в Markdown"""
        while True:
            response = requests.get(
                f"{self.base_url}/pdf/{pdf_id}",
                headers={
                    "app_id": self.mathpix_id,
                    "app_key": self.mathpix_key
                }
            )
            
            status = response.json().get("status", "")
            if status == "completed":
                break
            elif status == "error":
                raise Exception("PDF processing error")
            
            time.sleep(2)
        
        response = requests.get(
            f"{self.base_url}/pdf/{pdf_id}.md",
            headers={
                "app_id": self.mathpix_id,
                "app_key": self.mathpix_key,
                "Accept": "text/markdown"
            }
        )
        
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Markdown download error: {response.text}")

    def process_pdf_to_markdown(self, pdf_path: str, md_path: str) -> Tuple[bool, int]:
        """Основная функция конвертации PDF в Markdown"""
        try:
            pdf_id = self._upload_pdf(pdf_path)
            
            markdown_content = self._get_conversion_results(pdf_id)
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            page_count = markdown_content.count("\n# ") + 1
            return True, page_count
        
        except Exception as e:
            print(f"Ошибка при обработке PDF: {str(e)}")
            return False, 0
import os
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename

from pdf_to_md import PDFToMarkdownConverter
from md_to_xlsx import MarkdownToExcelConverter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['MATHPIX_ID'] = 'MATHPIX_ID'
app.config['MATHPIX_KEY'] = 'MATHPIX_KEY'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            pdf_filename = secure_filename(file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            file.save(pdf_path)
            
            try:
                # PDF в Markdown
                md_filename = os.path.splitext(pdf_filename)[0] + '.md'
                md_path = os.path.join(
                    app.config['OUTPUT_FOLDER'], md_filename)
                
                pdf_md_converter = PDFToMarkdownConverter(
                    mathpix_id=app.config['MATHPIX_ID'],
                    mathpix_key=app.config['MATHPIX_KEY']
                )
                success, page_count = pdf_md_converter.process_pdf_to_markdown(
                    pdf_path, md_path)
                
                if not success:
                    return "Ошибка при конвертации PDF в Markdown", 500
                
                # Markdown в Excel
                excel_filename = os.path.splitext(pdf_filename)[0] + '.xlsx'
                excel_path = os.path.join(
                    app.config['OUTPUT_FOLDER'], excel_filename)
                
                md_to_excel_converter = MarkdownToExcelConverter()
                success, page_count = md_to_excel_converter.process_md_to_excel(md_path, excel_path)
                
                if not success:
                    return "Ошибка при конвертации Markdown в Excel", 500

                return send_file(
                    excel_path,
                    as_attachment=True,
                    download_name=excel_filename,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            except Exception as e:
                return f"Произошла ошибка: {str(e)}", 500
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

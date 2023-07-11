from flask import Blueprint, render_template, request, redirect, url_for, send_file
import fitz
from werkzeug.utils import secure_filename
import os, zipfile
from PIL import Image, ImageChops

bp=Blueprint('blueprint', __name__)
tmp_folder_name="tmp"

@bp.route('/')
@bp.route('/img_playground')
def index():
    return render_template('index.html', title="HomePage")

@bp.route('/pdf2img', methods=['POST', 'GET'])
def convert(**kwargs):
    if request.method == 'POST':
        format=request.form.get('image-format')
        # Get the uploaded PDF file
        pdf_file = request.files['file']
        pdf_file_name=secure_filename(pdf_file.filename)
        file_dir=os.path.join(tmp_folder_name, pdf_file_name)
        pdf_file.save(file_dir)
        filename_no_extension=pdf_file_name.replace(".pdf", "")

        f = fitz.open(file_dir)
        zoom=4
        mat = fitz.Matrix(zoom, zoom)
        for i in range(len(f)):
            f_name=filename_no_extension + "_" + str(i) + "." + str(format)
            val=f"{tmp_folder_name}/{f_name}"
            page=f.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            print(val)
            pix.save(val)
            with zipfile.ZipFile(f"{tmp_folder_name}/{filename_no_extension}.zip", 'a') as zipf:
                zipf.write(val, arcname=f_name)
        f.close()
        os.remove(file_dir)
        # Redirect to the page displaying the converted images
        return send_file(f'{tmp_folder_name}/{filename_no_extension}.zip', as_attachment=True)
    for filename in os.listdir(tmp_folder_name):
        file_path = os.path.join(tmp_folder_name, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return render_template('convert.html', title="PDF to Image")
    
@bp.route('/trim', methods=['POST', 'GET'])
def trim():
    if request.method == 'POST':
        f = request.files['file']
        f_name=secure_filename(f.filename)
        file_dir=os.path.join(tmp_folder_name, f_name)
        f.save(file_dir)

        im = Image.open(file_dir)
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            trimmed= im.crop(bbox)
        else: 
            # Failed to find the borders, convert to "RGB"        
            trimmed=im.convert('RGB')
        im=trimmed.save(file_dir)
        return send_file(file_dir, as_attachment=True)
    for filename in os.listdir(tmp_folder_name):
        file_path = os.path.join(tmp_folder_name, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return render_template('trim.html', title="Remove Whitespaces")
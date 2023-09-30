from flask import Flask, render_template, request, redirect, send_file
from main import process_info

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content_list = request.form.to_dict()
        process_info(content_list)
        return redirect('/download-resume')

    else:
        return render_template('index.html')
    
@app.route('/download-resume/')
def download_resume():
    return send_file('resume.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(port=5500)
from flask import Flask, render_template, request
from analyzer import analyze_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = {}
    code = ""
    if request.method == 'POST':
        code = request.form['code']
        analysis = analyze_code(code)
    return render_template('index.html', analysis=analysis, code=code)

if __name__ == '_main_':
    app.run(debug=True)
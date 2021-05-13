# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from urllib import request
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__, template_folder='template', static_folder='static')
# use google search engine
# browser = webdriver.Chrome()
# browser.get("https://www.google.com/")

results = {'meal': '', 'diet_restrictions': []}
others = []


@app.route('/', methods=["GET", "POST"])
def index():
    # if request.method == 'POST':
    #     return f'''<label class="btn btn-outline-secondary">\
    #         <input type="checkbox" name="diet_button" \
    #         value="{{ request.form.get('other') }}">"{{ request.form.get('other') }}"\
    #             </label>'''
    # else:
    # if request.method == 'POST':
    #     others.append(request.form.get('other'))
    #     return render_template('index.html', others=others)
    return render_template('index.html')


@app.route('/add_other', methods=['POST'])
def add_other():
    others.append(request.form.get('other'))
    return render_template('index.html', others=others)


@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)

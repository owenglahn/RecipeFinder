from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup as soup

app = Flask(__name__, template_folder='template', static_folder='static')


user_input = {'meal': '', 'diet_restrictions': []}
others = []


@app.route('/', methods=["GET", "POST"])
def index():
    user_input['diet_restrictions'] = request.form.getlist('diet_button')
    user_input['meal'] = request.form.get('meal')
    return render_template('index.html')


@app.route('/add_other', methods=['POST'])
def add_other():
    others.append(request.form.get('other'))
    return render_template('index.html', others=others)


@app.route('/results')
def results():
    search_string = ''
    for rest in user_input['diet_restrictions']:
        search_string += rest + ';'
    # use google search engine
    search_string += user_input.get('meal') + ';recipe'
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    google_search = driver.find_element_by_name("q")
    google_search.clear()
    # search with user input as keywords
    google_search.send_keys(search_string)
    google_search.send_keys(Keys.ENTER)
    # sleep(4)
    assert "No results found." not in driver.page_source
    # get page source
    recipes = soup(driver.page_source, 'html.parser').find_all('a')[5:]
    driver.quit()
    # web scrape results from search
    return render_template('results.html', recipes=recipes, search_string=search_string)

if __name__ == '__main__':
    app.run(debug=True)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup as soup
import os
import validators

app = Flask(__name__, template_folder='template', static_folder='static')

user_input = {'meal': '', 'diet_restrictions': []}
others = []


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_input['meal'] = request.form.get('meal')
        user_input['diet_restrictions'] = request.form.getlist('diet_button')
        return redirect(url_for('results'))
    return render_template('index.html')


@app.route('/results')
def results():
    search_string = ''
    for rest in user_input['diet_restrictions']:
        search_string += rest + ';'

    search_string += user_input.get('meal') + ';recipe'
    # depends on safari being installed and safaridriver being enabled
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # use google search engine
    driver.get("https://www.google.com/")
    google_search = driver.find_element_by_name("q")
    google_search.clear()
    # search with user input as keywords
    google_search.send_keys(search_string)
    google_search.send_keys(Keys.ENTER)
    assert "No results found." not in driver.page_source
    # web scrape results from search, filter valid links
    recipes = soup(driver.page_source, 'html.parser').find_all('a')[10:30]
    # recipes = filter(validators.url, recipes)
    for link in recipes:
        valid = validators.url(link.get('href'))
        if not valid or len(link.get_text()) < 15:
            recipes.remove(link)
    driver.quit()
    return render_template('results.html', recipes=recipes, search_string=search_string)


if __name__ == '__main__':
    app.run(debug=True)

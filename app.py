from functions import monster_search

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        form_data = request.form
        monster_name = form_data.get('monster')
        search_results = monster_search(monster_name)
        return render_template('results.html', results=search_results)
    else:
        return 'Wrong HTTP method', 400


if __name__ == '__main__':
    app.run(debug=True)
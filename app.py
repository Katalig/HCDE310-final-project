from functions import monster_search

from flask import Flask, render_template, request

# Create an instance of Flask

app = Flask(__name__)

# Create a view function for /
@app.route('/')
def index():
    return render_template('index.html')


# Create a view function for /results
@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        form_data = request.form
        monster_name = form_data.get('monster')
        search_results = monster_search(monster_name)
        print(search_results)
        return render_template('results.html', monster=monster_name, results=search_results)
    else:
        return 'Wrong HTTP method', 400


if __name__ == '__main__':
    app.run(debug=True)
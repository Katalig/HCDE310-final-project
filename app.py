from functions import wikipedia_locationsearch

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
        max_results = int(form_data.get('max_results', 10))
        radius = float(form_data.get('radius', 2.0))
        place = form_data.get('place')
        sort = form_data.get('sort')
        search_results = wikipedia_locationsearch(place, max_results, radius, sort)
        return render_template('results.html', place=place, results=search_results)
    else:
        return 'Wrong HTTP method', 400


if __name__ == '__main__':
    app.run(debug=True)
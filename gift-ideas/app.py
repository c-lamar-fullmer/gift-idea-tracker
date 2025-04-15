from flask import Flask, render_template, redirect, request, url_for, session

app = Flask(__name__)

app.secret_key='secret1'

people_gift_list = {
    "LaMar": ['toys', 'shoes'],
    "Gus": ["ipad", 'wallet', 'shoes'],
    "Daphny": ['necklace', 'books'],
}

def search_matching(query):
    if not query:
        return []

    results = []
    query_lower = query.lower()
    for name, items_lst in session['people_gift_list'].items():
        matching_items = [item for item in items_lst if query_lower in item.lower()]
        if matching_items:
            results.append({'name': name, 'items_lst': matching_items})
    return results

def highlight(text, term):
    return text.replace(term, f'<strong>{term}</strong>')

@app.before_request
def initialize_session():
    if 'people_gift_list' not in session:
        session['people_gift_list'] = people_gift_list
        # session['people_gift_list'] = []

@app.route("/")
def home():
    return render_template('home.html', people=session['people_gift_list'])

@app.route("/person/<name>")
def person(name):
    if name in session['people_gift_list']:
        return render_template('name.html', name=name, people_gifts=session['people_gift_list'])
    else:
        return redirect(url_for('home'))

@app.route("/search")
def search():
    query = request.args.get('query', '')
    results = search_matching(query)
    return render_template('search.html', query=query, results=results)

# Define the missing 'edit_page' route (for now, it just redirects to home)
@app.route("/edit_person")
def edit_person():
    return render_template('edit_person.html') # You'll need to create this template

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5003)
from uuid import uuid4

from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session,
    )

app = Flask(__name__)

app.secret_key='secret1'

def find_person(name):
    for person in session['people_gift_list']:
        if person['name'] == name:
            return person

def search_matching(query):
    if not query:
        return []

    results = []
    query_lower = query.lower()
    for person in session['people_gift_list']:
        matching_items = [item for item in person['gift_lst'] if query_lower in item.lower()]
        if matching_items:
            results.append({'name': person['name'], 'items_lst': matching_items})
    return results

def highlight(text, term):
    return text.replace(term, f'<strong>{term}</strong>')

@app.before_request
def initialize_session():
    session['people_gift_list'] = [
        {'id': str(uuid4()),
         'name': "LaMar",
         'gift_lst': ['toys', 'shoes']
         },
         {'id': str(uuid4()),
         'name': "Gus",
         'gift_lst': ['books', 'puzzles']
         },
         ]

@app.route("/")
def home():
    return render_template('home.html', people=session['people_gift_list'])

@app.route("/<name>")
def person(name):
    for person in session['people_gift_list']:
        if person['name'] == name:
            name = person['name']
            gift_lst = person['gift_lst']
            return render_template('name.html', name=name, gift_lst=gift_lst)
    else:
        return redirect(url_for('home'))

@app.route("/search")
def search():
    query = request.args.get('query', '')
    results = search_matching(query)
    return render_template('search.html', query=query, results=results)

@app.route("/edit")
def edit_list():
    return render_template('edit_list.html', people=session['people_gift_list'])

@app.route("/edit/<name>")
def edit_person(name):
    person = find_person(name)
    name = person['name']
    formatted_gift_lst = '\n'.join(person['gift_lst'])
    return render_template('edit_person.html',
                           name=name,
                           gift_lst=formatted_gift_lst
                           )

# @app.route("/edit_person", methods=["POST"])
# def delete_person():
#     return redirect(url_for('edit_person'))

@app.route("/edit/add_person")
def add_person():
    return render_template('add_person.html')

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5003)
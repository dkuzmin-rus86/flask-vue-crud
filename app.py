# https://tproger.ru/translations/developing-app-with-flask-and-vue-js/

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
import sqlite3
import uuid


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# instantiate the app
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
# app.config["DEBUG"] = True
# app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

# enable CORS
cors = CORS(app, resources={r'/*': {'origins': '*'}})


class GetAllBook(Resource):
    def get(self):
        con = sqlite3.connect("books.db")
        cur = con.cursor()
        cur.execute("select * from students")  
        rows = cur.fetchall(); 
        print(rows)
        return rows


class CreateTableStudent(Resource):
    def post(self):
        conn = sqlite3.connect('books.db')
        conn.execute('CREATE TABLE students (name TEXT, city TEXT)')
        print('Table created successfully')
        conn.close()
        return 'Table created successfully'


class HelloWorld(Resource):
    def get(self):
        return jsonify({
             'status': 'success',
             'data': 'Hello World'
            })
    
    def post(self):
        return {'data': 'Posted success'}


api.add_resource(HelloWorld, '/helloworld')
api.add_resource(CreateTableStudent, '/createtable')
api.add_resource(GetAllBook, '/students')


@app.route('/test', methods=['GET'])
def test():
    return jsonify('Тестовое json сообщение')


@app.route("/", methods=['GET'])
def index():
    pagetitle = "HomePage"
    return render_template("home.html",
                            mytitle=pagetitle
                          )


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


@app.route("/test2/", methods=["POST"])
@cross_origin()
def post_example():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        print(request.get_json())
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(debug=True)
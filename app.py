
from flask import Flask, request, jsonify
from database import get_db, close_db
from models import create_tables
from utils import generate_token, paginate
from datetime import date


app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

@app.before_request
def initialize():
    if not hasattr(app, 'initialized'):
        create_tables()
        app.initialized = True

# CRUD operations for books
@app.route('/books', methods=['GET', 'POST'])
def books():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO books (title, author, published_year) VALUES (%s, %s, %s)",
                       (data['title'], data['author'], data['published_year']))
        db.commit()
        return jsonify({"message": "Book added successfully"}), 201

    # GET: Search and Paginate
    title = request.args.get('title')
    author = request.args.get('author')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")
    if author:
        query += " AND author LIKE %s"
        params.append(f"%{author}%")

    cursor.execute(query, params)
    books = cursor.fetchall()

    # Adding status: either 'not issued' or member_id
    for book in books:
        if book['member_id'] is None:
            book['status'] = 'not issued'
        else:
            book['status'] = f'Issued to member ID: {book["member_id"]}'

    return jsonify(paginate(books, page, per_page))

@app.route('/issued_books_by_member/<int:member_id>', methods=['GET'])
def issued_books_by_member(member_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT * FROM books WHERE member_id = %s
    """
    cursor.execute(query, (member_id,))
    books = cursor.fetchall()

    # Adding status: issued to this member
    for book in books:
        book['status'] = f'Issued to member ID: {member_id}'

    return jsonify(books)

@app.route('/books/<int:book_id>', methods=['PUT', 'DELETE', 'GET', 'POST', 'PATCH'])
def manage_book(book_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE books SET title=%s, author=%s, published_year=%s WHERE id=%s",
                       (data['title'], data['author'], data['published_year'], book_id))
        db.commit()
        return jsonify({"message": "Book updated successfully"})

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        db.commit()
        return jsonify({"message": "Book deleted successfully"})
    elif request.method == 'PATCH':
        # Assign a member to a book
        data = request.json
        member_id = data.get("member_id")
        
        # Validate if member_id exists in the members table (optional but recommended)
        cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"}), 404

        cursor.execute("UPDATE books SET member_id = %s WHERE id = %s", (member_id, book_id))
        db.commit()
        return jsonify({"message": f"Book {book_id} issued to member {member_id}"}), 200

    elif request.method == 'GET':
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(book), 200
    
# CRUD operations for members
@app.route('/members', methods=['GET', 'POST'])
def members():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (data['name'], data['email']))
        db.commit()
        return jsonify({"message": "Member added successfully"}), 201

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    return jsonify(members)

@app.route('/members/<int:member_id>', methods=['PUT', 'DELETE'])
def manage_member(member_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE members SET name=%s, email=%s WHERE id=%s",
                       (data['name'], data['email'], member_id))
        db.commit()
        return jsonify({"message": "Member updated successfully"})

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM members WHERE id=%s", (member_id,))
        db.commit()
        return jsonify({"message": "Member deleted successfully"})

@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    data = request.json

    cursor.execute("SELECT * FROM members WHERE email=%s", (data['email'],))
    member = cursor.fetchone()
    if member:
        token = generate_token()
        cursor.execute("INSERT INTO tokens (member_id, token) VALUES (%s, %s)", (member['id'], token))
        db.commit()
        return jsonify({"token": token})
    return jsonify({"error": "Invalid email"}), 401

@app.route('/validate', methods=['POST'])
def validate():
    token = request.headers.get('Authorization')
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tokens WHERE token=%s", (token,))
    if cursor.fetchone():
        return jsonify({"message": "Valid token"})
    return jsonify({"error": "Invalid token"}), 401

@app.route('/return_book/<int:book_id>', methods=['POST'])
def return_book(book_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Check if the book exists and is currently issued to a member
    cursor.execute("SELECT * FROM books WHERE id = %s AND member_id IS NOT NULL", (book_id,))
    book = cursor.fetchone()

    if not book:
        return jsonify({"error": "Book is not issued or doesn't exist"}), 404

    # Update the book to set member_id to NULL (i.e., return the book)
    cursor.execute("UPDATE books SET member_id = NULL WHERE id = %s", (book_id,))
    db.commit()

    return jsonify({"message": f"Book {book_id} returned successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)

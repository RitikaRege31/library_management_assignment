# Library Management API
## Overview
This project provides an API for managing a library system, including functionalities for performing CRUD operations on books, members, issuing books to members, and returning books. The API also allows querying the list of books and books assigned to particular members,  Includes search functionality for books by title or author and  Implements pagination and token-based authentication.
## Prerequisites
Before setting up and running the project, ensure you have the following installed on your machine:
Python 3.7+
MySQL or MariaDB
Postman (for testing API endpoints)
Pip (Python package installer)

## Project Setup
1. Clone the Repository
   ```bash
   git clone https://github.com/your-username/library-management-api.git
   cd library-management-api
2. Create a Virtual Environment
   ```bash
   python -m venv venv
   venv\Scripts\Activate #For windows
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
4. Set Up Database
   1. Create the Database:
      Log in to MySQL
      ```bash
      mysql -u root -p
      CREATE DATABASE library_db;
    2. Configure database
       In the database.py file, configure the database connection settings:
       ```bash
       import mysql.connector
       def get_db():
          return mysql.connector.connect(
             host="localhost",
             user="root",  # Your MySQL username
             password="password",  # Your MySQL password
             database="library_db"  # The database you created
          )
5. Run the Application
   The application will be available at http://127.0.0.1:5000/books
   ```bash
   python app.py

## Testing the API with Postman
Follow the steps below to test the API using Postman:

1. Add Books (POST /books)
To add a new book to the system, use the POST {/books} endpoint.
Request:
  Method: {POST}
  Endpoint: {/books}
  Body:
   ```json
   {
     "title": "Book Title",
     "author": "Author Name",
     "published_year": 2022
   }
  response:
   ```json
   {
    "message": "Book added successfully"
   }

2. Add Members (POST /members)
To add a new member to the system, use the POST /members endpoint.
Request:
  Method: {POST}
  Endpoint: /members
  Body:
   ```json
   {
     "name": "Member Name",
     "email": "member@example.com"
   }
  response:
   ```json
   {
    "message": "Member added successfully"
   }

3. Issue a Book (PATCH /books/{book_id})
   To issue a book to a member, use the PATCH /books/{book_id} endpoint.
   Request:
    Method: {PATCH'}
    Endpoint: /books/{book_id} (Replace {book_id} with the actual book ID)
    Body:
     ```json
     {
      "member_id": 1  // Replace with the actual member ID
     }
    Response:
     ```json
      {
       "message": "Book {book_id} issued to member {member_id}"
      }

4. Return a Book (POST /return_book/{book_id})
   To return a book, use the POST /return_book/{book_id} endpoint.
   Request:
    Method: {POST}
    Endpoint: {/return_book/{book_id}} (Replace {book_id} with the actual book ID)
    Body: (Empty body)
     ```json
     {}
    Response:
     ```json
     {
      "message": "Book {book_id} returned successfully"
     }

5. Get Books by Member ({GET /issued_books_by_member/{member_id}})
   To retrieve a list of books issued to a specific member, use the {GET /issued_books_by_member/{member_id}}endpoint.
   Request:
    Method: {GET}
    Endpoint: {/issued_books_by_member/{member_id}} (Replace {member_id} with the actual member ID)
   Response:
    ```json
    [
     {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "published_year": 2022,
        "member_id": 1,
        "status": "Issued to member ID: 1"
     }
    ]

6. Log In to Get a Token (POST /login)
   Method: {POST}
   URL: http://127.0.0.1:5000/login
   Body:
   Select Body > raw.
   Choose JSON from the dropdown.
   Add the following payload
    ```json
    {
      "email": "john.doe@example.com"
    }
   Send Request: Click Send.
   Expected Response:
    ```json
    {
      "token": "generated_token_here"
    }
   Note: Copy the token for use in subsequent requests

7. Validate Token (POST {/validate})
   Method: {POST}
   URL: http://127.0.0.1:5000/validate
   Headers:
   Add a header: {Authorization: generated_token_here}.
   Send Request: Click Send.
   Expected Response:
    ```json
    {
      "message": "Valid token"
    }

## Design Decisions
  1. Database Schema
     Books Table: The books table contains columns for id, title, author, published_year, and member_id. The member_id is NULL when a book is not issued, and it stores the ID of the member to whom the book is issued.
     Members Table: The members table contains columns for id, name, and email to store member details.

  2. API Endpoints
     CRUD for Books: The /books endpoint supports both GET and POST methods. It allows for adding books and searching books by title or author with pagination.
     CRUD for Members: The /members endpoint supports GET and POST methods, enabling adding members and retrieving all members.

   Issue and Return Books: The API supports issuing books (PATCH /books/{book_id}) by assigning a member_id, and returning books (POST /return_book/{book_id}) by setting member_id to NULL.

   Handling Book Status: A status field is dynamically added to the book data, showing either "not issued" or "Issued to member ID: {member_id}" based on the member_id.

  3. Authentication (optional)
     For a production environment, an authentication mechanism such as JWT (JSON Web Tokens) would be ideal. In this current version, the authentication part is simplified, but it’s highly recommended to add token-based authentication for security.

## Contributor
   Ritika Rege
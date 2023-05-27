from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.sqlite3"
app.config["SECRET_KEY"] = "random string"
CORS(app)

db = SQLAlchemy(app)


# Books model
class Books(db.Model):
    id = db.Column("ID", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year_published = db.Column(db.String(100))
    book_type = db.Column(db.Integer)

    def __init__(self, name, author, year_published, book_type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "year_published": self.year_published,
            "book_type": self.book_type,
        }


# Function to display books
@app.route("/show-books", methods=["GET"])
def show_books():
    books_list = [book.to_dict() for book in Books.query.all()]
    return jsonify(books_list)


# Function to add a book
@app.route("/add-book", methods=["POST"])
def add_book():
    data = request.get_json()
    name = data.get("name")
    author = data.get("author")
    year_published = data.get("year_published")
    book_type = data.get("book_type")

    new_book = Books(name, author, year_published, book_type)
    db.session.add(new_book)
    db.session.commit()
    return "A new record was created."


# Function to delete a book
@app.route("/delete-book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Books.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return "Book deleted."
    else:
        return "Book not found."


# Get a single book info
@app.route("/get-book/<book_id>", methods=["GET"])
def get_book(book_id):
    book = Books.query.get(book_id)
    return jsonify(book.to_dict())


# Function to update a book
@app.route("/update-book/<book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    name = data.get("name")
    author = data.get("author")
    year_published = data.get("year_published")
    type_book = data.get("type_book")

    book = Books.query.get(book_id)
    if book:
        book.name = name
        book.author = author
        book.year_published = year_published
        book.type_book = type_book
        db.session.commit()
        return "The record was updated."
    else:
        return "Book not found."


# Customers model
class Customers(db.Model):
    id = db.Column("ID", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    age = db.Column(db.String(100))

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "age": self.age,
        }


# Function to display customers
@app.route("/show-customers", methods=["GET"])
def show_customers():
    customers_list = [customer.to_dict() for customer in Customers.query.all()]
    return jsonify(customers_list)


# Function to add a customer
@app.route("/add-customer", methods=["POST"])
def add_customer():
    data = request.get_json()
    name = data.get("name")
    city = data.get("city")
    age = data.get("age")

    new_customer = Customers(name, city, age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new record was created."


# Function to delete a customer
@app.route("/delete-customer/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customers.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return "Customer deleted."
    else:
        return "Customer not found."


# Get a single customer info
@app.route("/get-customer/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customers.query.get(customer_id)
    return jsonify(customer.to_dict())


# Function to update a customer
@app.route("/update-customer/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    name = data.get("name")
    city = data.get("city")
    age = data.get("age")

    customer = Customers.query.get(customer_id)
    if customer:
        customer.name = name
        customer.city = city
        customer.age = age
        db.session.commit()
        return "The record was updated."
    else:
        return "Customer not found."


# Loans model
class Loans(db.Model):
    id = db.Column("ID", db.Integer, primary_key=True)
    custid = db.Column("custid", db.Integer, db.ForeignKey("customers.ID"))
    bookid = db.Column("bookid", db.Integer, db.ForeignKey("books.ID"))
    loandate = db.Column(db.Date)
    returndate = db.Column(db.Date)

    # customer = relationship("Customers", foreign_keys=[cust_id])
    # book = relationship("Books", foreign_keys=[book_id])

    def __init__(self, cust_id, book_id, loan_date, return_date):
        self.custid = cust_id
        self.bookid = book_id
        self.loandate = loan_date
        self.returndate = return_date

    def to_dict(self):
        return {
            "id": self.id,
            "cust_id": self.cust_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date.strftime("%d/%m/%Y"),
            "return_date": self.return_date.strftime("%d/%m/%Y"),
        }


# Function to display loans
@app.route("/show-loans", methods=["GET"])
def show_loans():
    loans_list = [loan.to_dict() for loan in Loans.query.all()]
    return jsonify(loans_list)


# Function to add a loan
@app.route("/add-loan", methods=["POST"])
def add_loan():
    try:
        data = request.get_json()
        cust_id = int(data["cust_id"])
        book_id = int(data["book_id"])
        loan_date = datetime.strptime(data["loan_date"], "%d/%m/%Y").date()
        return_date = datetime.strptime(data["return_date"], "%d/%m/%Y").date()

        # Check if a loan with the same cust_id and book_id already exists
        existing_loan = Loans.query.filter_by(custid=cust_id, bookid=book_id).first()
        if existing_loan:
            return "Loan already exists for the given customer and book."
        customer = Customers.query.get(cust_id)
        book = Books.query.get(book_id)

        if not customer or not book:
            return "Invalid customer or book."

        # Calculate the loan duration based on book_type
        book_type_to_days = {
            1: timedelta(days=10),
            2: timedelta(days=5),
            3: timedelta(days=2),
        }
        loan_duration = book_type_to_days.get(book.book_type)
        if loan_duration:
            return_date = loan_date + loan_duration
            print(f"loan date is {loan_date}")
            print(f"return_date is {return_date}")
            new_loan = Loans(
                cust_id=cust_id,
                book_id=book_id,
                loan_date=loan_date,
                return_date=return_date,
            )
            db.session.add(new_loan)
            db.session.commit()
            return "A new loan was created."
        else:
            return "Invalid book type."
    except Exception as error:
        print("error: %s" % error)
        return "shtok"


# Function to fetch book data from Google Books API and add it to the database
# def fetch_and_add_books():
#     url = "https://www.googleapis.com/books/v1/volumes?q=python"  # Replace 'python' with your desired search query
#     response = requests.get(url)
#     data = response.json()

#     for item in data.get("items", []):
#         volume_info = item.get("volumeInfo", {})
#         title = volume_info.get("title", "")
#         authors = volume_info.get("authors", [])
#         published_date = volume_info.get("publishedDate", "")
#         book_type = random.randint(1, 3)

#         new_book = Books(title, ", ".join(authors), published_date, book_type)
#         db.session.add(new_book)

#     # db.session.add(new_book)

#     db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

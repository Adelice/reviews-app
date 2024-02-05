from flask import Flask, request, jsonify,redirect, url_for, flash
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager 
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_migrate import Migrate
import json
import requests

from models import db, User, Categories, Book, Comment, Notification, Movie, Hotel, Review
import os

app = Flask(__name__)
CORS(app)

#Database Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'thisisasecretkey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO', 'False').lower() in ['true', '1', 't']

#Email configuration
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)


jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "<p>Critiq Hub</p>"

@app.route('/logintoken', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email=email).first()

    
    if user is None:
        return jsonify({"error": "Wrong email or passwords"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}),  401

    access_token = create_access_token(identity=email)
  
    
    return jsonify({
        "email": email,
        "access_token": access_token

    })

@app.route("/signup", methods=["POST"])
def signup():
    email = request.json["email"]
    password = request.json["password"]    
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    
    # Convert the birthday string to a date object
    birthday_str = request.json["birthday"]
    birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password, birthday=birthday)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response 

@app.route('/profile/<getemail>')
@jwt_required() 
def my_profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
       
    
    response_body = {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
    }
  
    return jsonify(response_body)

@app.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"message": "If an account with this email exists, a password reset link has been sent."}), 200

    return jsonify({"message": "If an account with this email exists, a password reset link has been sent."}), 200

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json.get("email")
    new_password = request.json.get("new_password")
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Invalid request"}), 400
    
    hashed_password = bcrypt.generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password has been successfully reset."}), 200


@app.route('/books')
def books():
    api_key = 'AIzaSyAuzbJr7axrcL_C9V0Ph0GQxEx1OFod42o'
    api_url = f'https://www.googleapis.com/books/v1/volumes?q=programming&key={api_key}'

    response = requests.get(api_url)
    data = response.json()

    for item in data.get('items', []):
        volume_info = item.get('volumeInfo', {})
        book_id = item.get('id')
        title = volume_info.get('title', 'No Title')
        author = ', '.join(volume_info.get('authors', ['Unknown Author']))
        description = volume_info.get('description', 'No Description')
        published_date = volume_info.get('publishedDate', '')
        page_count = volume_info.get('pageCount', 0)

        image_links = volume_info.get('imageLinks', {})
        thumbnail_url = image_links.get(
            'thumbnail', 'https://via.placeholder.com/128x192.png')

        existing_book = Book.query.get(book_id)

        if existing_book:
            existing_book.title = title
            existing_book.author = author
            existing_book.description = description
            existing_book.published_date = published_date
            existing_book.page_count = page_count
            existing_book.thumbnail_url = thumbnail_url
        else:
            new_book = Book(
                id=book_id,
                title=title,
                author=author,
                description=description,
                published_date=published_date,
                page_count=page_count,
                thumbnail_url=thumbnail_url
            )
            db.session.add(new_book)

    db.session.commit()

    # Return the books data as JSON
    books = Book.query.all()
    books_data = [book.to_dict() for book in books]
    return jsonify(books_data)

@app.route('/movies')
def movies():

    tmdb_api_key = '37b6a378f10e5a19a9f9d40c5a1b0fb5'
    tmdb_endpoint = f'https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=en-US&page=1'

    response = requests.get(tmdb_endpoint)
    data = response.json()

    for movie_data in data.get('results', []):
        movie_id = movie_data.get('id')
        title = movie_data.get('title', 'No Title')
        year = movie_data.get('release_date', '')[:4]
        description = movie_data.get('overview', 'No Description')
        poster_url = f'https://image.tmdb.org/t/p/w500/{movie_data.get("poster_path", "")}'

        # Check if the movie already exists in the database
        existing_movie = Movie.query.get(movie_id)

        if existing_movie:
            existing_movie.title = title
            existing_movie.year = year
            existing_movie.description = description
            existing_movie.poster_url = poster_url
        else:
            new_movie = Movie(
                id=movie_id,
                title=title,
                year=year,
                description=description,
                poster_url=poster_url
            )
            db.session.add(new_movie)

    db.session.commit()

    # Return the movies data as JSON
    movies = Movie.query.all()
    movies_data = [movie.to_dict() for movie in movies]
    return jsonify(movies_data)

@app.route('/hotels')
def hotels():
    api_key = 'AIzaSyB1cpqF-_4SBuY4_DS5rhaDXycjI7pzrd0'
    location = 'Nairobi'
    radius = 4000  

    data = fetch_restaurant_data(api_key, location, radius)

    update_database_with_hotels(data)

    hotels = Hotel.query.all()
    hotels_data = [hotel.to_dict() for hotel in hotels]
    return jsonify(hotels_data)


def fetch_restaurant_data(api_key, location, radius):
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    params = {
        'location': location,
        'radius': radius,
        'type': 'restaurant',  
        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def update_database_with_hotels(data):
    for result in data.get('results', []):
        hotel_id = result.get('place_id')
        name = result.get('name', 'No Name')
        address = result.get('vicinity', 'No Address')
        rating = result.get('rating', 0.0)

        # Get the first photo URL if available
        photo_reference = result.get('photos', [{}])[
            0].get('photo_reference', '')
        photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}'

        existing_hotel = Hotel.query.get(hotel_id)

        if existing_hotel:
            existing_hotel.name = name
            existing_hotel.address = address
            existing_hotel.rating = rating
            existing_hotel.photo_url = photo_url
        else:
            new_hotel = Hotel(
                id=hotel_id,
                name=name,
                address=address,
                rating=rating,
                photo_url=photo_url
            )
            db.session.add(new_hotel)

    db.session.commit()

@app.route('/tables')
def check_tables():
    try:
        with app.app_context():
            db.create_all()
            db.session.commit()

        # Check if tables exist by querying them
        hotels_exist = db.session.query(Hotel).first() is not None
        books_exist = db.session.query(Book).first() is not None
        movies_exist = db.session.query(Movie).first() is not None

        return jsonify({
            'hotels_table_exist': hotels_exist,
            'books_table_exist': books_exist,
            'movies_table_exist': movies_exist
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Categories
def populate_categories():
    categories = [
        Categories(name='Books', category='books'),
        Categories(name='Movies', category='movies'),
        Categories(name='Hotels', category='hotels'),
    ]

    for category in categories:
        db.session.add(category)

    db.session.commit()

    return categories

with app.app_context():
    db.create_all()
    all_categories = populate_categories()

#allcategories

@app.route('/categories', methods=['GET'])
def get_all_categories():
    all_categories = Categories.query.all()
    categories_list = [category.to_dict() for category in all_categories]
    return jsonify({'categories': categories_list})

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    content = data.get('content')
    rating = data.get('rating')
    product_type = data.get('product_type')
    product_id = data.get('product_id')
    category_id = data.get('category_id')

    if not content or not rating or not product_type or not product_id or not category_id:
        return jsonify({'error': 'Missing data'}), 400

    review = Review(
        content=content,
        rating=rating,
        category_id=category_id,
        book_id=data.get('book_id'),
        movie_id=data.get('movie_id'),
        hotel_id=data.get('hotel_id'),
    )

    db.session.add(review)
    db.session.commit()

    send_review_email(review.author.email, review.content)
    return jsonify({'message': 'Review added successfully'}), 201

@app.route('/categories/<category>', methods=['GET'])
def get_category_products(category):

    if category == 'books':
        products = Book.query.all()
    elif category == 'hotels':
        products = Hotel.query.all()
    elif category == 'movies':
        products = Movie.query.all()
    # Add other categories similarly

    products_list = [product.to_dict() for product in products]
    return jsonify({'category': category, 'products': products_list})


@app.route('/products/<product_type>/<product_id>/reviews', methods=['GET'])
def get_reviews(product_type, product_id):
    if product_type == 'hotels':
        reviews = Review.query.filter_by(hotel_id=product_id).all()
    elif product_type == 'books':
        reviews = Review.query.filter_by(book_id=product_id).all()
    
    else:
        return jsonify({'error': 'Invalid product type'}), 400

    return jsonify({'reviews': [review.to_dict() for review in reviews]})


@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)

    if not review:
        return jsonify({'error': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully'})


@app.route('/reviews/<review_id>/comments', methods=['POST'])
def add_comment(review_id):
    review = Review.query.get(review_id)

    if not review:
        return jsonify({'error': 'Review not found'}), 404

    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Missing comment content'}), 400

    comment = Comment(content=content, review_id=review_id)
    db.session.add(comment)
    db.session.commit()

    send_comment_email(comment.author.email, comment.content)
    return jsonify({'message': 'Comment added successfully'}), 201


#send emails
def send_signup_email(email):
    subject = 'Welcome to Critiq Hub!'
    body = f'Thank you for signing up with Your App, {email}! We are excited to have you on board.'
    send_email(email, subject, body)


def send_review_email(author_email, review_content):
    subject = 'New Review Submitted'
    body = f'Hello!\n\nA new review has been submitted:\n\n{review_content}\n\nBest regards,\nYour App Team'
    send_email(author_email, subject, body)


def send_comment_email(author_email, comment_content):
    subject = 'New Comment Submitted'
    body = f'Hello!\n\nA new comment has been submitted:\n\n{comment_content}\n\nBest regards,\nCritiq Hub'
    send_email(author_email, subject, body)


def send_email(recipient, subject, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    # If you want to include HTML content in your emails, you can set msg.html as well
    mail.send(msg)
    flash(f'A message was sent to {recipient}.')
    return redirect(url_for('home'))


@app.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    company_id = data.get('company_id')
    review_id = data.get('review_id')
    content = data.get('content')

    if not company_id or not review_id or not content:
        return jsonify({'error': 'Missing data'}), 400

    new_notification = Notification(
        company_id=company_id,
        review_id=review_id,
        content=content,
        timestamp=datetime.utcnow()
    )

    db.session.add(new_notification)
    db.session.commit()

    return jsonify({'message': 'Notification created successfully'}), 201


@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    notifications_dict_list = [notification.to_dict()
                               for notification in notifications]
    return jsonify({'notifications': notifications_dict_list})


@app.route('/notifications/<int:notification_id>', methods=['PUT'])
def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)

    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({'message': 'Marked as read'}), 200



if __name__ == '__main__':
    app.run(debug=True)
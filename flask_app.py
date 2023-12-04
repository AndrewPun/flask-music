from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, login_required, LoginManager, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="musicdbhw",
    password="",
    hostname="musicdbhw.mysql.pythonanywhere-services.com",
    databasename="musicdbhw$music",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = ""
login_manager = LoginManager()
login_manager.init_app(app)


class Users(db.Model, UserMixin):

    __tablename__ = "Users"

    USER_ID = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String(255))
    PASSWORD = db.Column(db.String(255))
    FIRST_NAME = db.Column(db.String(255))
    LAST_NAME = db.Column(db.String(255))
    STREET_ADDRESS = db.Column(db.String(255))
    STATE_ABBREVIATION = db.Column(db.String(255))
    ZIPCODE = db.Column(db.String(255))
    EMAIL_ADDRESS = db.Column(db.String(255))
    CITY = db.Column(db.String(255))
    COUNTRY = db.Column(db.String(255))



    def get_password(self):
        return self.PASSWORD

    def get_id(self):
        return str(self.USER_ID)

@login_manager.user_loader
def load_user(USER_ID):
    USER_ID = str(USER_ID)
    return Users.query.filter_by(USERNAME=USER_ID).first()

def validate_password(self, password):
        old_user = self
        user = Users.query.filter_by(PASSWORD=password).first()
        if user is None:
            return False
        elif old_user != user:
            return False
        return True


class Album(db.Model):

    __tablename__ = "Album"

    ALBUM_ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(255))
    DESCRIPTION = db.Column(db.String(255))
    NUMBER_SOLD = db.Column(db.String(255))
    RATING = db.Column(db.String(255))
    ARTIST_ID = db.Column(db.Integer, db.ForeignKey('Artist.ARTIST_ID'))

class Artist(db.Model):

    __tablename__ = "Artist"

    ARTIST_ID = db.Column(db.Integer, primary_key=True)
    FIRST_NAME = db.Column(db.String(255))
    LAST_NAME = db.Column(db.String(255))

class CD(db.Model):

    __tablename__ = "CD"

    CD_ID = db.Column(db.Integer, primary_key=True)
    SIZE_CD = db.Column(db.Integer)

class Genre(db.Model):

    __tablename__ = "Genre"

    GENRE_ID = db.Column(db.Integer, primary_key=True)
    GENRE_NAME = db.Column(db.String(255))

class MP3(db.Model):

    __tablename__ = "MP3"

    MP3_ID = db.Column(db.Integer, primary_key=True)
    SIZE_MP3 = db.Column(db.Integer)

class Orders(db.Model):

    __tablename__ = "Orders"

    ORDER_ID = db.Column(db.Integer, primary_key=True)
    USER_ID = db.Column(db.Integer, db.ForeignKey('Users.USER_ID'))


class Track(db.Model):

    __tablename__ = "Track"

    TRACK_ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(255))
    LENGTH = db.Column(db.Integer)
    ALBUM_ID = db.Column(db.Integer, db.ForeignKey('Album.ALBUM_ID'))
    GENRE_ID = db.Column(db.Integer, db.ForeignKey('Genre.GENRE_ID'))

class Vinyl(db.Model):

    __tablename__ = "Vinyl"

    VINYL_ID = db.Column(db.Integer, primary_key=True)
    SIZE_VINYL = db.Column(db.Integer)

class Product(db.Model):

    __tablename__ = "Product"

    PRODUCT_ID = db.Column(db.Integer, primary_key=True)
    PRODUCT_NAME = db.Column(db.String(255))
    PRODUCT_TYPE = db.Column(db.String(255))
    SINGLE_OR_ALBUM = db.Column(db.String(1))
    PRICE = db.Column(db.Numeric(4,2))
    INVENTORY_COUNT = db.Column(db.String(255))
    ARTIST_ID = db.Column(db.Integer, db.ForeignKey('Artist.ARTIST_ID'), nullable=True)
    GENRE_ID = db.Column(db.Integer, db.ForeignKey('Genre.GENRE_ID'), nullable=True)
    TRACK_ID = db.Column(db.Integer, db.ForeignKey('Track.TRACK_ID'), nullable=True)
    ALBUM_ID = db.Column(db.Integer, db.ForeignKey('Album.ALBUM_ID'), nullable=True)
    VINYL_ID = db.Column(db.Integer, db.ForeignKey('Vinyl.VINYL_ID'), nullable=True)
    MP3_ID = db.Column(db.Integer, db.ForeignKey('MP3.MP3_ID'), nullable=True)
    CD_ID = db.Column(db.Integer, db.ForeignKey('CD.CD_ID'), nullable=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    print(current_user.is_authenticated)
    return render_template('index.html')

@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)
    user = Users.query.filter_by(USERNAME=request.form["username"]).first()
    if user:
        if not check_password_hash(user.PASSWORD, request.form["password"]):
            return render_template("login.html", error=True)
    if user is None:
        return render_template("login.html", error=True)
    login_user(user)
    return redirect(url_for('shop'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['demo-username']
        password = request.form['demo-password']
        name = request.form['demo-name']
        lastName = request.form['demo-last_name']
        email = request.form['demo-email']
        street = request.form['demo-streetaddr']
        state = request.form['demo-state']
        zip = request.form['demo-zip']
        country = request.form['demo-Country']
        city = request.form['demo-city']

        username_exists = Users.query.filter_by(USERNAME=username).first()
        email_exists = Users.query.filter_by(EMAIL_ADDRESS=email).first()
        if username_exists is not None:
            return render_template('register.html', error=True, username_error=True)
        elif email_exists is not None:
            return render_template('register.html', error=True, email_error=True)

        new_user = Users(USERNAME=username,
                        PASSWORD=generate_password_hash(password, method='sha256'), FIRST_NAME=name, LAST_NAME=lastName, STREET_ADDRESS=street, CITY=city,
        STATE_ABBREVIATION=state, ZIPCODE= zip, EMAIL_ADDRESS=email, COUNTRY=country)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('shop'))
    return render_template('register.html')

@app.route('/shop', methods=["GET"])
def shop():
    product_arr = Product.query.all()
    return render_template('shop.html', product_arr=product_arr)


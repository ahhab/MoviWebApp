from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, User
import movies as movie_commands

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
data_manager = DataManager()

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    user_name = request.form.get("user_name")
    if user_name:
        data_manager.add_user(user_name)
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = User.query.get(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user=user)

@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    movie_title = request.form.get("movie_title")
    if movie_title:
        movie_data = movie_commands.get_movie_data(movie_title)
        if movie_data:
            data_manager.add_movie(user_id, movie_data)
    return redirect(url_for('user_movies', user_id=user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

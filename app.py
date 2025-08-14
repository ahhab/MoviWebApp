from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, User, Movie
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
    user = User.query.get_or_404(user_id)
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


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        new_title = request.form.get("new_title")
        if new_title:
            data_manager.update_movie(movie_id, new_title)
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html', movie=movie)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

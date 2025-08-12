from models import db, User, Movie

class DataManager:
    def get_users(self):
        return User.query.all()

    def add_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, movie_data):
        new_movie = Movie(
            title=movie_data['title'],
            year=movie_data['year'],
            director=movie_data['director'],
            poster_image_url=movie_data['poster_image_url'],
            user_id=user_id
        )
        db.session.add(new_movie)
        db.session.commit()

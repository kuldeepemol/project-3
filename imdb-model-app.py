# Import modules
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from sklearn.externals import joblib
from keras.models import load_model

score_model = joblib.load('Models/rf_simple.pkl')
gross_model = joblib.load('Models/gross.pkl')
#score_model = load_model('Models/neural_network_simple.h5')
#gross_model = load_model('Models/gross_model_nn.h5')
#score_model._make_predict_function()
gross_model._make_predict_function()

app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/movie_db.sqlite')


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/directors")
def directors():
    """Return a list of all directors."""
    # Query All Directors in the the Database
    data = engine.execute('''SELECT distinct director_name, director_facebook_likes
                            FROM movie_db order by CAST(director_facebook_likes AS integer) desc limit 15''')
    directors = []

    for record in data:
        directors.append({'name': record[0], 'value': record[1]})

    data = engine.execute('''SELECT distinct director_name, director_facebook_likes
                                FROM movie_db order by CAST(director_facebook_likes AS integer) asc limit 15''')

    for record in data:
        directors.append({'name': record[0], 'value': record[1]})

    # Return a list of the column names (sample names)
    return jsonify(directors)

@app.route("/actors_1")
def actors_1():
    """Return a list of all actors."""
    # Query All Actors-1 in the the Database
    data = engine.execute('''SELECT distinct actor_1_name, actor_1_facebook_likes
                            FROM movie_db order by CAST(actor_1_facebook_likes AS integer) desc limit 15''')
    actors = []

    for record in data:
        actors.append({'name': record[0], 'value': record[1]})

    # Query All Actors-1 in the the Database
    data = engine.execute('''SELECT distinct actor_1_name, actor_1_facebook_likes
                            FROM movie_db order by CAST(actor_1_facebook_likes AS integer) asc limit 15''')

    for record in data:
        actors.append({'name': record[0], 'value': record[1]})

    # Return a list of the column names (sample names)
    return jsonify(actors)


@app.route("/actors_2")
def actors_2():
    """Return a list of all actors."""
    # Query All Actors-2 in the the Database
    data = engine.execute('''SELECT distinct actor_2_name, actor_2_facebook_likes
                            FROM movie_db order by CAST(actor_2_facebook_likes AS integer) desc limit 15''')
    actors = []

    for record in data:
        actors.append({'name': record[0], 'value': record[1]})

    data = engine.execute('''SELECT distinct actor_2_name, actor_2_facebook_likes
                                FROM movie_db order by CAST(actor_2_facebook_likes AS integer) asc limit 15''')

    for record in data:
        actors.append({'name': record[0], 'value': record[1]})

    # Return a list of the column names (sample names)
    return jsonify(actors)


@app.route("/actors_3")
def actors_3():
    """Return a list of all actors."""
    # Query All Actors-3 in the the Database
    data = engine.execute('''SELECT distinct actor_3_name, actor_3_facebook_likes
                            FROM movie_db order by CAST(actor_3_facebook_likes AS integer) desc limit 15''')
    actors = []

    for record in data:
        actors.append({'name': record[0], 'value': record[1]})

    data = engine.execute('''SELECT distinct actor_3_name, actor_3_facebook_likes
                                FROM movie_db order by CAST(actor_3_facebook_likes AS integer) asc limit 15''')

    for record in data:
        actors.append({'name': record[0], 'value': record[1]})

    # Return a list of the column names (sample names)
    return jsonify(actors)


@app.route("/ratings")
def content_rating():
    """Return a list of content rating."""
    # Query All content ratings in the the database
    data = engine.execute('SELECT distinct content_rating FROM movie_db')
    content_ratings = []

    for record in data:
        content_ratings.append(record[0])

    # Return a json
    return jsonify(content_ratings)


@app.route("/predict/<director_likes>/<actor_1_likes>/<actor_2_likes>/<actor_3_likes>/<cr>/<duration>/<genre>/<budget>")
def predict(director_likes, actor_1_likes, actor_2_likes, actor_3_likes, cr, duration, genre, budget):

    (content_rating_G, content_rating_NC_17, content_rating_PG, content_rating_PG_13, content_rating_R) = (0, 0, 0, 0, 0)

    if cr == 'G':
        content_rating_G = 1
    elif cr == 'NC-17':
        content_rating_NC_17 = 1
    elif cr == 'PG':
        content_rating_PG = 1
    elif cr == 'PG-13':
        content_rating_PG_13 = 1
    elif cr == 'R':
        content_rating_R = 1

    (drama, comedy, thriller, action, romance, adventure, crime, fantasy, sci_fi, family,
     horror, mystery, biography, animation, music, war, history, sport, musical, western,
     documentary, film_noir) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    allGenres = genre.split(',')
    for genre in allGenres:
        genre = genre.lower()

        if genre == 'drama':
            drama = 1
        if genre == 'comedy':
            comedy = 1
        if genre == 'thriller':
            thriller = 1
        if genre == 'action':
            action = 1
        if genre == 'romance':
            romance = 1

        if genre == 'adventure':
            adventure = 1
        if genre == 'crime':
            crime = 1
        if genre == 'fantasy':
            fantasy = 1
        if genre == 'sci-fi':
            sci_fi = 1
        if genre == 'family':
            family = 1

        if genre == 'horror':
            horror = 1
        if genre == 'mystery':
            mystery = 1
        if genre == 'biography':
            biography = 1
        if genre == 'animation':
            animation = 1
        if genre == 'music':
            music = 1

        if genre == 'war':
            war = 1
        if genre == 'history':
            history = 1
        if genre == 'sport':
            sport = 1
        if genre == 'musical':
            musical = 1
        if genre == 'western':
            western = 1
        if genre == 'documentary':
            documentary = 1
        if genre == 'film-noir':
            film_noir = 1

    cast_total_facebook_likes = int(actor_1_likes) + int(actor_2_likes) + int(actor_3_likes)

    data_dict = {
        'duration': [duration],
        'director_facebook_likes': [director_likes],
        'actor_1_facebook_likes': [actor_1_likes],
        'actor_2_facebook_likes': [actor_2_likes],
        'actor_3_facebook_likes': [actor_3_likes],
        'cast_total_facebook_likes': [cast_total_facebook_likes],
        'facenumber_in_poster': [3],
        'budget': [budget],
        'content_rating_G': [content_rating_G],
        'content_rating_NC-17': [content_rating_NC_17],
        'content_rating_PG': [content_rating_PG],
        'content_rating_PG-13': [content_rating_PG_13],
        'content_rating_R': [content_rating_R],
        'Drama': [drama],
        'Comedy': [comedy],
        'Thriller': [thriller],
        'Action': [action],
        'Romance': [romance],
        'Adventure': [adventure],
        'Crime': [crime],
        'Fantasy': [fantasy],
        'Sci-Fi': [sci_fi],
        'Family': [family],
        'Horror': [horror],
        'Mystery': [mystery],
        'Biography': [biography],
        'Animation': [animation],
        'Music': [music],
        'War': [war],
        'History': [history],
        'Sport': [sport],
        'Musical': [musical],
        'Western': [western],
        'Documentary': [documentary],
        'Film-Noir': [film_noir],
    }

    predict_df = pd.DataFrame(data_dict)

    final_prediction = score_model.predict(predict_df)
    gross_prediction = gross_model.predict(predict_df)

    gross_label = {
        0: "< 1 Million",
        1: "1 - 10 Million",
        2: "10 - 20 Million",
        3: "20 - 40 Million",
        4: "40 - 65 Million",
        5: "65 - 100 Million",
        6: "100 - 150 Million",
        7: "150 - 200 Million",
        8: "> 200 Million",
    }

    index = 0
    gross_index = 0
    for i in gross_prediction:
        for j in i:
            if j == 1:
                gross_index = index
            index += 1

    target_names = {
        1: "IMDB score: 0 - 6 (Bad) and Gross earnings: " + gross_label[gross_index],
        2: "IMDB score: 6 - 8 (Good) and Gross earnings: " + gross_label[gross_index],
        3: "IMDB score: 8 - 10 (Excellent) and Gross earnings: " + gross_label[gross_index],
    }

    final_data = {
        'final_predict_message': target_names[final_prediction[0]],
        'final_predict_category': int(final_prediction[0]),
    }

    return jsonify(final_data)


if __name__ == "__main__":
    app.run(debug=True)
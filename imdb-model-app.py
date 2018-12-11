# Import modules
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from sklearn.externals import joblib

model = joblib.load('Models/rf_simple.pkl')
#model._make_predict_function()


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


@app.route("/predict/<director_likes>/<actor_1_likes>/<actor_2_likes>/<actor_3_likes>/<cr>/<duration>/<budget>")
def predict(director_likes, actor_1_likes, actor_2_likes, actor_3_likes, cr, duration, budget):

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
    }

    print(data_dict)

    predict_df = pd.DataFrame(data_dict)

    final_prediction = model.predict(predict_df)

    target_names = {
        1: "Based on the parameters your IMDB score will be between 0 - 6 (Bad)",
        2: "Based on the parameters your IMDB score will be between 6 - 8 (Good)",
        3: "Based on the parameters your IMDB score will be between 8 - 10 (Excellent)",
        #4: "Based on the parameters your IMDB score will be between 8 - 10 (Excellent)"
    }

    final_data = {
        'final_predict_message': target_names[final_prediction[0]],
        'final_predict_category': int(final_prediction[0]),
    }

    return jsonify(final_data)


if __name__ == "__main__":
    app.run(debug=True)
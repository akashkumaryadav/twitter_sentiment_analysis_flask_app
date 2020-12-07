from flask import Flask, render_template, request
from twitter import all_analyised_tweets, post_dataframe, polarity_subjectivity, worldCloud
app = Flask(__name__)


def initiate_twitter_sentiment(username):
    data_frame = post_dataframe(username)
    positive, negative = all_analyised_tweets(data_frame)
    polarity_graph = polarity_subjectivity(data_frame, username)
    world_cloud = worldCloud(data_frame, username)
    data = {}
    if len(positive) != 0:
        data["positive"] = positive
    if len(negative) != 0:
        data["negative"] = negative
    if polarity_graph:
        data['p_graph'] = polarity_graph
    if world_cloud != None:
        data['world_cloud'] = world_cloud
    return data


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        username = request.form.get("username")
        if len(username) != 0:
            data = initiate_twitter_sentiment(username)
            return render_template('index.html', data=data)
    return render_template('index.html', data=None)

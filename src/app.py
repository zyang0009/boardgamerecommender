from flask import Flask, render_template, request, jsonify
import pandas as pd
import predict

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    game_title, num_games = user_data['game_title'], user_data['num_games']
    data = predict.recommend_games(game_title, int(num_games))
    if data == None:
        headings = ["Error!"]
        nogame = [["Sorry, we could not find that game! Try another one?"]]
        return render_template('recommend.html', headings=headings, data=nogame)
    headings = ("Name","Categories","Mechanics","Description")
    data = data.values.tolist()

    return render_template('recommend.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

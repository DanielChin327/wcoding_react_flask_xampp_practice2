from flask import Flask, request, jsonify
from flask_cors import CORS #preventing the Cors errors: prevents errors during transfer from website to website.
import sqlalchemy



app = Flask(__name__)

db = sqlalchemy.create_engine("mariadb+pymysql://root:@localhost:3307/simpledb")


@app.route("/")
def hello():
    return "Hello World"


def get_comments():
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM comments;"))
        print("result", result, "-----", type(result))
        print("result.all()", result.all(), "-----", type(result.all()))
    return result.all()

# comment_id, username, comment_text
def add_comment(username, comment_text):
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("""
        INSERT INTO `comments` (`comment_id`, `username`, `comments_txt`) VALUES (NULL, :username, :comment_text) """),
        {
            "username": username,
            "comment_text": comment_text,  # This is the corrected key
        })
        conn.commit()
    return get_comments()

@app.route('/api/comment', methods = ["POST"])
def add_comment_route():
    data = request.get_json()
    print(data)
    username = data.get("username")
    comment = data.get('comments_txt')

    add_comment(username, comment)

    return jsonify({'message': 'comment succesfully added'}), 200

# @app.route('/api/comment', methods = ["GET"])


if __name__ == '__main__':
    app.run(debug=True)
    # get_comments()
    # add_comment("Stacy", "This is Stacy's comment")

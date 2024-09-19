from flask import Flask
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




if __name__ == '__main__':
    # app.run(debug=True)
    get_comments()

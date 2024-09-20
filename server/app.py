from flask import Flask, request, jsonify
from flask_cors import CORS #preventing the Cors errors: prevents errors during transfer from website to website.
import sqlalchemy



app = Flask(__name__)

db = sqlalchemy.create_engine("mariadb+pymysql://root:@localhost:3307/simpledb")


@app.route("/")
def hello():
    return "Hello World"




@app.route('/api/comments', methods = ["GET"])
def get_comment_route():
    get_comments()
    return jsonify({"Message": "Retrieve Message"}), 200


# comment_id, username, comment_text
@app.route('/api/comment', methods = ["POST"])
def add_comment_route():
    data = request.get_json()
    print(data)
    username = data.get("username")
    comment = data.get('comments_txt')
    add_comment(username, comment)

    return jsonify({'message': 'comment succesfully added'}), 200


# Update Comment
@app.route('/api/comment/<int:comment_id>', methods=['PUT'])
def update_comment_route(comment_id):
    data = request.get_json()
    username = data.get("username")
    comment_text = data.get('comments_txt')
    update_comment(comment_id, username, comment_text)
    return jsonify({'message': 'Comment successfully updated'}), 200


# Delete Comment
@app.route('/api/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment_route(comment_id):
    delete_comment(comment_id)
    return jsonify({'message': 'Comment successfully deleted'}), 200














def get_comments():
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM comments;"))
        print("result", result, "-----", type(result))
        print("result.all()", result.all(), "-----", type(result.all()))
    return result.all()

def add_comment(username, comment_text):
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("""
        INSERT INTO `comments` (`comment_id`, `username`, `comments_txt`) VALUES (NULL, :username, :comments_txt) """),
        {
            "username": username,
            "comments_txt": comment_text,
        })
        conn.commit() # this changes the db.
    return get_comments()


def update_comment(comment_id, username, comment_text):
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("""
            UPDATE comments
            SET username = :username, comments_txt = :comments_txt
            WHERE comment_id = :comment_id
        """), {
            "comment_id": comment_id,
            "username": username,
            "comments_txt": comment_text,
        })
        conn.commit()
    return get_comments()

def delete_comment(comment_id):
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("""
            DELETE FROM comments
            WHERE comment_id = :comment_id
        """), {
            "comment_id": comment_id,
        })
        conn.commit()
    return get_comments()




# @app.route('/api/comment/<account_name>', methods = ["PUT"])
# # @cross_origin()
# def update_comment_route():
#     data = request.get_json()
#     print(data)

#     comment_id = data.get("comment_id")
#     comment = data.get("comment_text")

#     update_comment(comment_id, comment)

#     return jsonify({"message": "Comment successfully updated"}), 200

# @app.route("/api/comment/", methods = ["DELETE"])
# # @cross_origin()
# def delete_comment_route():
#     data= request.get_json()
#     print(data)

#     comment_id = data.get("comment_id")
#     comment_text = data.get("comment_text")

#     delete_comment(comment_id, comment_text)

#     return jsonify({"message": "Comment successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    # get_comments()
    # add_comment("Stacy", "This is Stacy's comment")

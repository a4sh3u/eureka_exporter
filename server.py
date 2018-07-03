from flask import Flask


app = Flask(__name__)


@app.route("/")
def home():
    return "Nothing to see here! Move on!"

if __name__ == "__main__":
    app.run()

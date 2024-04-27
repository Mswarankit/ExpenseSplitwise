from flask import Flask
from router import expense

app = Flask(__name__)
app.register_blueprint(expense)

@app.route('/')
def home():
    return "Welcome to the Expense Splitter!"

if __name__ == '__main__':
    app.run(debug=True)
from chatbot import chatbot
from flask import Flask, render_template, request

app = Flask(__name__,template_folder='/Users/linpei/Desktop/590/chatbot/templates')
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userinput = request.args.get('msg')
    return str(chatbot.get_response(userinput))

if __name__ == "__main__":
    app.run(debug=True) 

## http://localhost:5000/ 


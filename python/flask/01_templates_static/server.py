from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/helloworld")
def helloworld():
	return "Hello, World!"

if __name__ == "__main__":
	app.run(debug=True, port=8080, host='0.0.0.0')

from flask import Flask,render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/about/afy")
def afy():
    return "AFY hakkında"

@app.route("/about/VG")
def VG():
    return "VG hakkında"

if __name__ ==  "__main__":
    app.run(debug=True)


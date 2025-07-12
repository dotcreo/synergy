from flask import Flask, render_template, request

app = Flask(__name__)
lst = [1, 2, 3]
@app.route("/")
def index():
	return render_template('index.html')

my_dict = {}
@app.route("/note", methods=["GET", "POST"])
def note():
	if request.method == 'POST':
		title = request.form['title']
		string = request.form['string']
		my_dict[title] = string
	return render_template('note.html', data=my_dict)

@app.errorhandler(404)
def not_found(e):
	return render_template('/templates/404.html', 404)

if __name__ == "__main__":
	app.run(debug=True)
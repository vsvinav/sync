from flask import Flask, flash, render_template, request, redirect, url_for

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        message = request.form['message']
        duration = request.form['duration']
        duration_unit = request.form['duration_unit']

        flash("Message scheduled")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
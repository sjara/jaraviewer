from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

	
@app.route('/save', methods=['GET','POST'])
def save():
    import pdb; pdb.set_trace()
    return redirect(url_for('index'))


app.run(debug=True, host='0.0.0.0', port=8000)


from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

	
# @app.route('/save', methods=['POST'])
# def save():
#     import pdb; pdb.set_trace()
#     return redirect(url_for('index'))

@app.route('/profile', methods=['POST'])
def profile():
	if request.method == 'POST':

		subject = request.form.getlist('subject[]')
		plotType = request.form.getlist('plotType[]')
		dateRange = request.form['dateRange']


	# TODO: code to save it!!!!!
		print(subject)
		print(plotType)
		print(dateRange)
		
		# elif request.form['submit'] == 'submit':
			# subject = request.form.getlist('subject')
			# plotType = request.form.getlist('plotType')
			# dateRange = request.form['dateRange']

			# print("Subjects:" + str(subject))
			# print("Plot Types:" + str(plotType))
			# print("Date Range:" + dateRange)
		# 	pass
		# else:
		# 	pass # clear
	if request.method == 'GET':
		pass 

	# TODO: Get the saved profile
	responseJson = {
		'subject': subject,
		'plotType': plotType,
		'dateRange': dateRange
	}

	return jsonify(**responseJson), 200




app.run(debug=True, host='0.0.0.0', port=8000)


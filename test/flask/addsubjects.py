from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('addsubjects.html')

@app.route('/modify')
def modify():
	return render_template('modify.html')
	
# @app.route('/save', methods=['POST'])
# def save():
#     import pdb; pdb.set_trace()
#     return redirect(url_for('index'))

@app.route('/profile', methods=['POST'])
def profile():
	# Get user inputs
 	if request.method == 'POST':
            subject = request.form.getlist('subject')
            plotType = request.form.getlist('plotType')
            dateRange = request.form['dateRange']
            columNum = request.form['columNum']

            #Get the saved profile
            responseJson = {
                'subject': subject,
                'plotType': plotType,
                'dateRange': dateRange,
                'columNum': columNum
            }
        else:
            responseJson = {}
	return jsonify(**responseJson), 200


@app.route('/addsubs', methods=['POST'])
def addsubs():
    if request.method == 'POST':
        if request.form['modifsubj']=='Add':
            responseJson = {'Add subject': request.form['subjectname']}
        elif request.form['modifsubj']=='Delete':
            responseJson = {'Delete subject': request.form['subjectname']}
  	return jsonify(**responseJson), 200




if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)


from flask import Flask,render_template, request
import pickle
import numpy as np
import pymongo
from pymongo import MongoClient
app = Flask(__name__)

cluster = MongoClient("mongodb+srv://abcd:qwertyuiop@cluster0.0ihqm.mongodb.net/ipl?retryWrites=true&w=majority")
db=cluster['ipl']
collection=db['data']

filename = 'ipl_model.pkl'
regressor = pickle.load(open(filename, 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
         
        overs = float(request.form['overs'])
        runs = int(request.form['score'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_last5'])
        wickets_in_prev_5 = int(request.form['wickets_in_last5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])

        my_data={
            'batting-team': batting_team,
            'bowling-team': bowling_team,
            'overs': overs,
            'score': runs,
            'wickets': wickets,
            'runs_in_last5':runs_in_prev_5,
            'wickets_in_last5':wickets_in_prev_5,
            'pred':my_prediction
            }
        
        collection.insert_one(my_data)
	    
        
        lower=my_prediction-5
        upper=my_prediction+5

        if lower<runs:
            lower=runs
            upper=runs+10
	    

        

        return render_template('result.html', lower_limit = lower, upper_limit = upper)
	
	

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')



if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import pandas as pd
from flask_cors import CORS 
import json

app = Flask(__name__)
CORS(app,
     resources={
       r"/upload": {
         "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/distance_plot":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/average_steps_plot":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/heart_points_vs_steps":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/mean_steps_by_day_of_week":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/mean_steps_by_month":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/activity_distribution":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       },
       r"/walking_distribution_heatmap":{
        "origins": ["http://localhost:8000", "https://pipstur.github.io"]
       }
     })

def convert_ms_to_hours_minutes(ms_duration):
    if pd.notnull(ms_duration):
        seconds = ms_duration / 1000
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f'{int(hours)} hours {int(minutes)} minutes'
    else:
        return None
def format_date(date_str):
    return pd.to_datetime(date_str).strftime('%d/%m/%Y')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file:
        uploaded_df = pd.read_csv(file)
        uploaded_df = uploaded_df.drop(columns=['Heart Minutes', 'Average heart rate (bpm)', 'Min heart rate (bpm)', 'Max heart rate (bpm)', 'Low latitude (deg)', 'Low longitude (deg)', 'High latitude (deg)', 'High longitude (deg)', 'Average weight (kg)', 'Max weight (kg)', 'Min weight (kg)', 'Biking duration (ms)', 'Inactive duration (ms)', 'Swimming duration (ms)', 'Paced walking duration (ms)'], axis=1)

        max_distance_row = uploaded_df.loc[uploaded_df['Distance (m)'].idxmax()]
        max_steps_row = uploaded_df.loc[uploaded_df['Step count'].idxmax()]
        max_heart_points_row = uploaded_df.loc[uploaded_df['Heart Points'].idxmax()]
        max_walking_duration_row = uploaded_df.loc[uploaded_df['Walking duration (ms)'].idxmax()]
        
        results = {
            'max_distance': {
                'date': format_date(max_distance_row['Date']),
                'value': round(max_distance_row['Distance (m)'],2)
            },
            'max_steps': {
                'date': format_date(max_steps_row['Date']),
                'value': max_steps_row['Step count']
            },
            'max_heart_points': {
                'date': format_date(max_heart_points_row['Date']),
                'value': max_heart_points_row['Heart Points']
            },
            'max_walking_duration': {
                'date': format_date(max_walking_duration_row['Date']),
                'value': convert_ms_to_hours_minutes(max_walking_duration_row['Walking duration (ms)'])
            },
        }
        
        return jsonify(results)
    
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/distance_plot', methods=['POST'])
def distance_plot():
    file = request.files['file']
    
    if file:
        uploaded_df = pd.read_csv(file)

        uploaded_df['Date'] = pd.to_datetime(uploaded_df['Date'])
        uploaded_df = uploaded_df.drop(columns=['Heart Minutes', 'Average heart rate (bpm)', 'Min heart rate (bpm)', 'Max heart rate (bpm)', 'Low latitude (deg)', 'Low longitude (deg)', 'High latitude (deg)', 'High longitude (deg)', 'Average weight (kg)', 'Max weight (kg)', 'Min weight (kg)', 'Biking duration (ms)', 'Inactive duration (ms)', 'Swimming duration (ms)', 'Paced walking duration (ms)'], axis=1)
        uploaded_df = uploaded_df.fillna(0)

        distance_data = uploaded_df[['Date', 'Distance (m)']]
        
        plot_data = {
            'x': distance_data['Date'].dt.strftime('%d/%m/%Y').tolist(), 
            'y': distance_data['Distance (m)'].tolist(),  
            'type': 'scatter',
            'mode': 'lines',
            'marker': {'color': 'blue'},
            'name': 'Distance plot over time',
        }
        
        return jsonify({'plot_data': [plot_data]})
    
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/average_steps_plot', methods=['POST'])
def average_steps_plot():
    file = request.files['file']
    
    if file:
        uploaded_df = pd.read_csv(file)

        uploaded_df['Date'] = pd.to_datetime(uploaded_df['Date'])
        uploaded_df = uploaded_df.drop(columns=['Heart Minutes', 'Average heart rate (bpm)', 'Min heart rate (bpm)', 'Max heart rate (bpm)', 'Low latitude (deg)', 'Low longitude (deg)', 'High latitude (deg)', 'High longitude (deg)', 'Average weight (kg)', 'Max weight (kg)', 'Min weight (kg)', 'Biking duration (ms)', 'Inactive duration (ms)', 'Swimming duration (ms)', 'Paced walking duration (ms)'], axis=1)
        uploaded_df = uploaded_df.fillna(0)

        weekly_average_steps = uploaded_df.groupby([
                uploaded_df['Date'].dt.year, 
                uploaded_df['Date'].dt.isocalendar().week
            ])['Step count'].mean().reset_index()
        
        
        weekly_average_steps['Week_Year'] = weekly_average_steps.apply(lambda row: f"{row['Date']}-{row['week']}", axis=1)

        plot_data = {
            'x': weekly_average_steps['Week_Year'].tolist(),
            'y': weekly_average_steps['Step count'].tolist(),
            'type': 'scatter',
            'mode': 'lines',
            'marker': {'color': 'green'},
            'name': 'Average Steps',
        }
        
        return jsonify({'plot_data': [plot_data]})
    
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/mean_steps_by_month', methods=['POST'])
def mean_steps_by_month():
    try:
        file = request.files['file']

        if file:
            uploaded_df = pd.read_csv(file)

            uploaded_df['Date'] = pd.to_datetime(uploaded_df['Date'])

            mean_steps_by_month = uploaded_df.groupby(uploaded_df['Date'].dt.to_period("M"))['Step count'].mean().reset_index()

            mean_steps_by_month['Date'] = mean_steps_by_month['Date'].astype(str)
            plot_data = {
                'x': mean_steps_by_month['Date'].tolist(),
                'y': mean_steps_by_month['Step count'].tolist(),
                'type': 'bar',
                'marker': {'color': 'blue'},
                'name': 'Mean Steps',
            }
            return jsonify({'plot_data': [plot_data]})

        return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/mean_steps_by_day_of_week', methods=['POST'])
def mean_steps_by_day_of_week():
    try:
        file = request.files['file']

        if file:
            uploaded_df = pd.read_csv(file)
            uploaded_df['Date'] = pd.to_datetime(uploaded_df['Date'])

            days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            cat_dtype = pd.CategoricalDtype(categories=days_order, ordered=True)
            uploaded_df['Date'] = uploaded_df['Date'].dt.day_name().astype(cat_dtype)

            mean_steps_by_day_of_week = uploaded_df.groupby('Date')['Step count'].mean().reset_index()
            plot_data = {
                'x': mean_steps_by_day_of_week['Date'].tolist(),
                'y': mean_steps_by_day_of_week['Step count'].tolist(),
                'type': 'bar',
                'marker': {'color': 'orange'},
                'name': 'Mean Steps',
            }

            return jsonify({'plot_data': [plot_data]})

        return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(e) 
        return jsonify({'error': str(e)}), 500

@app.route('/heart_points_vs_steps', methods=['POST'])
def heart_points_vs_steps():
    try:
        file = request.files['file']

        if file:
            uploaded_df = pd.read_csv(file)
            mean_heart_points_steps = uploaded_df.groupby('Date')[['Heart Points', 'Step count']].mean().dropna()

            plot_data = {
                'x': mean_heart_points_steps['Heart Points'].tolist(),
                'y': mean_heart_points_steps['Step count'].tolist(),
                'type': 'scatter',
                'mode': 'markers',
                'marker': {'color': 'red'},
                'name': 'Heart Points vs Steps',
            }

            return jsonify({'plot_data': [plot_data]})

        return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/activity_distribution', methods=['POST']) # this is a work in progress
def activity_distribution():
    try:
        file = request.files['file']

        if file:
            uploaded_df = pd.read_csv(file)

            activity_columns = ['Biking duration (ms)', 'Walking duration (ms)', 'Running duration (ms)', 'Jogging duration (ms)', 'Swimming duration (ms)', 'Paced walking duration (ms)']

            total_durations = uploaded_df[activity_columns].sum()

            plot_data = {
                'x': total_durations.tolist(),
                'y': activity_columns,
                'type': 'bar',
                'marker': {'color': 'blue'},
                'name': 'Activity Distribution',
            }

            return jsonify({'plot_data': plot_data})

        return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(e) 
        return jsonify({'error': str(e)}), 500


@app.route('/walking_distribution_heatmap', methods=['POST']) # This is unused 
def walking_distribution_heatmap():
    try:
        file = request.files['file']

        if file:
            uploaded_df = pd.read_csv(file)

            uploaded_df['Date'] = pd.to_datetime(uploaded_df['Date'])

            uploaded_df['Day'] = uploaded_df['Date'].dt.day_name()
            uploaded_df['Hour'] = uploaded_df['Date'].dt.hour

            walking_heatmap_data = uploaded_df[uploaded_df['Walking duration (ms)'].notnull()] \
            .groupby(['Day', 'Hour'])['Walking duration (ms)'] \
            .sum() \
            .reset_index()
            heatmap_data = {
                'xValues': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23],
                'yValues': walking_heatmap_data.index.tolist(),
                'zValues': walking_heatmap_data.values.tolist()
            }
            print(heatmap_data['xValues'])
            print(walking_heatmap_data.index.tolist())
            print(walking_heatmap_data.values.tolist())
            return jsonify({'heatmap_data': heatmap_data})

        return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
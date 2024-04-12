from flask import Flask, request, jsonify
import schedule
import time

import requests
from bs4 import BeautifulSoup

def get_follower_count(username):
    url = f'https://www.instagram.com/{username}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        follower_count_element = soup.find('meta', attrs={'property': 'og:description'})
        if follower_count_element:
            follower_count_text = follower_count_element['content']
            follower_count = follower_count_text.split()[0]
            return follower_count
    return None

app = Flask(__name__)

# Sample value to return
follower_count = 2000

# Define a route to accept requests and return a value
@app.route('/get_value', methods=['GET'])
def get_value():
    return jsonify({'count': follower_count})

# Function to be executed every day at 12 am
def daily_task():
    # Your code to run daily at 12 am
    follower_count = get_follower_count('gsproductionhouse')

# Schedule the daily task
schedule.every().day.at("00:00").do(daily_task)

# Function to run the scheduled tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start the scheduler in a separate thread
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    
    # Start the Flask app
    app.run(debug=True)  # Set debug=True for development, change it to False in production

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def random_date():
    today = datetime.now()
    start_date = today - timedelta(days=365)
    end_date = today + timedelta(days=365)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    return random_date.strftime('%d-%m-%Y')


# API endpoint
@app.route('/validate_licenses', methods=['POST'])
def verify_exams():
    try:
        data = request.json

        print(data)

        if 'licenses' in data and isinstance(data['licenses'], list):
            licenses = data['licenses']
            random_dates = {license_number: random_date() for license_number in licenses}
            return jsonify(random_dates)
        else:
            return jsonify({'error': 'Invalid input format'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

if __name__ == '__main__':
    app.run(debug=True)
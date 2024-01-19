import xml.etree.ElementTree as et
from flask import Flask, request, jsonify

app = Flask(__name__)

# parse XML data
def parse_file_content(file_data):
    root = et.fromstring(file_data)
    return root

# extract athelete information
def extract_athlete_info(athlete_element):
    return {
        'athleteid': athlete_element.get('athleteid'),
        'lastname': athlete_element.get('lastname'),
        'firstname': athlete_element.get('firstname'),
        'gender': athlete_element.get('gender'),
        'license': athlete_element.get('license'),
        'birthdate': athlete_element.get('birthdate')
    }

# simulate medical exam verification, return true if year of birth >= 2005
def sim_exam(athlete):
    valid_exam = int(athlete['birthdate'].split('-')[0]) >= 2005
    return valid_exam

# API endpoint
@app.route('/verify-exams', methods=['POST'])
def verify_exams():
    try:
        file_data = request.data
        root = parse_file_content(file_data)

        athletes = []
        for athlete_element in root.findall('.//ATHLETE'):
            athlete_info = extract_athlete_info(athlete_element)
            athlete_info['valid_exam'] = sim_exam(athlete_info) #adiciona um campo chamado 'valid_exam' à informacao do atleta
            athletes.append(athlete_info)

        return jsonify({'athletes': athletes}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

if __name__ == '__main__':
    app.run(debug=True)
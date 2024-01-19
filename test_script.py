import zipfile
import os
import json
import xml.etree.ElementTree as et
import requests


def unzip():
    lxf_file_path = 'Inscricoes-CNAC-CIDjuvjunsen.lxf'

    #create temporary dir to extract the file
    temp_dir = 'temp_extracted'
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(lxf_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    lef_file_path = os.path.join(temp_dir, lxf_file_path[:-3] + "lef")

    with open(lef_file_path, 'r') as file:
        xml_data = file.read()
        os.rmdir(temp_dir)
        return xml_data

def extract_athlete_info(athlete_element):
    return {
        'athleteid': athlete_element.get('athleteid'),
        'lastname': athlete_element.get('lastname'),
        'firstname': athlete_element.get('firstname'),
        'gender': athlete_element.get('gender'),
        'license': athlete_element.get('license'),
        'birthdate': athlete_element.get('birthdate')
    }

def get_licenses(root):
    licenses = []
    for athlete_element in root.findall('.//ATHLETE'):
            athlete_info = extract_athlete_info(athlete_element)
            #athlete_info['valid_exam'] = sim_exam(athlete_info) #adiciona um campo chamado 'valid_exam' à informacao do atleta
            licenses.append(athlete_info['license'])

    return licenses

def make_request(licenses):
    url = 'http://127.0.0.1:5000/validate_licenses'

    json_licenses = {'licenses': licenses}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data = json.dumps(json_licenses), headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print(f"Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
    xml_data = unzip()

    root = et.fromstring(xml_data)

    licenses = get_licenses(root)

    make_request(licenses)


from flask import Flask, request, json, render_template
from flask_cors import CORS, cross_origin
import os
import glob
import logging
import csv
from src.main.python.simulation.Main import Main

app = Flask(__name__)
CORS(app)

# Define Folder Path
INPUT_FOLDER = '/app/src/main/in'
OUTPUT_FOLDER = '/app/src/main/out'
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
Test = Main(num_up=2, num_down=1, num_floors=9)

@app.route("/random", methods=['GET'])
@cross_origin()
def random_simulation():

  logging.warning('Started')

  input_files = glob.glob(os.path.join(app.config['INPUT_FOLDER'], '*'))
  for f in input_files:
      os.remove(f)

  logging.warning('Removed input files')

  output_files = glob.glob(os.path.join(app.config['OUTPUT_FOLDER'], '*'))
  for f in output_files:
      os.remove(f)

  logging.warning('Removed output files')

  # execute the simulation process
  Test.run(64800, mode='default')

  # prepare the output

  elevators_filepath_otis = os.path.join(app.config['OUTPUT_FOLDER'], 'output_elevator_Otis.json')
  persons_filepath_otis = os.path.join(app.config['OUTPUT_FOLDER'], 'output_persons_Otis.json')

  elevators_filepath_egcs = os.path.join(app.config['OUTPUT_FOLDER'], 'output_elevator_ModernEGCS.json')
  persons_filepath_egcs = os.path.join(app.config['OUTPUT_FOLDER'], 'output_persons_ModernEGCS.json')

  elevators_data_otis = json.load(open(elevators_filepath_otis))
  persons_data_otis = json.load(open(persons_filepath_otis))

  elevators_data_egcs = json.load(open(elevators_filepath_egcs))
  persons_data_egcs = json.load(open(persons_filepath_egcs))
  
  data = {
    'Otis':{
      'Elevators': elevators_data_otis, 
      'Persons': persons_data_otis
    }, 
          
    'ModernEGCS':{
      'Elevators': elevators_data_egcs, 
      'Persons': persons_data_egcs
    }
  }

  return data

@app.route("/manual", methods=['GET', 'POST'])
@cross_origin()
def manual_simulation():

  logging.warning('Started')

  input_files = glob.glob(os.path.join(app.config['INPUT_FOLDER'], '*'))
  for f in input_files:
      os.remove(f)

  logging.warning('Removed input files')

  output_files = glob.glob(os.path.join(app.config['OUTPUT_FOLDER'], '*'))
  for f in output_files:
      os.remove(f)

  logging.warning('Removed output files')

  # get the uploaded file
  json_input = json.dumps(request.get_json(), indent=4)

  logging.warning(json_input)

  file_path = os.path.join(app.config['INPUT_FOLDER'], 'input.json')

  # set the file path
  with open(file_path, 'w') as f:
    f.write(json_input)

  # execute the simulation process
  Test.run(64800, mode='manual')

  # prepare the output

  elevators_filepath_otis = os.path.join(app.config['OUTPUT_FOLDER'], 'output_elevator_Otis.json')
  persons_filepath_otis = os.path.join(app.config['OUTPUT_FOLDER'], 'output_persons_Otis.json')

  elevators_filepath_egcs = os.path.join(app.config['OUTPUT_FOLDER'], 'output_elevator_ModernEGCS.json')
  persons_filepath_egcs = os.path.join(app.config['OUTPUT_FOLDER'], 'output_persons_ModernEGCS.json')

  elevators_data_otis = json.load(open(elevators_filepath_otis))
  persons_data_otis = json.load(open(persons_filepath_otis))

  elevators_data_egcs = json.load(open(elevators_filepath_egcs))
  persons_data_egcs = json.load(open(persons_filepath_egcs))
  
  data = {
    'Otis':{
      'Elevators': elevators_data_otis, 
      'Persons': persons_data_otis
    }, 
          
    'ModernEGCS':{
      'Elevators': elevators_data_egcs, 
      'Persons': persons_data_egcs
    }
  }

  return data

if __name__ == '__main__':
    app.run(debug = True)

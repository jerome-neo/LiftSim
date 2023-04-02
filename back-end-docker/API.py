from flask import Flask, request, json, render_template
import os
import glob
import logging
import csv

app = Flask(__name__)

# Define Folder Path
INPUT_FOLDER = os.path.join(os.getcwd(), 'src/main/in')
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'src/main/out')
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route("/upload", methods=['GET', 'POST'])
def simulation():

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
  logging.warning(request.files)
  uploaded_file = request.files['file']
  
  if uploaded_file.filename != '':

    if uploaded_file.filename[len(uploaded_file.filename)-3:] != 'csv':
      return {"message": "The file must be a CSV file"}

    file_path = os.path.join(app.config['INPUT_FOLDER'], 'input.csv')

    # set the file path
    uploaded_file.save(file_path)

    # execute the simulation process
    import src.main.python.simulation.Main

    # prepare the output

    elevators_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'output_elevator.json')
    persons_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'output_persons.json')

    elevators_data = json.load(open(elevators_filepath))
    persons_data = json.load(open(persons_filepath))
    
    data = {'elevators': elevators_data, 'persons': persons_data}

    return data

    
  return {'message': 'No file found'}

if __name__ == '__main__':
    app.run(debug = True)

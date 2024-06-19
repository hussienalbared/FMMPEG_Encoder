from flask import Flask, request, jsonify
import subprocess
import logging
from flask_cors import CORS
# Initialize Flask app
import subprocess
import re
from tqdm import tqdm
import os
import time
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    input_file=data['input_file']
    #output_file=data['output_file']
    #uploaded_file = request.files['file']
    #print(uploaded_file.filename)
    #if uploaded_file.filename != '':
    #    file_path = os.path.join('C:/Users/hussi/OneDrive/Desktop/Interview/tmp', uploaded_file.filename)
    #    uploaded_file.save(file_path)
        
    
    #command = request.form.get('command')
    

    
    #logger.info(f"Executing command: {command}")
    
    
    

    try:
        #input_video = r'C:/Users/hussi/OneDrive/Desktop/Interview/nasa.mp4'
        
        timestamp = time.time()
        output_video = f'{timestamp}_output.mp4'
        command= [
        'ffmpeg',
        '-i', input_file, '-vf', 'scale=1280:-1' ,'-c:v', 'libx264', 
        '-preset' ,'veryslow' ,'-crf', '24', output_video,'-y'
    ]
        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        for line in process.stdout.readlines():
            print(line)
        retval = process.wait()
        if process.returncode == 0:
            result= f"Video encoded successfully: {output_video}"
        else:
          #raise Exception("Error occurred during encoding")
          response = jsonify({"result": "Error occurred during encoding"})
          response.status_code = 500
          return response
        
    
        
        return jsonify({'result': f'{result}'})
    
       
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})




def get_duration(input_file):
    result = subprocess.run(
        ['ffmpeg', '-i', input_file],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', result.stderr)
    if duration:
        hours, minutes, seconds = map(float, duration.groups())
        return hours * 3600 + minutes * 60 + seconds
    return None


  

   
    
    
    

# Example usage





if __name__ == '__main__':
    app.run(debug=True)

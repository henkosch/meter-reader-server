from flask import Flask, request
from flask import jsonify
import json
import numpy as np
import tempfile
import os
from waitress import serve
import easyocr

print("Starting...")
reader = easyocr.Reader(['en'])
print()

app = Flask(__name__)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def get_tempfile_name(some_id):
    return os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + "_" + some_id)

@app.route("/read", methods=['POST'])
def read():
    filename = get_tempfile_name("snap.jpg")
    print(filename)
    file = request.files['file']
    file.save(filename)
    global reader
    result = reader.readtext(filename, 
        detail = 1, 
        allowlist="0123456789 .,",
        # decoder="beamsearch",
        # text_threshold=0.8,
        # low_text=0.5
        )
    os.remove(filename)
    return json.dumps(result, cls=NpEncoder)

def run():
    return app

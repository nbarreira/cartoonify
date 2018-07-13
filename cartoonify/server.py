from __future__ import division
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name, model_path
from pathlib import Path
import logging
import datetime
from flask import Flask, request, jsonify
from PIL import Image
import io

root = Path(__file__).parent
# init objects
dataset = DrawingDataset(str(root / 'downloads/drawing_dataset'), str(root / 'app/label_mapping.jsonl'))
imageprocessor = ImageProcessor(str(model_path),
                                str(root / 'app' / 'object_detection' / 'data' / 'mscoco_label_map.pbtxt'),
                                tensorflow_model_name)

# configure logging
logging_filename = datetime.datetime.now().strftime('%Y%m%d-%H%M.log')
logging_path = Path(__file__).parent / 'logs'
if not logging_path.exists():
    logging_path.mkdir()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=str(Path(__file__).parent / 'logs' / logging_filename))

app = Workflow(dataset, imageprocessor)
app.setup()

#flask app
flask_app = Flask(__name__)


@flask_app.route('/cartoon', methods=['POST'])
def get_cartoon():
    print("Request received")
    if request and 'image' in request.files:
        # Read the bytestring
        imagestr = request.files['image'].read()
        image = imageprocessor.load_image_from_bytestring(imagestr)
        # Process the image and return the results
        app.process(image)
        cartoon = app.get_results()
        #imageprocessor.get_composite(image, cartoon).show()
        byteStr = imageprocessor.npimage_to_bytestring(cartoon)
        return jsonify({'cartoon': byteStr})


    return "No image was provided\n"




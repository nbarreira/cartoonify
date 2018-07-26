from __future__ import division
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name, model_path
from pathlib import Path
import logging
import datetime
from flask import Flask, request, jsonify

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
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR, filename=str(Path(__file__).parent / 'logs' / logging_filename))

app = Workflow(dataset, imageprocessor)
app.setup()

#flask app
flask_app = Flask(__name__)


@flask_app.errorhandler(404)
def page_not_found(e):
    return jsonify({'msg': 'Page not found'}), 404

@flask_app.route('/cartoon', methods=['POST'])
def get_cartoon():
    print('Request received')
    if request and 'image' in request.files:
        try:
            # Read the bytestring
            imagestr = request.files['image'].read()
            image = imageprocessor.load_image_from_bytestring(imagestr)

            # Process the image and return the results
            app.process(image)
            cartoon = app.get_png_cartoon()            
            #imageprocessor.get_composite(image, cartoon).show()

            byteStr = imageprocessor.npimage_to_bytestring(cartoon)
            return jsonify({'cartoon': byteStr})
        except Exception as e:
            print('exception', e)
            return jsonify({'msg': 'Invalid image format'}), 400

    return jsonify({'msg': 'No image was provided'}), 400


@flask_app.route('/time')
def time():
    return str(datetime.datetime.today()) + '\n'


if __name__ == '__main__':
    flask_app.run()
    

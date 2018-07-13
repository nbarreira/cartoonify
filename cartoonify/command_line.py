from __future__ import division
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name, model_path
from pathlib import Path
import logging
import datetime
import sys


if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], " image_name")
else:

    filename = sys.argv[1]

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

    image = imageprocessor.load_image_into_numpy_array(filename)
    app.process(image)

    #app.save_results(debut=False)
    cartoon = app.get_results()
    imageprocessor.get_composite(image, cartoon).show()
    app.close()
import sys
import numpy as np
import requests
import base64
from io import BytesIO
from PIL import Image

URL="http://127.0.0.1:5000/cartoon"

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], " image_name")
else:

    filename = sys.argv[1]

    # Open the file to send
    file = { 'image': open(filename, 'rb')}

    # Send the image to the server by a POST request
    r = requests.post(URL, files=file)
    data = r.json()
    if 'cartoon' in data:
        dst = Image.open(BytesIO(base64.b64decode(data['cartoon'])))
        src = Image.open(filename)
        src.show()
        dst.show()



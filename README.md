## Cartoonify REST Server

This is a REST server based on the Cartoonify project. The aim of this project is convert photographs into cartoons. First, the main objects of the scene are detected  using a Single Shot Multibox Detector (SSD).  In particular, a MobilenetSSD model was implemented in tensorflow and trained with the Coco dataset.  Then, drawings from the Google QuickDraw dataset are randomly picked to replace the identified objects.

In this fork, as it is intended to run in a desktop computer, all the references to raspberry pi and arduino were removed.


This project contains a REST server written in Flask that exposes only one type of request:

- URL:    /cartoon
- Method: POST
- Data params: { 'image': 'base64 encoded string with the image data'}
- Success response: 
	  - Code: 200
	  - Content: { 'cartoon': 'base64 encoded string with the cartoon data'}




### Desktop installation (only tested in linux)

- Requirements:
    * Python 3.x*
- install dependencies using `pip3 install -r requirements_desktop.txt` from the `install` subdirectory.
- download the cartoon dataset (~1.4GB) and the tensorflow model (~30MB) by running `python3 download_assets.py` from the  `install` subdirectory.

### Standalone 
You can run the Cartoonify project in a standalone mode. In the `cartoonify`directory, just execute:

`python3 command_line.py path_to_image `

If everything is ok, the original image and its cartoon version will be shown in a window.

### REST server

For running the REST server, execute the following commands in the directory `cartoonify`:

`export FLASK_APP=server.py`

`python3 -m flask run`

To shutdown the server, hit Ctrl+C.

It was also implemented a client program, written in python, that receives a path to an image as an argument, makes the http request to the flask server and receives the cartoon image. 


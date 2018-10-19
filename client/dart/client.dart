import 'dart:convert';
import  'dart:io';
import 'package:http/http.dart' as http;
import "package:path/path.dart" show dirname;


main()  async{
    // Getting the absolute path to this script file
    var currentPath = dirname(Platform.script.path);
    // Generating  absolute paths for the input/output images
    var pathImage="$currentPath/../samples/image.jpg";
    var pathCartoon="$currentPath/../samples/cartoon.png";

    // Reading image
    var image = File(pathImage);
    var imageAsBytes = await image.readAsBytes();

    // Creating request
    // NOTE: In the emulator, localhost ip is 10.0.2.2
    var uri = Uri.parse('http://127.0.0.1:5000/cartoon');
    var request = http.MultipartRequest("POST", uri);
    var inputFile = http.MultipartFile.fromBytes('image', imageAsBytes, filename: 'image.jpg');
    request.files.add(inputFile);

    try {
        // Sending request and waiting for response
        var response = await request.send();
        if (response.statusCode == 200) {
            // Receiving response stream
            var responseStr = await response.stream.bytesToString();

            // Converting response string to json dictionary
            var data = jsonDecode(responseStr);

            // Accessing response data
            var cartoon = data['cartoon'];
            if (cartoon != null) {
                // Creating the output file
                var outputFile = File(pathCartoon);
                // Decoding base64 string received as response
                var imageResponse = base64.decode(cartoon);

                // Writing the decoded image to the output file
                await outputFile.writeAsBytes(imageResponse);
            }
        }
    } catch  (e) {
        print( 'Server is down');
    }
}

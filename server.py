from flask import Flask, Response, request
from werkzeug.datastructures import Headers
from re import findall
import os

app = Flask(__name__)
@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/test.zip')
def test_zip():
    return send_file("test.zip")


def send_file(wantedFile):
    headers = Headers()
    headers.add('Content-Disposition', 'attachment',
                filename=wantedFile)
    headers.add('Content-Transfer-Encoding','binary')
    
    size = os.stat('./%s'%wantedFile).st_size
    print(size)
    status = 200 #OK
    startAt = 0
    endAt = size-1

    if request.headers.has_key("Range"):
	    status = 206  # Partial Content
	    headers.add('Accept-Ranges', 'bytes')
	    ranges = findall(r"\d+", request.headers["Range"])
	    begin = int(ranges[0])  
	    if len(ranges) > 1:
	    	end = int(ranges[1])
	    headers.add('Content-Range', 'bytes %s-%s/%s' %(str(begin), 
                    str(end), str(end - begin)))

    headers.add('Content-Length', str((endAt - startAt) + 1))

    response = Response(wantedFile, status=status,
                         headers=headers, direct_passthrough=True)
    return response

import logging

import azure.functions as func

import urllib.request
import PyPDF2
import io
#from readers import readerDescription


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    path = req.params.get('path')
    if not path:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            path = req_body.get('path')

    if path:
        req = urllib.request.Request(path, headers={'User-Agent' : "Magic Browser"})
        remote_file = urllib.request.urlopen(req).read()
        remote_file_bytes = io.BytesIO(remote_file)
        pdf = PyPDF2.PdfReader(remote_file_bytes)

        #des = readerDescription.getDescription(pdf)
        return func.HttpResponse(f"The text is : Hi")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


    

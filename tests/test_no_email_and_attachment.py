import os
import filetype
from werkzeug.datastructures import FileStorage

def test_no_email_and_attachment(app, client):
    del app
    
    my_document  = os.path.join("tests/data/ct_section13.pdf") 
    
    #Not 100% foolproof, but it will do for now 
    kind = filetype.guess(my_document)
    print('File MIME type: %s' % kind.mime)

    my_file = FileStorage(
    stream=open(my_document, "rb"),
    filename="ct_section13.pdf",
    content_type=kind.mime
    )

    data = dict()
    data['file']=my_file

    res = client.post('/email', data=data)
    assert res.status_code == 400

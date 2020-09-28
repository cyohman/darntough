def test_invalid_email(app, client):
    del app
    parameters = dict(recipient='notavalidemail')
    res = client.post('/email' , data=parameters)
    assert res.status_code == 400

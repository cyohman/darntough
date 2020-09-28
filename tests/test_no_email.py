def test_no_email(app, client):
    del app
    res = client.post('/email')
    assert res.status_code == 400

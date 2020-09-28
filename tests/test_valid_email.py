def test_valid_email(app, client):
    del app
    parameters = dict(recipient='chance.yohman@gmail.com')
    res = client.post('/email' , data=parameters)
    assert res.status_code == 200

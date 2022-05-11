reg = '/register'
try:
    from routes import app
    import unittest

except Exception as e:
    print(e)

class FlaskTest(unittest.TestCase):

    # check response is 200 or not
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get(reg)
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get(reg)
        self.assertEqual(response.content_type,'text/html; charset=utf-8')

    
if __name__ == '__main__':
    unittest.main()




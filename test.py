import unittest
from routes import app
reg = '/register'
# try:
#     from routes import app
#     import unittest

# except Exception as e:
#     print(e)


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

    # check response is 200 or not
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/view')
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get('/view')
        self.assertEqual(response.content_type,'text/html; charset=utf-8')

    # check for data returned or not
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get('/view')
        self.assertFalse(b'message' in response.data)

    def test_cannot_add_empty_list_items(self):
        tester = app.test_client(self)
        response = tester.get('/view')
        self.assertTrue('Fill All the fields')

    def test_index2(self):
        tester = app.test_client(self)
        response = tester.get('/stopcheque')
        statuscode = response.status_code
        self.assertEqual(statuscode,200)


    def test_index_s(self):
        tester = app.test_client(self)
        response = tester.get('/stopcheque')
        self.assertEqual(response.content_type,'text/html; charset=utf-8')


    def test_index_st(self):
        tester = app.test_client(self)
        response = tester.get('/stopcheque')
        self.assertFalse(b'message' in response.data)

    def test_index_stop(self):
        tester = app.test_client(self)
        response = tester.get('/stopcheque')
        self.assertTrue('Fill All the fields')
    
if __name__ == '__main__':
    unittest.main()




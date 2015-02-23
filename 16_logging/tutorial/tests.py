import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import TutorialViews

        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.home()
        self.assertEqual('Home View', response['page_title'])

    def test_hello(self):
        from .views import TutorialViews

        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.hello()
        self.assertEqual('Hello View', response['page_title'])
        

class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>TutorialViews - Home View</h1>', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy/john/deep', status=200)
        self.assertIn(b'<p>Welcome, john deep</p>', res.body)

    def test_hello_json(self):
        res = self.testapp.get('/howdy.json', status=200)
        self.assertIn(b'{"page_title": "Hello View"}', res.body)
        self.assertEqual(res.content_type, 'application/json')
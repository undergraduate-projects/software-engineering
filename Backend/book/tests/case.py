from django.test import TestCase
from book.views import views_response


class ViewsTestCase(TestCase):

    def assertResponse(self, response, correct_response):
        self.assertEqual(response.getvalue(), correct_response.getvalue())

    def checkMethod(self, client, path, not_allowed_methods):
        for method in not_allowed_methods:
            if method == 'GET':
                response = client.get(path)
            elif method == 'PUT':
                response = client.put(path)
            elif method == 'POST':
                response = client.post(path)
            elif method == 'DELETE':
                response = client.delete(path)
            elif method == 'PATCH':
                response = client.patch(path)
            else:
                response = None
            self.assertResponse(response, views_response.method_not_allowed(method))
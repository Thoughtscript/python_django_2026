from django.test import TestCase, RequestFactory
from django.http import JsonResponse, QueryDict
from djangoexample.models import Example
from djangoexample.views import one_example
import json

ERROR_ENCOUNTERED = "Error Encountered"
WRONG_REQUEST_METHOD_SET = "Wrong Request Method Sent"

class OneExampleViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.example = Example.objects.create(
            name="Test Example",
            pk=1,
        )

    def test_get_valid_pk_returns_example(self):
        """GET with a valid pk returns the example data."""
        request = self.factory.get(
            "/one_example/",
            {"pk": self.example.pk},
        )
        response = one_example(request)
        data = json.loads(response.content)
        
        self.assertEqual(data.get('pk'), 1)
        self.assertEqual(data.get('name'), "Test Example")
        self.assertEqual(response.status_code, 200)

    '''
    Errors - 500
    '''

    def test_get_invalid_pk_returns_error(self):
        """GET with a non-existent pk returns the error payload."""
        request = self.factory.get(
            "/one_example/",
            {"pk": 99999},
        )
        response = one_example(request)
        data = json.loads(response.content)

        self.assertEqual(data, ERROR_ENCOUNTERED)
        self.assertEqual(response.status_code, 500)

    def test_get_missing_pk_returns_error(self):
        """GET without a pk returns the error payload."""
        request = self.factory.get("/one_example/")
        response = one_example(request)
        data = json.loads(response.content)

        self.assertEqual(data, ERROR_ENCOUNTERED)
        self.assertEqual(response.status_code, 500)


    def test_invalid_pk_type_returns_error(self):
        """Non-integer pk values are handled gracefully."""
        request = self.factory.get(
            "/one_example/",
            {"pk": "abc"},
        )
        response = one_example(request)
        data = json.loads(response.content)

        self.assertEqual(data, ERROR_ENCOUNTERED)
        self.assertEqual(response.status_code, 500)

    '''
    Wrong Method - 401
    '''

    def test_post_returns_wrong_method(self):
        """POST requests are rejected."""
        request = self.factory.post("/one_example/")
        response = one_example(request)
        data = json.loads(response.content)

        self.assertEqual(data, WRONG_REQUEST_METHOD_SET)
        self.assertEqual(response.status_code, 401)

    def test_put_returns_wrong_method(self):
        """PUT requests are rejected."""
        request = self.factory.put("/one_example/")
        response = one_example(request)
        data = json.loads(response.content)

        self.assertEqual(data, WRONG_REQUEST_METHOD_SET)
        self.assertEqual(response.status_code, 401)

    def test_delete_returns_wrong_method(self):
        """DELETE requests are rejected."""
        request = self.factory.delete("/one_example/")
        response = one_example(request)
        data = json.loads(response.content)

        self.assertEqual(data, WRONG_REQUEST_METHOD_SET)
        self.assertEqual(response.status_code, 401)


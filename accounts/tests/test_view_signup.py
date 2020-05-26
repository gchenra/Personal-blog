from django.test import TestCase
from django.urls import reverse, resolve 
from ..views import signup
from ..forms import SignUpForm 
from django.contrib.auth.models import User

class SignUpTests(TestCase):

	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(url)

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_signup_url_resolves_signup_view(self):
		view = resolve('/signup/')
		self.assertEquals(view.func, signup)

	def tet_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SignUpForm)

	def test_form_inputs(self):
		"""
		The view must contain five inputs: csrf, username, email,
		password1, password2
		"""
		# what does <input mean in html
		# why not checking csrf, oh cuz it was checked in test_csrf!
		self.assertContains(self.response, '<input', 5)
		self.assertContains(self.response, 'type="text"', 1)
		self.assertContains(self.response, 'type="email"', 1)
		self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		data = {
			'username': 'john',
			'email':'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
		}
		self.response = self.client.post(url, data)
		self.home_url = reverse('home')

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		"""
		Create a new request to an arbitrary page.
		The resulting response should now have a 'user' to its context
		after a successful sign up
		"""
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.post(url, {}) # submit an empty form

	def test_signup_status_code(self):
		"""
		Invalid form submission should return to the same page 
		"""
		# only checking the status code is enough? 
		# how are you sure its not redirecting to e.g. home page 
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_dont_create_user(self):
		self.assertFalse(User.objects.exists())






















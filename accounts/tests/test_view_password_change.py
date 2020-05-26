from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as aviews
from django.urls import resolve, reverse
from django.test import TestCase

class PasswordChangeTest(TestCase):
	def setUp(self):
		user = User.objects.create_user(username='john', email='john@doe.com', password='secret123')
		url = reverse('password_change')
		self.client.login(username='john', password='secret123')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_url_resolve_correct_view(self):
		view = resolve('/settings/password/')
		self.assertEquals(view.func.view_class, aviews.PasswordChangeView)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, PasswordChangeForm)

	def test_form_inputs(self):
		'''
		The view must contain four inputs: csrf, old_password, new_password1, new_password2
		'''
		self.assertContains(self.response, '<input', 4)
		self.assertContains(self.response, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):
	def test_redirection(self):
		url = reverse('password_change')
		login_url = reverse('login')
		response = self.client.get(url)
		self.assertRedirects(response, '{}?next={}'.format(login_url, url))

class PasswordChangeTestCase(TestCase):
    '''
    Create a user for the use of next test case
    '''
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)

class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        '''
        refresh the user instance from database to get the new password
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_use_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have an 'user
        to its context, after a successful signup
        '''
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidPasswordChangeTests(PasswordChangeTestCase):
    '''
    This class don't need the setUp function.
    Because the parent class' setUp function is already
    posting invalid change password inputs to the password_change url
    '''
    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
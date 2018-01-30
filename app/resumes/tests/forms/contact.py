from . import (
    TransactionTestCase, HR, EMPLOYEE, CANDIDATE,
    Company, Resume, mock, ContactForm, Workplace, Skill, Contact
)
import ipdb

class ContactFormTest(TransactionTestCase):
    """ Tests for ContactForm class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml',
        'contacts.yaml'
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.resume = Resume.objects.last()
        self.company = Company.objects.first()
        self.contact = Contact.objects.last()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.params = {
            'resume_id': self.resume.id,
            'email': self.user.email,
            'phone': '+79214438239'
        }

    def test_success_validation(self):
        """ Test success validation of form """

        form = ContactForm(obj=Contact(), params=self.params)
        self.assertTrue(form.is_valid())

    def test_failed_validation_email_already_exists(self):
        """ Test failed validation of form if contact with this email
        already exist """

        self.params['email'] = self.contact.email
        form = ContactForm(obj=Contact(), params=self.params)
        form.is_valid()
        form.submit()
        assert 'email' in form.errors, True

    def test_failed_validation_phone_already_exists(self):
        """ Test failed validation of form if contact with this phone
        already exist """

        self.params['phone'] = self.contact.phone
        form = ContactForm(obj=Contact(), params=self.params)
        form.is_valid()
        form.submit()
        assert 'phone' in form.errors, True
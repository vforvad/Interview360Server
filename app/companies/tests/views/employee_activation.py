from . import (
    APITestCase, Company, CompanyMember, User, Token, datetime
)

class EmployeeActivationTests(APITestCase):
    """ Tests for EmployeeActivationTests """

    def setUp(self):
        """ Setting up test credentials """

        self.user = User.objects.create(email="example@mail.com")
        self.company = Company.objects.create(name="Test",
                                         city="Test",
                                         start_date=datetime.date.today())
        self.token = Token.objects.create(user=self.user)

        self.form_data = {
            'company_id': self.company.id,
            'token': self.token.key,
            'password': 'aaaaaa',
            'password_confirmation': 'aaaaaa'
        }

    # TODO: rebuild this tests
    # def test_success_employee_activation(self):
    #     """ Test success response for route """
    #
    #     url = "/api/v1/companies/{}/activate_member/".format(self.company.id)
    #     response = self.client.put(url, self.form_data)
    #     self.assertTrue('message' in response.data)
    #
    # def test_failed_employee_activation(self):
    #     """ Test failed response for route """
    #
    #     url = "/api/v1/companies/{}/activate_member/".format(self.company.id)
    #     response = self.client.put(url, {})
    #     self.assertTrue('errors' in response.data)
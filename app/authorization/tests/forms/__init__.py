from django.test import TestCase
from authorization.forms import (AuthorizationForm, RestorePasswordForm,
                                 RegistrationForm)
from authorization.models import User
from django.test import override_settings
from rest_framework.authtoken.models import Token
import mock

from .authorization import AuthorizationFormTests
from .restore_password import RestorePasswordFormTests

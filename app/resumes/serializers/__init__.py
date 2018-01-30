from rest_framework import serializers
from resumes.models import Resume, Workplace
from authorization.models import User
from vacancies.fields import SkillsField
from skills.serializers import SkillSerializer
from common.serializers.user_serializer import UserSerializer
from common.fields import CustomField
from resumes.index import ResumesIndex
from common.serializers.base_company_serializer import BaseCompanySerializer

from .resumes import ResumesSerializer
from .workplace import WorkplaceSerializer
from .resume import ResumeSerializer
from rest_framework import serializers
from .models import Vacancy
from django.db import transaction
from skills.models import Skill
from companies.models import Company
from companies.serializers import CompanySerializer
import ipdb

class VacancyCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = [
            field for field in CompanySerializer.Meta.fields if field not in ['employees']
        ]
        read_only_fields = ('__all__',)

class VacancySerializer(serializers.ModelSerializer):
    """ Serializer for vacancies object """

    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False)
    salary = serializers.DecimalField(max_digits=6, decimal_places=2, required=True)
    company_id = serializers.IntegerField(required=True, write_only=True)
    company = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'salary',
            'company',
            'company_id',
            'created_at',
            'updated_at',
            'skills'
        ]

    def get_company(self, vacancy):
        company = Company.objects.get(id=vacancy.company_id)
        return VacancyCompanySerializer(company, read_only=True).data

    def create(self, data):
        """ Create new instance of Vacancy and add Skills objects to it """

        try:
            with transaction.atomic():
                skills = data.pop('skills', None)
                vacancy = Vacancy.objects.create(**data)
                vacancy.skills.set(skills)
                return vacancy
        except:
            return False

    def update(self, instance, data):
        """ Update vacancy parameters """

        with transaction.atomic():
            instance.title = data.get('title', instance.title)
            instance.description = data.get('description', instance.description)
            instance.salary = data.get('salary', instance.salary)
            instance.skills.set(data.get('skills', []))

            return instance
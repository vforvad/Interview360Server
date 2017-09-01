from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InterviewSerializer
from companies.models import Company
from vacancies.models import Vacancy
from .models import Interview

import ipdb

class InterviewViewSet(viewsets.ModelViewSet):
    """ View class for Interviews """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = InterviewSerializer

    def get_queryset(self):
        """
        Return scope of interviews where current user is participated
        """
        params = self.kwargs
        company = get_object_or_404(Company, pk=params['company_pk'])
        vacancy = get_object_or_404(Vacancy, pk=params['vacancy_pk'])
        queryset = vacancy.interview_set.all()
        return queryset

    def create(self, request, company_pk=None, vacancy_pk=None):
        """ POST action for create a new interview """

        company = get_object_or_404(Company, pk=company_pk)
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and serializer.save():
            return Response(
                { 'interview': serializer.data }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                { 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None, company_pk=None, vacancy_pk=None):
        """ PUT action for update the interview instance """

        company = get_object_or_404(Company, pk=company_pk)
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
        interview = get_object_or_404(Interview, pk=pk)
        serializer = self.serializer_class(
            interview, data=request.data, partial=True
        )
        if serializer.is_valid() and serializer.save():
            return Response(
                { 'interview': serializer.data }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                { 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST
            )

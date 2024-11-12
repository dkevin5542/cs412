from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django import forms
from django.db.models import Q
from datetime import date
import plotly.express as px
import pandas as pd
from plotly.offline import plot
from typing import Any, Dict
import plotly.graph_objects as go
from django.db.models.query import QuerySet

class VoterFilterForm(forms.Form):
    """
    Form to filter Voter data based on various criteria.
    Fields include:
      - party affiliation
      - minimum and maximum date of birth
      - voter score
      - participation in specific elections
    """
    party_affiliation = forms.ChoiceField(
        choices=[('', 'Any')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False
    )
    min_dob = forms.ChoiceField(
        choices=[('', 'Any')] + [(year, year) for year in range(1900, date.today().year + 1)],
        required=False
    )
    max_dob = forms.ChoiceField(
        choices=[('', 'Any')] + [(year, year) for year in range(1900, date.today().year + 1)],
        required=False
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(score, score) for score in range(6)],
        required=False
    )
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)

class VoterListView(ListView):
    """
    View to display a list of Voter records with optional filtering.
    Uses pagination to show 100 records per page.
    """
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """
        Retrieves the queryset for Voter records, applying filters
        from VoterFilterForm if provided in the request.
        """
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        
        # Apply filters if the form is valid
        if form.is_valid():
            # Filter by party affiliation if selected
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            # Filter by date of birth range
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_dob'])
            # Filter by voter score
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            # Filter by participation in specific elections
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field):
                    queryset = queryset.filter(**{field: form.cleaned_data[field]})
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds the filter form to the context for use in the template.
        """
        context = super().get_context_data(**kwargs)
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    """
    View to display detailed information for a single Voter record.
    """
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphListView(ListView):
    """
    View to display graphical representations of aggregate data about Voter records.
    Uses Plotly to generate visualizations, with filtering options via VoterFilterForm.
    """
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self) -> QuerySet[Any]:
        """
        Retrieves the queryset for Voter records, applying filters
        from VoterFilterForm if provided in the request.
        """
        qs = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        
        # Apply filters if the form is valid
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                qs = qs.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_dob']:
                qs = qs.filter(date_of_birth__year__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                qs = qs.filter(date_of_birth__year__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['voter_score']:
                qs = qs.filter(voter_score=form.cleaned_data['voter_score'])
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field):
                    qs = qs.filter(**{field: form.cleaned_data[field]})
        
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Adds graphs to the context using Plotly based on the filtered Voter data.
        Generates:
          - Histogram of Voter distribution by year of birth
          - Pie chart of Voter distribution by party affiliation
          - Bar chart of Voter participation in recent elections
        """
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        
        # Add filter form to context
        context['filter_form'] = VoterFilterForm(self.request.GET)

        # Convert queryset to DataFrame for easier data manipulation
        data = pd.DataFrame(list(voters.values()))

        if not data.empty:
            # Generate Histogram for Year of Birth
            data['date_of_birth'] = pd.to_datetime(data['date_of_birth'], errors='coerce')
            data['year_of_birth'] = data['date_of_birth'].dt.year
            birth_counts = data['year_of_birth'].value_counts().sort_index()
            birth_hist_fig = go.Figure(data=[go.Bar(x=birth_counts.index, y=birth_counts.values)])
            birth_hist_fig.update_layout(
                title='Voter Distribution by Year of Birth',
                xaxis_title='Year of Birth',
                yaxis_title='Count'
            )
            context['birth_hist'] = plot(birth_hist_fig, output_type='div')

            # Generate Pie Chart for Party Affiliation
            party_counts = data['party_affiliation'].value_counts()
            party_pie_fig = go.Figure(data=[go.Pie(labels=party_counts.index, values=party_counts.values)])
            party_pie_fig.update_layout(title='Voter Distribution by Party Affiliation')
            context['party_pie'] = plot(party_pie_fig, output_type='div')

            # Generate Bar Chart for Election Participation
            election_participation = {
                '2020 State Election': data['v20state'].sum(),
                '2021 Town Election': data['v21town'].sum(),
                '2021 Primary Election': data['v21primary'].sum(),
                '2022 General Election': data['v22general'].sum(),
                '2023 Town Election': data['v23town'].sum()
            }
            election_df = pd.DataFrame(list(election_participation.items()), columns=['Election', 'Voter Count'])
            election_hist_fig = go.Figure(data=[go.Bar(x=election_df['Election'], y=election_df['Voter Count'])])
            election_hist_fig.update_layout(
                title='Voter Participation in Elections',
                xaxis_title='Election',
                yaxis_title='Number of Participants'
            )
            context['election_hist'] = plot(election_hist_fig, output_type='div')

        return context

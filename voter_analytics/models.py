from django.db import models

class Voter(models.Model):
    """
    Model representing a registered voter, including personal information,
    address details, party affiliation, precinct number, voter score, and
    participation in recent elections.
    """
    
    # Personal information fields
    last_name = models.CharField(max_length=50, help_text="Voter's last name")
    first_name = models.CharField(max_length=50, help_text="Voter's first name")
    
    # Address fields
    residential_street_number = models.CharField(max_length=10, help_text="Street number of the voter's residential address")
    residential_street_name = models.CharField(max_length=100, help_text="Street name of the voter's residential address")
    residential_apartment_number = models.CharField(max_length=10, blank=True, null=True, help_text="Apartment number, if applicable")
    residential_zip_code = models.CharField(max_length=10, help_text="Zip code of the voter's residential address")
    
    # Date fields
    date_of_birth = models.DateField(help_text="Voter's date of birth")
    date_of_registration = models.DateField(help_text="Date the voter registered to vote")
    
    # Party affiliation and precinct information
    party_affiliation = models.CharField(max_length=50, help_text="Voter's party affiliation")
    precinct_number = models.CharField(max_length=10, help_text="Precinct number associated with the voter's address")
    
    # Boolean fields for participation in past elections
    v20state = models.BooleanField(help_text="Participation in 2020 State Election")
    v21town = models.BooleanField(help_text="Participation in 2021 Town Election")
    v21primary = models.BooleanField(help_text="Participation in 2021 Primary Election")
    v22general = models.BooleanField(help_text="Participation in 2022 General Election")
    v23town = models.BooleanField(help_text="Participation in 2023 Town Election")
    
    # Voter engagement score based on participation in past elections
    voter_score = models.IntegerField(help_text="Number of elections the voter participated in (out of 5)")

    def __str__(self):
        """
        Returns a string representation of the voter, including their
        first and last name, and party affiliation.
        """
        return f"{self.first_name} {self.last_name} - {self.party_affiliation}"

    @classmethod
    def load_data(cls, file_path):
        """
        Class method to load voter data from a CSV file into the database.
        
        Parameters:
            file_path (str): Path to the CSV file containing voter data.

        The CSV file must include the following fields:
          - Last Name, First Name, Residential Address - Street Number,
            Residential Address - Street Name, Residential Address - Apartment Number,
            Residential Address - Zip Code, Date of Birth, Date of Registration,
            Party Affiliation, Precinct Number, v20state, v21town, v21primary,
            v22general, v23town, voter_score
        """
        import csv
        from datetime import datetime

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert 'TRUE'/'FALSE' string values to boolean
                def to_bool(value):
                    return value.strip().upper() == 'TRUE'
                
                # Create a new Voter instance for each row in the CSV file
                voter = cls(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    residential_street_number=row['Residential Address - Street Number'],
                    residential_street_name=row['Residential Address - Street Name'],
                    residential_apartment_number=row.get('Residential Address - Apartment Number', None),
                    residential_zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=to_bool(row['v20state']),
                    v21town=to_bool(row['v21town']),
                    v21primary=to_bool(row['v21primary']),
                    v22general=to_bool(row['v22general']),
                    v23town=to_bool(row['v23town']),
                    voter_score=int(row['voter_score']),
                )
                # Save the voter instance to the database
                voter.save()

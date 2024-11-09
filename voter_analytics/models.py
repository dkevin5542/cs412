from django.db import models
from datetime import datetime

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
    def load_data(cls):
        """
        Load data records from a CSV file into model instances.
        Clears existing records and loads new data from a specified file.
        """
        # Clear existing records
        cls.objects.all().delete()

        # Define file path (update with actual file path if needed)
        filename = 'C:/Users/dongk/django/voter_analytics/newton_voters.csv'

        import csv
        from datetime import datetime

        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)  # Use DictReader to match by column names

                for row in reader:
                    try:
                        # Convert 'TRUE'/'FALSE' strings to boolean values
                        def to_bool(value):
                            return value.strip().upper() == 'TRUE'

                        # Attempt to parse dates; if they fail, skip the row
                        try:
                            date_of_birth = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
                            date_of_registration = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
                        except ValueError as date_error:
                            print(f"Skipping row {row['Voter ID Number']} due to date parsing error: {date_error}")
                            continue  # Skip this row if dates are invalid

                        # Create a new Voter instance using named fields
                        voter = cls(
                            last_name=row['Last Name'],
                            first_name=row['First Name'],
                            residential_street_number=row['Residential Address - Street Number'],
                            residential_street_name=row['Residential Address - Street Name'],
                            residential_apartment_number=row.get('Residential Address - Apartment Number', None),
                            residential_zip_code=row['Residential Address - Zip Code'],
                            date_of_birth=date_of_birth,
                            date_of_registration=date_of_registration,
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
                        print(f'Created voter: {voter}')

                    except Exception as e:
                        # Print error details for the problematic row
                        print(f"Error processing row {row['Voter ID Number']}: {e}")

        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"An error occurred while opening the file: {e}")



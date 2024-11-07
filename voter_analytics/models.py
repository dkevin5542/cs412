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
        # Delete all records to clear the database
        cls.objects.all().delete()

        # Define the file path (update with your own path as needed)
        filename = 'C:/Users/dongk/django/voter_analytics/newton_voters.csv'
        # On Windows: '/C/Users/YOURNAME/Desktop/2023_chicago_results.csv'

        # Open the file for reading
        with open(filename, mode='r') as file:
            headers = file.readline()  # Read and discard the header line
            print(headers)  # Optional: print headers for debugging

            # Loop to read each line in the file
            for line in file:
                try:
                    # Split the line by commas to get individual fields
                    fields = line.strip().split(',')

                    # Convert 'TRUE'/'FALSE' strings to boolean
                    def to_bool(value):
                        return value.strip().upper() == 'TRUE'

                    # Create a new Voter instance using the fields from the CSV line
                    voter = cls(
                        last_name=fields[0],
                        first_name=fields[1],
                        residential_street_number=fields[2],
                        residential_street_name=fields[3],
                        residential_apartment_number=fields[4] if fields[4] else None,
                        residential_zip_code=fields[5],
                        date_of_birth=datetime.strptime(fields[6], '%Y-%m-%d').date(),
                        date_of_registration=datetime.strptime(fields[7], '%Y-%m-%d').date(),
                        party_affiliation=fields[8].strip(),
                        precinct_number=fields[9],
                        v20state=to_bool(fields[10]),
                        v21town=to_bool(fields[11]),
                        v21primary=to_bool(fields[12]),
                        v22general=to_bool(fields[13]),
                        v23town=to_bool(fields[14]),
                        voter_score=int(fields[15]),
                    )

                    # Save the voter instance to the database
                    voter.save()
                    print(f'Created voter: {voter}')  # Optional: print confirmation

                except Exception as e:
                    # If an error occurs, print the line and the error message
                    print(f"Exception processing line: {line}")
                    print(f"Error: {e}")


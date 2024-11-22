from django.db import models
import pandas as pd
from django.db.utils import IntegrityError
from django.contrib.auth.models import User as AuthUser



# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)  # Unique username for the user
    email = models.EmailField(unique=True)  # Unique email for contact
    image_file = models.ImageField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True) 

    auth_user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,  # Delete the custom User instances if the auth User is deleted
        related_name='custom_users',  # Reverse lookup from AuthUser to custom Users
        help_text="The associated Django auth user.",
        default=1 
    )


    favorite_anime = models.ManyToManyField(
        'Anime',  # Reference the Anime model
        related_name='favorited_by',  # Reverse lookup for Anime -> Users who favorited it
        blank=True, 
        help_text="Select your favorite anime."
    )

    # Many-to-Many relationship to Merchandise
    selected_merchandise = models.ManyToManyField(
        'Merchandise',  # Related to Merchandise model
        blank=True,  # Users may not have picked merchandise yet
        related_name='buyers'  # Reverse lookup from Merchandise to users who picked it
    )


    def __str__(self):
        return self.username
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['auth_user'],  # Ensure each AuthUser can have only one associated User
                name='unique_auth_user_constraint'
            )
        ]
    



class Anime(models.Model):
    uid = models.IntegerField(unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    genre = models.JSONField()  # To store genres as a JSON array
    aired = models.CharField(max_length=255)  # Use CharField for date ranges
    episodes = models.FloatField(null=True, blank=True)  # Float for episodes (e.g., 1.0)
    members = models.IntegerField()
    popularity = models.IntegerField()
    ranked = models.FloatField(null=True, blank=True)  # Some rankings may be null
    score = models.FloatField(null=True, blank=True)
    img_url = models.URLField(max_length=500)
    link = models.URLField(max_length=500)

    def __str__(self):
        return self.title
    
def load_data(file_path):
    """
    Loads anime data from a CSV file into the Anime model.

    Args:
        file_path (str): The file path to the CSV file.
    """
    try:
        # Read the CSV file
        anime_data = pd.read_csv(file_path)
        
        # Convert 'genre' column from string to list
        anime_data['genre'] = anime_data['genre'].apply(eval)

        # Iterate through the rows and create Anime objects
        for _, row in anime_data.iterrows():
            try:
                Anime.objects.create(
                    uid=row['uid'],
                    title=row['title'],
                    synopsis=row['synopsis'],
                    genre=row['genre'],
                    aired=row['aired'],
                    episodes=row['episodes'] if not pd.isna(row['episodes']) else None,
                    members=row['members'],
                    popularity=row['popularity'],
                    ranked=row['ranked'] if not pd.isna(row['ranked']) else None,
                    score=row['score'] if not pd.isna(row['score']) else None,
                    img_url=row['img_url'],
                    link=row['link']
                )
            except IntegrityError:
                print(f"Anime with UID {row['uid']} already exists. Skipping.")
            except Exception as e:
                print(f"Error adding anime {row['title']}: {e}")
        print("Data successfully loaded.")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

class Character(models.Model):
    # Fields
    name = models.CharField(max_length=255)  # Character's name
    anime = models.ForeignKey(
        'Anime', 
        on_delete=models.CASCADE,  # Deletes character when anime is deleted
        related_name='characters'  # Related name for reverse lookup
    )
    description = models.TextField(blank=True, null=True)  # Description of the character
    role = models.CharField(max_length=50, choices=[  # Character's role
        ('main', 'Main'),
        ('supporting', 'Supporting'),
        ('antagonist', 'Antagonist'),
    ], default='supporting')
    image_url = models.URLField(blank=True, null=True)  
    popularity = models.IntegerField(blank=True, null=True)  # Popularity ranking or score

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} ({self.get_role_display()}) in {self.anime.title}"
    
class Merchandise(models.Model):
    # Fields
    item_name = models.CharField(max_length=255)  # Name of the merchandise item
    type = models.CharField(max_length=50, choices=[  # Type of merchandise
        ('figurine', 'Figurine'),
        ('poster', 'Poster'),
        ('apparel', 'Apparel'),
        ('accessory', 'Accessory'),
        ('other', 'Other'),
    ], default='other')
    description = models.TextField(blank=True, null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the merchandise
    user = models.ForeignKey(
        'User',  # Link to the User model
        on_delete=models.CASCADE,  # Deletes merchandise when the user is deleted
        related_name='merchandise'  # Related name for reverse lookup
    )
    character = models.ForeignKey(
        'Character',  # Link merchandise to a specific Character
        on_delete=models.CASCADE,  # Deletes merchandise when the character is deleted
        related_name='merchandise'  # Related name for reverse lookup
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.item_name} ({self.type})"
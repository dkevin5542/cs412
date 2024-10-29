from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User




# Create your models here.
class Profile(models.Model):
    '''creates the model for each profile for the mini_fb'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False, null=True, unique=True)
    # image_url = models.URLField(blank=True) 
    image_file = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 


    
    def __str__(self):
        '''Return a string representation of this profile object.''' 
        return f"{self.first_name} {self.last_name}'s Profile"
    
    def get_statusMessage(self):
        '''Return all of the statusMessage about this profile.'''
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        '''Returns the URL to display this profile.'''
        return reverse('profile', args=[self.pk])
    
    def get_friends(self):
        '''Return a list of this profile's friends (Profile instances).'''
        # Get all Friend instances where this profile is profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        # Collect the corresponding friends from the Friend instances
        friends_profiles = []
        
        # Append profile2 from friends where self is profile1
        for friend in friends_as_profile1:
            friends_profiles.append(friend.profile2)
        
        # Append profile1 from friends where self is profile2
        for friend in friends_as_profile2:
            friends_profiles.append(friend.profile1)

        return friends_profiles
    
    def add_friend(self, other):
        """
        Add a Friend relationship between this profile (self) and the other profile,
        ensuring no duplicates and preventing self-friending.
        """
        if self == other:
            # Prevent self-friending
            return "You cannot friend yourself."

        # Check if a Friend relation already exists between the two profiles
        friend_exists = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) |
            models.Q(profile1=other, profile2=self)
        ).exists()

        if friend_exists:
            # Prevent duplicate friend relations
            return "Friendship already exists."

        # Create a new Friend relationship if no duplicate exists
        new_friendship = Friend(profile1=self, profile2=other)
        new_friendship.save()
        return "Friendship added successfully."
    
    def get_friend_suggestions(self):
        """
        Return a list of Profiles that the current profile (self) is not friends with.
        """
        # Get profiles that are already friends
        friends = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        friend_ids = set()  # Set to store friend profile IDs

        for friend in friends:
            if friend.profile1 == self:
                friend_ids.add(friend.profile2.id)
            else:
                friend_ids.add(friend.profile1.id)

        # Get all profiles excluding self and existing friends
        suggestions = Profile.objects.exclude(id=self.id).exclude(id__in=friend_ids)

        return suggestions
    
    def get_news_feed(self):
        """
        Returns a queryset of StatusMessages for the profile and their friends,
        ordered by the most recent first.
        """
        # Get the current profile's friends
        friends = self.get_friends()

        # Get the current profile's status messages
        profile_statuses = StatusMessage.objects.filter(profile=self)

        # Get status messages for all friends
        friends_statuses = StatusMessage.objects.filter(profile__in=friends)

        # Combine and order by timestamp (most recent first)
        news_feed = profile_statuses.union(friends_statuses).order_by('-timestamp')

        return news_feed





class StatusMessage(models.Model):
    '''creates the model for each status message for each profile for the mini_fb'''
    profile  = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)


    def __str__(self):
        '''Return the string representation of this comment.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all images associated with this status message.'''
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    '''Creates the model for images associated with status messages.'''
    status_message = models.ForeignKey(StatusMessage, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this image object.'''
        return f'Image for: {self.status_message.message[:20]}...' 


class Friend(models.Model):
    '''Represents a friendship (edge) between two profiles in a social network.'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends_profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends_profile2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        '''Return a string representation of the friendship, showing both profiles' names.'''
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
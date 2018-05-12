from django.contrib.auth.models import User
from custom.users.models import Profile

users = User.objects.all()
for user in users:
    try:
        profile = Profile.objects.get(user=user)
    except Exception as e:
        print("Creating profile for user {}".format(user.id))
        profile = Profile.objects.create(user=user, username=user.username,
                                         email=user.email)
    print("Done")

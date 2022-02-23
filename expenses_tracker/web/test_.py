from expenses_tracker.web.models import Profile


def get_profile():
    profiles = Profile.objects.all()
    print(profiles)

from .models import Profile_master

def user_profile(request):
    if request.user.is_authenticated:
        try:
            return {
                'profile': Profile_master.objects.get(user=request.user)
                
            }
        except Profile_master.DoesNotExist:
            return {'profile': None}
    return {'profile': None}

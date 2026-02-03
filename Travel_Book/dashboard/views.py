from django.shortcuts import render ,redirect, get_object_or_404 , get_list_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib.auth.models import User 
from .models import Profile_master ,TravelDiary, Plan_trip , Categories, blogs,gallary
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import date 
from django.http import JsonResponse


# Create your views here.


@login_required
def Dashboard(request):
    total_trips_count = TravelDiary.objects.filter(user=request.user).count()
    total_blogs_count = blogs.objects.filter(user=request.user).count()
    total_photos_count = gallary.objects.filter(user=request.user).count()
    recent_travel_entries = TravelDiary.objects.filter(user=request.user).order_by('-created_at')[:2]
    recent_plan_entries = Plan_trip.objects.filter(user=request.user).order_by('-created_at')[:2]
    return render(request, 'Dashboard/dashboard.html',{
        'total_trips_count':total_trips_count,
        'total_blogs_count':total_blogs_count,
        'total_photos_count':total_photos_count,
        'recent_travel_entries':recent_travel_entries,
        'recent_plan_entries':recent_plan_entries,
    })


from django.db import IntegrityError
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    profile, created = Profile_master.objects.get_or_create(user=request.user)
    user = request.user

    if request.method == "POST":
        profile.First_name = request.POST.get('first-name')
        profile.Last_name = request.POST.get('last-name')
        profile.about = request.POST.get('about')

        if request.FILES.get('file-upload'):
            profile.profile_photo = request.FILES.get('file-upload')

        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # ✅ Validate username
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken')
                return redirect('profile')
            user.username = new_username

        # ✅ Validate email
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, 'Email already taken')
                return redirect('profile')
            user.email = new_email

        # ✅ SINGLE SAVE POINT
        try:
            user.save()
            profile.save()
        except IntegrityError:
            messages.error(request, 'Duplicate value detected')
            return redirect('profile')

        messages.success(request, 'Profile Updated Successfully')
        return redirect('profile')

    return render(request, 'Dashboard/profile.html', {
        'profile': profile,
    })




def check_username(request):
    username = request.GET.get('username', '').strip()

    if not username:
        return JsonResponse({'available': False, 'message': 'Username required'})

    if request.user.is_authenticated:
        exists = User.objects.filter(username=username)\
                             .exclude(id=request.user.id)\
                             .exists()
    else:
        exists = User.objects.filter(username=username).exists()

    if exists:
        return JsonResponse({'available': False, 'message': 'Username already taken'})

    return JsonResponse({'available': True, 'message': 'Username available'})


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_email(request):
    email = request.GET.get('email', '').strip()

    if not email:
        return JsonResponse({'available': False, 'message': 'Email required'})

    if request.user.is_authenticated:
        exists = User.objects.filter(email=email)\
                             .exclude(id=request.user.id)\
                             .exists()
    else:
        exists = User.objects.filter(email=email).exists()

    if exists:
        return JsonResponse({'available': False, 'message': 'Email already taken'})

    return JsonResponse({'available': True, 'message': 'Email available'})

    




@login_required
def mytrip(request):
    diary_list = TravelDiary.objects.filter(user=request.user)
    plan_trip_list = Plan_trip.objects.filter(user=request.user)
    total = len(diary_list)
    total_plans = len(plan_trip_list)
    types = Categories.objects.all()

    categories_id = None

    if request.method == "GET":
        categories_id = request.GET.get('categories')

        if categories_id:
            diary_list = diary_list.filter(categories_id=categories_id)
            plan_trip_list = plan_trip_list.filter(categories_id=categories_id)


    return render(request, 'Dashboard/mytrip.html', {'diary_list': diary_list,'total':total,'plan_trip_list':plan_trip_list,'total_plans':total_plans,'types':types,'id': int(categories_id) if categories_id else None })



@login_required
def add_diary(request):
    types = Categories.objects.all()
    if request.method == "POST":
        categories_id = request.POST.get('categories')
        c_id = Categories.objects.get(id=categories_id)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        today = date.today()

        # 🔒 Validation 1: start <= end
        if start_date and end_date:
            if date.fromisoformat(start_date) > date.fromisoformat(end_date):
                messages.error(request, "Start date cannot be after end date.")
                return redirect('add_diary')

        # 🔒 Validation 2: end date <= today
        if end_date:
            if date.fromisoformat(end_date) > today:
                messages.error(request, "End date cannot be greater than today.")
                return redirect('add_diary')

        # ✅ Save only if validation passes
        TravelDiary.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            location=request.POST.get('location'),
            start_date=start_date,
            end_date=end_date or None,
            categories=c_id,
            description=request.POST.get('description'),
            highlights=request.POST.get('highlights'),
            cover_photo=request.FILES.get('cover_photo')
        )

        messages.success(request, "Travel memory saved successfully!")
        return redirect('trip')

    return render(request, 'Dashboard/add_content/add_diary.html',{'types':types})



@login_required
def diary_detail(request, id):
    diary = get_object_or_404(TravelDiary, id=id, user=request.user)
    return render(request, 'Dashboard/display_pages/diary_view.html', {'diary': diary})




@login_required
def edit_diary(request, id):
    diary = get_object_or_404(TravelDiary, id=id, user=request.user)
    types = Categories.objects.all()

    if request.method == "POST":
        categories_id = request.POST.get('categories')
        c_id = Categories.objects.get(id=categories_id)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        today = date.today()

        # 🔒 Validation 1: start <= end
        if start_date and end_date:
            if date.fromisoformat(start_date) > date.fromisoformat(end_date):
                messages.error(request, "Start date cannot be after end date.")
                return redirect('edit_diary', id=id)

        # 🔒 Validation 2: end date <= today
        if end_date:
            if date.fromisoformat(end_date) > today:
                messages.error(request, "End date cannot be greater than today.")
                return redirect('edit_diary', id=id)

        # ✅ Update fields
        diary.title = request.POST.get('title')
        diary.location = request.POST.get('location')
        diary.start_date = start_date
        diary.end_date = end_date or None
        diary.categories = c_id
        diary.description = request.POST.get('description')
        diary.highlights = request.POST.get('highlights')

        if request.FILES.get('cover_photo'):
            diary.cover_photo = request.FILES.get('cover_photo')

        diary.save()

        messages.success(request, "Travel memory updated successfully!")
        return redirect('diary_detail', id=diary.id)

    return render(request, 'Dashboard/display_pages/edit_diary_view.html', {
        'diary': diary,
        'types':types
    })

@login_required
def delete_diary(request, id):
    diary = get_object_or_404(TravelDiary, id=id, user=request.user)
    diary.delete()
    messages.success(request, "Travel memory deleted successfully!")
    return redirect('trip')



@login_required
def plan_trip(request):
    types = Categories.objects.all()
    if request.method == "POST":
        categories_id = request.POST.get('categories')
        c_id = Categories.objects.get(id=categories_id)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        today = date.today()

        # 🔒 Validation 1: start <= end
        if start_date and end_date:
            if date.fromisoformat(start_date) > date.fromisoformat(end_date):
                messages.error(request, "Start date cannot be after end date.")
                return redirect('plan_trip')

        # 🔒 Validation 2: end date <= today
        if start_date:
            if date.fromisoformat(start_date) < today:
                messages.error(request, "Start date Must be greater than today.")
                return redirect('plan_trip')
            
        if end_date:
            if date.fromisoformat(end_date) < today:
                messages.error(request, "End date cannot be greater than today.")
                return redirect('plan_trip')

        # ✅ Save only if validation passes
        Plan_trip.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            location=request.POST.get('location'),
            start_date=start_date,
            end_date=end_date or None,
            categories=c_id,
            description=request.POST.get('description'),
            highlights=request.POST.get('highlights'),
            cover_photo=request.FILES.get('cover_photo')
        )
        

        messages.success(request, "Travel memory saved successfully!")
        return redirect('trip')

    return render(request, 'Dashboard/add_content/plan_trip.html',{'types':types})

@login_required
def edit_plantrip(request, id):
    plan_trip = get_object_or_404(Plan_trip, id=id, user=request.user)
    today = date.today()
    types = Categories.objects.all()

    if request.method == "POST":
        categories_id = request.POST.get('categories')
        c_id = Categories.objects.get(id=categories_id)
        print(c_id)
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert strings → date
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None

        # 🔒 Validation 1: start date must be today or future
        if start_date and start_date < today:
            messages.error(request, "Start date must be today or a future date.")
            return redirect('edit_plantrip', id=id)

        # 🔒 Validation 2: end date >= start date
        if start_date and end_date and start_date > end_date:
            messages.error(request, "End date cannot be before start date.")
            return redirect('edit_plantrip', id=id)

        # 🔒 Validation 3: end date must be today or future
        if end_date and end_date < today:
            messages.error(request, "End date must be today or a future date.")
            return redirect('edit_plantrip', id=id)

        # ✅ Update fields (NO commas!)
        plan_trip.title = request.POST.get('title')
        plan_trip.location = request.POST.get('location')
        plan_trip.start_date = start_date
        plan_trip.end_date = end_date
        plan_trip.categories = c_id
        plan_trip.description = request.POST.get('description')
        plan_trip.highlights = request.POST.get('highlights')

        if request.FILES.get('cover_photo'):
            plan_trip.cover_photo = request.FILES.get('cover_photo')

        plan_trip.save()

        messages.success(request, "Plan trip updated successfully!")
        return redirect('trip')

    return render(
        request,
        'Dashboard/display_pages/edit_plan_trip.html',
        {'plan_trip': plan_trip,
         'types':types}
    )




@login_required
def delete_plan_trip(request, id):
        plan_trip = get_object_or_404(Plan_trip,id=id,user=request.user)
        plan_trip.delete()
        messages.success(request, "Plan trip deleted successfully!")
        return redirect('trip')



@login_required
def Blogs(request):
    bloglist = blogs.objects.filter(user=request.user)
    types = Categories.objects.all()

    category_id = request.GET.get('categories')

    if category_id:
        try:
            category = Categories.objects.get(id=category_id)
            bloglist = bloglist.filter(categories=category)
        except Categories.DoesNotExist:
            pass

    return render(request, 'Dashboard/display_pages/blogs.html', {
        'bloglist': bloglist,
        'types': types,
        'category_id': int(category_id) if category_id else None
    })



@login_required
def create_blog(request):
    types = Categories.objects.all()
    if request.method == "POST":
        category_id = request.POST.get('categories')

        if not category_id:
            messages.error(request, "Please select a category")
            return redirect('create_blog')

        category = get_object_or_404(Categories, id=category_id)

        blogs.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            about=request.POST.get('about'),
            body=request.POST.get('body'),
            categories=category
        )

        messages.success(request, 'Blog Added Successfully')
        return redirect('blogs')
    return render(request, 'Dashboard/add_content/add_blog.html',
                  {
                      'types':types,
                  }
                  )

@login_required
def blog_details(request, id):
    blog = get_object_or_404(blogs, id=id, user=request.user)
    return render(request, 'Dashboard/display_pages/blog_view.html', {'blog': blog})

@login_required
def delete_blog(request, id):
    blog = get_object_or_404(blogs, id=id, user=request.user)
    blog.delete()
    messages.success(request, "Blog deleted successfully!")
    return redirect('blogs')



@login_required
def gallery(request):
    gallery_list = gallary.objects.filter(user=request.user)
    trip_list = TravelDiary.objects.filter(user=request.user)

    check_id = request.GET.get('categories')

    if check_id:
        check_id = int(check_id)   # 🔥 FIX
        gallery_list = gallary.objects.filter(
            user=request.user,
            name_id=check_id       # assuming FK to TravelDiary
        )

    return render(
        request,
        'Dashboard/display_pages/gallery_view.html',
        {
            'gallery_list': gallery_list,
            'check_id': check_id,
            'trip_list': trip_list
        }
    )


@login_required
def upload_photo(request):
    diary=TravelDiary.objects.filter(user=request.user)
    if request.method == "POST":
        check_id = request.POST.get('name')
        diary_id = TravelDiary.objects.get(id=check_id)
        gallary.objects.create(
            user=request.user,
            name=diary_id,
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        messages.success(request, 'Photo Uploaded Successfully')
        return redirect('gallery')


    return render(request, 'Dashboard/add_content/upload_photo.html',{'diary':diary})

@login_required
def delete_photo(request,id):
    photo = get_object_or_404(gallary,id=id,user=request.user)
    photo.delete()
    messages.success(request, "Photo deleted successfully!")
    return redirect('gallery')
    
@login_required
def journey(request):
    trips = TravelDiary.objects.filter(
        user=request.user
    ).order_by('-end_date')

    return render(request, 'Dashboard/journey.html', {'trips': trips})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        user = User.objects.get(username=request.user.username)

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New password and confirmed password do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        elif current_password == new_password:
            messages.error(request, 'New password cannot be the same as the old password.')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')

    return render(request,'Dashboard/change_password.html')



@login_required
def Userlogout(request):
    logout(request)
    return redirect('userlogin')
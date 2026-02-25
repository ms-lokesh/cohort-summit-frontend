"""
HTTP endpoint to create production users
Can be called via POST request to initialize the database
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile


@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_production_users_endpoint(request):
    """
    Create default production users via HTTP endpoint
    Security: Uses a setup key to prevent unauthorized access
    """
    # Get setup key from POST or GET params
    setup_key = request.POST.get('setup_key') or request.GET.get('setup_key', '')
    
    # Security check
    if setup_key != 'cohort_setup_2024':
        return JsonResponse({
            'error': 'Invalid or missing setup_key',
            'hint': 'Add ?setup_key=cohort_setup_2024 to the URL'
        }, status=403)
    
    results = {
        'created': [],
        'updated': [],
        'errors': []
    }
    
    # Define production users
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@cohortsummit.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_superuser': True,
            'is_staff': True,
            'role': 'ADMIN'
        },
        {
            'username': 'student',
            'email': 'student@cohortsummit.com',
            'password': 'student123',
            'first_name': 'Test',
            'last_name': 'Student',
            'role': 'STUDENT'
        },
        {
            'username': 'mentor',
            'email': 'mentor@cohortsummit.com',
            'password': 'mentor123',
            'first_name': 'Test',
            'last_name': 'Mentor',
            'role': 'MENTOR'
        },
        {
            'username': 'floorwing',
            'email': 'floorwing@cohortsummit.com',
            'password': 'floorwing123',
            'first_name': 'Floor',
            'last_name': 'Wing',
            'role': 'FLOOR_WING'
        }
    ]
    
    for user_data in users_data:
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        role = user_data.pop('role')
        
        try:
            # Check if user exists
            user = User.objects.filter(username=username).first()
            
            if user:
                # Update existing user
                user.email = email
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.is_superuser = user_data.get('is_superuser', False)
                user.is_staff = user_data.get('is_staff', False)
                user.set_password(password)
                user.save()
                results['updated'].append(f"{username} ({email})")
            else:
                # Create new user
                is_superuser = user_data.get('is_superuser', False)
                is_staff = user_data.get('is_staff', False)
                
                if is_superuser:
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name']
                    )
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=is_staff
                    )
                results['created'].append(f"{username} ({email})")
            
            # Create or update profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.campus = 'TECH'
            profile.floor = 2
            profile.save()
            
        except Exception as e:
            results['errors'].append(f"Error creating {username}: {str(e)}")
    
    return JsonResponse({
        'success': True,
        'results': results,
        'message': 'Production users created/updated successfully',
        'credentials': [
            {'email': 'admin@cohortsummit.com', 'password': 'admin123'},
            {'email': 'student@cohortsummit.com', 'password': 'student123'},
            {'email': 'mentor@cohortsummit.com', 'password': 'mentor123'},
            {'email': 'floorwing@cohortsummit.com', 'password': 'floorwing123'}
        ]
    })

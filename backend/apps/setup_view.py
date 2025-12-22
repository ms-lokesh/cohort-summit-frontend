"""
Simple setup endpoint to initialize database with users
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import csv
import os

@csrf_exempt
@require_http_methods(["POST"])
def setup_database(request):
    """
    One-time setup endpoint to create admin and import users
    Add a simple auth check for security
    """
    # Simple security check - only allow if no users exist or if secret key provided
    setup_key = request.POST.get('setup_key', '')
    
    if User.objects.count() > 0 and setup_key != 'cohort_setup_2024':
        return JsonResponse({'error': 'Database already initialized or invalid setup key'}, status=403)
    
    results = {
        'admin_created': False,
        'students_created': 0,
        'students_updated': 0,
        'errors': []
    }
    
    # Create admin user
    admin_email = "admin@test.com"
    try:
        if not User.objects.filter(email=admin_email).exists():
            admin = User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            results['admin_created'] = True
        else:
            admin = User.objects.get(email=admin_email)
            admin.set_password('admin123')
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            results['admin_updated'] = True
    except Exception as e:
        results['errors'].append(f'Admin creation error: {str(e)}')
    
    # Import CSV users
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dummy users - Sheet1.csv')
    
    if not os.path.exists(csv_path):
        results['errors'].append(f'CSV not found at: {csv_path}')
        return JsonResponse(results)
    
    campus = 'TECH'
    floor = 2
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    email = row['email'].strip()
                    username = row['username'].strip()
                    
                    user, is_new = User.objects.get_or_create(
                        email=email,
                        defaults={
                            'username': username,
                            'first_name': username.split()[0] if username else '',
                            'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''
                        }
                    )
                    
                    user.set_password('pass123#')
                    user.save()
                    
                    profile, _ = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={'role': 'STUDENT', 'campus': campus, 'floor': floor}
                    )
                    profile.role = 'STUDENT'
                    profile.campus = campus
                    profile.floor = floor
                    profile.save()
                    
                    if is_new:
                        results['students_created'] += 1
                    else:
                        results['students_updated'] += 1
                        
                except Exception as e:
                    results['errors'].append(f'Error with {email}: {str(e)}')
                    
    except Exception as e:
        results['errors'].append(f'CSV reading error: {str(e)}')
    
    results['success'] = True
    results['total_users'] = User.objects.count()
    
    return JsonResponse(results)

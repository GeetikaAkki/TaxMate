import logging
import json
from django.http import JsonResponse
from .models import User
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        logger.info("Received create user request")

        data = json.loads(request.body)
        logger.info(f"Parsed data: {data}")

        # Required fields validation
        required_fields = ['first_name', 'last_name', 'email', 'password', 
                           'contact_number', 'address']

        for field in required_fields:
            if field not in data:
                logger.error(f"Missing field: {field}")
                return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

       
        if User.objects.filter(email=data['email']).exists():
            logger.error("Email already registered")
            return JsonResponse({'status': 'error', 'message': 'Email already registered'}, status=400)

       
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            contact_number=data['contact_number'],
            address=data['address'],
            filing_status=data.get('filing_status'),
            pan_id=data.get('pan_id'),
            tax_id=data.get('tax_id'),
            preferred_language=data.get('preferred_language', 'en')
        )

        # Set password
        user.set_password(data['password'])

        # Save user
        user.save()
        logger.info(f"User {user.email} created successfully")

        return JsonResponse({'status': 'success', 'message': 'User created successfully', 'user_id': user.user_id}, status=201)

    except json.JSONDecodeError:
        logger.error("Invalid JSON format")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except Exception as e:
        logger.exception("Internal server error")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
@csrf_exempt
@require_http_methods(["GET"])
def get_all_users(request):
    try:
        logger.info("Fetching all users")
        users = User.objects.all().values('user_id', 'first_name', 'last_name', 'email', 'contact_number', 'address', 'filing_status', 'preferred_language')
        return JsonResponse({'status': 'success', 'users': list(users)}, status=200)
    except Exception as e:
        logger.exception("Internal server error")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, user_id):
    try:
        logger.info(f"Received update request for user {user_id}")
        data = json.loads(request.body)
        logger.info(f"Parsed data: {data}")

        user = User.objects.get(user_id=user_id)

        restricted_fields = ['user_id', 'pan_id', 'tax_id', 'password']
        for field, value in data.items():
            if field in restricted_fields:
                logger.error(f"Attempt to update restricted field: {field}")
                return JsonResponse({'status': 'error', 'message': f'Cannot update {field}'}, status=400)
            setattr(user, field, value)

        user.save()
        logger.info(f"User {user_id} updated successfully")
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'})
    
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON format")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except ObjectDoesNotExist:
        logger.error("User not found")
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        logger.exception("Internal server error")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        logger.info(f"Received delete request for user {user_id}")
        user = User.objects.get(user_id=user_id)
        user.delete()
        logger.info(f"User {user_id} deleted successfully")
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
    except ObjectDoesNotExist:
        logger.error("User not found")
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        logger.exception("Internal server error")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

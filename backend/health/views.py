
from django.http import JsonResponse
from django.db import connection, DatabaseError
from django.views.decorators.http import require_GET


@require_GET
def liveness_check(request):
    return JsonResponse({
        "status": "alive",
        "message": "Pharmacy API is running"
    })


@require_GET
def readiness_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse({
            "status": "ready",
            "database": "connected",
            "message": "Pharmacy API is ready to accept requests"
        })

    except DatabaseError:
        return JsonResponse({
            "status": "not_ready",
            "database": "disconnected",
            "message": "Database connection failed"
        }, status=503)

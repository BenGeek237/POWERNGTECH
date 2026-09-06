import os
import django
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()

try:
    c = Client(SERVER_NAME="powerngtech.onrender.com")
    # Log in
    login_success = c.login(email="admin@powerngtech.com", password="Admin@PowerNG2026!")
    print(f"Login success: {login_success}")
    
    # Fetch admin page
    response = c.get("/admin/")
    print(f"Admin page status: {response.status_code}")
    if response.status_code >= 400:
        print(response.content.decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()

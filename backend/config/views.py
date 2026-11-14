
from django.http import HttpResponse


def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pharmacy Management Platform</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
            }
            .container {
                max-width: 850px;
                margin: 90px auto;
                padding: 35px;
                text-align: center;
                background: white;
                border-radius: 14px;
                box-shadow: 0 5px 25px #00000012;
            }
            h1 { color: #0f766e; }
            .status {
                display: inline-block;
                padding: 10px 18px;
                background: #dcfce7;
                color: #166534;
                border-radius: 20px;
                font-weight: bold;
            }
            .links { margin-top: 30px; }
            a {
                display: inline-block;
                margin: 8px;
                padding: 12px 18px;
                background: #0f766e;
                color: white;
                text-decoration: none;
                border-radius: 7px;
            }
            a:hover { background: #115e59; }
            footer {
                margin-top: 35px;
                color: #64748b;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Pharmacy Management Platform</h1>
            <p>Manage medicines, batches and pharmacy inventory efficiently.</p>

            <p class="status">API Service is Running</p>

            <div class="links">
                <a href="/api/health/">Health Check</a>
                <a href="/api/health/live/">Liveness Check</a>
                <a href="/api/health/ready/">Readiness Check</a>
                <a href="/admin/">Admin Panel</a>
            </div>

            <footer>
                Pharmacy Management Platform | Powered by Django REST Framework
            </footer>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

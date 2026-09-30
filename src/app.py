import os
from create_app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1']
    print(f"Starting CollabSphere Clean Architecture API on port {port}...")
    print(f"Swagger Documentation available at http://localhost:{port}/docs")
    app.run(host='0.0.0.0', port=port, debug=debug)
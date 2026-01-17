"""
Application entry point.
Run this file to start the Flask development server.
"""
from __init__ import create_app
import os

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("\n" + "="*60)
    print("TradeSense Backend Server Starting...")
    print("="*60)
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug Mode: {debug}")
    print("="*60 + "\n")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug  # Auto-reload on code changes in development
    )

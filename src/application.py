try:
    from src.server import create_app
except:
    from server import create_app

application = create_app()
application.debug = True

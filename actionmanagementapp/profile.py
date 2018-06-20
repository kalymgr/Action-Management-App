"""
This script is used for profiling the application
"""
from actionmanagementapp import create_app
from actionmanagementapp.utilities import database_setup
from werkzeug.contrib.profiler import ProfilerMiddleware

if __name__ == '__main__':
    database_setup  # I put that here. Maybe I do it in a different way
    app = create_app()
    app.secret_key = 'super_secret_key'  # TODO: change the secret key before production
    app.debug = True
    app.env = 'development'  # this must be changed to production, before deployment

    # setup profiling
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                      restrictions=[10])  # restrictions parameters sets the number of functions to show

    app.run(host='127.0.0.1', port=5000)  # initially the address was 0.0.0.0
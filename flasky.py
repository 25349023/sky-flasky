import os
import sys
import click
from app import create_app, db
from app.models import User, Role, Permission, Post, Follow
from flask_migrate import Migrate, upgrade
from werkzeug.serving import run_simple


COV = None
if os.getenv('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
migrate = Migrate(app, db)

app.logger.warning(f'starting at {os.getenv("PORT")}')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    print(f'exec: {sys.executable}')
    print(f'argv: {sys.argv}')
    if coverage and not os.getenv('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print(f'HTML version: file://{covdir}/index.html')
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    run_simple('127.0.0.1', 5000, app)  # app.run(debug=False)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()

    Role.insert_roles()
    User.add_self_follows()


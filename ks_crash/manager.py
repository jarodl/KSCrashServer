from __future__ import absolute_import
from flask.ext.script import Manager

from ks_crash import create_app

app = create_app()
manager = Manager(app)
install_celery_commands(manager)

if __name__ == "__main__":
    manager.run()

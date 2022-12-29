import os.path

from flask import current_app, Flask

from .__bp__ import bp


@bp.route('/css/<path:res_path>/<name>.css', methods=['GET'], defaults={'directory': 'css', 'extension': 'css'})
@bp.route('/js/<path:res_path>/<name>.js', methods=['GET'], defaults={'directory': 'js', 'extension': 'js'})
@bp.route('/assets/<path:res_path>/<name>.<extension>', methods=['GET'], defaults={'directory': 'assets'})
@bp.route('/css/<name>.css', methods=['GET'], defaults={'directory': 'css', 'extension': 'css'})
@bp.route('/js/<name>.js', methods=['GET'], defaults={'directory': 'js', 'extension': 'js'})
@bp.route('/assets/<name>.<extension>', methods=['GET'], defaults={'directory': 'assets'})
def send_static_resources(name: str, directory: str, extension: str, res_path: str = None):
    app: Flask = current_app

    if res_path:
        file_path = os.path.join(directory, res_path, f'{name}.{extension}')
    else:
        file_path = os.path.join(directory, f'{name}.{extension}')

    return app.send_static_file(file_path)

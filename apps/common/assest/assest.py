from flask_assets import Bundle

bundles = {}

bundles['login_css'] = Bundle(
    'css/user/body.css',
    output='css/user/body.min.css',
    filters='cssmin'
)
bundles['common_css'] = Bundle(
    'css/adminlte/adminlte.css',
    'css/bootstrap/bootstrap.css',
    'css/icheck/square/blue.css',
    output='css/common.css',
    filters='cssmin'
)

bundles['common_js'] = Bundle(
    'js/jquery/jquery-2.2.3.min.js',
    'js/bootstrap/bootstrap.js',
    'js/icheck/icheck.js',
    output='js/common.js',
    filters='jsmin'
)

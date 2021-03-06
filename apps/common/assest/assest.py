from flask_assets import Bundle

"""
压缩资源使用
"""

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
    'css/app/skins/_all-skins.css',
    'css/fontawesome/font-awesome.css',
    'css/ionicons/ionicons.css',
    output='css/common.css',
    filters='cssmin'
)

bundles['common_js'] = Bundle(
    'js/jquery/jquery-2.2.3.min.js',
    'js/bootstrap/bootstrap.js',
    'js/icheck/icheck.js',
    'js/template/app.min.js',
    output='js/common.js',
    filters='jsmin'
)

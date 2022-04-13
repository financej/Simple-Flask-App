from os.path import dirname, join
from flask import Flask, render_template

from . import db, blog


app = Flask(__name__)
# extension 및 help 라이브러리에서 사용하는 일부 구성 정보를 지정하기 위해서 사용
# Flask 앱에서 공유할 수 있는 구성 데이터 및 설정을 정의
# OIDC_CLIENT_SECRETS : OpenID Connect 구성 파일이 있는 위치를 Flask-OIDC 에 알려줌
# OIDC_CLIENT_SECURE : SSL 을 사용하지 않고 개발 중인 사용자 로그인 및 등록을 테스트 할 수 있음
#                      (사이트를 공개적으로 이용하려는 경우 이 옵션을 제거)
# OIDC_CALLBACK_ROUTE : Flask-OID C에 사이트의 어떤 URL 이 사용자 로그인을 처리할지 알려줌
# OIDC_SCOPES : Flask-OIDC 에 사용자가 로그인할 때 사용자에 대해 요청할 데이터를 알려줌
#               (여기서는 기본 사용자의 정보(이메일, 이름 등)을 요청함)
# SECRET_KEY : Flask 세션(쿠키)을 조작할 수 없도록 보호하는데 사용(노출되어서는 안됨)

app.config.from_mapping(
    SECRET_KEY='LONG_RANDOM_STRING',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI="sqlite:///" + join(dirname(dirname(__file__)), "database.sqlite"),
)

db.init_app(app)

app.register_blueprint(blog.bp)


@app.errorhandler(404)
def page_not_found():
    """Render a 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(403)
def insufficient_permissions():
    """Render a 403 page."""
    return render_template("403.html"), 403

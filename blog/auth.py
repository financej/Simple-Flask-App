from flask import Blueprint, redirect, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient


# Blueprint 는 코드를 모듈화해서 대규모 시스템에서 재사용할 수 있도록 하는 방법
# 각 Blueprint 에는 이름, URL 접두사, 자체 미니 애플리케이션 객체가 있다.
# okta_client 는 Okta API 와 연동하여 사용자 데이터를 검색할 수 있습니다.
#             (반드시 필요한 것은 아니지만 더 쉽게 작업할 수 있게 해준다.)
bp = Blueprint("auth", __name__, url_prefix="/")
oidc = OpenIDConnect()
okta_client = UsersClient("https://dev-23532132-admin.okta.com/admin/dashboard", "00Tfbjp2jBbo7GCgX5d6")


@bp.route("/login")
@oidc.require_login
def login():
    """
    Force the user to login, then redirect them to the dashboard.
    """
    return redirect(url_for("blog.dashboard"))


@bp.route("/logout")
def logout():
    """
    Log the user out of their account.
    """
    oidc.logout()
    return redirect(url_for("blog.index"))

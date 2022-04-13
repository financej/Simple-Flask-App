from datetime import datetime

from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

# CLI (Command Line Interface) : 가상 커미널 또는 터미널을 통해 사용자와 컴퓨터가 상호 작용하는 방식
# click library : 파이선으로 간단하게 CLI 도구를 만들 수 있게 도와주는 라이브러리

# SQLAlchemy 셋팅
# db 라는 전역 Object 생성 - 후에 DB 만들때 사용할 예정
# Flask-SQLAlchemy 초기화 - 아직 다른 셋팅은 하지 않은 상태
db = SQLAlchemy()


# SQLAlchemy 에게 어떤 종류의 데이터를 저장하고 어떤 필드를 포함하지 알려주는 데이터베이스 모델 정의
class Post(db.Model):
    """A blog post."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False)


@command("init-db")
@with_appcontext
# FLASK_APP=blog flask init-db 커맨드로 init_db_command 를 실행시킬 예정
def init_db_command():
    """Database 초기화"""
    # create_all 은 데이터베이스 테이블과 환경을 초기화한다.
    db.create_all()
    echo("Initialized the database")


# 메인 어플리케이션 초기화 코드에서 실행하기 위한 것
# init_db_command 함수를 올바른 방식으로 앱에 연결시켜준다
def init_app(app):
    """Flask app 초기화"""
    db.init_app(app)
    app.cli.add_command(init_db_command)

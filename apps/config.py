from pathlib import Path

basedir = Path(__file__).parent.parent

class BaseConfig():
    SECRET_KEY = "2azsmSS3P5qpBCy2HbSj"
    UPLOAD_FOLDER = str(Path(basedir, "apps", "uploads"))
    
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
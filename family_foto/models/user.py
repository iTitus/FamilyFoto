from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from family_foto.models import db
from family_foto.models.user_settings import UserSettings


class User(UserMixin, db.Model):
    """
    Database entity of an user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    settings = relationship('UserSettings', foreign_keys='UserSettings.user_id',
                            back_populates='user', uselist=False)
    photos = relationship('Photo')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """
        Sets the password of an user.
        :param password: The new plain text password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        :param password: the plain text password typed in by the user
        :return: boolean if the hash code does match
        """
        return check_password_hash(self.password_hash, password)

    def get_photos(self):
        """
        Gets all photos from this user.
        :return: List of photo objects.
        """
        return User.query.filter_by(id=self.id).first().photos

    def share_all_with(self, other_user):
        settings: UserSettings = UserSettings.query.get(self.id)
        if not settings:
            raise AttributeError(f'There are no user settings for the user with the id: {self.id}')
        settings.share_all_photos_with(other_user)

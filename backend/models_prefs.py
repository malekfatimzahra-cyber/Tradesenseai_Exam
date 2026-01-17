
class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    language = db.Column(db.String(10), default='en')
    theme = db.Column(db.String(20), default='dark')
    timezone = db.Column(db.String(50), default='UTC')
    currency = db.Column(db.String(10), default='USD')
    notifications_enabled = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'language': self.language,
            'theme': self.theme,
            'timezone': self.timezone,
            'currency': self.currency,
            'notifications_enabled': self.notifications_enabled
        }

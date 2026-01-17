
class ChallengePlan(db.Model):
    __tablename__ = 'challenge_plans'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capital = db.Column(db.Integer, nullable=False)
    profit_target = db.Column(db.Integer, nullable=False)
    max_drawdown = db.Column(db.Integer, nullable=False)
    daily_loss_limit = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default='MAD')
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capital': self.capital,
            'profitTarget': self.profit_target,
            'maxDrawdown': self.max_drawdown,
            'dailyLossLimit': self.daily_loss_limit,
            'price': self.price,
            'currency': self.currency,
            'description': self.description
        }

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

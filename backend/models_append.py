
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

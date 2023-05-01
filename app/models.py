from app import db

class Dashboard(db.Model):
    __tablename__ = "dashboard"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False,unique=True)
    sections = db.relationship("Section", backref="dashboard", lazy = True)    


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    components = db.relationship("Component", backref="section", lazy = True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboard.id"))


class Component(db.Model):
    __tablename__ = "component"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)
    component_id = db.Column(db.Integer, db.ForeignKey("component.id"))
    sub_components = db.relationship('Component', backref=db.backref('component', remote_side=[id]))


class MarketPrice(db.Model):
    __tablename__ = "market_price"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Trades(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
    buy_volume = db.Column(db.Float, nullable=False)
    sell_volume = db.Column(db.Float, nullable=False)
    buy_value = db.Column(db.Float, nullable=False)
    sell_value = db.Column(db.Float, nullable=False)

# Views
class CalculatedTrades(db.Model):
    __tablename__ = "calculated_trades_view"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
    balance_value = db.Column(db.Float, nullable=False)
    balance_volume = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)


class CalculatedMarketTrades(db.Model):
    __tablename__ = "calculated_market_trades_view"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
    buy_price_spread = db.Column(db.Float, nullable=False)
    sell_price_spread = db.Column(db.Float, nullable=False)




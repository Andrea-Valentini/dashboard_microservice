import pytest
from config import Settings
from app import create_app
from app.db import db
from app.models import Dashboard, Section, Component


@pytest.fixture
def app():
    app = create_app(
        f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST_NAME}/{Settings.DB_NAME}_test"
    )
    app.debug = True

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield app


@pytest.fixture
def client(app_ctx):
    return app_ctx.test_client()


@pytest.fixture()
def dashboard_id():
    id = "ff6ec1a9-4681-4e8f-98a1-a4c17a0bdf5a"
    dashboard = Dashboard(id=id, name="Sample dashboard")
    db.session.add(dashboard)

    return id


@pytest.fixture()
def dashboard_layout(dashboard_id):
    sections = ["cockpit", "section_1", "section_2"]
    for section in sections:
        section_layout = Section(dashboard_id=dashboard_id, name=section)
        db.session.add(section_layout)

    cockpit = [
        "balance_value-cum-y",
        "sell_value-cum-y",
        "sell_value-cum-m",
        "buy_value-cum-m",
    ]

    for component in cockpit:
        component_object = Component(section_id=1, code=component)
        db.session.add(component_object)

    db.session.add(Component(section_id=2, code="buy_value"))
    db.session.add(Component(section_id=2, code="buy_price-avg-m", component_id=5))
    db.session.add(Component(section_id=2, code="buy_price-lstdff-m", component_id=5))

    db.session.add(Component(section_id=3, code="balance_value"))
    db.session.add(Component(section_id=3, code="balance_value-cum-y", component_id=8))
    db.session.add(
        Component(section_id=3, code="balance_value-lstdff-m", component_id=8)
    )

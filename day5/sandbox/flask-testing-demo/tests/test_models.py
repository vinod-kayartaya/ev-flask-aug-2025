from api.models import Customer
from api.extensions import db

def test_create_customer(app):
    """Test creating and saving a Customer model"""
    with app.app_context():
        customer = Customer(
            name="Vinod",
            city="Bangalore",
            email="vinod@vinod.co",
            phone="9731424784"
        )
        db.session.add(customer)
        db.session.commit()

        saved = Customer.query.filter_by(email="vinod@vinod.co").first()
        assert saved is not None
        assert saved.name == "Vinod"
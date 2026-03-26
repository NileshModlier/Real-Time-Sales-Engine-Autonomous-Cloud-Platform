
from src.producer import generate_event

def test_event_structure():
    evt = generate_event()
    assert "transaction_id" in evt
    assert "product_id" in evt
    assert "timestamp" in evt

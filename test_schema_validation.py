
from schema import sales_event_schema

def test_schema_fields():
    assert len(sales_event_schema.fields) == 8

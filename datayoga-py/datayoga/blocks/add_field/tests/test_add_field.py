from datayoga.blocks.add_field.block import Block


def test_add_field():
    block = Block({"field": "full_name",
                   "language": "jmespath",
                   "expression": "[fname,lname] | join(' ', @)"})
    assert block.run([{"fname": "john", "lname": "doe"}]) == [
        {"fname": "john", "lname": "doe", "full_name": "john doe"}]


def test_add_nested_field():
    block = Block({"field": "name.full_name",
                   "language": "jmespath",
                   "expression": "[name.fname,name.lname] | join(' ', @)"})
    assert block.run([{"name": {"fname": "john", "lname": "doe"}}]) == [
        {"name": {"fname": "john", "lname": "doe", "full_name": "john doe"}}]


def test_add_multiple_fields():
    block = Block({"fields": [{"field": "name.full_name", "language": "jmespath", "expression": "concat([name.fname, ' ', name.lname])"}, {
                  "field": "name.fname_upper", "language": "jmespath", "expression": "upper(name.fname)"}]})
    assert block.run([{"name": {"fname": "john", "lname": "doe"}}]) == [
        {"name": {"fname": "john", "lname": "doe", "full_name": "john doe", "fname_upper": "JOHN"}}]


def test_add_field_with_dot():
    block = Block({"field": "name\.full_name",
                   "language": "jmespath",
                   "expression": "[fname,lname] | join(' ', @)"})
    assert block.run([{"fname": "john", "lname": "doe"}]) == [
        {"fname": "john", "lname": "doe", "name.full_name": "john doe"}]
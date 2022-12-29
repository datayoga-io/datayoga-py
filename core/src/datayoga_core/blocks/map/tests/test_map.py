import pytest
from datayoga_core import result
from datayoga_core.blocks.map.block import Block


@pytest.mark.asyncio
async def test_map_expression_jmespath():
    block = Block(properties={"language": "jmespath",
                              "expression": """{
                        "new_field": `hello`
                   }"""})
    block.init()
    assert await block.run([{"fname": "john", "lname": "doe"}]) == ([
        {"new_field": "hello"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_field_multiple_expressions_jmespath():
    block = Block(properties={"language": "jmespath",
                              "expression": """{
                            "new_field": `hello`, "name" : fname
                    }"""})
    block.init()
    assert await block.run([{"fname": "john", "lname": "doe"}]) == ([
        {"new_field": "hello", "name": "john"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_field_nested_expression_jmespath():
    block = Block(properties={"language": "jmespath",
                              "expression": """{
                            "new_field": `hello`, "name" : details.fname
                    }"""})
    block.init()
    assert await block.run([{"details": {"fname": "john", "lname": "doe"}}]) == ([
        {"new_field": "hello", "name": "john"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_field_double_nested_expression_jmespath():
    block = Block(properties={"language": "jmespath",
                              "expression": """{
                            "new_field": `hello`, "name" : details.name.fname
                    }"""})
    block.init()
    assert await block.run([{"details": {"name": {"fname": "john", "lname": "doe"}, "country": "israel"}}]) == ([
        {"new_field": "hello", "name": "john"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_expression_non_quoted_jmespath():
    block = Block(properties={"language": "jmespath",
                              "expression": {
                                  "name": "fname"
                              }})
    block.init()
    assert await block.run([{"fname": "john", "lname": "doe"}]) == ([
        {"name": "john"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_multiple_expressions_non_quoted_jmespath():
    block = Block(properties={"language": "jmespath",
                              "expression": {
                                  "name": "fname", "last name": "lname"
                              }})
    block.init()
    assert await block.run([{"fname": "john", "lname": "doe"}]) == ([
        {"name": "john", "last name": "doe"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_expression_sql():
    block = Block(properties={"language": "sql",
                              "expression": {
                                  "new_field": "fname"
                              }})
    block.init()
    assert await block.run([{"fname": "john", "lname": "doe"}]) == ([
        {"new_field": "john"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_multiple_expressions_sql():
    block = Block(properties={"language": "sql",
                              "expression": {
                                  "name": "fname", "last name": "lname"
                              }})
    block.init()
    assert await block.run([{"fname": "john", "lname": "doe"}]) == ([
        {"name": "john", "last name": "doe"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_double_nested_expression_sql():
    block = Block(properties={"language": "sql",
                              "expression": {
                                  "name": "(`details.name.fname`)"
                              }})
    block.init()
    assert await block.run([{"details": {"name": {"fname": "john", "lname": "doe"}, "country": "israel"}}]) == ([
        {"name": "john"}], [result.SUCCESS]
    )


@pytest.mark.asyncio
async def test_map_nested_expression_sql():
    block = Block(properties={"language": "sql",
                              "expression": {
                                  "name": "(`details.fname`)"
                              }})
    block.init()
    assert await block.run([{"details": {"fname": "john", "lname": "doe"}}]) == ([
        {"name": "john"}], [result.SUCCESS]
    )
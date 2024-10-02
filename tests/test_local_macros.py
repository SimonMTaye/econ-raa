import pytest
from prototype.local_macro import StataMacroExpander

@pytest.fixture(scope="module")
def expander():
    do_file_path = "./tests/sample.do"
    return StataMacroExpander(do_file_path)

def test_simple_macros(expander):
    assert expander.get_macro_values("simple_macro1") == ["This is a simple macro"]
    assert expander.get_macro_values("simple_macro2") == ["42"]

@pytest.mark.parametrize("i", range(1, 6))
def test_forvalues_macro(expander, i):
    assert expander.get_macro_values(f"forvalues_macro{i}") == [f"Value {i}"]

@pytest.mark.parametrize("fruit", ["apple", "banana", "cherry"])
def test_foreach_macros(expander, fruit):
    assert expander.get_macro_values(f"foreach_macro_{fruit}") == [f"This is a {fruit}"]

@pytest.mark.parametrize("i", range(1, 4))
def test_foreach_expanded_macros(expander, i):
    assert expander.get_macro_values(f"foreach_expanded_{i}") == [f"Number {i}"]

def test_nested_macros(expander):
    assert expander.get_macro_values("inner_macro") == ["nested"]
    assert expander.get_macro_values("outer_macro") == ["This is a nested macro"]

def test_conditional_macros(expander):
    conditional_macro1 = expander.get_macro_values("conditional_macro1")
    assert len(conditional_macro1) == 2
    assert any("If $dataset_year < 2000: 20th century" in value for value in conditional_macro1)
    assert any("If not ($dataset_year < 2000): 21st century" in value for value in conditional_macro1)

    conditional_macro2 = expander.get_macro_values("conditional_macro2")
    assert len(conditional_macro2) == 3
    assert any("If $region == \"North\": Cold" in value for value in conditional_macro2)
    assert any("If $region == \"South\": Warm" in value for value in conditional_macro2)
    assert any("If not ($region == \"North\") and not ($region == \"South\"): Moderate" in value for value in conditional_macro2)

@pytest.mark.parametrize("i, expected", [
    (1, ["If 1 == 1: Base: 10"]),
    (2, ["If not (2 == 1): Derived: 20"]),
    (3, ["If not (3 == 1): Derived: 30"])
])
def test_complex_nested_macros(expander, i, expected):
    assert expander.get_macro_values(f"complex_macro{i}") == expected

def test_mixed_macro(expander):
    expected = "The year is $dataset_year and the region is [If $region == \"North\": Cold, If $region == \"South\": Warm, If not ($region == \"North\") and not ($region == \"South\"): Moderate]"
    assert expander.get_macro_values("mixed_macro") == [expected]
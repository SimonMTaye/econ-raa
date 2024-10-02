* Example Stata Do File with Various Macro Types
* Simple macro definitions
local simple_macro1 "This is a simple macro"
local simple_macro2 42

* Forvalues loop
forvalues i = 1/5 {
    local forvalues_macro`i' "Value `i'"
}

* Foreach loop with a list
local item_list "apple banana cherry"
foreach fruit of local item_list {
    local foreach_macro_`fruit' "This is a `fruit'"
}

* Foreach loop with macro expansion
local numbers 1 2 3
foreach num of local numbers {
    local foreach_expanded_`num' "Number `num'"
}

* Nested macro
local inner_macro "nested"
local outer_macro "This is a `inner_macro' macro"

* If-else conditional macros
if $dataset_year < 2000 {
    local conditional_macro1 "20th century"
} 
else {
    local conditional_macro1 "21st century"
}

if $region == "North" {
    local conditional_macro2 "Cold"
}
else if $region == "South" {
    local conditional_macro2 "Warm"
}
else {
    local conditional_macro2 "Moderate"
}

* Complex nested structure
local base_value 10
forvalues j = 1/3 {
    if `j' == 1 {
        local complex_macro`j' "Base: `base_value'"
    }
    else {
        local complex_macro`j' "Derived: `=`base_value' * `j''"
    }
}

* Macro with mixed content
local mixed_macro "The year is $dataset_year and the region is `conditional_macro2'"
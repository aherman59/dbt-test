{% macro generate_table_name(code) -%}
        pci_{{ code | trim }}
{%- endmacro %}
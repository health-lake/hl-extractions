# HEALTHLAKE EXTRACTIONS

## ValidateOperator
    Performs validations under a dataset according to its manifest.
        
### PARAMETERS:
* dataset_file: path to the dataset file
* manifest_file: path to the manifest file
* delimiter: by default columns are delimited using ',' but delimiter can be set to any character
* mode: determines the parsing mode. By default it is PERMISSIVE. Possible values are:
  1. **PERMISSIVE:** _(default)_ tries to parse all lines: nulls are inserted for missing tokens and extra tokens are ignored.
  2. **DROPMALFORMED:** drops lines which have fewer or more tokens than expected or tokens which do not match the schema
  3. **FAILFAST:** aborts with a RuntimeException if encounters any malformed line
               
      ```check out more on: https://github.com/databricks/spark-csv```

* format_output: output format file. It can be either **CSV** _(default)_, **PARQUET** or **JSON**
  

# HEALTHLAKE EXTRACTIONS

## OPERATORS

### S3 Writer Operator
    Writes an extracted file on a S3 bucket.

#### PARAMETERS
* extraction_file: path of the file extracted on your script
* extraction_name: name of the file extracted who will be written
* extraction_source: name of the source related to your extraction
* bucket_name: name of the bucket to write on.
    **Default:** "s3://health-lake-input"

-----

### Validation Operator
    Performs validations under a dataset according to its manifest.
        
#### PARAMETERS:
* dataset_file: path to the dataset file
* manifest_file: path to the manifest file
* delimiter: by default columns are delimited using ',' but delimiter can be set to any character
* mode: determines the parsing mode. By default it is PERMISSIVE. Possible values are:
  1. **PERMISSIVE:** _(default)_ tries to parse all lines: nulls are inserted for missing tokens and extra tokens are ignored.
  2. **DROPMALFORMED:** drops lines which have fewer or more tokens than expected or tokens which do not match the schema
  3. **FAILFAST:** aborts with a RuntimeException if encounters any malformed line
               
      ```check out more on: https://github.com/databricks/spark-csv```

* format_output: output format file. It can be either **CSV** _(default)_, **PARQUET** or **JSON**

## DOCKER

Cleaning up any dead containers that are in the graveyard:

```bash
docker rm -f $(docker ps --all -q -f status=exited)
docker rm -f $(docker ps --all -q -f status=dead)
```

Building extractor docker to run CNAC, SRAG and RCIV (use your AWS keys for now, but don't expose to the outside world neither hard-code them in the source code):

```bash
cd extractors
docker build -t hl-extractions:latest --build-arg AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY> --build-arg AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY> .
```

> **TBD** we need to set these keys either through a sts assume role (which will an output role with credentials that can be used) or using service roles such as IRSA

Running extractor docker to execute extractions on a single run for testing purposes can be done after building successfully (this will turn down the docker machine when the scripts are done executing):

```bash
docker run hl-extractions
```
# HEALTHLAKE EXTRACTIONS
## CONTRIBUTING FLOW    
To add another extraction script the developer must create it under the `modules` folder. And if selenium is necessary to the extraction, the webdriver must be initialized with the ChromeDriver class, which is in the `utils` folder.

After developing the new extraction script, the file `config.json` must be updated, adding a key with the extraction identifier, and the value must contain the script path and the args, if any. 

To test the script, the developer can clone the repository and change the `CMD` in Dockerfile, passing the new script key. For example, if I create another extraction for vaccines data, the key should be something like `VACCINE` and to run the script, the `CMD` must be updated from:
```bash
CMD ["python3", "-u", "extract.py"]
```
to:
```bash
CMD ["python3", "-u", "extract.py", "VACCINE"]
```
Then follow the instructions below, in Docker topic, to build the container and run the extraction.
With everything tested, the developer can proceed with the pull request. After the merge with the master, the CI will be activated and the new extraction script will be loaded to the ECR.

After it, the developer must update the script fargate_dag.py, from the [dags repository](https://github.com/health-lake/hl-dags), with the new extraction.
#
## OPERATORS
#
### Chrome Driver
This class configures and returns a webdriver object from Selenium. You must use it when creating a new webscraping script.
    
Example of implementation:

```python
from utils.chrome_driver import ChromeDriver

webdriver = ChromeDriver.get_driver()
```

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

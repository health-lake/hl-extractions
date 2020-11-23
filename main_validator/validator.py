"""
    -> validar valores em branco
    -> validar se valores estao de acordo com o manifest (ex: se "primary_key" o esperado é int, e ela retorna uma string)
    -> validar os valores padrões dos dados de acordo com o manifest

Formatos permitidos: int, double, string, boolean
Opções: null/not null
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, IntegerType, StructType

class ValidateOperator:
    """
        Class ValidateOperator: performs validations under a dataset
            according to its manifest.
        
        -> PARAMS:
            - dataset: path to the dataset file
            - manifest: path to the manifest file
        
        -> METHODS:
            - check_validations: checa as validações dos dados internos
    """

    def __init__(self, dataset, manifest):
        self.spark = SparkSession.builder.master("local[2]").getOrCreate()
        self.dataset = self.spark.read.option("header", "true").format("csv").load(dataset)
        self.dataset.show()
        self.schema = self._retrieve_schema(manifest)
    
    
    def _retrieve_schema(self, manifest):
        rdd = self.spark.sparkContext.wholeTextFiles(manifest)
        text = rdd.collect()[0][1]
        dict = json.loads(str(text))
        custom_schema = StructType.fromJson(dict)

        return custom_schema

    def check_validations(self):
        print(self.dataset.schema)
        print(self.schema)

def HandlerValidateOperator(dataset='./example.csv', manifest='./manifest.json'):
    validador = ValidateOperator(dataset, manifest).check_validations()

HandlerValidateOperator()
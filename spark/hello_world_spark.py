import findspark
from pyspark.sql import SparkSession

findspark.init()

spark = SparkSession.builder \
         .master("local[*]") \
         .appName("Iniciando com spark") \
         .config("spark.ui.port", "4050") \
         .getOrCreate()

data = [('Zeca','35'), ('Eva', '29')]
colNames = ['Nome', 'Idade']
df = spark.createDataFrame(data, colNames)
df.toPandas()

print(df.toPandas())

# http://localhost:8080/ -> Portal
# http://localhost:4050/jobs/ -> Spark UI

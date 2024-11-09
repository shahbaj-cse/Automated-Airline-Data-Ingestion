import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Airport Dim Table From Redshift
AirportDimTableFromRedshift_node1693406103666 = (
    glueContext.create_dynamic_frame.from_catalog(
        database="airlines-table-catalog",
        table_name="dev_airlines_airports_dim",
        redshift_tmp_dir="s3://temp-s3-data/airport_dim/",
        transformation_ctx="AirportDimTableFromRedshift_node1693406103666",
    )
)

# Script generated for node Daily Flights Data
DailyFlightsData_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="airlines-table-catalog",
    table_name="airlines_dataset_gds",
    transformation_ctx="DailyFlightsData_node1",
)

# Script generated for node Filter
Filter_node1693406120672 = Filter.apply(
    frame=DailyFlightsData_node1,
    f=lambda row: (row["depdelay"] > 60),
    transformation_ctx="Filter_node1693406120672",
)

# Script generated for node Join For Departure
Filter_node1693406120672DF = Filter_node1693406120672.toDF()
AirportDimTableFromRedshift_node1693406103666DF = (
    AirportDimTableFromRedshift_node1693406103666.toDF()
)
JoinForDeparture_node1693406193082 = DynamicFrame.fromDF(
    Filter_node1693406120672DF.join(
        AirportDimTableFromRedshift_node1693406103666DF,
        (
            Filter_node1693406120672DF["originairportid"]
            == AirportDimTableFromRedshift_node1693406103666DF["airport_id"]
        ),
        "left",
    ),
    glueContext,
    "JoinForDeparture_node1693406193082",
)

# Script generated for node Select Fields After Departure
SelectFieldsAfterDeparture_node1693406895894 = SelectFields.apply(
    frame=JoinForDeparture_node1693406193082,
    paths=["carrier", "destairportid", "depdelay", "arrdelay", "city", "name", "state"],
    transformation_ctx="SelectFieldsAfterDeparture_node1693406895894",
)

# Script generated for node Change Schema After Departure
ChangeSchemaAfterDeparture_node1693407094301 = ApplyMapping.apply(
    frame=SelectFieldsAfterDeparture_node1693406895894,
    mappings=[
        ("carrier", "string", "carrier", "string"),
        ("destairportid", "long", "destairportid", "long"),
        ("depdelay", "long", "depdelay", "long"),
        ("arrdelay", "long", "arrdelay", "long"),
        ("city", "string", "dep_city", "string"),
        ("name", "string", "dep_airport", "string"),
        ("state", "string", "dep_state", "string"),
    ],
    transformation_ctx="ChangeSchemaAfterDeparture_node1693407094301",
)

# Script generated for node Join For Arrival
ChangeSchemaAfterDeparture_node1693407094301DF = (
    ChangeSchemaAfterDeparture_node1693407094301.toDF()
)
AirportDimTableFromRedshift_node1693406103666DF = (
    AirportDimTableFromRedshift_node1693406103666.toDF()
)
JoinForArrival_node1693406560504 = DynamicFrame.fromDF(
    ChangeSchemaAfterDeparture_node1693407094301DF.join(
        AirportDimTableFromRedshift_node1693406103666DF,
        (
            ChangeSchemaAfterDeparture_node1693407094301DF["destairportid"]
            == AirportDimTableFromRedshift_node1693406103666DF["airport_id"]
        ),
        "left",
    ),
    glueContext,
    "JoinForArrival_node1693406560504",
)

# Script generated for node Select Fields After Arrival
SelectFieldsAfterArrival_node1693407281200 = SelectFields.apply(
    frame=JoinForArrival_node1693406560504,
    paths=[
        "carrier",
        "depdelay",
        "arrdelay",
        "dep_city",
        "dep_airport",
        "dep_state",
        "airport_id",
        "city",
        "name",
        "state",
    ],
    transformation_ctx="SelectFieldsAfterArrival_node1693407281200",
)

# Script generated for node Change Schema
ChangeSchema_node2 = ApplyMapping.apply(
    frame=SelectFieldsAfterArrival_node1693407281200,
    mappings=[
        ("carrier", "string", "carrier", "varchar"),
        ("depdelay", "long", "dep_delay", "bigint"),
        ("arrdelay", "long", "arr_delay", "bigint"),
        ("dep_city", "string", "dep_city", "varchar"),
        ("dep_airport", "string", "dep_airport", "varchar"),
        ("dep_state", "string", "dep_state", "varchar"),
        ("city", "string", "arr_city", "varchar"),
        ("name", "string", "arr_airport", "varchar"),
        ("state", "string", "arr_state", "varchar"),
    ],
    transformation_ctx="ChangeSchema_node2",
)

# Script generated for node Amazon Redshift
AmazonRedshift_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node2,
    connection_type="redshift",
    connection_options={
        "redshiftTmpDir": "s3://aws-glue-assets-348532040329-us-east-1/temporary/",
        "useConnectionProperties": "true",
        "dbtable": "airlines.daily_flights_fact",
        "connectionName": "redshift-connection",
        "preactions": "CREATE TABLE IF NOT EXISTS airlines.daily_flights_fact (carrier VARCHAR, dep_delay VARCHAR, arr_delay VARCHAR, dep_city VARCHAR, dep_airport VARCHAR, dep_state VARCHAR, arr_city VARCHAR, arr_airport VARCHAR, arr_state VARCHAR);"
    },
    transformation_ctx="AmazonRedshift_node3",
)

job.commit()

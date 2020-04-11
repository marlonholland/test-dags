# """Example DAG demonstrating the usage of the SnowflakeOperator & Hook."""


# import logging
# import airflow
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator

# #Python "plugins" we were talking about
# #When we set up our environment, we added a couple python dependencies such as the snowflake module
# from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
# from airflow.contrib.operators.snowflake_operator import SnowflakeOperator

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# #Defining our default arguments
# args = {
#     'owner': 'Marlon',
#     'start_date': airflow.utils.dates.days_ago(2),
#     'email': ['marlonholland7@gmail.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     #'retries': 1,
#     #'retry_delay': timedelta(minutes=5),
#     # 'queue': 'bash_queue',
#     # 'pool': 'backfill',
#     # 'priority_weight': 10,
#     # 'end_date': datetime(2016, 1, 1),
#     # 'wait_for_downstream': False,
#     # 'dag': dag,
#     # 'sla': timedelta(hours=2),
#     # 'execution_timeout': timedelta(seconds=300),
#     # 'on_failure_callback': some_function,
#     # 'on_success_callback': some_other_function,
#     # 'on_retry_callback': another_function,
#     # 'sla_miss_callback': yet_another_function,
# }

# #Creating our dag object
# dag = DAG(
#     dag_id="azure_to_snowflake_demo", 
#     default_args=args, 
#     schedule_interval=None
# )

# #SQL query being used to create our table in the snowflake storage
# create_query = [
#     """USE WAREHOUSE MY_SAMPLE;""",
#     """USE DATABASE APACHE_AIRFLOW_DEMO;""",
#     """USE SCHEMA PUBLIC;""",
#     """CREATE OR REPLACE TABLE "APACHE_AIRFLOW_DEMO"."PUBLIC"."SUPERSTORE_DEMO" (
#         "Profit Ratio" VARCHAR (100),
#         "Category" VARCHAR (100),
#         "City" VARCHAR (100),
#         "Country" VARCHAR (100),
#         "Customer Name" VARCHAR (100),
#         "Discount" VARCHAR (100), 
#         "Number of Records" VARCHAR (100),
#         "Order Date" VARCHAR (100),
#         "Order ID" VARCHAR (100),
#         "Postal Code" VARCHAR (100),
#         "Manufacturer" VARCHAR (100),
#         "Product Name" VARCHAR (400),
#         "Profit" VARCHAR (100),
#         "Quantity" VARCHAR (100),
#         "Region" VARCHAR (100),
#         "Sales" VARCHAR (100),
#         "Segment" VARCHAR (100),
#         "Ship Date" VARCHAR (100),
#         "Ship Mode" VARCHAR (100),
#         "State" VARCHAR (100),
#         "Sub-Category" VARCHAR (100));"""
# ]

# #SQL query being used to insert data from our Azure storage account into our newly created table
# insert_query = [
#     """USE WAREHOUSE MY_SAMPLE;""",
#     """USE DATABASE APACHE_AIRFLOW_DEMO;""",
#     """USE SCHEMA PUBLIC;""",
#     """COPY INTO SUPERSTORE_DEMO
#     FROM @AZURE_DEMO_STAGE
#     FILES = ('superstore_sample_data.csv')
#     file_format = (format_name = CSV_FILE_FORMAT)
#     FORCE = TRUE;"""
# ]

# #Example use of a Snowflake hook to grab data from Snowflake.
# snowflake_hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")

# #Using snowflake hook in custom python functions
# def check_table(**context):
#     result = snowflake_hook.get_first("SELECT COUNT(*) FROM PUBLIC.SUPERSTORE_DEMO")
#     logging.info("Number of rows in 'SUPERSTORE_DEMO'  - %s", result[0])

# def check_raw(**context):
#     result = snowflake_hook.get_first("SELECT COUNT(*) FROM @AZURE_DEMO_STAGE/superstore_sample_data.csv (FILE_FORMAT => CSV_FILE_FORMAT);")
#     logging.info("Number of rows in raw file  - %s", result[0])


# #Using a with statement to execute cleanup code
# with dag:

#     #Using a snowflake operator to execute a select command on our raw data in Azure
#     check_raw = PythonOperator(
#         task_id = "check_raw",
#         python_callable = check_raw
#     )

#     #Using a snowflake operator to execute our create command in Snowflake
#     create = SnowflakeOperator(
#         task_id = "snowflake_create",
#         sql = create_query,
#         snowflake_conn_id = "snowflake_conn",
#     )

#     #Using a snowflake operator to execute our insert command in Snowflake
#     insert = SnowflakeOperator(
#         task_id = "snowflake_insert",
#         sql = insert_query,
#         snowflake_conn_id = "snowflake_conn",
#     )

#     #Using a python operator to execute a user-defined python function
#     check_table = PythonOperator(
#         task_id = "check_table", 
#         python_callable = check_table
#     )

# #Using python bitwise shift operators to determine the workflow of our dag (the order in which our tasks will executed)
# [check_raw, create] >> insert >> check_table

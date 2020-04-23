import logging
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

args = {
	"owner": "Airflow", 
	"start_date": airflow.utils.dates.days_ago(2)}

dag = DAG(
    dag_id="ntt_snfk_conn", 
	default_args=args, 
	schedule_interval=None
)

create_query = [
    """create table sap.test_table;""", 
]


with dag:
    create = SnowflakeOperator(
        task_id="snowflake_create",
        sql=create_query,
        snowflake_conn_id="ntt_snfk_conn",
    )

   
# create_query 
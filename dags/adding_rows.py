from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(dag_id="adding_rows",description="This dag was made to add rows in our database!",start_date=datetime(2025,5,2),catchup=False,schedule_interval="0 * * * *")

task1 = BashOperator(task_id="add_scrapping",bash_command='python /opt/airflow/database/rows_scrapping.py',dag=dag)
task2 = BashOperator(task_id="add_weather",bash_command='python /opt/airflow/database/rows_table.py',dag=dag)


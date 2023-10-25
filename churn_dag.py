from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
import time
import logging

def get_glue_client(region_name='us-west-1'):
    """
    Establishes a connection and returns an AWS Glue client using boto3 session.
    :param region_name: AWS region name (default is 'us-west-1')
    :return: AWS Glue client object
    """
    session = AwsGenericHook(aws_conn_id='aws_s3_conn')
    boto3_session = session.get_session(region_name=region_name)
    return boto3_session.client('glue')


def glue_job_s3_redshift_transfer(job_name, **kwargs):
    """
    Triggers the specified AWS Glue job.
    :param job_name: Name of the Glue job to trigger
    """
    logging.info(f"Triggering Glue job: {job_name}")
    
    client = get_glue_client()
    client.start_job_run(JobName=job_name)


def get_run_id():
    """
    Fetches and returns the run ID of the Glue job.
    :return: Glue job run ID
    """
    logging.info("Fetching Glue job run ID...")
    
    time.sleep(8)
    client = get_glue_client()
    response = client.get_job_runs(JobName="s3_upload_to_redshift_gluejob")
    job_run_id = response["JobRuns"][0]["Id"]
    logging.info(f"Retrieved Glue job run ID: {job_run_id}")
    
    return job_run_id

# Define default arguments for the Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 24),
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=10)
}

# Define the Airflow DAG and its structure
with DAG('my_dag',
        default_args=default_args,
        schedule_interval='@weekly',
        catchup=False) as dag:

        # Define the task to trigger the Glue job
        glue_job_trigger = PythonOperator(
            task_id='tsk_glue_job_trigger',
            python_callable=glue_job_s3_redshift_transfer,
            op_kwargs={'job_name': 's3_upload_to_redshift_gluejob'}
        )

        # Define the task to fetch the Glue job run ID
        grab_glue_job_run_id = PythonOperator(
            task_id='tsk_grab_glue_job_run_id',
            python_callable=get_run_id
        )

        # Define the task to monitor the completion status of the Glue job
        is_glue_job_finish_running = GlueJobSensor(
            task_id="tsk_is_glue_job_finish_running",
            job_name='s3_upload_to_redshift_gluejob',
            run_id='{{task_instance.xcom_pull("tsk_grab_glue_job_run_id")}}',
            verbose=True,
            aws_conn_id='aws_s3_conn',
            poke_interval=60,
            timeout=3600
        )

        # Set the task dependencies, defining the order in which they should run
        glue_job_trigger >> grab_glue_job_run_id >> is_glue_job_finish_running

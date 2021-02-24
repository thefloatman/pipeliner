import codecs
import logging
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates

logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_dag(dag_id):
    default_args = {
        "owner": "pipeliner",
        "description": (
            "Stream Tweets and publish it to kafka"
        ),
        "depends_on_past": False,
        "start_date": dates.days_ago(1),
        "retries": 1,
        "retry_delay": timedelta(minutes=10),
        "provide_context": True,
    }

    new_dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=timedelta(minutes=10),
    )

    def stream_tweets():
        logger.info('=====Start Tweets Streaming=====')

        return 0

    def publish_to_kafka():
        logger.info('=====Publish to Kafka=====')

        return 0

    with new_dag:
        task1 = PythonOperator(task_id='stream_tweets', python_callable=stream_tweets)
        return new_dag

dag_id = "twitter_streamer"
globals()[dag_id] = create_dag(dag_id)
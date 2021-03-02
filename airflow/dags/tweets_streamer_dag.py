import codecs
import logging
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils import dates
from custom_operators.tweets_streamer_operator import TweetsStreamerOperator

logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_TOPIC = "tweets"

def create_dag(dag_id):
    default_args = {
        "owner": "pipeliner",
        "description": (
            "Stream Tweets and publish it to kafka"
        ),
        "depends_on_past": False,
        "start_date": dates.days_ago(0),
        "retries": 1,
        "retry_delay": timedelta(minutes=60),
        "provide_context": True,
    }

    dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=timedelta(days=1),
    )

    with dag:

        tweets_streaming = TweetsStreamerOperator(
            task_id="listening_tweets",
            kafka_topic=DEFAULT_TOPIC,
            tweets_topic='Jakarta',
            dag=dag
        )

        start = DummyOperator(
            task_id='start',
            dag=dag
        )

        finish = DummyOperator(
            task_id='finish',
            dag=dag
        )

        start >> tweets_streaming >> finish

        return dag

dag_id = "twitter_streamer"
globals()[dag_id] = create_dag(dag_id)
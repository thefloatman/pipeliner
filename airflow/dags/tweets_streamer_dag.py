import codecs
import logging
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates
from custom_operators.tweets_streamer_operator import TweetsStreamerOperator

logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def dummy_callable(action):
    message = f"{datetime.now()}: {action} stream tweets!"
    logger.info(message)

    return message

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

    dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=timedelta(minutes=10),
    )

    with dag:

        start = PythonOperator(
            task_id="starting_pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "starting"},
            dag=dag
        )

        tweets_streaming = TweetsStreamerOperator(
            task_id="listening_tweets",
            topic = 'trump',
            dag=dag
        )

        finish = PythonOperator(
            task_id="finishing_pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "finishing"},
            dag=dag
        )

        start >> tweets_streaming >> finish

        return dag

dag_id = "twitter_streamer"
globals()[dag_id] = create_dag(dag_id)
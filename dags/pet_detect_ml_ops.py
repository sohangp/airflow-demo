import datetime
import pendulum

from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash import BashOperator

from pet_detector.data_ingest import get_pet_detector_training_data
from pet_detector.push_to_s3 import upload_file_to_s3 

# ML Ops DAG, does the below
# 1. Gets the Pet Images from Oxford-IIIT Pet Dataset.
# 2. Train's the model with FastAI, builds the model into a byte stream.
# 3. Runs tests to validate the model.
# 4. Uploads the model to a S3 Bucket (version control)
# 5. Deploys the Application that uses the model. With the new version of the model built.
@dag(
    dag_id="pet_detect_ml_ops",
    schedule_interval='*/1 * * * *',  # Schedule every 10 mins for testing else @daily
    start_date=pendulum.now(),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def PetDetectMLOpp():

    # Gets the Pet Images to train the model
    @task(task_id="Get-Training-Data")
    def get_training_data():
        print("Starting the Get-Training-Data Task.")
        get_pet_detector_training_data()

    # Use FastAI to train the model
    # @task(task_id="Train-Pet-Detection-Model", trigger_rule=TriggerRule.ONE_SUCCESS)
    # def train_model():
    #     print("Starting the Train-Pet-Detection-Model Task.")

    train_model_bash_command = '''
       echo "Starting the Train-Pet-Detection-Model Task."
       python3 /opt/airflow/dags/pet_detector/model_training.py
       echo "Finished the Train-Pet-Detection-Model Task."
    '''
    train_model = BashOperator(
        task_id='Train-Pet-Detection-Model',
        bash_command=train_model_bash_command,
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    # Upload Pickled model file to S3 (version control example)
    @task(task_id="Upload-Model-To-S3", trigger_rule=TriggerRule.ALL_SUCCESS)
    def upload_model():
        print("Starting the Upload-Model-To-S3 Task.")
        endpoint_url = 'http://s3:9090'
        bucket_name = 'models'
        key = 'export.pkl'
        file_path = '/opt/airflow/models/export.pkl'        
        upload_file_to_s3(endpoint_url, bucket_name, key, file_path)

    # Run Sample predictions
    # @task(task_id="Validate-New-Model", trigger_rule=TriggerRule.ALL_SUCCESS)
    # def validate_new_model():
    #     print("Starting the Validate-New-Model Task.")
    #     validate_success()

    validate_new_model_bash_command = '''
       echo "Starting the Validate-New-Model Task."
       python3 /opt/airflow/dags/pet_detector/validate_model.py
       echo "Finished the Validate-New-Model Task."
    '''
    validate_new_model = BashOperator(
        task_id='Validate-New-Model',
        bash_command=validate_new_model_bash_command,
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    # Run Docker commands to mimic deployment to an external application.
    @task(task_id="Deploy-Pet-Detection-Service", trigger_rule=TriggerRule.ALL_SUCCESS)
    def deploy_ml_service():
        print("Starting the Deploy-Pet-Detection-Service Task.")

    # The Flow
    get_training_data() >> train_model >> upload_model() >> validate_new_model >> deploy_ml_service()


pet_ml_ol = PetDetectMLOpp()

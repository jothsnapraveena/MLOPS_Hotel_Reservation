import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *
from utils.common_functions import read_yaml

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\joths\Downloads\dazzling-ego-453401-c9-7c45c117aaf0.json"

logger=get_logger(__name__)
class DataIngestion:
    def __init__(self,config):
        self.config=config["data_ingestion"]
        self.bucket_name=self.config["bucket_name"]
        self.file_name=self.config["bucket_file_name"]
        self.train_test_ratio=self.config["train_ratio"]

        os.makedirs(RAW_DIR,exist_ok=True)
        logger.info(f"Data Ingestion started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client=storage.Client()
            bucket=client.bucket(self.bucket_name)
            blob=bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Downloaded {self.file_name} from {self.bucket_name} successfully")

        except Exception as e:
            logger.error(f"Error occurred while downloading file: {str(e)}")
            raise CustomException(f"Error occurred while downloading file: {str(e)}",error_detail=str(e))
    
    def split_data(self):
        try:
            logger.info("starting the splitting process")
            data=pd.read_csv(RAW_FILE_PATH)

            train_data,test_data=train_test_split(data,test_size=1-self.train_test_ratio,random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH,index=False)
            test_data.to_csv(TEST_FILE_PATH,index=False)
            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Train data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error occurred while splitting data: {str(e)}")
            raise CustomException(f"Error occurred while splitting data: {str(e)}",error_detail=str(e))
        
    def run(self):
        try:
            logger.info("Starting Data Ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data Ingestion completed successfully")
        
        except CustomException as e:

            logger.error(f"Data Ingestion failed due to: {str(e)}")
            raise CustomException(f"Data Ingestion failed due to: {str(e)}",error_detail=str(e))
        finally:
            logger.info("Data Ingestion process completed")
    
if __name__=="__main__":

    data_ingestion=DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()



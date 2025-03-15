from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml 
from config.paths_config import *




if __name__=="__main__":

    ### Data ingestion ###

    data_ingestion=DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    ## Data Processing #####

    processor=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()

    ### Model Training ###

    trainer = ModelTraining(processed_train_data_path,processed_test_data_path,MODEL_OUTPUT_PATH)
    trainer.run()




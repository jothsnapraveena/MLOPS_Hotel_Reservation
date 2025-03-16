import os

####### DATA INGESTION ###########

RAW_DIR="artifacts/raw"
RAW_FILE_PATH=os.path.join(RAW_DIR,"raw.csv")
TRAIN_FILE_PATH=os.path.join(RAW_DIR,"train.csv")
TEST_FILE_PATH=os.path.join(RAW_DIR,"test.csv")

CONFIG_PATH=r"config\config.yaml"

####### DATA PROCESSING ###########

PROCESSED_DIR="artifacts/processed"
processed_train_data_path=os.path.join(PROCESSED_DIR,"processed_train.csv")
processed_test_data_path=os.path.join(PROCESSED_DIR,"processed_test.csv")



####### MODEL TRAINING ###########

MODEL_OUTPUT_PATH="artifacts/models/lgbm_model.pkl"

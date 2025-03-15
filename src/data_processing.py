import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger=get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        
        self.config=read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self,df):
        try:
            logger.info("Starting preprocessing")

            logger.info("Dropping irrelevant columns")
            df.drop(columns=['Booking_ID'] , inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols=self.config['data_processing']['categorical_columns']
            num_cols=self.config['data_processing']['numeric_columns']
            
            logger.info("Label encoding")
            label_encoder = LabelEncoder()
            mappings={}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])

                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
            logger.info("Label Mappings are : ")
            for col,mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            logger.info("Skewness handling:")

            skewness_threshold= self.config['data_processing']['skewness_threshold']
            skewness=df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness>skewness_threshold].index:
                df[column]=np.log1p(df[col])
            return df
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise CustomException("Error in preprocessing",e)
        
    def balance_data(self,df):
        try:
            logger.info("Hanlding Imbalance datae")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            smote = SMOTE(random_state=42)

            X_resampled , y_resampled = smote.fit_resample(X,y)
            balanced_df = pd.DataFrame(X_resampled , columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error in handling imbalance: {str(e)}")
            raise CustomException("Error in handling imbalance", e)
        
    def select_features(self,df):
        try:
            logger.info("Feature selection started")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                        'feature':X.columns,
                        'importance':feature_importance
                            })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select=self.config['data_processing']['no_of_features']
            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values

            logger.info(f"Top 10 features selected are : {top_10_features} ")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Top 10 features selected successfully")

            return top_10_df
        except Exception as e:
            logger.error(f"Error in feature selection: {str(e)}")
            raise CustomException("Error in feature selection",e)
    
    def save_data(self,df,file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
        except Exception as e:
            logger.error(f"Error in saving data: {str(e)}")
            raise CustomException("Error in saving data",e)
        
    def process(self):
        try:
            logger.info("Starting data processing")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df=self.balance_data(train_df)
            test_df=self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df=test_df[train_df.columns]

            self.save_data(train_df,processed_train_data_path)
            self.save_data(test_df,processed_test_data_path)

            logger.info("Data processing completed successfully")


        
        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}")
            raise CustomException("Error in data processing",e)
        

if __name__=="__main__":
    processor=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()

        




            




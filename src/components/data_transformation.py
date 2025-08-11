import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils import save_object
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    """
    Configuration for data transformation preprocessing.

    Attributes:
        preprocessor_obj_file_path (str): Path to save the preprocessing pipeline.
    """
    preprocessor_ob_file_path = os.path.join('artifacts', 'pipeline.pkl')

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        """
        This function is created to handle the data transformation.
        e.g.
         - Handle missing values.
         - Encode Categorical features.
         - Apply Standard Scaling to get all the observations into similar range. (This increase model accruacy)
        """
        try:
            numerical_columns = ['reading_score', 'writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = 'median')),
                    ("scaler", StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean = False))
                ]
            )

            # logging.info("Numerical Columns Standard Scaling Completed.")
            # logging.info("Categorical Columns Encoding Completed.")
            logging.info(f"Categorical Columns: {categorical_columns}")
            logging.info(f"Numerical Columns: {numerical_columns}")

            # To combine the numerical pipeline with the categorical piepline, column transformer will be used.

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_columns),
                    ("categorical_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)        
            
    def initiate_data_transformation(self, train_path, test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train and Test Data Completed.")

            logging.info("Obtaining Preprocessing Object...")            

            preprocessing_object = self.get_data_transformer_object()

            target_column = 'math_score'
            numerical_columns = ['reading_score', 'writing_score']
            
            input_feature_train_df = train_df.drop(columns = target_column, axis = 1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns = target_column, axis = 1)
            target_feature_test_df = test_df[target_column]

            logging.info("Applying the preprocessing object on train dataframe and test dataframe.")

            input_feature_train_array = preprocessing_object.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessing_object.transform(input_feature_test_df)

            train_array = np.c_[
                input_feature_train_array, np.array(target_feature_train_df)
            ]
            
            test_array = np.c_[
                input_feature_test_array, np.array(target_feature_test_df)
            ]

            logging.info("Saved Preprocessing Object")

            save_object(
                file_path = self.data_tranformation_config.preprocessor_ob_file_path,
                obj = preprocessing_object
            )

            return(
                train_array,
                test_array,
                self.data_tranformation_config.preprocessor_ob_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
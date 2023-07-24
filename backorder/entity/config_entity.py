from collections import namedtuple

#we are using named tuple so that it will be in suggestions
DataIngestionConfig=namedtuple("DataIngestionConfig",
["dataset_download_url","tgz_download_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig", ["schema_file_path","report_file_path","report_page_file_path"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["transformed_train_dir",
                                                                   "transformed_test_dir",
                                                                   "preprocessed_object_file_path"]) #pickle object of feature engineering here i.e in preprcessed file path


ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["trained_model_file_path","base_accuracy","model_config_file_path"]) #pickle file for best model performed with some datum accuracy(base accuracy)>

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path","time_stamp"]) #all model in production 


ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])#if your trained model is better than model in production that should be stored in same folder of production

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
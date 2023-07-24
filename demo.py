from backorder.pipeline.pipeline import Pipeline
from backorder.exception import backorderException
from backorder.logger import logging
from backorder.config.configuration import Configuartion
from backorder.component.data_transformation import DataTransformation
import os
import webbrowser
import templates

def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))
        #pipeline.run_pipeline()
        pipeline.start()
        logging.info("main function execution completed.")
        # # data_validation_config = Configuartion().get_data_transformation_config()
        # # print(data_validation_config)
        # schema_file_path=r"D:\Project\machine_learning_project\config\schema.yaml"
        # file_path=r"D:\Project\machine_learning_project\backorder\artifact\data_ingestion\2022-06-27-19-13-17\ingested_data\train\backorder.csv"

        # df= DataTransformation.load_data(file_path=file_path,schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)
        #index_html_path = os.path.join(r"C:\Users\akshay\Desktop\project\final_back_order_prediction\templates\predict.html")  # Replace with the actual path to index.html
        #webbrowser.open(index_html_path)
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()
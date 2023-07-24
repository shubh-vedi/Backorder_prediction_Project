from backorder.entity.config_entity import DataIngestionConfig
import sys,os
import zipfile
from backorder.exception import backorderException
from backorder.logger import logging
from backorder.entity.artifact_entity import DataIngestionArtifact
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import requests
from zipfile import ZipFile
import io
import traceback
import gzip
from numba.core.errors import NumbaDeprecationWarning
from numba.core.errors import NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)


class DataIngestion:
                                                        #from entity
    def __init__(self,data_ingestion_config:DataIngestionConfig ):# this data_ingestion_config:DataIngestionConfig parameter is necessary to intialise object of this class
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise backorderException(e,sys)
    
    
    def download_backorder_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url   

            #folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            
            os.makedirs(tgz_download_dir,exist_ok=True) #if above folder is not available create it and if available then proceed

            backorder_file_name = os.path.basename(download_url) #extract file name of zip file

            tgz_file_path = os.path.join(tgz_download_dir, backorder_file_name)#complete file path

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
             # Send a GET request to download the zip file
            #response = requests.get(download_url,tgz_file_path)    
            urllib.request.urlretrieve(download_url, tgz_file_path) #download file from  url passed and location where to download
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path

        except Exception as e:
            raise backorderException(e,sys) from e
    
        
    """
    def download_backorder_data(self) -> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir, exist_ok=True)

            backorder_file_name = os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir, backorder_file_name)

            logging.info(f"Downloading file from: [{download_url}] into: [{tgz_file_path}]")
            
            # Send a GET request to download the zip file
            response = requests.get(download_url)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Save the downloaded content to the file
                with open(tgz_file_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"File: [{tgz_file_path}] has been downloaded successfully.")
            else:
                raise backorderException(f"Failed to download the file. Status code: {response.status_code}", sys)

            return tgz_file_path

        except Exception as e:
            raise backorderException(e, sys) from e
    
    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            if os.path.exists(tgz_file_path):
                try:
                    
                     if response.status_code == 200:
                       #with zipfile.ZipFile(tgz_file_path , 'r') as zip_file:
                         with ZipFile(io.BytesIO(response.content)) as zip_file:
                           zip_file.extractall(path=raw_data_dir)
            #with tarfile.open(tgz_file_path) as backorder_tgz_file_obj:
                #backorder_tgz_file_obj.extractall(path=raw_data_dir)
                except zipfile.BadZipFile as e:
                # Log the specific error message for BadZipFile
                    logging.error(f"BadZipFile error: {e}")
                # Print the traceback for additional details
                traceback.print_exc()
            else:
               logging.error(f"The tgz_file_path: [{tgz_file_path}] does not exist.")  

            logging.info(f"Extraction completed")

        except Exception as e:
            raise backorderException(e,sys) from e
    """
    def extract_tgz_file(self, tgz_file_path: str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.removee(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            raw_file_path = os.path.join(raw_data_dir , os.path.basename(tgz_file_path).replace(".gz",""))
            if os.path.exists(tgz_file_path):
                with gzip.open(tgz_file_path, 'rb') as f_in:
                    with open(raw_file_path, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                logging.error(f"The tgz_file_path: [{tgz_file_path}] does not exist.")

        except Exception as e:
            raise backorderException(e, sys) from e

    """
    def extract_tgz_file(self, tgz_file_path: str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.rmdir(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f"Extracting zip file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            if os.path.exists(tgz_file_path):
                try:
                    with gzip.open(tgz_file_path,'rb')  as backorder_zip_file_obj:
                        #with open(raw_data_dir,'wb') as f_out:
                           # f_out.write(f_in.read())
                        backorder_zip_file_obj.extractall(path=raw_data_dir)
                   
                    #with zipfile.ZipFile(tgz_file_path, 'r') as backorder_zip_file_obj:
                        #backorder_zip_file_obj.extractall(path=raw_data_dir)
                #except zipfile.BadZipFile as e:
                    # Log the specific error message for BadZipFile
                   # logging.error(f"BadZipFile error: {e}")
                    # Print the traceback for additional details
                    #traceback.print_exc()
                except Exception as e:
                    print("error extarcting gzip file",e)
            else:
                logging.error(f"The tgz_file_path: [{tgz_file_path}] does not exist.")

            logging.info("Extraction completed")

        except Exception as e:
            raise backorderException(e, sys) from e
    """
    """      
    def extract_tgz_file(self, tgz_file_path: str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            if os.path.exists(tgz_file_path):
                try:
                    with tarfile.open(tgz_file_path) as backorder_tgz_file_obj:
                        backorder_tgz_file_obj.extractall(path=raw_data_dir)
                except tarfile.ReadError as e:
                    # Log the specific error message for ReadError
                    logging.error(f"ReadError: {e}")
                    # Print the traceback for additional details
                    traceback.print_exc()
            else:
                logging.error(f"The tgz_file_path: [{tgz_file_path}] does not exist.")

            logging.info("Extraction completed")

        except Exception as e:
            raise backorderException(e, sys) from e
    """

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_list = os.listdir(raw_data_dir)

            #if not file_list:
                #raise backorderException("The raw_data_dir is empty. No files found in the directory.", sys)
            #file_name = os.listdir(raw_data_dir)[0]
            file_name = file_list[0]  #accesing file name from raw data ,[0] gives file name
            
            backorder_file_path = os.path.join(raw_data_dir,file_name)#creating file path
            

            logging.info(f"Reading csv file: [{backorder_file_path}]")
            backorder_data_frame = pd.read_csv(backorder_file_path,  low_memory=False)
            backorder_data_frame.drop(columns=['Unnamed: 0.1', 'Unnamed: 0', 'sku'], inplace=True , axis=1)
            
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            
            stratified_shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=0.4, random_state=42)
            for train_index, test_index in stratified_shuffle_split.split(backorder_data_frame, backorder_data_frame['went_on_backorder'].fillna(backorder_data_frame['went_on_backorder'].mode()[0])):
                strat_train_set = backorder_data_frame.loc[train_index]
                strat_test_set = backorder_data_frame.loc[test_index]

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise backorderException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path =  self.download_backorder_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise backorderException(e,sys) from e
    


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
        #__del__() is a special method that gets called when an object is about to be destroyed or garbage collected. 
        # It is commonly used for performing cleanup operations or finalizing tasks before an object is removed from memory.
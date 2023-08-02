from flask import Flask, request
import sys
from backorder.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from backorder.logger import logging
from backorder.exception import backorderException
import os, sys
import json
from backorder.config.configuration import Configuartion
from backorder.constant import CONFIG_DIR, get_current_time_stamp
from backorder.pipeline.pipeline import Pipeline
from backorder.entity.backorder_predictor import backorderPredictor, backorderData
from flask import send_file, abort, render_template
import pandas as pd

#intialization for flask application
ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "backorder"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from backorder.logger import get_log_dataframe

BACKORDER_DATA_KEY = "backorder_data"
WENT_ON_BACK_ORDER_KEY = "went_on_backorder"



application = Flask(__name__)
app=application

@app.route('/artifact', defaults={'req_path': 'backorder'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("backorder", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)

#to get html page
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():     #go to predict url
    context = {
        BACKORDER_DATA_KEY: None,
        WENT_ON_BACK_ORDER_KEY: None
    }
    try:
        if request.method == 'POST':
      
           national_inv= float(request.form['national_inv'])
           lead_time=float(request.form['lead_time'])
           in_transit_qty=float(request.form['in_transit_qty'])
           forecast_3_month=float(request.form['forecast_3_month'])
           forecast_6_month=float(request.form['forecast_6_month'])
           forecast_9_month=float(request.form['forecast_9_month'])
           sales_1_month=float(request.form['sales_1_month'])
           sales_3_month=float(request.form['sales_3_month'])
           sales_6_month=float(request.form['sales_6_month'])
           sales_9_month=float(request.form['sales_9_month'])
           min_bank=float(request.form['min_bank'])
           potential_issue=request.form['potential_issue']
           pieces_past_due=float(request.form['pieces_past_due'])
           perf_6_month_avg=float(request.form['perf_6_month_avg'])
           perf_12_month_avg=float(request.form['perf_12_month_avg'])
           local_bo_qty=float(request.form['local_bo_qty'])
           deck_risk=request.form['deck_risk']
           oe_constraint=request.form['oe_constraint']
           ppap_risk=request.form['ppap_risk']
           stop_auto_buy=request.form['stop_auto_buy']
           rev_stop=request.form['rev_stop']

           backorder_data = backorderData(national_inv=national_inv,
                                      lead_time	= lead_time,
                                      in_transit_qty=in_transit_qty,	
                                      forecast_3_month=forecast_3_month,
                                      forecast_6_month=forecast_6_month,	
                                      forecast_9_month=forecast_9_month,	
                                      sales_1_month	=sales_1_month,
                                      sales_3_month	=sales_3_month,
                                      sales_6_month	=sales_6_month,
                                      sales_9_month	=sales_9_month,
                                      min_bank=min_bank,
                                      potential_issue=potential_issue,
                                      pieces_past_due=pieces_past_due,	
                                      perf_6_month_avg=perf_6_month_avg,	
                                      perf_12_month_avg=perf_12_month_avg,
                                      local_bo_qty=local_bo_qty,
                                      deck_risk=deck_risk,
                                      oe_constraint=oe_constraint,
                                      ppap_risk=ppap_risk,
                                      stop_auto_buy=stop_auto_buy,
                                      rev_stop=rev_stop,
                                   )
           backorder_df = backorder_data.get_backorder_input_data_frame() #calling function from backorder predictor entity to save data frame
           backorder = backorderPredictor(model_dir=MODEL_DIR) #save model directory
           went_on_backorder = backorder.predict(X=backorder_df)
           context = {
                 BACKORDER_DATA_KEY: backorder_data.get_backorder_data_as_dict(),
                 WENT_ON_BACK_ORDER_KEY :went_on_backorder ,
              }
           return render_template('predict.html', context=context)
        return render_template("predict.html", context=context)

    except  Exception as e:
        logging.exception(e)
        return str(e)
"""
@app.route('/predict', methods=['POST'])
def predict():
    features = ['national_inv', 'lead_time', 'in_transit_qty', 'forecast_3_month',
       'forecast_6_month', 'forecast_9_month', 'sales_1_month',
       'sales_3_month', 'sales_6_month', 'sales_9_month', 'min_bank',
       'potential_issue', 'pieces_past_due', 'perf_6_month_avg',
       'perf_12_month_avg', 'local_bo_qty', 'deck_risk', 'oe_constraint',
       'ppap_risk', 'stop_auto_buy', 'rev_stop']

    input_data = pd.DataFrame(columns=features)
    input_row = {}
    for feature in features:
        input_value = request.form.get(feature)
        try:
            input_value = int(input_value)
        except ValueError:
            input_value = 0
        input_row[feature] = [input_value]
    input_data = pd.DataFrame.from_dict(input_row)
    # Perform prediction using the loaded model
    if os.path.exists(MODEL_DIR):
        predictor = backorderPredictor(model_dir=MODEL_DIR)
        prediction = predictor.predict(input_data)
    else:
        prediction = None
    
    if prediction is not None:
        if prediction == 0:
            result = 'Not Default'
        else:
            result = 'Default'
    else:
        result = None
    return render_template('predict.html', prediction_result=result )
"""

@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_model_files.html', result=result) #saved_models_files


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


#if __name__ == "__main__":
    #app.run()


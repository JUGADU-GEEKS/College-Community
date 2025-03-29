import joblib
from sklearn.linear_model import LinearRegression
import xgboost as xgb

def predict_price_equipment(item_type, months_old, condition):
    # Load the model dictionary
    model_dict = joblib.load('./model/PricePredictorCollegeEquipments.joblib')
    model = model_dict['model']  # Get the LinearRegression model
    
    arr = [months_old, 5]
    
    # Convert item_type to match form values
    if item_type == 'apron':
        arr.extend([1,0,0,0])
    elif item_type == 'drafter':
        arr.extend([0,1,0,0])
    elif item_type == 'labcoat':
        arr.extend([0,0,1,0])
    elif item_type == 'sheetholder':
        arr.extend([0,0,0,1])
    
    # Convert condition to match form values
    if condition == 'fair':
        arr.extend([1,0,0,0])
    elif condition == 'good':
        arr.extend([0,1,0,0])
    elif condition == 'new':
        arr.extend([0,0,1,0])
    elif condition == 'wornout':
        arr.extend([0,0,0,1])
    
    return model.predict([arr])

def predict_price_calculator(item_type, condition, months_old, demand):
    model_dict = joblib.load('./model/calculatorModel.joblib')
    model = model_dict['model']
    arr = [months_old, demand]
    if item_type == 'Model_fx-570ES':
        arr.extend([1,0,0])
    elif item_type == 'Model_fx-82MS':
        arr.extend([0,1,0])
    elif item_type == 'Model_fx-991MS':
        arr.extend([0,0,1])

    if condition == 'Condition_Heavily Used':
        arr.extend([1,0,0,0])
    elif condition == 'Condition_Like New':
        arr.extend([0,1,0,0])
    elif condition == 'Condition_New':
        arr.extend([0,0,1,0])
    elif condition == 'Condition_Used':
        arr.extend([0,0,0,1])
    
    return model.predict([arr])

print(predict_price_calculator('Model_fx-991MS', 'Condition_Like New', 20, 6))


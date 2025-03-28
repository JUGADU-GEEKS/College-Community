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

def predict_price_calculator(item_type, months_old):
    # Load the model dictionary
    model_dict = joblib.load('./model/PricePredictorCollegeCalculator.joblib')
    
    # Get the model and convert it to XGBoost format if needed
    if isinstance(model_dict['model'], xgb.XGBRegressor):
        model = model_dict['model']
    else:
        # If it's a raw booster, convert it to XGBRegressor
        model = xgb.XGBRegressor()
        model.load_model(model_dict['model'])
    
    arr = [months_old]
    if item_type == '573ms':
        arr.extend([1, 0, 0])
    elif item_type == '81ms':
        arr.extend([0, 1, 0])
    elif item_type == '991ms':
        arr.extend([0, 0, 1])
    return model.predict([arr])

print(predict_price_equipment('apron', 1, 'good'))


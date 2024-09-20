import pandas as pd
import joblib

def recommend_plans(total_mins, total_charge, model_path='random_forest_model.pkl', scaler_path='scaler.pkl', plans_path='tariff_plans.csv', top_n=3):
    print(f"Received Total Mins: {total_mins}")
    print(f"Received Total Charge: {total_charge}")

    # Load model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # Load plans
    plans = pd.read_csv(plans_path)
    
    # Create user_data DataFrame with all required features
    user_data = pd.DataFrame({
        'Account Length': [0],  # Placeholder value
        'VMail Message': [0],   # Placeholder value
        'Total Mins': [total_mins],
        'Total Calls': [0],     # Placeholder value
        'Total Charge': [total_charge],
        'CustServ Calls': [0]   # Placeholder value
    })
    
    print(f"user_data DataFrame:\n{user_data}")

    # Feature columns
    feature_columns = ['Account Length', 'VMail Message', 'Total Mins', 'Total Calls', 'Total Charge', 'CustServ Calls']
    user_data = user_data[feature_columns]
    
    # Transform user_data
    user_data_transformed = scaler.transform(user_data)
    
    print(f"Transformed user_data:\n{user_data_transformed}")

    # Predict churn (if needed)
    user_prediction = model.predict(user_data_transformed)

    # Define thresholds for outlier detection
    mins_threshold = 2000
    calls_threshold = 1000
    charge_threshold = 200

    # Check for outliers
    is_outlier = (total_mins > mins_threshold) or (total_international_mins > calls_threshold) or (user_data['Total Charge'].values[0] > charge_threshold)
    
    if is_outlier:
        recommendations = pd.DataFrame([{
            'PlanID': 'UNLIMITED',
            'PlanDescription': 'Unlimited Postpaid Plan',
            'MonthlyCost': 'As Per Usage',
        }])
        
        # Include other plans as available options
        other_plans = plans.copy()
        
        return recommendations, other_plans

    # Calculate expected cost for non-outlier recommendations
    plans['Expected Cost'] = plans.apply(
        lambda row: abs(row['IncludedMins'] - total_mins) +
                    max(0, total_international_mins - row['IncludedCalls']) +
                    max(0, user_data['Total Charge'].values[0] - row['MonthlyCost']),
        axis=1
    )

    best_plans = plans.sort_values('Expected Cost').head(top_n)
    other_plans = plans.sort_values('Expected Cost').iloc[top_n:]
    
    # Prepare DataFrames for output
    recommended_plans = pd.DataFrame([{
        'PlanID': plan['PlanID'],
        'PlanDescription': plan['PlanDescription'],
        'MonthlyCost': plan['MonthlyCost'],
    } for _, plan in best_plans.iterrows()])

    other_plans_details = pd.DataFrame([{
        'PlanID': plan['PlanID'],
        'PlanDescription': plan['PlanDescription'],
        'MonthlyCost': plan['MonthlyCost'],
    } for _, plan in other_plans.iterrows()])
    
    return recommended_plans, other_plans_details

if __name__ == "__main__":
    # Example usage
    total_mins = float(input("Enter the number of minutes: "))
    total_international_mins = float(input("Enter the number of international minutes: "))
    total_charge=float(input("Enter the total charge: "))
    
    recommended_plans, other_plans = recommend_plans(total_mins,total_charge)
   

    print("Top 3 Recommended Plans:")
    print(recommended_plans)
    
    print("\nOther Available Plans:")
    print(other_plans)

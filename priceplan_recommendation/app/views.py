from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.conf import settings
import joblib
import pandas as pd

def index(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Load the CSV files
        cdr_file = settings.BASE_DIR / 'app/files/CDR-Call-Details.csv'
        new_customer_file = settings.BASE_DIR / 'app/files/new_customer.csv'

        try:
            cdr_df = pd.read_csv(cdr_file)
            new_customer_df = pd.read_csv(new_customer_file)
        except FileNotFoundError:
            return HttpResponse("Required files are missing.", status=500)

        # Print column names for debugging
        print("CDR File Columns:", cdr_df.columns)
        print("New Customer File Columns:", new_customer_df.columns)
        
        # Search for the phone number in CDR-Call-Details.csv
        customer_data = cdr_df[cdr_df['Phone Number'] == phone_number]

        if not customer_data.empty:
            # Extract total minutes and total charge
            total_mins = customer_data[['Day Mins', 'Eve Mins', 'Night Mins']].sum(axis=1).values[0]
            total_charge = customer_data[['Day Charge', 'Eve Charge', 'Night Charge', 'Intl Charge']].sum(axis=1).values[0]

            # Save to new_customer.csv if not present
            if phone_number not in new_customer_df['Phone Number'].values:
                new_entry = pd.DataFrame({
                    'Phone Number': [phone_number],
                    'Total Mins': [total_mins],
                    'Total Charge': [total_charge]
                })
                new_customer_df = pd.concat([new_customer_df, new_entry], ignore_index=True)
                new_customer_df.to_csv(new_customer_file, index=False)
            
            # Store phone number and details in session and redirect to output page
            request.session['phone_number'] = phone_number
            request.session['total_mins'] = total_mins
            request.session['total_charge'] = total_charge
            return redirect('output')
        
        # Check new_customer.csv
        new_customer_data = new_customer_df[new_customer_df['Phone Number'] == phone_number]
        
        if not new_customer_data.empty:
            # Retrieve total minutes and total charge
            total_mins = new_customer_data['Total Mins'].values[0]
            
            if 'Total Charge' in new_customer_data.columns:
                total_charge = new_customer_data['Total Charge'].values[0]
            else:
                total_charge = 0  # Default value or handle as needed

            # Store phone number and details in session
            request.session['phone_number'] = phone_number
            request.session['total_mins'] = total_mins
            request.session['total_charge'] = total_charge
            return redirect('output')
        
        # If not found in both files, redirect to additional details
        request.session['phone_number'] = phone_number
        return render(request, 'additional_details.html', {'not_found': True})
    
    return render(request, 'index.html')

import pandas as pd
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest

def additional_details(request):
    if request.method == 'POST':
        try:
            # Get the total minutes and total charge from the form
            total_mins_str = request.POST.get('total_mins')
            total_charge_str = request.POST.get('total_charge')
            
            if total_mins_str is None or total_charge_str is None:
                return HttpResponseBadRequest("Missing total_mins or total_charge")

            total_mins = float(total_mins_str)
            total_charge = float(total_charge_str)
            
            # Save the total minutes and total charge in the session
            request.session['total_mins'] = total_mins
            request.session['total_charge'] = total_charge

            # Get the phone number from the session
            phone_number = request.session.get('phone_number')
            if phone_number is None:
                return HttpResponseBadRequest("Phone number not found in session")

            # Save the phone number and details to new_customer.csv
            new_customer_file = settings.BASE_DIR / 'app/files/new_customer.csv'

            # Ensure the file exists and is readable
            try:
                new_customer_df = pd.read_csv(new_customer_file)
            except FileNotFoundError:
                new_customer_df = pd.DataFrame(columns=['Phone Number', 'Total Mins', 'Total Charge'])
            except pd.errors.EmptyDataError:
                new_customer_df = pd.DataFrame(columns=['Phone Number', 'Total Mins', 'Total Charge'])

            new_entry = pd.DataFrame({
                'Phone Number': [phone_number],
                'Total Mins': [total_mins],
                'Total Charge': [total_charge]
            })
            new_customer_df = pd.concat([new_customer_df, new_entry], ignore_index=True)
            new_customer_df.to_csv(new_customer_file, index=False)

            # Redirect to the output page
            return redirect('output')
        
        except ValueError as e:
            return HttpResponseBadRequest(f"Invalid input: {e}")
        
    return render(request, 'additional_details.html')



def output(request):
    phone_number = request.session.get('phone_number')
    
    # Load the CSV files and model
    cdr_file = settings.BASE_DIR / 'app/files/CDR-Call-Details.csv'
    new_customer_file = settings.BASE_DIR / 'app/files/new_customer.csv'
    model_file = settings.BASE_DIR / 'app/files/random_forest_model.pkl'
    scaler_file = settings.BASE_DIR / 'app/files/scaler.pkl'
    plans_file = settings.BASE_DIR / 'app/files/tariff_plans.csv'
    
    cdr_df = pd.read_csv(cdr_file)
    new_customer_df = pd.read_csv(new_customer_file)
    plans_df = pd.read_csv(plans_file)
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    
    if phone_number:
        customer_data = cdr_df[cdr_df['Phone Number'] == phone_number]

        if not customer_data.empty:
            # Extract total minutes and total charge
            total_mins = customer_data[['Day Mins', 'Eve Mins', 'Night Mins']].sum(axis=1).values[0]
            total_charge = customer_data[['Day Charge', 'Eve Charge', 'Night Charge', 'Intl Charge']].sum(axis=1).values[0]

        else:
            total_mins = request.session.get('total_mins')
            total_charge = request.session.get('total_charge')

    # Recommend plans using the session values
    recommendations, other_plans = recommend_plans(total_mins, total_charge,
                                                    model_path=model_file,
                                                    scaler_path=scaler_file,
                                                    plans_path=plans_file)
    
    return render(request, 'output.html', {
        'phone_number': phone_number,
        'total_mins': int(total_mins),
        'total_charge': float(total_charge),
        'recommended_plans': recommendations.to_dict(orient='records'),
        'other_plans': other_plans.to_dict(orient='records')
    })

def recommend_plans(total_mins, total_charge, model_path='random_forest_model.pkl', scaler_path='scaler.pkl', plans_path='tariff_plans.csv', top_n=3):
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
        'Total Calls': [0],
        'Total Charge': [total_charge], 
        'CustServ Calls': [0]   # Placeholder value
    })
    
    # Define feature columns
    feature_columns = ['Account Length', 'VMail Message', 'Total Mins', 'Total Calls', 'Total Charge', 'CustServ Calls']
    
    # Ensure the user_data DataFrame has the same columns as those used for scaling
    user_data = user_data[feature_columns]
    
    # Transform user_data
    user_data_transformed = scaler.transform(user_data)
    
    # Predict churn (not used in recommendations but included for completeness)
    user_prediction = model.predict(user_data_transformed)
    
    # Define thresholds for outlier detection
    mins_threshold = 2000
    calls_threshold = 1000
    charge_threshold = 200

    # Check for outliers
    is_outlier = (total_mins > mins_threshold) or (total_charge > charge_threshold)
    
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
                    max(0, total_charge - row['MonthlyCost']),
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


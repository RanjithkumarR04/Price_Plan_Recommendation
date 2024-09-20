# Price_Plan_Recommendation

The Price Plan Recommendation System is a machine learning-based application designed to help telecom users select the most cost-effective mobile plans. The system uses a Random Forest Classifier to analyze users' call detail records (CDR) and recommend the top three tariff plans that best suit their usage patterns. By leveraging historical data, the model can predict user needs and minimize their costs by recommending plans that align with their calling, messaging, and data usage.


## Acknowledgements

 - [KAGGLE](https://www.kaggle.com/datasets/anshulmehtakaggl/cdrcall-details-record-predict-telco-churn)
 - [RANDOM FOREST](https://www.ibm.com/topics/random-forest)
 - [NORMALIZATION](https://www.javatpoint.com/dbms-normalization)
 - [STANDARD SCALAR](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)


## Appendix

## Data Processing

- *Normalization*: A preprocessing step used to standardize features to ensure consistency and improve model performance.
- *StandardScaler*: This technique rescales each feature to have a mean of 0 and a standard deviation of 1, which helps in normalizing the data.

## Model Building

- *Model Chosen: Random Forest Classifier*
  - The Random Forest Classifier was selected due to its robustness, ability to handle large datasets, and capability to manage high-dimensional data without significant overfitting. Additionally, it provides feature importance, aiding in understanding the impact of different features on the predictions.
  
- *Model Training*:
  - The RandomForestClassifier was fitted to the training data, allowing the model to learn patterns and relationships from the dataset. This process enables the model to make accurate predictions based on the learned information.

## Telecom Plans Creation

- A set of 25 telecom plans was created with varying features:
  - *Monthly Cost*: Ranging between $50 and $200.
  - *Included Minutes*: Between 200 and 1500 minutes.
  - *Included Calls*: Between 100 and 500 calls.
  - *Included International Minutes*: Between 1 and 20 international minutes.

## Model Evaluation

- *Accuracy*: The model achieved an accuracy of 97% on the test data, indicating its effectiveness in correctly predicting user churn and recommending appropriate telecom plans.

## Recommendation Logic

- *Process Overview*:
  - *Existing Users*: The system analyzes historical data to recommend the best plans based on past usage patterns.
  - *New Users*: The system prompts for key usage data (such as total minutes and calls) and provides plan recommendations based on the input provided.

## User Interface

- *Interactive System*:
  - *User Input Prompt*: The system prompts users to enter their phone number to receive tailored plan recommendations. For new users or those without historical data, the system collects relevant usage information directly.

---


## DEVELOPERS:

- [DHARUNIKHA](https://github.com/DHARUNIKHA)
- [SIVAKSHA SIVAGAMI](https://github.com/Sivaksha)
- [SWETHA](https://github.com/swe024)
- [GOWTHAM](https://github.com/GowthamShanmugam03)
- [RANJITH RAVIKUMAR](https://github.com/RanjithkumarR04)
- [BARATH](https://github.com/Barath-PR)


## Output Screenshots

![Screenshot 1](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%201.jpg)
![Screenshot 2](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%202.jpg)
![Screenshot 3](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%203.jpg)
![Screenshot 4](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%204.jpg)
![Screenshot 5](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%205.jpg)
![Screenshot 6](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%206.jpg)
![Screenshot 7](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%207.jpg)
![Screenshot 8](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%208.jpg)
![Screenshot 9](https://github.com/DHARUNIKHA/Price_Plan_Recommendation/blob/9a3821cc98ac16de535f5f210993bb8667569054/assets/image%209.jpg)

## Used By

This project is used by the following company:

 ### COGNIZANT
![](https://github.com/prabhakarvenkat/Potential_Customer_for_upsell/blob/4f1ba9a3b0e251d4a482cff767e11512e7c07e6d/assets/cognizant.jpg)

<html>
  <head></head>
  <body>
<h2>Contributing</h2>
  <p>If you would like to contribute to this project, please follow these guidelines:</p>
  <ol>
    <li>Fork the repository</li>
    <li>Create a new branch for your feature or bug fix</li>
    <li>Submit a pull request with a detailed description of your changes</li>
  </ol>

  <h2>License</h2>
  <p>This project is licensed under DHARUNIKHA and her team. See the <a href="LICENSE">LICENSE</a> file for more information.</p>

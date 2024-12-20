import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from src.data.correlation import ethnicity_to_group



def train_linear_regression():
    # Load data
    df = pd.read_csv('actor_data_for_regression')

    df = pd.read_csv('actor_data_for_regression.csv')
    df = ethnicity_to_group(df)
    df = df.drop(['Actor name', 'Usable Uni Rank', 'Citizenship', 'QS University Rank', 'Birth City', 'University',], axis=1)


    # One-hot encode categorical variables
    df = pd.get_dummies(df,columns = ['Gender', 'Birth Region', 'Ethnicity', 'Sports', 'Birth Month'])
    df.dropna(inplace=True)

    # Define features and target variable
    X = df.drop(columns=['Success Score'])
    y = df['Success Score']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R^2: {r2}')

    return model


def predict_success(model, new_data):
    df = pd.read_csv('actor_data_for_regression.csv')

    # Convert new data to DataFrame
    new_df = pd.DataFrame(new_data)

    # Encode new data
    new_df = pd.get_dummies(new_df, columns=['Gender', 'Birth Region', 'Ethnicity', 'Sports', 'Birth Month'])

    # Align new data with training data columns
    new_df, _ = new_df.align(df.drop(columns=['Success Score']), join='right', axis=1, fill_value=0)

    # Make prediction
    new_prediction = model.predict(new_df)
    return new_prediction
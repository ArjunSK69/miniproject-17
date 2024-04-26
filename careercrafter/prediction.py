import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier


# Load the datasets
personality_dataset = pd.read_csv('16P.csv', encoding='cp1252')
career_dataset = pd.read_csv('./career.csv')  # Replace 'career_dataset.csv' with your career dataset filename

# Preprocess the personality dataset
encoder = LabelEncoder()
personality_dataset['Personality'] = encoder.fit_transform(personality_dataset['Personality'])
X_personality = personality_dataset.drop(columns=['Personality', 'Response Id'])
y_personality = personality_dataset['Personality']

# Train the KNN model for personality prediction
X_train_personality, X_test_personality, y_train_personality, y_test_personality = train_test_split(X_personality,
                                                                                                    y_personality,
                                                                                                    test_size=0.2,
                                                                                                    random_state=42)
knn_personality = KNeighborsClassifier(n_neighbors=5)
knn_personality.fit(X_train_personality, y_train_personality)

# Preprocess the career dataset
career_mapping = dict(zip(career_dataset['Personality Type'], career_dataset[
    'Career']))  # Assuming 'Personality Type' and 'Career' are columns in your career dataset

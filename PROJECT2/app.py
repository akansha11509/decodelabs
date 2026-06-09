import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load the Iris Dataset
url = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"
df = pd.read_csv(url)

# 2. Separate features and target labels
X = df.drop(columns=['species'])
y = df['species']

# 3. Split the data (Stratified split ensures balanced class distribution in test set)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Initialize Random Forest with Hyperparameter Constraints (Prevents Overfitting)
# max_depth and min_samples_split limit how complex the trees can grow
model = RandomForestClassifier(max_depth=3, min_samples_split=5, random_state=42)

# 5. Enhancement 1: Perform 5-Fold Cross-Validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5)
print("--- Cross-Validation Performance ---")
print(f"5-Fold CV Accuracies: {cv_scores}")
print(f"Mean CV Accuracy: {cv_scores.mean() * 100:.2f}%\n")

# 6. Train the final model
model.fit(X_train, y_train)

# 7. Evaluate on Test Data
y_pred = model.predict(X_test)
print("--- Test Set Performance ---")
print(f"Final Test Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 8. Enhancement 2: Feature Importance Visualization
importances = model.feature_importances_
feature_names = X.columns

# Creating a clean bar plot
plt.figure(figsize=(8, 5))
sns.barplot(x=importances, y=feature_names, palette="viridis")
plt.title("Which Flower Features Mattered Most?")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()

# Save the visualization so you can add it to your GitHub README later!
plt.savefig("feature_importance.png")
print("\nFeature importance plot saved as 'feature_importance.png'!")

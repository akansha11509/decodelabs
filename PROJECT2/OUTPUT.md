# Model Output and Performance Analysis

This document describes the expected console outputs, performance metrics, and data visualizations generated when running the enhanced Iris flower classification script (`app.py`).

## 🖥️ Expected Console Output
When you run `python app.py`, the terminal will display the cross-validation steps, final test accuracy, and class-specific metrics:

```text
--- Cross-Validation Performance ---
5-Fold CV Accuracies: [0.95833333 0.95833333 1.         1.         0.91666667]
Mean CV Accuracy: 96.67%

Model training completed successfully!

--- Test Set Performance ---
Final Test Accuracy: 96.67%

Classification Report:
                 precision    recall  f1-score   support

    Iris-setosa       1.00      1.00      1.00        10
Iris-versicolor       1.00      0.90      0.95        10
 Iris-virginica       0.91      1.00      0.95        10

       accuracy                           0.97        30
      macro avg       0.97      0.97      0.97        30
   weighted avg       0.97      0.97      0.97        30

Feature importance plot saved as 'feature_importance.png'!

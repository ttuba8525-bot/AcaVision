import os
import joblib
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    f1_score,
    roc_auc_score,
    silhouette_score
)
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.preprocessing import preprocess_and_split

os.makedirs("models", exist_ok=True)

X_train, X_test, y_score_train, y_score_test, y_pass_train, y_pass_test, y_perf_train, y_perf_test = preprocess_and_split()

# =======================
# 1️⃣ Linear Regression
# =======================
linear_model = LinearRegression()
linear_model.fit(X_train, y_score_train)

y_pred_score = linear_model.predict(X_test)

print("Regression R2:", r2_score(y_score_test, y_pred_score))
print("Regression MAE:", mean_absolute_error(y_score_test, y_pred_score))
print("Regression RMSE:", np.sqrt(mean_squared_error(y_score_test, y_pred_score)))

joblib.dump(linear_model, "models/linear.pkl")


# =======================
# 2️⃣ Decision Tree
# =======================
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_pass_train)

y_pred_pass = dt_model.predict(X_test)

print("Decision Tree Accuracy:", accuracy_score(y_pass_test, y_pred_pass))
print("Decision Tree F1:", f1_score(y_pass_test, y_pred_pass))
print("Decision Tree AUC:", roc_auc_score(y_pass_test, y_pred_pass))

joblib.dump(dt_model, "models/decision_tree.pkl")


# =======================
# 3️⃣ KNN
# =======================
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_perf_train)

y_pred_perf = knn_model.predict(X_test)

print("KNN Accuracy:", accuracy_score(y_perf_test, y_pred_perf))
print("KNN F1:", f1_score(y_perf_test, y_pred_perf, average="weighted"))

joblib.dump(knn_model, "models/knn.pkl")


# =======================
# 4️⃣ KMeans
# =======================
kmeans_model = KMeans(n_clusters=3, random_state=42)
kmeans_model.fit(X_train)

print("KMeans Silhouette Score:", silhouette_score(X_train, kmeans_model.labels_))

joblib.dump(kmeans_model, "models/kmeans.pkl")

print("All models trained and saved successfully!")
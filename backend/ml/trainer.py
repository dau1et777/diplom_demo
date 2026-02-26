"""
Machine Learning Model Trainer for Career Recommendation System
Handles dataset loading, preprocessing, model training, evaluation,
and saving trained artifacts.
"""

import os
import warnings
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

warnings.filterwarnings("ignore")


class CareerModelTrainer:
    """
    Trains and evaluates a Random Forest classifier
    for career recommendation based on user skills,
    interests, and work preferences.
    """

    def __init__(self, model_dir="ml/models", data_dir="ml/data"):
        self.model_dir = model_dir
        self.data_dir = data_dir

        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None

        os.makedirs(self.model_dir, exist_ok=True)

    # --------------------------------------------------
    # DATA LOADING
    # --------------------------------------------------
    def load_dataset(self, filename="career_dataset.csv"):
        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found: {filepath}")

        df = pd.read_csv(filepath)
        print(f"Dataset loaded: {len(df)} samples, {len(df.columns) - 1} features")
        return df

    # --------------------------------------------------
    # DATA PREPARATION
    # --------------------------------------------------
    def prepare_data(self, df):
        X = df.drop("career", axis=1)
        y = df["career"]

        self.feature_names = X.columns.tolist()

        print(f"\nFeatures ({len(self.feature_names)}):")
        print(self.feature_names)

        print("\nTarget classes:")
        print(y.unique())

        print("\nClass distribution:")
        print(y.value_counts())

        return X, y

    # --------------------------------------------------
    # PREPROCESSING
    # --------------------------------------------------
    def normalize_features(self, X_train, X_test):
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    def encode_labels(self, y_train, y_test):
        self.label_encoder = LabelEncoder()
        y_train_enc = self.label_encoder.fit_transform(y_train)
        y_test_enc = self.label_encoder.transform(y_test)
        return y_train_enc, y_test_enc

    # --------------------------------------------------
    # MODEL TRAINING
    # --------------------------------------------------
    def train_model(self, X_train, y_train):
        print("\nTraining Random Forest model...")

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_train, y_train)
        print("Model training completed.")

    # --------------------------------------------------
    # EVALUATION
    # --------------------------------------------------
    def evaluate_model(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print("\n" + "=" * 60)
        print(f"Model Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
        print("=" * 60)

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        feature_importance = pd.DataFrame({
            "feature": self.feature_names,
            "importance": self.model.feature_importances_
        }).sort_values(by="importance", ascending=False)

        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))

    # --------------------------------------------------
    # SAVE ARTIFACTS
    # --------------------------------------------------
    def save_model(
        self,
        model_name="career_model.joblib",
        scaler_name="scaler.joblib",
        encoder_name="label_encoder.joblib"
    ):
        joblib.dump(self.model, os.path.join(self.model_dir, model_name))
        joblib.dump(self.scaler, os.path.join(self.model_dir, scaler_name))
        joblib.dump(self.label_encoder, os.path.join(self.model_dir, encoder_name))

        print("\nSaved artifacts:")
        print(f"- Model: {model_name}")
        print(f"- Scaler: {scaler_name}")
        print(f"- Label Encoder: {encoder_name}")

    # --------------------------------------------------
    # FULL PIPELINE
    # --------------------------------------------------
    def run_full_pipeline(self):
        print("Starting Career Model Training Pipeline...\n")

        # 1. Load data
        df = self.load_dataset()

        # 2. Prepare data
        X, y = self.prepare_data(df)

        # 3. Train-test split (IMPORTANT FIX)
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.3,          # ⚠ FIXED: must be >= number of classes
            random_state=42,
            stratify=y
        )

        print(f"\nTrain-test split:")
        print(f"- Train samples: {len(X_train)}")
        print(f"- Test samples:  {len(X_test)}")

        # 4. Normalize
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)

        # 5. Encode labels
        y_train_enc, y_test_enc = self.encode_labels(y_train, y_test)

        # 6. Train model
        self.train_model(X_train_scaled, y_train_enc)

        # 7. Evaluate
        self.evaluate_model(X_test_scaled, y_test_enc)

        # 8. Save
        self.save_model()

        print("\n" + "=" * 60)
        print("Training pipeline completed successfully!")
        print("=" * 60)


def main():
    trainer = CareerModelTrainer()
    trainer.run_full_pipeline()


if __name__ == "__main__":
    main()

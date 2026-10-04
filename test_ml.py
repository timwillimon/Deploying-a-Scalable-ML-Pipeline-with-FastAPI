import numpy as np
from sklearn.ensemble import RandomForestClassifier

from ml.model import (
    compute_model_metrics,
    inference,
    train_model,
)


def test_compute_model_metrics():
    """Verify precision, recall, and F1 against known results."""
    labels = np.array([0, 1, 1, 0])
    predictions = np.array([0, 1, 0, 0])

    precision, recall, f1 = compute_model_metrics(
        labels,
        predictions,
    )

    assert precision == 1.0
    assert recall == 0.5
    assert round(f1, 4) == 0.6667


def test_train_model():
    """Verify that training returns a fitted Random Forest classifier."""
    features = np.array(
        [
            [0, 1],
            [1, 0],
            [1, 1],
            [0, 0],
        ]
    )
    labels = np.array([0, 1, 1, 0])

    model = train_model(features, labels)

    assert isinstance(model, RandomForestClassifier)
    assert hasattr(model, "classes_")
    assert set(model.classes_) == {0, 1}


def test_inference():
    """Verify that inference returns valid predictions of the right shape."""
    features = np.array(
        [
            [0, 1],
            [1, 0],
            [1, 1],
            [0, 0],
        ]
    )
    labels = np.array([0, 1, 1, 0])

    model = train_model(features, labels)
    predictions = inference(model, features)

    assert isinstance(predictions, np.ndarray)
    assert predictions.shape == labels.shape
    assert set(predictions).issubset({0, 1})

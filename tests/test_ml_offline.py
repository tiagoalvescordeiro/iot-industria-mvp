# Offline ML sanity test (does not hit DB). Ensures sklearn is available and model trains.
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def test_offline_random_forest_sanity():
    rng = np.random.default_rng(42)
    X = rng.uniform(18, 35, size=(500,1))
    # target correlated with temperature + noise
    y = 0.8 * X[:,0] + 5 + rng.normal(0, 0.5, size=500)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    assert mae < 0.6, f"MAE too high: {mae}"

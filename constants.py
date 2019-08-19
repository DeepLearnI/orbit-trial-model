import numpy as np
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
np.random.seed(42)

# configurable simulation parameters
minimum_monthly_growth = 0.2
maximum_monthly_growth = 0.3
n_custs = 3000
n_features = 2
min_feature_value = 0
max_feature_value = 4
min_theta_value = -1.5
max_theta_value = 0.5

# test config
test_mode = True
retrain_date = datetime.datetime(year=2099, month=12, day=1)

issues = [
         {"type": "special_value",
           "column":"feat_0",
           "special_value":-1,
           "percentage":1,
           "trigger_date":datetime.datetime(year=2020, month=1, day=1)},
          {"type": "distribution_shift",
           "trigger_date": datetime.datetime(year=2021, month=1, day=1),
           "months_remaining":8,
           "scale": 0.1,
           "step_size": 0.2,
           "min_drift": 0.5,
           "max_drift": 0.5}
          ]
# issues = []

# derived constants
feature_cols = [f"feat_{i}" for i in range(n_features)]
# Usage

To use icdcodex in a project:

    from icdcodex import icd2vec, hierarchy
    X, y = get_data()
    embedder = icd2vec.Icd2Vec(num_embedding_dimensions=64, walk_length=10, num_walks=200, workers=-1)
    G, icd_codes = hierarchy.icd9hierarchy("icd9Hierarchy.json")
    embedder.fit(G, icd_codes)
    y_train_continuous = embedder.to_vec(y_train.reshape(-1))

For example:

```python
import pandas as pd
import numpy as np
from sklearn import preprocessing
import xgboost as xgb
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
import sklearn.metrics as M

from icdcodex import icd2vec, hierarchy
```

From the MIMIC-III Big Query database, run:
```sql
SELECT
    i.seq_num, i.subject_id, i.icd9_code, j.los, k.gender, k.dob, k.dod, l.admittime
FROM `physionet-data.mimiciii_clinical.diagnoses_icd` as i
    INNER JOIN
        `physionet-data.mimiciii_clinical.icustays` as j
        ON i.hadm_id = j.hadm_id
    INNER JOIN
        `physionet-data.mimiciii_clinical.patients` as k
        ON i.subject_id = k.subject_id
    INNER JOIN
        `physionet-data.mimiciii_clinical.admissions` as l
        ON i.hadm_id = l.hadm_id
```

Save the results as `data.json.gz`


```python
df = pd.read_csv("data.csv").rename(columns={
    "los": "length_of_stay",
    "dob": "date_of_birth",
    "dod": "date_of_death",
    "admittime": "date_of_admission"
})
df["date_of_birth"] = pd.to_datetime(df["date_of_birth"]).dt.date
df["date_of_death"] = pd.to_datetime(df["date_of_death"]).dt.date
df["date_of_admission"] = pd.to_datetime(df["date_of_admission"]).dt.date
df["age"] = df.apply(lambda e: (e['date_of_admission'] - e['date_of_birth']).days/365, axis=1)
df = df[df.seq_num == 1]
le = preprocessing.LabelEncoder()
le.fit(df.gender)
df.gender = le.transform(df.gender)
drg_severity_le = preprocessing.LabelEncoder()
df.drg_severity = drg_severity_le.fit_transform(df.drg_severity)
drg_mortality_le = preprocessing.LabelEncoder()
df.drg_mortality = drg_mortality_le.fit_transform(df.drg_mortality)
curr_service_le = OneHotEncoder()
one_hot_service = curr_service_le.fit_transform(df.curr_service.values.reshape(-1,1))
df = df.merge(pd.DataFrame(one_hot_service.todense()).set_index(df.index), left_index=True, right_index=True)
```

```python
G, icd_codes = hierarchy.icd9hierarchy("icd9Hierarchy.json")
```

```python
df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>seq_num</th>
      <th>subject_id</th>
      <th>icd9_code</th>
      <th>length_of_stay</th>
      <th>gender</th>
      <th>date_of_birth</th>
      <th>date_of_death</th>
      <th>date_of_admission</th>
      <th>curr_service</th>
      <th>drg_severity</th>
      <th>...</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
      <th>17</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>256</td>
      <td>53240</td>
      <td>0.0044</td>
      <td>1</td>
      <td>2086-07-31</td>
      <td>NaT</td>
      <td>2170-08-16</td>
      <td>MED</td>
      <td>181</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>256</td>
      <td>53240</td>
      <td>0.0044</td>
      <td>1</td>
      <td>2086-07-31</td>
      <td>NaT</td>
      <td>2170-08-16</td>
      <td>MED</td>
      <td>2</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>256</td>
      <td>53240</td>
      <td>0.0044</td>
      <td>1</td>
      <td>2086-07-31</td>
      <td>NaT</td>
      <td>2170-08-16</td>
      <td>MED</td>
      <td>2</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>256</td>
      <td>53240</td>
      <td>1.7219</td>
      <td>1</td>
      <td>2086-07-31</td>
      <td>NaT</td>
      <td>2170-08-16</td>
      <td>MED</td>
      <td>314</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>256</td>
      <td>53240</td>
      <td>1.7219</td>
      <td>1</td>
      <td>2086-07-31</td>
      <td>NaT</td>
      <td>2170-08-16</td>
      <td>MED</td>
      <td>2</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 30 columns</p>
</div>




```python
df = df[df.icd9_code.isin(G.nodes())]
```


```python
features = ["length_of_stay", "gender", "age", "drg_severity"] + list(range(17))
df[features].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>length_of_stay</th>
      <th>gender</th>
      <th>age</th>
      <th>drg_severity</th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>...</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0044</td>
      <td>1</td>
      <td>84.09863</td>
      <td>181</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0044</td>
      <td>1</td>
      <td>84.09863</td>
      <td>2</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0044</td>
      <td>1</td>
      <td>84.09863</td>
      <td>2</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.7219</td>
      <td>1</td>
      <td>84.09863</td>
      <td>314</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1.7219</td>
      <td>1</td>
      <td>84.09863</td>
      <td>2</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>




```python
X = df[features].values
y = df[["icd9_code"]].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```


```python
ohe = OneHotEncoder(handle_unknown="ignore")
y_train_onehot = ohe.fit_transform(y_train)
clf_onehot = RandomForestClassifier()
clf_onehot.fit(X_train, y_train_onehot.todense())

f1 = M.f1_score(ohe.transform(y_test), clf_onehot.predict(X_test), average="weighted")
acc = M.accuracy_score(ohe.transform(y_test), clf_onehot.predict(X_test))
f"accuracy = {acc:.2f}, f1 = {f1:.2f}"
```

    /home/j/Desktop/icd-codex/venv/lib/python3.8/site-packages/sklearn/metrics/_classification.py:1464: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no true nor predicted samples. Use `zero_division` parameter to control this behavior.
      _warn_prf(





    'accuracy = 0.53, f1 = 0.56'

```python
embedder = icd2vec.Icd2Vec(num_embedding_dimensions=64, walk_length=10, num_walks=200, workers=-1)
embedder.fit(icd_codes, G)
y_train_continuous = embedder.to_vec(y_train.reshape(-1))
```


```python
clf = RandomForestRegressor()
clf.fit(X_train, y_train_continuous)
y_pred = embedder.to_code(clf.predict(X_test))

acc = M.accuracy_score(y_test, y_pred)
f1 = M.f1_score(y_test, y_pred, average="weighted")
f"accuracy = {acc:.2f}, f1 = {f1:.2f}"
```
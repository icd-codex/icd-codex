# Usage

To use icdcodex in a project

```python
    from icdcodex import icd2vec, hierarchy
    embedder = icd2vec.Icd2Vec(num_embedding_dimensions=64)
    embedder.fit(*hierarchy.icd9hierarchy())
    y = embedder.to_vec(y)
```

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

Save the results as `data.csv`

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
G, icd_codes = hierarchy.icd9hierarchy("icd9Hierarchy.json")
df = df[df.icd9_code.isin(G.nodes())]
features = ["length_of_stay", "gender", "age", "drg_severity"] + list(range(17))

X = df[features].values
y = df[["icd9_code"]].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

We can look at a baseline model

```python
ohe = OneHotEncoder(handle_unknown="ignore")
y_train_onehot = ohe.fit_transform(y_train)
clf_onehot = RandomForestClassifier()
clf_onehot.fit(X_train, y_train_onehot.todense())
f1 = M.f1_score(ohe.transform(y_test), clf_onehot.predict(X_test), average="weighted")
acc = M.accuracy_score(ohe.transform(y_test), clf_onehot.predict(X_test))
f"accuracy = {acc:.2f}, f1 = {f1:.2f}"
```

And compare it to our embedding model

```python
embedder = icd2vec.Icd2Vec(num_embedding_dimensions=64, walk_length=10, num_walks=200, workers=-1)
embedder.fit(icd_codes, G)
y_train_continuous = embedder.to_vec(y_train.reshape(-1))
clf = RandomForestRegressor()
clf.fit(X_train, y_train_continuous)
y_pred = embedder.to_code(clf.predict(X_test))
acc = M.accuracy_score(y_test, y_pred)
f1 = M.f1_score(y_test, y_pred, average="weighted")
f"accuracy = {acc:.2f}, f1 = {f1:.2f}"
```
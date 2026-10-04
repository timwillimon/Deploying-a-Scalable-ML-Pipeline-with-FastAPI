# Deploying a Scalable ML Pipeline with FastAPI

This project builds, evaluates, monitors, and deploys a binary classification
model using publicly available Census Bureau data. The model predicts whether
an individual's annual income is greater than $50,000.

The completed project includes data preprocessing, model training, performance
evaluation, categorical slice monitoring, unit tests, continuous integration,
saved model artifacts, and a REST API built with FastAPI.

## Project Repository

Public GitHub repository:

[Deploying a Scalable ML Pipeline with FastAPI](https://github.com/timwillimon/Deploying-a-Scalable-ML-Pipeline-with-FastAPI)

## Project Structure

```text
Deploying-a-Scalable-ML-Pipeline-with-FastAPI/
├── .github/
│   └── workflows/
│       └── manual.yml
├── data/
│   └── census.csv
├── ml/
│   ├── __init__.py
│   ├── data.py
│   └── model.py
├── model/
│   ├── encoder.pkl
│   ├── lb.pkl
│   └── model.pkl
├── screenshots/
│   ├── continuous_integration.png
│   ├── local_api.png
│   └── unit_test.png
├── environment.yml
├── local_api.py
├── main.py
├── model_card.md
├── requirements.txt
├── slice_output.txt
├── test_ml.py
└── train_model.py
```

## Environment Setup

The project uses Python 3.10 and the Conda environment defined in
`environment.yml`.

Create the environment:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate fastapi
```

Install flake8 for local code-quality checks:

```bash
python -m pip install flake8
```

Confirm the Python version:

```bash
python --version
```

The expected version is Python 3.10.

## Dataset

The project uses the supplied `data/census.csv` dataset. It contains 32,561
records and 15 columns.

The target column is `salary`, with two possible classes:

```text
<=50K
>50K
```

The dataset contains:

- 24,720 records labeled `<=50K`
- 7,841 records labeled `>50K`

The target classes are imbalanced, so model performance is evaluated with
precision, recall, and F1 rather than accuracy alone.

Categorical features include:

- `workclass`
- `education`
- `marital-status`
- `occupation`
- `relationship`
- `race`
- `sex`
- `native-country`

The categorical features are transformed with a one-hot encoder. Unknown
categories are ignored during inference so the API can process previously
unseen category values without failing.

## Model

The project uses a scikit-learn `RandomForestClassifier` with the following
configuration:

```text
n_estimators=100
max_depth=20
min_samples_leaf=2
random_state=42
n_jobs=-1
```

The model uses a reproducible 80/20 train-test split stratified by the
`salary` target.

The trained artifacts are stored in the `model/` directory:

- `model/model.pkl`
- `model/encoder.pkl`
- `model/lb.pkl`

The constrained Random Forest configuration keeps the serialized model within
GitHub's regular repository file-size limit while maintaining useful
classification performance.

## Train the Model

Run the complete training pipeline from the repository root:

```bash
python train_model.py
```

The script:

1. Loads `data/census.csv`.
2. Creates the training and test datasets.
3. Processes categorical and continuous features.
4. Trains the Random Forest classifier.
5. Saves the model, encoder, and label binarizer.
6. Evaluates the model against the held-out test data.
7. Calculates model performance for categorical data slices.
8. Writes the slice results to `slice_output.txt`.

## Model Performance

The trained model produced the following results on the held-out test dataset:

```text
Precision: 0.7872
Recall: 0.6180
F1: 0.6924
```

Precision measures how often a predicted `>50K` classification is correct.
Recall measures how many actual `>50K` records the model identifies. F1
provides a combined measure of precision and recall.

The model has higher precision than recall. It is more conservative when
predicting the `>50K` class and does not identify every higher-income record.

## Slice Performance

The pipeline calculates precision, recall, F1, and record count for every
unique value of each categorical feature.

The results are stored in:

```text
slice_output.txt
```

The monitored categorical features are:

```text
workclass
education
marital-status
occupation
relationship
race
sex
native-country
```

These results make it possible to compare model behavior across demographic,
education, employment, relationship, and location-related data slices.

Slice metrics do not establish that the model is fair or appropriate for
high-impact use. Slices with very few records may produce unstable metrics.

## Unit Tests

The project includes three deterministic tests for the model functions:

- `test_compute_model_metrics`
- `test_train_model`
- `test_inference`

Run them with:

```bash
pytest test_ml.py -v
```

Expected result:

```text
3 passed
```

The passing-test evidence is stored in:

```text
screenshots/unit_test.png
```

## Code Quality

Run the strict syntax and undefined-name check:

```bash
flake8 . --count --select=E9,F63,F7,F82 \
  --show-source --statistics
```

Run the complete local style check:

```bash
flake8 . --count --max-complexity=10 \
  --max-line-length=88 --statistics
```

Both commands should complete without errors.

## Continuous Integration

The repository includes a GitHub Actions workflow at:

```text
.github/workflows/manual.yml
```

The workflow runs on every push and:

1. Uses Python 3.10.
2. Installs the project dependencies.
3. Runs flake8.
4. Runs `pytest test_ml.py -v`.

The passing workflow evidence is stored in:

```text
screenshots/continuous_integration.png
```

## FastAPI Application

The FastAPI application is defined in `main.py`.

The API provides two endpoints:

```text
GET /
POST /data/
```

### GET Endpoint

The root endpoint returns a welcome message:

```json
{
  "message": "Hello from the API!"
}
```

### POST Endpoint

The `/data/` endpoint accepts one Census record, applies the saved encoder,
runs model inference, and returns one of the following classifications:

```text
<=50K
>50K
```

## Run the API Locally

Start the API from the repository root:

```bash
uvicorn main:app --reload
```

The service will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

Leave the API running and open a second terminal.

Activate the environment:

```bash
conda activate fastapi
```

Run the local client:

```bash
python local_api.py
```

Expected output structure:

```text
Status Code: 200
Result: Hello from the API!
Status Code: 200
Result: <=50K
```

The successful local GET and POST evidence is stored in:

```text
screenshots/local_api.png
```

## Model Card

Detailed model documentation is available in:

```text
model_card.md
```

The model card documents:

- model configuration
- intended use
- training data
- evaluation data
- metrics
- ethical considerations
- caveats and recommendations

This model is an educational demonstration and should not be used for
employment, lending, insurance, housing, eligibility, compensation, or other
high-impact decisions.

## Required Project Evidence

The repository contains the following required screenshots:

- `screenshots/unit_test.png`
- `screenshots/local_api.png`
- `screenshots/continuous_integration.png`

It also contains:

- the trained classifier
- the categorical encoder
- the label binarizer
- categorical slice results
- the completed model card
- the FastAPI application
- the local API client
- the GitHub Actions workflow

## Final Validation

Run the following commands before submission:

```bash
pytest test_ml.py -v
```

```bash
flake8 . --count --select=E9,F63,F7,F82 \
  --show-source --statistics
```

```bash
flake8 . --count --max-complexity=10 \
  --max-line-length=88 --statistics
```

Confirm the repository is clean:

```bash
git status
```

Confirm the required files are tracked:

```bash
git ls-files model screenshots slice_output.txt model_card.md README.md
```

## Submission

The public GitHub repository is:

[Deploying a Scalable ML Pipeline with FastAPI](https://github.com/timwillimon/Deploying-a-Scalable-ML-Pipeline-with-FastAPI)

This repository URL must also be included in the project Submission Details
box.

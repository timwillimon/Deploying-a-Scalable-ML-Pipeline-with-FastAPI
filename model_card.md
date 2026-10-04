# Model Card

For additional information, see the
[Model Cards for Model Reporting paper](https://arxiv.org/abs/1810.03993).

## Model Details

This project uses a scikit-learn `RandomForestClassifier` to predict whether
an individual's annual income is greater than $50,000 based on publicly
available Census Bureau data.

The classifier contains 100 decision trees with a maximum tree depth of 20 and
a minimum leaf size of 2. A random state of 42 is used to make training and
evaluation reproducible. The model is trained by `train_model.py`, and the
trained classifier is stored in `model/model.pkl`.

Categorical variables are transformed with a fitted `OneHotEncoder` that uses
`handle_unknown="ignore"`. The fitted encoder is stored in
`model/encoder.pkl`. A fitted `LabelBinarizer` is stored in `model/lb.pkl` and
is used to convert between the binary model output and the income labels
`<=50K` and `>50K`.

## Intended Use

The model is intended as an educational demonstration of a complete machine
learning workflow. The workflow includes data preprocessing, model training,
evaluation, performance monitoring across categorical data slices, artifact
persistence, and model inference through a FastAPI service.

The model may be used to demonstrate binary classification and REST API
deployment in a controlled learning environment. It should not be used to make
employment, lending, insurance, housing, compensation, eligibility, or other
high-impact decisions about individuals.

The model output is an estimate based on patterns in the training data. It is
not a verified statement about an individual's income or financial condition.

## Training Data

The model was trained using the `census.csv` dataset supplied with the project.
The dataset contains 32,561 records and 15 columns. The target column is
`salary`, with two possible values:

- `<=50K`
- `>50K`

The complete dataset contains 24,720 records labeled `<=50K` and 7,841 records
labeled `>50K`. This indicates that the target classes are imbalanced, with
substantially more records in the lower-income class.

The data contains a combination of continuous and categorical features.
Categorical features used by the model include:

- `workclass`
- `education`
- `marital-status`
- `occupation`
- `relationship`
- `race`
- `sex`
- `native-country`

Categorical features are one-hot encoded. The remaining columns are passed to
the classifier as continuous features. The data is divided into training and
test sets using an 80/20 split. The split uses a random state of 42 and is
stratified by the `salary` label.

## Evaluation Data

Model performance was evaluated on the held-out 20 percent test split. The
same fitted categorical encoder and label binarizer used during training were
applied to the test data.

The test data was not used to fit the model. Stratification was used to
preserve the target-class distribution across the training and test datasets.

In addition to overall test-set evaluation, performance was calculated for
each unique value of every categorical feature. The resulting precision,
recall, F1, and record count values are stored in `slice_output.txt`.

## Metrics

The model is evaluated with precision, recall, and F1 score for the `>50K`
class.

- **Precision** measures the proportion of predicted `>50K` records that were
  actually labeled `>50K`.
- **Recall** measures the proportion of actual `>50K` records that the model
  correctly identified.
- **F1 score** is the harmonic mean of precision and recall and provides a
  combined measure of both.

The model produced the following overall results on the held-out test data:

- **Precision:** 0.7872
- **Recall:** 0.6180
- **F1 score:** 0.6924

The precision result indicates that approximately 78.72 percent of the
model's `>50K` predictions were correct. The recall result indicates that the
model identified approximately 61.80 percent of the records actually labeled
`>50K`.

The lower recall compared with precision means the model is more conservative
when predicting the higher-income class. It produces fewer false-positive
higher-income predictions but does not identify every record in that class.

## Ethical Considerations

The dataset contains demographic and personal characteristics, including age,
race, sex, education, occupation, marital status, relationship status, and
national origin. These variables may reflect historical and social
inequalities present in the source data.

Model performance may differ across demographic and occupational groups. The
project calculates precision, recall, and F1 across categorical slices to make
those differences visible. However, reporting slice metrics does not establish
that the model is fair or appropriate for high-impact use.

The `race`, `sex`, and `native-country` variables are particularly sensitive.
Predictions involving these variables could reinforce historical patterns or
produce unequal outcomes. The model should not be used to assess a person's
value, ability, creditworthiness, employability, or eligibility for services.

The Census data describes group-level statistical patterns. A prediction for
one record should not be treated as a factual conclusion about a specific
individual.

## Caveats and Recommendations

The model is limited by the quality, scope, class distribution, and historical
context of the training data. Relationships learned from the supplied Census
dataset may not represent current income patterns, populations outside the
dataset, or future conditions.

The model has lower recall than precision for the `>50K` class, so some
higher-income records are classified as `<=50K`. This limitation should be
considered when interpreting predictions.

Slice-level results in `slice_output.txt` should be reviewed before any
expanded use. Slices containing very few records may produce unstable or
misleading metrics, including apparently perfect scores based on only one or
two examples.

Before any use outside this educational project, the model should be
retrained on current and representative data, evaluated for disparate
performance across relevant groups, reviewed for appropriate feature use, and
tested under the conditions in which it would operate.

The FastAPI service should be treated as a demonstration deployment. A
production implementation would also require authentication, request
validation, access controls, monitoring, secure artifact management, version
tracking, and a documented retraining process.
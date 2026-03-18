# 🏋️ [Tracking Barbell Exercises](https://github.com/Anujjadaun97/tracking-barbell-exercises)

An end-to-end machine learning pipeline that uses raw IMU sensor data from a wristband to **automatically classify barbell gym exercises** and **count repetitions** — no manual labelling required at inference time.

---

## 📌 Overview

This project processes 6-axis motion data (accelerometer + gyroscope) recorded during five common barbell movements. A trained classifier identifies which exercise is being performed, and a peak-detection algorithm counts the reps in real time.

**Exercises classified:**
- Squat
- Bench Press
- Deadlift
- Overhead Press
- Barbell Row

**Labels:** Heavy vs. Medium load per exercise.

---

## 🗂️ Project Structure

```
tracking-barbell-exercises/
│
├── data/
│   ├── external/          # Raw MetaMotion sensor exports (.csv)
│   ├── raw/               # Unprocessed accelerometer & gyroscope files
│   ├── interim/           # Cleaned & merged data
│   └── processed/         # Feature-engineered datasets ready for modelling
│
├── models/                # Serialised trained models (.pkl)
│
├── reports/
│   └── figures/           # Confusion matrices, feature importance plots, rep-count charts
│
├── src/
│   ├── make_dataset.py         # Load & merge acc + gyro CSV files
│   ├── remove_outliers.py      # Chauvenet's criterion & IQR filtering
│   ├── build_features.py       # Temporal, frequency-domain & PCA features
│   ├── train_model.py          # Train & evaluate classifiers
│   └── count_reps.py           # Peak-detection rep counter
│
├── database_connection.py      # Data ingestion helper
└── requirements.txt
```

---

## 🔬 [Sensor & Data](https://github.com/Anujjadaun97/tracking-barbell-exercises/blob/main/data/raw/raw%20zip)

| Property | Value |
|---|---|
| Device | Mbientlab MetaMotion wristband |
| Sensors | 3-axis accelerometer + 3-axis gyroscope |
| Features captured | `acc_x`, `acc_y`, `acc_z`, `gyr_x`, `gyr_y`, `gyr_z` |
| Sampling rate | ~12.5 Hz – 200 Hz |
| Participants | Multiple subjects, both heavy & medium sets |

Raw data is stored in separate CSV files for each sensor axis and merged in the first pipeline step.

---

## ⚙️ Pipeline

```
Raw CSVs  →  make_dataset  →  remove_outliers  →  build_features  →  train_model
                                                                           ↓
                                                                     models/*.pkl
                                                       count_reps  (runs independently)
```

### 1. [`make_dataset`](https://github.com/Anujjadaun97/tracking-barbell-exercises/blob/main/src/data/dataset.ipynb)
Reads individual accelerometer and gyroscope CSV files, aligns them by timestamp, and outputs a single merged DataFrame saved to `data/interim/`.

### 2. [`remove_outliers`](https://github.com/Anujjadaun97/tracking-barbell-exercises/blob/main/src/features/remove_outliers.ipynb)
Applies two statistical methods to drop noisy readings:
- **Chauvenet's criterion** — removes data points whose probability of occurring is below a threshold
- **IQR (Interquartile Range)** — clips extreme values per feature window

### 3. [`build_features`](https://github.com/Anujjadaun97/tracking-barbell-exercises/blob/main/src/features/build_features.ipynb)
Engineers a rich feature set from the cleaned signal:
- **Temporal features** — rolling mean, standard deviation, min/max per window
- **Frequency-domain features** — Fast Fourier Transform (FFT) magnitude components
- **PCA** — dimensionality reduction to capture dominant motion axes

### 4. [`train_model`](https://github.com/Anujjadaun97/tracking-barbell-exercises/blob/main/models/train_model.ipynb)
Trains and cross-validates multiple classifiers:
- Random Forest *(best performer)*
- Support Vector Machine (SVM)
- Neural Network (MLP)

Evaluation uses a held-out test set. Outputs confusion matrices and feature importance charts to `reports/figures/`. Best model is serialised to `models/`.

### 5. [`count_reps`](https://github.com/Anujjadaun97/tracking-barbell-exercises/blob/main/src/features/count_repetitions.ipynb)
Uses peak detection on the dominant acceleration axis to count repetitions per exercise set — without needing a model prediction.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/Anujjadaun97/tracking-barbell-exercises.git
cd tracking-barbell-exercises
pip install -r requirements.txt
```

### Run the pipeline

Run each step in order:

```bash
python src/make_dataset.py
python src/remove_outliers.py
python src/build_features.py
python src/train_model.py
python src/count_reps.py
```

> **Note:** Raw MetaMotion CSV files should be placed in `data/external/` before running the pipeline.

---

## 📊 Results

| Model | Accuracy |
|---|---|
| Random Forest | ~99% |
| Neural Network (MLP) | ~98% |
| Support Vector Machine | ~95% |

Confusion matrices and feature importance plots are saved in `reports/figures/` after running `train_model.py`.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data loading, merging, windowing |
| `numpy` | Numerical operations |
| `scikit-learn` | Model training, evaluation, PCA |
| `scipy` | FFT, peak detection |
| `matplotlib` / `seaborn` | Visualisations |

---

## 🙋 Author

**Anuj Jadaun**  
[GitHub](https://github.com/Anujjadaun97)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

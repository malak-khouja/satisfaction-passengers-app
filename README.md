# Passenger Satisfaction Prediction System

A machine learning-powered system to predict passenger satisfaction based on various flight and service factors. This project combines data exploration, model training, and a full-stack web application for predictions.

## 📋 Project Overview

This system predicts passenger satisfaction levels using a K-Nearest Neighbors (KNN) machine learning model. It features:
- Data exploration and analysis
- ML model training and optimization
- REST API backend with FastAPI
- Interactive dashboard with React & Vite
- Passenger satisfaction prediction form

## 🗂️ Project Structure

```
.
├── backend/                    # Python backend services
│   ├── api/                   # FastAPI REST API
│   │   └── main.py           # API endpoints
│   ├── data/                  # Training and test datasets
│   │   ├── train.csv
│   │   └── test.csv
│   ├── models/                # Trained model artifacts
│   │   ├── satisfaction_knn_model.joblib
│   │   ├── scaler.joblib
│   │   └── feature_order.json
│   ├── notebook/              # Jupyter notebooks for analysis
│   │   └── exploration.ipynb
│   ├── exploration.py         # Data exploration script
│   ├── train_model.py         # Model training script
│   └── env/                   # Python virtual environment
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Home.jsx
│   │   │   ├── NavBar.jsx
│   │   │   ├── SatisfactionForm.jsx
│   │   │   └── dashbord.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── dashbord/                  # Dashboard application
│   ├── app.py
│   └── package.json
│
├── image/                     # Project images/assets
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   # Windows
   env\Scripts\activate
   
   # macOS/Linux
   source env/bin/activate
   ```

3. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the API server:
   ```bash
   python api/main.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

### Dashboard Setup

1. Navigate to the dashboard directory:
   ```bash
   cd dashbord
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the dashboard:
   ```bash
   python app.py
   ```

## 📊 Data

### Dataset Files

- **train.csv**: Training dataset with passenger satisfaction records
- **test.csv**: Test dataset for model evaluation

### Data Exploration

Run the exploration script to analyze the data:
```bash
python backend/exploration.py
```

View the detailed analysis report:
```
backend/rapport_analyse_exploratrice.md
```

## 🤖 Machine Learning Model

### Training

Train the KNN model with:
```bash
python backend/train_model.py
```

### Model Artifacts

The trained model components are stored in `backend/models/`:
- **satisfaction_knn_model.joblib**: Trained KNN model
- **scaler.joblib**: Feature scaler for data normalization
- **feature_order.json**: Feature column ordering for consistency

## 🔌 API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /`: Health check
- `POST /predict`: Make a prediction
  - Request body: JSON with passenger features
  - Response: Predicted satisfaction level

Detailed API documentation available at `http://localhost:8000/docs` when the server is running.

## 🎨 User Interface

### Components

- **Home**: Landing page with project overview
- **NavBar**: Navigation menu
- **SatisfactionForm**: Form to input passenger details and get predictions
- **Dashboard**: Visualization of predictions and analytics

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/train_model.py` | Model training pipeline |
| `backend/exploration.py` | Data exploration and visualization |
| `backend/api/main.py` | FastAPI application and endpoints |
| `frontend/src/components/SatisfactionForm.jsx` | Prediction input form |
| `backend/models/satisfaction_knn_model.joblib` | Trained ML model |

## 🛠️ Technologies Used

### Backend
- Python 3.x
- FastAPI
- scikit-learn
- pandas
- numpy
- joblib

### Frontend
- React
- Vite
- JavaScript/JSX

### Data Science
- Jupyter Notebook
- Pandas
- Scikit-learn
- Matplotlib/Plotly

## 📝 Notes

- The model uses K-Nearest Neighbors (KNN) algorithm for predictions
- Data is scaled using StandardScaler for consistent feature importance
- The frontend communicates with the backend via REST API
- Ensure the backend server is running before using the prediction features

## 🤝 Contributing

Feel free to improve the model, add new features, or enhance the UI.

## 📄 License

This project is provided as-is for educational and commercial purposes.

---

**Last Updated**: January 2026

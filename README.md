# MLOps Assignment 1 - IMDB Sentiment Analysis

This repository contains a complete CI/CD pipeline implementation for a Machine Learning Operations assignment, featuring an IMDB movie review sentiment analysis model.

## 🎯 Project Overview

- **Model**: Logistic Regression for IMDB sentiment analysis (91% accuracy)
- **Framework**: Flask web application
- **Containerization**: Docker
- **CI/CD**: GitHub Actions + Jenkins
- **Testing**: Comprehensive unit and integration tests

## 🌿 Branch Structure

- **`dev`**: Development branch for feature implementation
- **`test`**: Testing branch for automated testing workflow  
- **`master`**: Production branch for final deployments

## 🔄 CI/CD Workflow

1. **Development**: Work happens on the `dev` branch
2. **Code Quality**: Flake8 checks on every push to `dev`
3. **Testing**: Features merged to `test` branch via pull requests
4. **Automated Testing**: Unit tests, integration tests, performance tests
5. **Production**: Tested features merged to `master` branch
6. **Deployment**: Jenkins builds Docker image and deploys to production
7. **Notification**: Email alerts to admin on deployment success/failure

## 🛠️ Tools & Technologies

- **Backend**: Python 3.9, Flask 2.3.3
- **ML**: scikit-learn, pandas, joblib
- **Testing**: pytest, pytest-cov, pytest-mock
- **Code Quality**: flake8, bandit
- **Containerization**: Docker
- **CI/CD**: GitHub Actions, Jenkins
- **Version Control**: Git

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MLOPs-Assignment_1
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Web Interface: http://localhost:5000
   - Health Check: http://localhost:5000/health
   - API Endpoint: http://localhost:5000/predict

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest test_app.py -v
```

### Code Quality Checks

```bash
# Run flake8
flake8 .

# Run security scan
bandit -r .
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t mlops-sentiment-analysis .
```

### Run Container
```bash
docker run -p 5000:5000 mlops-sentiment-analysis
```

## 📋 API Documentation

### Endpoints

#### `GET /`
- **Description**: Main web interface for sentiment analysis
- **Response**: HTML page with interactive form

#### `POST /predict`
- **Description**: Predict sentiment of a movie review
- **Request Body**:
  ```json
  {
    "review": "This movie is absolutely fantastic!"
  }
  ```
- **Response**:
  ```json
  {
    "prediction": "positive",
    "confidence": 0.85,
    "original_text": "This movie is absolutely fantastic!"
  }
  ```

#### `GET /health`
- **Description**: Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy",
    "model_loaded": true,
    "vectorizer_loaded": true
  }
  ```

## 🔧 CI/CD Pipeline Configuration

### GitHub Actions Workflows

1. **Code Quality** (`.github/workflows/code-quality.yml`)
   - Triggers on push to `dev` branch
   - Runs flake8, bandit security scan
   - Checks for TODO/FIXME comments

2. **Unit Testing** (`.github/workflows/testing.yml`)
   - Triggers on push to `test` branch
   - Runs comprehensive unit tests
   - Performance and integration tests

3. **Deployment** (`.github/workflows/deploy.yml`)
   - Triggers on push to `master` branch
   - Builds and pushes Docker image
   - Triggers Jenkins job
   - Sends email notifications

4. **Admin Approval** (`.github/workflows/admin-approval.yml`)
   - Manages pull request approvals
   - Sends notifications to admins
   - Enforces branch protection rules

### Jenkins Pipeline

The `Jenkinsfile` defines a complete CI/CD pipeline:
- Code quality checks
- Unit testing with coverage
- Docker image building
- Security scanning
- Staging deployment
- Production deployment
- Email notifications

## 👥 Admin Workflow

### Branch Protection Rules
- **`dev`**: Requires 1 reviewer approval
- **`test`**: Requires 1 reviewer approval  
- **`master`**: Requires 2 reviewer approvals (including admin)

### Pull Request Process
1. Developer creates feature branch from `dev`
2. Creates PR to `dev` → Admin reviews and approves
3. Admin creates PR from `dev` to `test` → Automated testing
4. Admin creates PR from `test` to `master` → Automated deployment

## 📧 Notification System

### Email Notifications
- **Success**: Admin receives email on successful deployment
- **Failure**: Admin receives email on deployment failure
- **PR Updates**: Admin receives notifications for PR status changes

### Required Secrets
Configure these secrets in GitHub repository settings:
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password
- `JENKINS_TOKEN`: Jenkins API token
- `JENKINS_URL`: Jenkins server URL
- `ADMIN_EMAIL`: Admin email address
- `EMAIL_USERNAME`: SMTP username
- `EMAIL_PASSWORD`: SMTP password
- `ADMIN_USERS`: Comma-separated list of admin usernames

## 📊 Model Performance

- **Accuracy**: 91.11% on test set
- **Precision**: 91% (positive), 92% (negative)
- **Recall**: 92% (positive), 90% (negative)
- **F1-Score**: 91% (positive), 91% (negative)

## 🧪 Test Coverage

The project includes comprehensive test coverage:
- Unit tests for all Flask endpoints
- Model loading and prediction tests
- Text preprocessing tests
- Error handling tests
- Performance tests
- Integration tests

## 📁 Project Structure

```
MLOPs-Assignment_1/
├── app.py                          # Main Flask application
├── test_app.py                     # Comprehensive test suite
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── Jenkinsfile                     # Jenkins pipeline
├── pytest.ini                     # Pytest configuration
├── .github/
│   ├── workflows/                  # GitHub Actions workflows
│   └── BRANCH_PROTECTION.md        # Branch protection documentation
├── imdb_logreg_model.pkl           # Trained ML model
├── tfidf_vectorizer.pkl            # TF-IDF vectorizer
├── IMDB Dataset.csv                # Training dataset
└── ML_Lab07_model_Code.ipynb       # Model training notebook
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure model files exist in the project root
   - Check Python version compatibility

2. **Docker Build Failures**
   - Verify Dockerfile syntax
   - Check for missing dependencies

3. **Test Failures**
   - Run tests locally before pushing
   - Check test data and mock configurations

4. **CI/CD Pipeline Issues**
   - Verify GitHub secrets are configured
   - Check Jenkins server connectivity

## 📝 Assignment Requirements Checklist

- ✅ Model and dataset implementation
- ✅ Flask web application
- ✅ Docker containerization
- ✅ GitHub Actions workflows
- ✅ Code quality checks (flake8)
- ✅ Unit testing
- ✅ Admin approval workflow
- ✅ Branch protection rules
- ✅ Jenkins pipeline
- ✅ Email notifications
- ✅ Complete CI/CD pipeline

## 👨‍💻 Contributors

- Group Member 1: [Name]
- Group Member 2: [Name]

## 📄 License

This project is created for educational purposes as part of MLOps Assignment 1.

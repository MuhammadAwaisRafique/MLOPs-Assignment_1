# MLOps Assignment 1 - IMDB Sentiment Analysis

This project is about building a CI/CD pipeline for a movie review sentiment analysis app. The app uses a machine learning model to predict if a review is positive or negative.

## Project Overview

- **Model:** Logistic Regression for IMDB sentiment analysis
- **App:** Flask web app
- **Container:** Docker
- **CI/CD:** GitHub Actions and Jenkins
- **Testing:** Unit and integration tests

## Branches

- `dev`: For new features and changes
- `test`: For running tests before production
- `master`: For production-ready code

## How the CI/CD Pipeline Works

1. Work starts on the `dev` branch.
2. When you push to `dev`, GitHub Actions checks code quality with flake8.
3. When a feature is ready, open a pull request (PR) from `dev` to `test`. The admin reviews and approves it.
4. Merging to `test` runs all tests automatically.
5. If tests pass, open a PR from `test` to `master`. The admin reviews and approves it.
6. Merging to `master` triggers Jenkins. Jenkins builds a Docker image, pushes it to Docker Hub, and deploys the app. Jenkins also sends an email to the admin about the deployment.

## Tools Used

- Python 3.9
- Flask
- scikit-learn
- pandas
- joblib
- pytest
- flake8
- bandit
- Docker
- GitHub Actions
- Jenkins
- Git

## How to Run the App Locally

1. Clone the repo:
   ```bash
   git clone <repository-url>
   cd MLOPs-Assignment_1
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open your browser at http://localhost:5000

## How to Run Tests

```bash
pytest
# Or for coverage:
pytest --cov=app --cov-report=html
```

## How to Check Code Quality

```bash
flake8 .
bandit -r .
```

## Docker

To build and run the app in Docker:
```bash
docker build -t mlops-sentiment-analysis .
docker run -p 5000:5000 mlops-sentiment-analysis
```

## API Endpoints

- `GET /` — Main web page
- `POST /predict` — Predict sentiment. Send JSON: `{ "review": "This movie is great!" }`
- `GET /health` — Health check

## CI/CD Pipeline Details

### GitHub Actions
- **Code Quality:** Runs on `dev` branch. Checks with flake8 and bandit.
- **Testing:** Runs on `test` branch. Runs all tests.
- **Deployment:** Runs on `master` branch. Builds Docker image, triggers Jenkins, sends email.
- **Admin Approval:** Only the admin can approve and merge PRs.

### Jenkins
- Builds and tests the app
- Builds and pushes Docker image
- Deploys the app
- Sends email notifications

## Required Secrets

Set these secrets in GitHub and Jenkins (ask the admin if you need access):
- `DOCKER_USERNAME` and `DOCKER_PASSWORD`: For Docker Hub
- `JENKINS_TOKEN` and `JENKINS_URL`: For Jenkins
- `ADMIN_EMAIL`: For notifications
- `EMAIL_USERNAME` and `EMAIL_PASSWORD`: For sending emails

## How to Contribute

1. Make a new branch from `dev`:
   ```bash
   git checkout dev
   git pull
   git checkout -b your-feature-branch
   ```
2. Make your changes.
3. Commit and push:
   ```bash
   git add .
   git commit -m "Describe your change"
   git push -u origin your-feature-branch
   ```
4. Open a PR to `dev`. The admin will review and approve.
5. After merging to `dev`, follow the PR process to `test` and then to `master`.

## FAQ

**Q: Who can approve PRs?**
A: Only the admin (your partner) can approve and merge PRs.

**Q: What if a test fails?**
A: Fix the code and push again. The pipeline will rerun.

**Q: How do I get access to secrets?**
A: Ask the admin to add them for you.

## Contributors

- Group Member 1: Zaim Abbasi
- Group Member 2: Awais Rafique

## License

This project is for MLOps Assignment 1.

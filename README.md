# FakeNewsHunter

A Django web application that uses Machine Learning and Natural Language Processing to detect fake news articles with full user authentication and personalization features.

## Features

- **Web Scraping**: Extracts article content, title, author, and publication date using `newspaper3k`
- **ML Prediction**: Uses a trained scikit-learn model to classify articles as Real/Fake
- **Sentiment Analysis**: Analyzes article sentiment using TextBlob
- **Named Entity Recognition**: Extracts entities using spaCy
- **Trust Score**: Evaluates source domain credibility
- **User Authentication**: Complete registration, login, logout, and password reset system
- **User Profiles**: Personalized profiles with full name, bio, and profile pictures
- **Personalized History**: User-specific analysis history with filtering and statistics
- **Session Management**: Secure session-based authentication
- **Beautiful UI**: Modern Bootstrap-based interface with responsive design

## Installation

1. **Clone the repository and navigate to the project folder**
   ```bash
   cd C:\Users\nitya\Desktop\Fake
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download required NLP models**
   ```bash
   python -m spacy download en_core_web_sm
   python -m textblob.download_corpora
   ```

4. **Train the ML model**
   ```bash
   python core/train_model.py
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser and go to**: http://127.0.0.1:8000/

## User Authentication Features

### Registration & Login
- **User Registration**: Create accounts with username, email, and password
- **Login/Logout**: Secure session-based authentication
- **Profile Management**: Edit personal information and upload profile pictures

### User Profiles
- **Personal Information**: Full name, bio, and profile picture
- **Profile Pictures**: Image upload with automatic resizing
- **Display Names**: Customizable display names or username fallback

### Personalized Features
- **My History**: User-specific analysis history with filtering
- **Personal Statistics**: Individual analysis statistics (total, real, fake)
- **Analysis Management**: Delete individual analyses or clear entire history
- **Anonymous Analysis**: Analyze articles without registration

## How It Works

### 1. Web Scraping (`core/scraper.py`)
- Uses `newspaper3k` to extract article content
- Handles various news websites automatically
- Extracts title, content, author, and publication date

### 2. Machine Learning (`core/train_model.py`)
- Trains a Logistic Regression model with TF-IDF features
- Uses sample dataset with fake/real news indicators
- Saves trained model as `fake_news_model.joblib`

### 3. NLP Analysis (`core/nlp_analysis.py`)
- **ML Prediction**: Uses trained model to classify articles
- **Sentiment Analysis**: TextBlob for sentiment scoring
- **Entity Recognition**: spaCy for named entity extraction
- **Trust Score**: Domain-based credibility assessment

### 4. User Management
- **UserProfile Model**: OneToOneField relationship with Django User
- **Authentication Views**: Registration, login, profile management
- **Session Security**: Django's built-in session management
- **Message Framework**: Success/error notifications

### 5. Fallback System
- If ML model fails, uses heuristic-based detection
- Analyzes text for fake news indicators
- Provides confidence scores

## Usage

### For Anonymous Users
1. **Enter a news article URL** in the form
2. **Wait for analysis** (scraping + ML processing)
3. **View results** including prediction, sentiment, and entities
4. **Register** to save your analysis history

### For Registered Users
1. **Sign in** to your account
2. **Analyze articles** - all results are automatically saved
3. **View My History** for personalized analysis tracking
4. **Manage your profile** with personal information
5. **Filter analyses** by Real/Fake prediction
6. **Download or delete** individual analyses

## Technical Stack

- **Backend**: Django 4.2
- **Authentication**: Django's built-in auth system
- **ML**: scikit-learn, joblib
- **NLP**: spaCy, TextBlob, NLTK
- **Web Scraping**: newspaper3k, BeautifulSoup
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite
- **Image Handling**: Pillow

## Model Performance

- **Accuracy**: ~75% on sample dataset
- **Features**: TF-IDF with 1-2 gram features
- **Algorithm**: Logistic Regression
- **Fallback**: Heuristic-based detection

## Customization

### Adding More Training Data
Edit `core/train_model.py` and add more examples to:
- `fake_texts` list for fake news examples
- `real_texts` list for real news examples

### Improving Trust Score
Edit `core/nlp_analysis.py` and update:
- `trusted_domains` list
- `unreliable_domains` list

### Enhancing User Features
- Add email verification
- Implement social authentication (django-allauth)
- Add user roles and permissions
- Create user analytics dashboard
- Add password reset functionality

### Enhancing ML Model
- Use larger datasets
- Try different algorithms (Random Forest, SVM)
- Add more features (domain info, author credibility)

## Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **Session Security**: Secure session management
- **Password Validation**: Django's built-in password strength validation
- **Login Required**: Protected views with @login_required decorator
- **User-Specific Data**: Users can only access their own analyses

## Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **NLTK data missing**
   ```bash
   python -m textblob.download_corpora
   ```

3. **ML model not found**
   ```bash
   python core/train_model.py
   ```

4. **Import errors**
   ```bash
   pip install -r requirements.txt
   ```

5. **Media files not loading**
   - Ensure `media/` directory exists
   - Check `MEDIA_URL` and `MEDIA_ROOT` in settings.py

6. **User profile not created**
   - Check that signals are properly registered
   - Run `python manage.py migrate` to ensure all migrations are applied

## License

MIT License - feel free to use and modify!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This is a demonstration project. For production use, consider:
- Using larger, more diverse training datasets
- Implementing more sophisticated ML models
- Adding email verification
- Implementing social authentication
- Adding API rate limiting
- Using a production database (PostgreSQL)
- Setting up proper email backend for password reset 
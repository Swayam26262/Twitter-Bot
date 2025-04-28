import random
import json
import os
from logger import logger

class ContentGenerator:
    def __init__(self):
        self.load_content_database()
    
    def load_content_database(self):
        """Load content database or create if it doesn't exist"""
        try:
            if not os.path.exists('content'):
                os.makedirs('content')
                
            content_file = 'content/ml_snippets.json'
            
            if not os.path.exists(content_file):
                # Create initial content database
                self.content_db = {
                    'ml_snippets': self.get_default_ml_snippets(),
                    'code_tips': self.get_default_code_tips(),
                    'interview_questions': self.get_default_interview_questions()
                }
                
                # Save to file
                with open(content_file, 'w') as f:
                    json.dump(self.content_db, f, indent=2)
            else:
                # Load existing database
                with open(content_file, 'r') as f:
                    self.content_db = json.load(f)
                    
            logger.info(f"Loaded content database with {len(self.content_db['ml_snippets'])} ML snippets")
            
        except Exception as e:
            logger.error(f"Error loading content database: {e}")
            # Fallback to defaults
            self.content_db = {
                'ml_snippets': self.get_default_ml_snippets(),
                'code_tips': self.get_default_code_tips(),
                'interview_questions': self.get_default_interview_questions()
            }
    
    def get_default_ml_snippets(self):
        """Default ML snippets to use if no database exists"""
        return [
            {
                "title": "Image Classification with CNN",
                "content": (
                    "📸 Build a Convolutional Neural Network in 5 steps:\n\n"
                    "```python\n"
                    "import tensorflow as tf\n"
                    "from tensorflow.keras import layers\n\n"
                    "# 1. Create model\n"
                    "model = tf.keras.Sequential([\n"
                    "    layers.Conv2D(32, (3, 3), activation='relu'),\n"
                    "    layers.MaxPooling2D(),\n"
                    "    layers.Conv2D(64, (3, 3), activation='relu'),\n"
                    "    layers.MaxPooling2D(),\n"
                    "    layers.Flatten(),\n"
                    "    layers.Dense(128, activation='relu'),\n"
                    "    layers.Dense(10, activation='softmax')\n"
                    "])\n\n"
                    "# 2. Compile\n"
                    "model.compile(optimizer='adam',\n"
                    "              loss='sparse_categorical_crossentropy',\n"
                    "              metrics=['accuracy'])\n"
                    "```\n\n"
                    "#MachineLearning #DeepLearning #Python"
                ),
                "hashtags": ["#MachineLearning", "#DeepLearning", "#Python", "#ComputerVision"]
            },
            {
                "title": "NLP Sentiment Analysis",
                "content": (
                    "💬 Sentiment Analysis in 5 lines of code:\n\n"
                    "```python\n"
                    "from transformers import pipeline\n\n"
                    "# Load sentiment analysis pipeline\n"
                    "sentiment_analyzer = pipeline('sentiment-analysis')\n\n"
                    "# Analyze a sample text\n"
                    "result = sentiment_analyzer('I love machine learning!')\n"
                    "print(f\"Label: {result[0]['label']}, Score: {result[0]['score']:.4f}\")\n"
                    "# Output: Label: POSITIVE, Score: 0.9998\n"
                    "```\n\n"
                    "#NLP #MachineLearning #Python #HuggingFace"
                ),
                "hashtags": ["#NLP", "#MachineLearning", "#Python", "#HuggingFace"]
            },
            {
                "title": "Time Series Forecasting",
                "content": (
                    "📈 Time Series Forecasting with LSTM:\n\n"
                    "```python\n"
                    "import tensorflow as tf\n"
                    "from tensorflow.keras.models import Sequential\n"
                    "from tensorflow.keras.layers import LSTM, Dense\n\n"
                    "# Create LSTM model\n"
                    "model = Sequential()\n"
                    "model.add(LSTM(50, activation='relu', input_shape=(time_steps, features)))\n"
                    "model.add(Dense(1))\n"
                    "model.compile(optimizer='adam', loss='mse')\n\n"
                    "# Train model\n"
                    "model.fit(X_train, y_train, epochs=100, validation_split=0.2)\n\n"
                    "# Make predictions\n"
                    "predictions = model.predict(X_test)\n"
                    "```\n\n"
                    "#TimeSeries #LSTM #MachineLearning #DataScience"
                ),
                "hashtags": ["#TimeSeries", "#LSTM", "#MachineLearning", "#DataScience"]
            },
            {
                "title": "K-Means Clustering",
                "content": (
                    "🔍 Customer Segmentation with K-Means Clustering:\n\n"
                    "```python\n"
                    "import numpy as np\n"
                    "from sklearn.cluster import KMeans\n"
                    "import matplotlib.pyplot as plt\n\n"
                    "# Generate sample data\n"
                    "X = customer_data[['annual_income', 'spending_score']]\n\n"
                    "# Find optimal number of clusters (Elbow method)\n"
                    "wcss = []\n"
                    "for i in range(1, 11):\n"
                    "    kmeans = KMeans(n_clusters=i, random_state=42)\n"
                    "    kmeans.fit(X)\n"
                    "    wcss.append(kmeans.inertia_)\n\n"
                    "# Apply K-Means with optimal cluster number\n"
                    "kmeans = KMeans(n_clusters=5, random_state=42)\n"
                    "clusters = kmeans.fit_predict(X)\n"
                    "```\n\n"
                    "#Clustering #DataScience #MachineLearning"
                ),
                "hashtags": ["#Clustering", "#DataScience", "#MachineLearning", "#Python"]
            },
            {
                "title": "Random Forest for Classification",
                "content": (
                    "🌲 Random Forest Classifier in action:\n\n"
                    "```python\n"
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import accuracy_score, classification_report\n\n"
                    "# Split data\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    features, target, test_size=0.25, random_state=42)\n\n"
                    "# Create and train model\n"
                    "rf_model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
                    "rf_model.fit(X_train, y_train)\n\n"
                    "# Evaluate\n"
                    "predictions = rf_model.predict(X_test)\n"
                    "print(f\"Accuracy: {accuracy_score(y_test, predictions):.4f}\")\n"
                    "print(classification_report(y_test, predictions))\n"
                    "```\n\n"
                    "#RandomForest #MachineLearning #Supervised #DataScience"
                ),
                "hashtags": ["#RandomForest", "#MachineLearning", "#Supervised", "#DataScience"]
            }
        ]
    
    def get_default_code_tips(self):
        """Default coding tips to use if no database exists"""
        return [
            {
                "title": "Python List Comprehension",
                "content": (
                    "✨ Python Pro Tip: Use list comprehensions for cleaner code\n\n"
                    "```python\n"
                    "# Instead of this:\n"
                    "squares = []\n"
                    "for i in range(10):\n"
                    "    squares.append(i**2)\n\n"
                    "# Do this:\n"
                    "squares = [i**2 for i in range(10)]\n\n"
                    "# With conditions:\n"
                    "even_squares = [i**2 for i in range(10) if i % 2 == 0]\n"
                    "```\n\n"
                    "#Python #Coding #ProgrammingTips"
                ),
                "hashtags": ["#Python", "#Coding", "#ProgrammingTips", "#CleanCode"]
            },
            {
                "title": "Git Workflow",
                "content": (
                    "🔄 Git Workflow Essentials:\n\n"
                    "```bash\n"
                    "# Create a feature branch\n"
                    "git checkout -b feature/new-feature\n\n"
                    "# Make your changes\n"
                    "git add .\n"
                    "git commit -m \"Add new feature\"\n\n"
                    "# Stay updated with main branch\n"
                    "git checkout main\n"
                    "git pull\n"
                    "git checkout feature/new-feature\n"
                    "git rebase main\n\n"
                    "# Push your changes\n"
                    "git push origin feature/new-feature\n"
                    "```\n\n"
                    "#Git #DevOps #Programming #VersionControl"
                ),
                "hashtags": ["#Git", "#DevOps", "#Programming", "#VersionControl"]
            },
            {
                "title": "JavaScript Promises",
                "content": (
                    "⛓️ Modern JavaScript: Promises and Async/Await\n\n"
                    "```javascript\n"
                    "// Using promises\n"
                    "fetch('https://api.example.com/data')\n"
                    "  .then(response => response.json())\n"
                    "  .then(data => console.log(data))\n"
                    "  .catch(error => console.error(error));\n\n"
                    "// Using async/await (cleaner!)\n"
                    "async function fetchData() {\n"
                    "  try {\n"
                    "    const response = await fetch('https://api.example.com/data');\n"
                    "    const data = await response.json();\n"
                    "    console.log(data);\n"
                    "  } catch (error) {\n"
                    "    console.error(error);\n"
                    "  }\n"
                    "}\n"
                    "```\n\n"
                    "#JavaScript #WebDev #AsyncAwait #Promises"
                ),
                "hashtags": ["#JavaScript", "#WebDev", "#AsyncAwait", "#Programming"]
            }
        ]
    
    def get_default_interview_questions(self):
        """Default interview questions to use if no database exists"""
        return [
            {
                "title": "ML Interview Question",
                "content": (
                    "📝 Machine Learning Interview Question:\n\n"
                    "Q: What's the difference between bagging and boosting in ensemble learning?\n\n"
                    "A: 🔹 Bagging (Bootstrap Aggregating):\n"
                    "- Trains models in parallel on random subsets of data\n"
                    "- Reduces variance (prevents overfitting)\n"
                    "- Example: Random Forest\n\n"
                    "🔹 Boosting:\n"
                    "- Trains models sequentially, each fixing errors of previous models\n"
                    "- Reduces bias (improves prediction accuracy)\n"
                    "- Examples: AdaBoost, Gradient Boosting, XGBoost\n\n"
                    "#MachineLearning #DataScience #InterviewTips"
                ),
                "hashtags": ["#MachineLearning", "#DataScience", "#InterviewTips", "#CareerAdvice"]
            },
            {
                "title": "Coding Interview",
                "content": (
                    "🧩 Coding Interview: Finding pairs that sum to target\n\n"
                    "```python\n"
                    "def find_pairs(nums, target):\n"
                    "    # Time: O(n), Space: O(n)\n"
                    "    seen = set()\n"
                    "    pairs = []\n"
                    "    \n"
                    "    for num in nums:\n"
                    "        complement = target - num\n"
                    "        if complement in seen:\n"
                    "            pairs.append((complement, num))\n"
                    "        seen.add(num)\n"
                    "        \n"
                    "    return pairs\n\n"
                    "# Example\n"
                    "nums = [2, 7, 11, 15, 3, 6]\n"
                    "target = 9\n"
                    "print(find_pairs(nums, target))  # [(2, 7), (3, 6)]\n"
                    "```\n\n"
                    "#CodingInterview #Programming #Algorithms #DataStructures"
                ),
                "hashtags": ["#CodingInterview", "#Programming", "#Algorithms", "#DataStructures"]
            }
        ]
    
    def generate_ml_snippet(self):
        """Generate a random ML snippet"""
        try:
            snippets = self.content_db['ml_snippets']
            snippet = random.choice(snippets)
            return snippet['content']
        except Exception as e:
            logger.error(f"Error generating ML snippet: {e}")
            return "Here's a basic ML snippet! #MachineLearning #Python"
    
    def generate_code_tip(self):
        """Generate a random code tip"""
        try:
            tips = self.content_db['code_tips']
            tip = random.choice(tips)
            return tip['content']
        except Exception as e:
            logger.error(f"Error generating code tip: {e}")
            return "Here's a coding tip! #Programming #Coding"
    
    def generate_interview_question(self):
        """Generate a random interview question"""
        try:
            questions = self.content_db['interview_questions']
            question = random.choice(questions)
            content = question['content']
            
            # Truncate if exceeds Twitter's character limit (280)
            if len(content) > 280:
                # Find a good cutoff point (preferably at a newline or period)
                cutoff = content[:277].rfind('\n\n')
                if cutoff == -1:
                    cutoff = content[:277].rfind('. ')
                if cutoff == -1:
                    cutoff = 277
                content = content[:cutoff] + "..."
            
            return content
        except Exception as e:
            logger.error(f"Error generating interview question: {e}")
            return "Here's an interview question! #JobSearch #Interview" 
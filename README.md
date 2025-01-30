# Social Study - Study While Scrolling Social Media

![demo](https://cloud-7f7v8216y-hack-club-bot.vercel.app/0demo.png)

---

## Overview

**Social Study** transforms social media scrolling into an educational experience. Instead of endlessly consuming content, this web application encourages productive learning by integrating multiple-choice questions (MCQs) into your feed.

Social Study fetches the latest top posts from social media, displaying five at a time. To unlock more, users must correctly answer an MCQ in subjects such as Computing, Mathematics, Physics, Chemistry, Economics, or English. This simple yet effective system promotes learning while minimising mindless scrolling.

The platform updates every two hours via the Reddit API (PRAW), ensuring fresh content and a continuous learning experience. Whether you're revising for exams or simply looking to sharpen your knowledge, Social Study turns distraction into a study tool.

## Features

### 1. **Answer Questions**
Unlock additional social media posts by answering MCQs, keeping you engaged while reinforcing knowledge.

### 2. **Add Questions**
Expand the platform's question pool by submitting your own MCQs across different subjects.

### 3. **Dark Mode**
Reduce eye strain with a dark mode option for a more comfortable studying and browsing experience.

## Future Improvements

1. **Expand Subject Coverage**

   Broaden the variety of questions by adding topics such as Biology, History, and more.

2. **Spaced Repetition**

   Implement a system that revisits questions periodically based on user performance to enhance learning retention.

3. **Text-Based Input**

   Allow freeform text responses, with AI evaluating correctness and providing constructive feedback.

## Demo

Check out the live demo: [Social Study Demo](https://study.mengshin.me)

## Running the Website

1. Clone this repository and navigate to the project directory.
2. Install the required dependencies:

   ```bash
   pip install Flask Flask-WTF
   ```

3. Start the Flask application:

   ```bash
   flask run
   ```

4. Create a `.env` file and add your Reddit API credentials:

   ```plaintext
   CLIENT_ID=your-client-id
   CLIENT_SECRET=your-client-secret
   ```

## Updating the Posts Database

1. Install additional dependencies:

   ```bash
   pip install praw load-dotenv
   ```

2. Run the update script:

   ```bash
   python main.py
   ```

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python with Flask
- **API Integration:** Reddit API using PRAW

## Credits

1. **Stack Overflow**
2. **PRAW Documentation**
3. **Flask-WTF Documentation**
4. **ChatGPT**

(Note: Don't worry, I built most of the project myself! ChatGPT primarily helped with generating the questions database and writing this README.)
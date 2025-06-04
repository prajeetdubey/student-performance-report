# 🧠 Student Performance Report Generator

> This project generates personalized student performance reports using AI and visualization tools.

---

## ✨ Features

✅ &nbsp;📊 Parses student test data from JSON  
✅ &nbsp;🤖 Uses OpenAI GPT to generate insightful, human-like feedback *(if API key is available)*  
✅ &nbsp;📈 Generates visual accuracy chart by subject  
✅ &nbsp;📄 Outputs a clean, professional PDF report  

---

## 🛠️ Technologies Used

🧩 &nbsp;Python  
🧠 &nbsp;OpenAI GPT *(GPT-4 / GPT-3.5 via API)*  
📊 &nbsp;`matplotlib` for charting  
📝 &nbsp;`reportlab` for PDF creation  
🔐 &nbsp;`python-dotenv` for secure API key management  

---

## 🚀 How to Use

### 🧠 Option 1: With OpenAI API *(Recommended)*

1. 🔑 **Get your OpenAI API Key** from [platform.openai.com](https://platform.openai.com/account/api-keys)  
2. 🗂️ **Create a `.env` file** in the project root:

    ```env
    OPENAI_API_KEY=your-api-key-here
    ```

3. 📦 **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. ▶️ **Run the script:**

    ```bash
    python main.py
    ```

5. 📂 Your PDF report will be saved in the `report/` folder.

---

### 💡 Option 2: Without OpenAI *(Free Mode)*

If you don't have an API key, you can still generate a report using dummy feedback.

🔁 In `main.py`, replace:

```python
ai_response = call_openai(prompt)
```

with:

```python
ai_response = """
Great effort! You performed well in English, and there's room for improvement in Math and Science.
Focus on time management and review key concepts regularly to improve overall performance.
"""
```

Then run the script as usual.

---

## 📂 Sample Input Format

The script expects a JSON file like `data/sample_submission.json`:

```json
[
  {
    "accuracy": 61,
    "totalMarkScored": 30,
    "totalAttempted": 50,
    "totalCorrect": 31,
    "totalTimeTaken": 900,
    "test": {
      "totalQuestions": 60
    },
    "subjects": [
      {
        "subjectId": { "$oid": "abc1233d90" },
        "accuracy": 52,
        "timeTaken": 300,
        "totalQuestions": 19,
        "totalAttempted": 15,
        "totalCorrect": 10
      }
    ]
  }
]
```

---

## 📄 Output

🧾 The PDF report includes:

- 🤖 AI-generated (or dummy) feedback  
- 📊 Subject-wise accuracy bar chart  
- ✨ Professional layout with clear visual insights  

---

## 🙋‍♂️ Author

👨‍💻 Developed by **Prajeet Dubey** 
📬 Reach out via [GitHub](https://github.com/prajeetdubey) or [LinkedIn](https://www.linkedin.com/in/prajeetdubey/)

---

## 📜 License

📝 [MIT License](LICENSE)

# Student Performance AI Feedback System

## 📌 Overview
This project analyzes student test performance and uses OpenAI's GPT to generate constructive feedback.

## ⚙️ Tech Stack
- Python
- OpenAI API
- ReportLab
- Matplotlib

## 📤 API Used
- [OpenAI GPT-4 API](https://platform.openai.com/)

## ✏️ Prompt Logic
We dynamically inject test metrics into a Jinja2 template to generate a personalized prompt, focusing on:
- Motivation
- Strength/weakness insights
- Suggestions

## 📄 Report Structure
1. Motivating message
2. Subject-wise breakdown
3. Time vs Accuracy plot
4. Actionable suggestions

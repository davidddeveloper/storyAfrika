"""
    gemini: basic setup for using gemini for assistive writing
"""

import google.generativeai as genai
import os


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

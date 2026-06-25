import time
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_llm(prompt, system="You are a helpful assistant.", max_tokens=1000):
    full_prompt = f"{system}\n\n{prompt}"
    
    for attempt in range(3):
        try:
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower() or "retry" in str(e).lower():
                wait_time = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time} seconds... (attempt {attempt + 1}/3)")
                time.sleep(wait_time)
            else:
                raise e
    
    return "Error: Max retries reached. Try again in a few minutes."
# Test 1 — Simple question
print("=== Test 1: Simple Question ===")
response = ask_llm("What is RAG in AI? Explain in 3 bullet points.")
print(response)
print()

# Test 2 — Custom system prompt
print("=== Test 2: Custom System Prompt ===")
response = ask_llm(
    prompt="What are the top 3 ways small businesses waste time?",
    system="You are a business efficiency consultant. Be direct and practical. No fluff."
)
print(response)
print()

# Test 3 — Summarise web content
print("=== Test 3: Summarise Web Content ===")
from script2_web_fetcher import fetch_webpage, extract_text

html = fetch_webpage("https://en.wikipedia.org/wiki/Prompt_engineering")
if html:
    text = extract_text(html)
    first_2000 = text[:2000]
    response = ask_llm(
        prompt=f"Summarise this content in 5 bullet points:\n\n{first_2000}",
        system="You are a technical writer. Be concise and clear."
    )
    print(response)
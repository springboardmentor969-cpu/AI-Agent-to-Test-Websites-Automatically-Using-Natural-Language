"""
Test if environment variables are loading correctly
"""
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

print("Testing environment variable loading...\n")

groq_key = os.getenv("GROQ_API_KEY")

if groq_key:
    print(f"✓ GROQ_API_KEY found: {groq_key[:20]}...")
else:
    print("✗ GROQ_API_KEY not found in environment")

print("\nAll environment variables:")
for key, value in os.environ.items():
    if "GROQ" in key:
        print(f"  {key}: {value[:20] if value else 'None'}...")

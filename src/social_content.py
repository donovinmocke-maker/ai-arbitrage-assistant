from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SocialContentGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.business_name = "CC Palms LLC"

    def generate_post(self, topic="recent project"):
        prompt = f"""Create a professional, engaging social media post for {self.business_name}, a home improvement contractor specializing in remodeling, plumbing, electrical, and general contracting.

Topic: {topic}

Requirements:
- Warm, trustworthy, professional tone
- Include a strong call-to-action (get a free quote, schedule a site visit, etc.)
- Relevant hashtags
- Short image generation prompt suitable for Grok image model

Return in this format:
CAPTION: [full caption]
IMAGE_PROMPT: [detailed prompt for image]
HASHTAGS: [list]"""

        response = self.client.chat.completions.create(
            model="grok-4.3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()

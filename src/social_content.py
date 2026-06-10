from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class SocialContentGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.business_name = "CC Palms LLC"

    def generate_post(self, topic="recent project"):
        # Generate caption + prompt
        text_prompt = f"""Create a professional social media post for {self.business_name} about: {topic}

Return in this exact format:
CAPTION: [engaging caption]
IMAGE_PROMPT: [detailed image prompt for Grok image model]"""

        text_response = self.client.chat.completions.create(
            model="grok-4.3",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.8,
            max_tokens=700
        )
        content = text_response.choices[0].message.content.strip()

        # Extract parts
        caption = content.split("IMAGE_PROMPT:")[0].replace("CAPTION:", "").strip() if "CAPTION:" in content else content
        image_prompt = content.split("IMAGE_PROMPT:")[-1].strip() if "IMAGE_PROMPT:" in content else f"Professional photo of {topic} for home improvement marketing"

        # Generate real image with Grok
        try:
            image_response = self.client.images.generate(
                model="grok-2-image",  # Grok's image model
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url
        except:
            image_url = None  # Fallback if image gen fails

        return {
            "caption": caption,
            "image_prompt": image_prompt,
            "image_url": image_url
        }

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
        # Text prompt for caption + image description
        text_prompt = f"""Create a professional social media post for {self.business_name} about: {topic}

Return in this exact format:
CAPTION: [engaging caption]
IMAGE_PROMPT: [detailed prompt for image generation]"""

        text_response = self.client.chat.completions.create(
            model="grok-4.3",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.8,
            max_tokens=700
        )
        content = text_response.choices[0].message.content.strip()

        # Extract parts
        caption = content.split("IMAGE_PROMPT:")[0].replace("CAPTION:", "").strip() if "CAPTION:" in content else content
        image_prompt = content.split("IMAGE_PROMPT:")[-1].strip() if "IMAGE_PROMPT:" in content else f"Professional photo of {topic} for {self.business_name}"

        # Try to generate real image
        image_url = None
        try:
            image_response = self.client.images.generate(
                model="grok-2-image-1212",   # Current Grok image model
                prompt=image_prompt + ", high quality, realistic, marketing style",
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url
        except Exception as e:
            image_url = None
            print("Image generation failed:", str(e))

        return {
            "caption": caption,
            "image_prompt": image_prompt,
            "image_url": image_url
        }

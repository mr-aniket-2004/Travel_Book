import requests
from django.conf import settings 

HUGGINGFACE_API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def generate_story(travellist_dic):
    payload = {
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": f"""
You are a professional travel blogger.

Using the following trip information, create a high-quality travel blog that can be directly filled into a blog creation form.

TRIP INFORMATION:
- Destination / Title: {travellist_dic.get("title")}
- Location / About: {travellist_dic.get("about")}
- Start Date: {travellist_dic.get("start_date")}
- End Date: {travellist_dic.get("end_date")}
- Description: {travellist_dic.get("description")}
- Highlights: {travellist_dic.get("highlights")}
- Category: {travellist_dic.get("type")}

OUTPUT FORMAT (VERY IMPORTANT):
Return the content in the EXACT structure below.
Do NOT add extra text outside these sections.

===BLOG_TITLE===
Write a catchy, friendly blog title (max 12 words)

===CATEGORY===
Use the provided category only

===SHORT_SUMMARY===
Write a concise 2-3 sentence summary suitable for a blog preview card

===BODY===
Write a friendly, engaging travel blog of 400–500 words using the structure below.
Use headings and paragraphs only (no bullet points).

## Introduction
Introduce the destination and why it is worth visiting.

## Top Attractions
Describe only well-known attractions related to the destination.
Do NOT invent places.

## Culture & Local Life
Discuss traditions, people, festivals, and daily lifestyle.

## Food & Cuisine
Highlight popular local dishes and food experiences.

## Things to Do & Experiences
Describe activities such as sightseeing, nature, adventure, or relaxation.


IMPORTANT RULES:
- Keep the tone friendly and human-like
- Do NOT invent facts, places, or dates
- Base the content strictly on the provided trip information
- Avoid emojis
- Output clean, ready-to-edit blog content
"""
        }
    ],
    "temperature": 0.7,
    "max_tokens": 700
}



    response = requests.post(
        HUGGINGFACE_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=90
    )

    # print(response.status_code, response.text)

    if response.status_code != 200:
        return f"Story generation failed ({response.status_code})"

    data = response.json()

    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    else:
        return "AI response not available at the moment."


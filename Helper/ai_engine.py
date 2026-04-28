"""
ai_engine.py  —  Helper.ai generation functions
Uses Groq API (llama-3.3-70b-versatile) — completely free tier.
Install:  pip install groq
Set env:  GROQ_API_KEY=your_key
"""

import os, json, re
from groq import Groq

# Configure Groq client
API_KEY = os.environ.get('GROQ_API_KEY', '').strip()

if not API_KEY:
    _client = None
else:
    _client = Groq(api_key=API_KEY)

# ── Shared helper ────────────────────────────────────────────────
def _ask(system: str, user: str, max_tokens: int = 2000) -> str:
    if not _client:
        raise Exception("Groq API key not configured. Please set GROQ_API_KEY in Vercel Environment Variables.")
    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=max_tokens,
        temperature=0.7,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ]
    )
    return response.choices[0].message.content.strip()

def _parse_json(raw: str) -> dict | list:
    """Strip markdown fences then parse JSON."""
    cleaned = re.sub(r'^```(?:json)?\s*', '', raw.strip())
    cleaned = re.sub(r'\s*```$', '', cleaned.strip())
    return json.loads(cleaned)

# ── PPT Generator ─────────────────────────────────────────────────
def generate_ppt(topic: str) -> dict:
    system = (
        "You are an expert presentation designer. "
        "Respond ONLY with valid JSON — no markdown, no extra text."
    )
    prompt = f"""
Create a complete presentation on: "{topic}"

Return JSON with this exact structure:
{{
  "title": "...",
  "subtitle": "...",
  "theme_color": "#5340B7",
  "slides": [
    {{
      "slide_number": 1,
      "type": "title",
      "heading": "...",
      "body": "...",
      "bullet_points": [],
      "speaker_notes": "..."
    }}
  ]
}}

Rules:
- 8-12 slides total
- slide types: title | content | bullets | image_suggestion | conclusion
- bullet_points: list of strings (empty array if not applicable)
- speaker_notes: 1-2 sentences per slide
- body: concise paragraph (1-3 sentences)
"""
    raw = _ask(system, prompt, max_tokens=3000)
    data = _parse_json(raw)
    return data if isinstance(data, dict) else {'slides': data}

# ── Report Generator ──────────────────────────────────────────────
def generate_report(topic: str) -> dict:
    system = (
        "You are an expert academic report writer. "
        "Respond ONLY with valid JSON — no markdown, no extra text."
    )
    prompt = f"""
Generate a structured academic report on: "{topic}"

Return JSON:
{{
  "title": "...",
  "abstract": "...",
  "sections": [
    {{"heading": "Introduction",         "content": "..."}},
    {{"heading": "Problem Statement",    "content": "..."}},
    {{"heading": "Methodology",          "content": "..."}},
    {{"heading": "Results & Analysis",   "content": "..."}},
    {{"heading": "Solution / Discussion","content": "..."}},
    {{"heading": "Conclusion",           "content": "..."}},
    {{"heading": "References",           "content": "..."}}
  ],
  "word_count_estimate": 1200,
  "keywords": ["...", "..."]
}}

Each section content should be 2-4 solid paragraphs.
References should list 3-5 credible sources.
"""
    raw = _ask(system, prompt, max_tokens=4000)
    return _parse_json(raw)

# ── Smart Notes Generator ─────────────────────────────────────────
def generate_notes(text: str) -> dict:
    system = (
        "You are an expert study-notes creator. "
        "Respond ONLY with valid JSON — no markdown, no extra text."
    )
    prompt = f"""
Convert the following input into clean, structured study notes:

INPUT:
\"\"\"{text}\"\"\"

Return JSON:
{{
  "title": "...",
  "summary": "...",
  "key_points": ["...", "..."],
  "sections": [
    {{
      "heading": "...",
      "content": "...",
      "important_terms": [{{"term": "...", "definition": "..."}}]
    }}
  ],
  "flashcards": [
    {{"question": "...", "answer": "..."}}
  ],
  "exam_tips": ["...", "..."]
}}

Rules:
- key_points: 4-8 bullet points
- sections: 2-5 logical sections
- flashcards: 5-8 Q&A pairs for exam prep
- exam_tips: 2-4 actionable study tips
"""
    raw = _ask(system, prompt, max_tokens=3000)
    return _parse_json(raw)

import os
import json
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from api.core.models import BlogSection, BlogPlan, FinalBlog
from typing import Type, TypeVar, Any
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def get_llm_client_and_model(requested_model: str):
    """
    Dynamically select the LLM client and model based on available API keys in environment.
    Supports Groq, Gemini, and OpenAI.
    """
    groq_key = os.environ.get("GROQ_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if "gemini" in requested_model.lower():
        if gemini_key:
            return OpenAI(
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=gemini_key
            ), requested_model
        elif groq_key:
            return OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=groq_key
            ), "llama-3.3-70b-versatile"
        elif openai_key:
            return OpenAI(api_key=openai_key), "gpt-4o-mini"
        else:
            raise ValueError("No API Key set! Please add GEMINI_API_KEY or GROQ_API_KEY or OPENAI_API_KEY to your .env file.")

    # Default logic: prefer Groq -> Gemini -> OpenAI
    if groq_key:
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_key
        ), "llama-3.3-70b-versatile"
    elif gemini_key:
        return OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=gemini_key
        ), "gemini-3.6-flash"
    elif openai_key:
        return OpenAI(api_key=openai_key), "gpt-4o-mini"
    else:
        raise ValueError("No API Key set! Please configure GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY in your .env file.")


import time
import re

def clean_json_string(s: str) -> str:
    if not s:
        return s
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
        s = re.sub(r"\n?```$", "", s).strip()
    s = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', s)
    return s

def call_structured_llm(model: str, system_prompt: str, user_prompt: str, response_model: Type[T]) -> T:
    """
    Call the LLM and enforce a structured Pydantic response format with automatic retries and JSON sanitization.
    """
    client, target_model = get_llm_client_and_model(model)
    
    schema_json = json.dumps(response_model.model_json_schema())
    full_system_prompt = (
        f"{system_prompt}\n\n"
        "### OUTPUT REQUIREMENT ###\n"
        "You MUST return a valid JSON object that follows the schema below. "
        "IMPORTANT: Do not return the schema itself. Return a JSON INSTANCE that represents the data.\n"
        f"SCHEMA: {schema_json}"
    )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            try:
                return response_model.model_validate_json(content)
            except Exception:
                cleaned = clean_json_string(content)
                data = json.loads(cleaned, strict=False)
                return response_model.model_validate(data)
        except Exception as e:
            err_msg = str(e)
            print(f"[DEBUG] Attempt {attempt + 1}/{max_retries} failed ({target_model}): {err_msg}")
            if attempt < max_retries - 1 and ("503" in err_msg or "UNAVAILABLE" in err_msg or "rate_limit" in err_msg.lower()):
                time.sleep(2 * (attempt + 1))
                continue
            raise


def run_pydantic_ai_pipeline(topic: str) -> FinalBlog:
    """
    Structured multi-agent pipeline using Pydantic for validation.
    """

    print(f"[AI] Planning: {topic}...")
    plan = call_structured_llm(
        model="llama-3.3-70b-versatile",
        system_prompt="You are a high-level Blog Planner. Create a structured 5+ section outline for a blog post.",
        user_prompt=f"Topic: {topic}",
        response_model=BlogPlan
    )
    
    print(f"[AI] Researching: {plan.suggested_title}...")
    researched_plan = call_structured_llm(
        model="llama-3.3-70b-versatile",
        system_prompt=(
            "You are a Researcher. For each section in the provided BlogPlan JSON, add in-depth research_notes. "
            "CRITICAL: You MUST preserve the 'topic' and 'suggested_title' fields exactly as they are in the input. "
            "The research_notes field MUST be a single cohesive Markdown string. DO NOT use lists or objects."
        ),
        user_prompt=f"Please research this plan and fill in the missing research_notes: {plan.model_dump_json()}",
        response_model=BlogPlan
    )
    
    print(f"[AI] Writing: {researched_plan.suggested_title}...")
    final_blog = call_structured_llm(
        model="llama-3.3-70b-versatile",
        system_prompt=(
            "You are a Professional Blogger. Write a comprehensive, high-quality long-form blog post (1000+ words) in Markdown format. "
            "Use the provided research_notes and outline to create a structured, engaging, and SEO-optimized post. "
            "Your output must be a JSON object with 'title', 'content' (Markdown), and 'word_count' fields."
        ),
        user_prompt=f"Please write the final blog post based on this researched plan: {researched_plan.model_dump_json()}",
        response_model=FinalBlog
    )
    
    return final_blog
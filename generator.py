import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_tests(endpoint_description: str) -> str:
    prompt = f"""You are a senior QA engineer. Generate PyTest tests for the following API endpoint.

Endpoint description:
{endpoint_description}

Requirements:
- Use the 'requests' library to make HTTP calls
- Cover: happy path, missing fields, invalid data, edge cases
- Each test must have a clear name and docstring
- Return ONLY the Python code, no explanations

Base URL: https://jsonplaceholder.typicode.com
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def save_tests(code: str, filename: str = "tests/test_placeholder.py"):
    # Strip markdown code blocks if present
    code = code.replace("```python", "").replace("```", "").strip()
    with open(filename, "w") as f:
        f.write(code)
    print(f"✅ Tests saved to {filename}")


if __name__ == "__main__":
    endpoint = """
    GET /posts/{id}
    Returns a single blog post by ID.
    Response fields: id (int), title (string), body (string), userId (int)
    """

    print("🤖 Generating tests with Claude API...")
    code = generate_tests(endpoint)
    print("Generated code preview:")
    print(code[:300])
    save_tests(code)
    print("✅ Done!")
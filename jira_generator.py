import os
import anthropic
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

jira = JIRA(
    server=os.getenv("JIRA_URL"),
    basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)


def get_ticket_description(ticket_id: str) -> str:
    issue = jira.issue(ticket_id)
    title = issue.fields.summary
    description = issue.fields.description or "No description provided"
    acceptance = ""

    if hasattr(issue.fields, "customfield_10016"):
        acceptance = str(issue.fields.customfield_10016) or ""

    return f"""
Ticket: {ticket_id}
Title: {title}
Description: {description}
Acceptance criteria: {acceptance}
"""


def generate_tests_from_ticket(ticket_id: str) -> str:
    ticket_info = get_ticket_description(ticket_id)
    print(f"📋 Got ticket info:\n{ticket_info[:300]}...")

    prompt = f"""You are a senior QA engineer. Generate PyTest API tests based on this Jira ticket.

{ticket_info}

Requirements:
- Use the 'requests' library
- Cover: happy path, negative cases, edge cases, acceptance criteria
- Each test must have a clear name and docstring
- Return ONLY Python code, no explanations, no markdown backticks
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def save_tests(code: str, ticket_id: str):
    filename = f"tests/test_{ticket_id.lower().replace('-', '_')}.py"
    code = code.replace("```python", "").replace("```", "").strip()
    with open(filename, "w") as f:
        f.write(code)
    print(f"✅ Tests saved to {filename}")
    return filename


if __name__ == "__main__":
    ticket_id = input("Enter Jira ticket ID (e.g. QA-123): ").strip()
    print(f"🤖 Generating tests for {ticket_id}...")
    code = generate_tests_from_ticket(ticket_id)
    filename = save_tests(code, ticket_id)
    print(f"\n🚀 Run tests with: pytest {filename} -v")
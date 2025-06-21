# Migrating from OpenAI Assistants API to Responses API

## Background

The OpenAI Assistants API that's currently used in our horoscope generator is deprecated in favor of the new Responses API. This guide provides a roadmap for future migration.

## Current Implementation

The current implementation in `daily_horoscope_sql_fix.py` uses the OpenAI Assistants API with code like:

```python
# Create a thread
thread = client.beta.threads.create()

# Add a message to the thread
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
)

# Run the thread with an assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

# Retrieve the run status
run_status = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

# Get messages from the thread
messages = client.beta.threads.messages.list(thread_id=thread.id)
```

## Migration to Responses API

Here's how to update the code to use the new OpenAI Responses API:

```python
from openai import OpenAI
client = OpenAI()

# Generate content using the Responses API
response = client.chat.completions.create(
    model="gpt-4",  # Use appropriate model (previously defined by the assistant)
    messages=[
        {"role": "system", "content": "You are an astrology expert specialized in generating accurate and insightful horoscope content."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=1500
)

# Extract the response content
content = response.choices[0].message.content
```

## Differences to Consider

1. **Model Selection**: With Assistants API, the model was defined when creating an assistant. With Responses API, specify it directly in each completion request.

2. **System Messages**: With Assistants API, instructions were defined at the assistant creation level. With Responses API, include them as system messages in each request.

3. **Tools/Functions**: If your assistants used tools, you'll need to implement function calling with the Responses API.

4. **Thread Management**: The Responses API doesn't maintain threads, so you'll need to manage conversation history manually if needed.

5. **Error Handling**: Update error handling to match the new API's error structure.

## Step-by-Step Migration Plan

1. **Create System Messages**: Convert each assistant's instructions into system messages.

2. **Update API Calls**: Replace all Assistants API calls with Responses API calls.

3. **Test Each System**: Test each horoscope system individually to ensure quality and accuracy.

4. **Update Environment Variables**: Replace assistant IDs with model specifications if needed.

## Example Implementation

Here's a simplified example of how the `generate_horoscope` function might look after migration:

```python
def generate_horoscope(system, date_str):
    # System-specific instructions
    system_instructions = {
        "european": "You are an expert in European astrology...",
        "chinese": "You are an expert in Chinese astrology...",
        # ... other systems
    }
    
    # Create the prompt
    prompt = f"Generate a detailed {system} horoscope for {date_str}..."
    
    # Call the OpenAI Responses API
    response = client.chat.completions.create(
        model="gpt-4",  # Or another appropriate model
        messages=[
            {"role": "system", "content": system_instructions.get(system, "You are an astrology expert.")},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    # Extract and clean content
    content = response.choices[0].message.content
    title, body = extract_title_and_body(content)
    summary = generate_summary(body)
    
    return title, body, summary
```

## Timeline Recommendation

Since the Assistants API still works but is deprecated, consider scheduling the migration within the next 3-6 months to avoid disruption when the API is eventually removed.

## Resources

- [OpenAI Chat Completions API Documentation](https://platform.openai.com/docs/api-reference/chat)
- [OpenAI Migration Guide](https://platform.openai.com/docs/guides/migration)

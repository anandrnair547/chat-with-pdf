import openai


def ask_llm(query, context, api_key, model="gpt-3.5-turbo"):
    """
    Sends a prompt to OpenAI's ChatCompletion API and returns the response.
    """
    openai.api_key = api_key

    prompt = f"Context:\n{context}\n\nQuestion:\n{query}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on provided context.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    return response["choices"][0]["message"]["content"].strip()

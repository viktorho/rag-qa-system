from zhipuai import ZhipuAI
from config import config

client = ZhipuAI(api_key=config["api-key"])
def get_response(prompt, client):
    response = client.chat.completions.create(
        model="glm-4",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
            temperature=0.2
    )
    ans = ""
    for chunk in response:
        ans += chunk.choices[0].delta.content
    return ans

def clarify_prompt(user_prompt: str, client) -> str:
    """
    Step 1: Clarify ambiguous or vague input into a more precise version.
    """
    clarification_instruction = (
        "You are a prompt engineering assistant."
        "Rewrite the user’s question to be clear, precise and fully self-contained, without changing its original meaning. Make sure the revised question guides the AI to give a direct, on-topic answer and includes any necessary details for context."
        f"user question:{user_prompt}"
    )

    response = client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": clarification_instruction}],
        temperature=0.3,
        stream=False
    )
    
    clarified = response.choices[0].message.content.strip()
    print(clarified)
    return clarified

if __name__ == '__main__':
    docs = "Theft of public or private property, in large amounts, or repeated theft, burglary, theft with weapons, or pickpocketing, shall be punished with imprisonment for less than three years, detention, or surveillance, and may also be fined; for theft involving a huge amount or other serious circumstances, the punishment is imprisonment for three to ten years, plus a fine; for theft involving an extremely large amount or particularly serious circumstances, the punishment is imprisonment for more than ten years or life imprisonment, plus a fine or confiscation of property."
    q = "What impact does a prior theft record have on being caught stealing again?"
    input_prompt = f"Given these Chinese laws: {docs} Please answer the questions: {q}"
    print(get_response(input_prompt, client))


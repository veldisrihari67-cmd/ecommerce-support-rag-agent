import os
import time
import json
from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

def policy_retriever_tool(category, query):
    folder = '/content/policies'
    context = []
    if not os.path.exists(folder): return "No policy folder."
    
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), 'r') as f:
                chunks = f.read().split('\n\n')
                for i, chunk in enumerate(chunks):
                    if category.lower() in chunk.lower() or any(word in chunk.lower() for word in query.split()[:3]):
                        context.append(f"Source: {filename} (Section {i}) | Content: {chunk.strip()}")
    return "\n\n".join(context[:3]) 

def triage_agent(ticket, order_context):
    print("🤖 Agent 1: Triaging & Classifying...")
    prompt = f"Ticket: {ticket}\nContext: {order_context}\nClassify issue type (REFUND/SHIPPING/PAYMENT/PROMO/FRAUD/OTHER). Identify missing info. Output JSON only."
    res = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.1-8b-instant", response_format={"type": "json_object"})
    return json.loads(res.choices[0].message.content)

def policy_agent(category, ticket):
    print("🔍 Agent 2: Retrieving grounded evidence...")
    return policy_retriever_tool(category, ticket)

def resolution_agent(ticket, context, policy):
    print("⚖️ Agent 3: Drafting Resolution...")
    time.sleep(2) 
    prompt = f"Ticket: {ticket}\nOrder: {context}\nPolicy: {policy}\nDecide Approve/Deny/Partial/Escalate. Use ONLY policy text. No hallucinations."
    res = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.1-8b-instant")
    return res.choices[0].message.content

def compliance_agent(resolution, policy):
    print("🛡️ Agent 4: Safety & Citation Check...")
    time.sleep(2)
    prompt = f"Review this resolution: {resolution}\nBased on policy: {policy}\nVerify citations. Remove unsupported claims. Output final structured response."
    res = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.1-8b-instant")
    return res.choices[0].message.content

def run_assessment_ticket(ticket_text, order_json):
  
    triage_data = triage_agent(ticket_text, order_json)
    
    policy_evidence = policy_agent(triage_data.get('issue_type', 'OTHER'), ticket_text)

    raw_resolution = resolution_agent(ticket_text, order_json, policy_evidence)
    
    final_output = compliance_agent(raw_resolution, policy_evidence)
    
    return final_output

ticket = "My order arrived late and the cookies are melted. I want a full refund."
order_context = {
    "order_date": "2024-05-01",
    "item_category": "perishable",
    "fulfillment_type": "first-party",
    "shipping_region": "US-NY"
}

print(run_assessment_ticket(ticket, order_context))

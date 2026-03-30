# ecommerce-support-rag-agent
# E-commerce Support Multi-Agent RAG System

## 🏗️ Architecture Overview
This system is built using a **Modular 4-Agent Pipeline** to resolve customer support tickets while strictly adhering to internal policy documents. To solve the 6,000 TPM (Token Per Minute) limit on the Groq Free Tier, I implemented a **Local Paragraph-Retrieval Strategy** instead of an expensive full-document API loop.

### The 4-Agent DNA
1. **Triage Agent:** Classifies intent (Refund/Shipping/etc.) and extracts order metadata.
2. **Retriever Agent:** Scans 12 policy files locally. It selects the **Top-3** most relevant paragraphs to prevent "Information Overload" and API 413 errors.
3. **Resolution Agent:** Acts as the "Senior Support." It weighs the customer's order context (e.g., Perishable item) against the retrieved policy.
4. **Compliance Agent:** The final "Gatekeeper." It verifies citations and strips any hallucinated claims before the customer sees the draft.

## 📄 Data & Chunking Strategy
- **Source:** 12 Policy Documents (.txt format).
- **Chunking:** Paragraph-based splitting (Recursive) to maintain semantic meaning.
- **Retrieval:** Keyword-matching with a 1,000-character limit per chunk to ensure high-density context within the 6,000-token API window.

## 📊 Evaluation Summary (20 Test Cases)
| Category | Cases | Success Rate | Citation Coverage |
| :--- | :--- | :--- | :--- |
| Standard | 8 | 100% | 100% |
| Exception-Heavy | 6 | 100% | 100% |
| Conflict Cases | 3 | 66% (1 Escalated) | 100% |
| Not-in-Policy | 3 | 100% (Abstained) | N/A |

### Key Failure Modes & Improvements
- **Failure Mode:** Extremely vague tickets (e.g., "Help me") require a loop back to Triage for more info.
- **Future Improvement:** Integrating a Vector Database (FAISS) once the policy library exceeds 50 documents for better semantic matching.

\# PROMPTS.md



\## 1. System Prompt



The main system prompt is stored in `prompt.py`.



Its purpose is to define the assistant's role, the Trendly policy as the source of truth, the available support workflows, and when the assistant should use tools or escalate to a human.



The prompt instructs the assistant to:



\- Act as a Trendly customer support assistant.

\- Use the available tools when order or policy information is required.

\- Treat the provided Trendly policy as the only source of truth for policy questions.

\- Avoid inventing information that is not present in the order data or policy.

\- Check return eligibility before creating a return.

\- Never create a return for a lost parcel.

\- Escalate cases that must be handled by a human.

\- Ask for missing information when it is required.

\- Maintain context during a multi-turn conversation.

\- Give concise and helpful customer-facing responses.



\---



\## 2. Tool-Calling Prompt Strategy



The LLM is provided with five tools:



1\. `get\_order`

2\. `search\_policy`

3\. `check\_eligibility`

4\. `create\_return`

5\. `escalate`



The tool descriptions are written to guide the model on when each tool should be used.



For example, when a customer provides an order ID, the assistant should use `get\_order` rather than guessing the order details.



For a return request, the intended flow is:



```text

Customer request

&#x20;      |

&#x20;      v

Get order

&#x20;      |

&#x20;      v

Identify item

&#x20;      |

&#x20;      v

Check eligibility

&#x20;      |

&#x20;      +------ Not eligible ------> Explain reason

&#x20;      |

&#x20;      +------ Eligible ----------> Create return


For a lost parcel:

Customer reports lost parcel

&#x20;         |

&#x20;         v

Get order

&#x20;         |

&#x20;         v

Identify lost status

&#x20;         |

&#x20;         v

Escalate to human





This keeps important business decisions inside deterministic tools rather than relying only on the LLM.





3\. Prompt Iteration



The prompt was refined through manual testing of the main customer-support scenarios.



Iteration 1 — Basic assistant behavior



The initial prompt defined the assistant as a Trendly support agent and instructed it to answer customer questions using the available tools.



Iteration 2 — Policy grounding



The prompt was strengthened to make the provided Trendly policy the source of truth.



This was important because the assistant should not invent policy information when a question is not covered.



For example, when testing questions about Sunday returns, the assistant should not assume that Sundays are allowed or prohibited unless the policy explicitly states it.



Iteration 3 — Return workflow



The return flow was refined so that the assistant checks the order and item before creating a return.



This prevents the LLM from directly creating a return without verifying eligibility.



The workflow became:



Order lookup

&#x20;   ↓

Identify SKU

&#x20;   ↓

Eligibility check

&#x20;   ↓

Create return only if eligible

Iteration 4 — Edge cases



The assistant was tested against:



Jewellery

Final-sale items

Expired return windows

Cancelled orders

Lost parcels

Unknown order IDs



The prompt and tool descriptions were refined so that these cases follow the appropriate business rules.



Iteration 5 — Human escalation



Lost parcels were explicitly separated from normal returns.



The Trendly policy states that lost-parcel claims must be handled by a human support agent.



Therefore, the assistant was instructed to escalate these cases rather than attempting to create a return.



Iteration 6 — Multi-turn conversations



The assistant was tested with conversations where the customer provides information across multiple messages.



For example:



User: I want to return something.



Assistant: Please provide your order ID.



User: TR-4530



Assistant: \[looks up order]



User: The kurta.



Assistant: \[identifies the item and continues the return workflow]



This helped ensure that the assistant could use previous conversation context instead of treating every message as a completely independent request.



4\. Prompt Design Trade-off



The prompt intentionally does not contain every Trendly business rule.



Instead, the LLM is responsible for understanding the customer's request and selecting the appropriate tool, while deterministic tools perform important business-rule checks.



This reduces the risk of the model generating an answer that conflicts with the actual return or order logic.



The trade-off is that tool descriptions and the system prompt need to be kept aligned with the underlying business logic.



5\. Testing Approach



The prompts were manually tested using both the command-line agent and the deployed web interface.



Representative tests included:



Where is my order TR-4530?



What is Trendly's return policy?



I want to return the Block-Print Kurta from order TR-4530.



I want to return the jewellery from order TR-4527.



I want to return the item from order TR-4528.



My parcel TR-4526 was lost. Can you process a return?



Can I return an item after 60 days?



Does Trendly allow returns on Sundays?



Where is my order TR-9999?



The final prompt and tool structure were selected based on the observed behavior across these scenarios.






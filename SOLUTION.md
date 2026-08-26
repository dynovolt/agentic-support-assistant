Trendly Agentic Support Assistant — Solution Note



1\. Overview



The solution is an agentic customer support assistant for Trendly.



The assistant handles common order and return-related support requests such as:



\- Order lookup

\- Policy questions

\- Return eligibility

\- Return creation

\- Lost parcel escalation

\- Unsupported policy questions

\- Multi-turn conversations



The system uses an LLM as the reasoning layer while keeping important business rules inside deterministic tools.



\---



2\. Architecture



The application consists of four main layers:



```text

Customer

&#x20;  |

&#x20;  v

Web Chat UI

&#x20;  |

&#x20;  v

FastAPI API

&#x20;  |

&#x20;  v

LLM Agent

&#x20;  |

&#x20;  +-------------------+

&#x20;  |                   |

&#x20;  v                   v

Tool Layer          Conversation

&#x20;  |                  Context

&#x20;  |

&#x20;  +-- get\_order

&#x20;  +-- search\_policy

&#x20;  +-- check\_eligibility

&#x20;  +-- create\_return

&#x20;  +-- escalate


The browser sends messages to the FastAPI /chat endpoint.



The agent passes the conversation to the LLM. When additional information or an action is required, the model can call one of the available tools.



The tools access the provided order data and Trendly policy and perform deterministic operations.



The final response is then returned to the web interface.



3\. Key Design Decisions and Trade-offs

LLM + tools instead of a fully scripted chatbot



A scripted flow would be predictable but would require many predefined conversation paths.



Using tool calling allows the assistant to handle natural language requests while still connecting those requests to controlled business operations.



The trade-off is that LLM behavior is probabilistic, so tool descriptions and system instructions need to be carefully designed.



Business rules outside the LLM



Return eligibility is implemented as a tool rather than asking the LLM to decide whether an item is eligible.



This reduces the risk of the model inventing or misinterpreting business rules.



For example:



User request

&#x20;    |

&#x20;    v

Order lookup

&#x20;    |

&#x20;    v

Eligibility check

&#x20;    |

&#x20;    +---- eligible ----> Create return

&#x20;    |

&#x20;    +---- not eligible -> Explain reason

Policy as the source of truth



The provided Trendly policy is treated as the source of truth.



If a question is not covered by the policy, the assistant should not invent an answer and should offer human support.



In-memory conversation state



The current implementation uses lightweight session-based conversation history.



This keeps the assignment simple and avoids introducing unnecessary infrastructure.



The trade-off is that conversations are lost when the application restarts.



4\. Important Safety / Business Rules



Several cases are intentionally handled differently from a normal return flow.



Lost parcels



A lost parcel is not treated as a return.



The policy requires lost-parcel claims to be handled by a human support agent, so the assistant escalates the request.



Final-sale items



Final-sale items cannot be returned for a refund. The assistant explains that only the permitted exchange flow is available.



Non-returnable categories



Jewellery and other non-returnable categories are rejected by the eligibility logic.



Unknown orders



If an order cannot be found, the assistant does not fabricate order information.



Unsupported policy questions



If the policy does not cover a question, the assistant does not guess and instead offers human support.



5\. Known Limitations



This implementation is intentionally scoped for the assignment.



Local sample data



Orders and policy information are stored locally rather than being connected to a real commerce platform.



A production system would integrate with Trendly's order management, inventory, payment, shipping and CRM systems.



In-memory sessions



Conversation state is currently stored in memory.



A production deployment would use persistent storage such as Redis or a database.



No authentication



The current demo does not authenticate customers before exposing order information.



A real deployment would require customer verification and authorization.



Limited operational integrations



Return creation and escalation are simulated through the provided tools.



A production version would connect these actions to real operational systems.



LLM dependency



The assistant depends on the availability and behavior of the selected LLM provider.



Production deployment would require monitoring, timeout handling, fallback strategies and usage controls.



6\. Discovery Questions for Trendly's Ops Team



Before building this system for real, I would ask the following questions.



1\. What systems are the source of truth for orders and returns?



I would want to understand whether order status, delivery information, inventory and return status live in one system or across multiple systems.



2\. What actions is the assistant actually allowed to perform?



For example, can the assistant directly create returns and exchanges, or should some actions always require human approval?



3\. How should customer identity be verified?



Before exposing order information or initiating a return, we need to know what authentication or verification requirements Trendly expects.



4\. What are the most common reasons customers contact support?



Understanding the highest-volume intents would help prioritize the first production version and determine which tools and workflows need the most investment.



5\. What happens operationally after an escalation?



I would want to understand which team receives escalations, how they are tracked, what SLA applies, and how the assistant should communicate the case status back to the customer.



7\. Production Evolution



If this prototype were taken into production, I would prioritize:



Authentication and authorization

Integration with real order and return systems

Persistent conversation storage

Human-agent handoff integration

Monitoring and observability

Tool-level authorization and audit logging

Evaluation datasets for measuring agent accuracy

Rate limiting and reliability controls


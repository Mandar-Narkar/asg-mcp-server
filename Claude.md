**#Assignment: Build a Useful MCP Server and Client**

—

100 pts

Pass: 60 pts

**Assignment: Build a Useful MCP Server and Client**



The goal of this assignment is to help you understand how Model Context Protocol (MCP) can be used to connect large language models with real-world tools, data sources, and services. In this assignment you will design and implement a functional MCP server and a client that can interact with it, and you will also think critically about the real-world impact and market potential of the system you build.



Your task is not just to write code, but to design a useful MCP-powered application that could realistically solve a meaningful problem. The emphasis of this assignment is on identifying industries or markets where large disruption is possible when AI systems are given structured access to tools and data through MCP.



**##Objective**

Build a **working MCP server and MCP client system** that allows a language model to interact with tools through MCP. The system should demonstrate a meaningful workflow where an LLM can call tools exposed by your MCP server and produce useful outputs for a user.



Examples of possible applications include, but are not limited to:



Financial analysis assistant



Medical research summarization tool



Legal document analysis assistant



Automated research paper summarizer



Developer productivity tools



Knowledge assistants for specific industries



Education assistants that process lecture content



Business intelligence assistants



You are strongly encouraged to think about industries where AI-enabled tool usage could cause major disruption, such as healthcare, finance, legal services, education, logistics, research, or software development.



**###Implementation Requirements**

You must build both of the following components:



**1. MCP Server**

Your MCP server should expose one or more useful tools that an LLM can call.



Examples of tools could include:



Retrieving data from an API



Processing documents or transcripts



Performing analysis or calculations



Querying databases or knowledge sources



Generating reports or summaries



The MCP server should follow the MCP protocol and clearly expose tool definitions and outputs.



**2. MCP Client**

You must also build a client that interacts with your MCP server and allows a user to run the system.



You have two options:



**Option A – Web Client (Recommended)**

Create a simple web interface where:



The user can paste their own LLM API key (for example OpenAI or Anthropic).



The client communicates with your MCP server.



The user can run prompts that trigger MCP tool calls.



The instructor should be able to open the website, paste an API key, and run the system immediately.



**Option B – Local Demonstration**

If you prefer to build a local application instead of a web interface:



Run the MCP client locally.



Record a 5-10 minute demonstration video using Loom explaining the system and showing it working.



Share the Loom video link.



**####Strategic Thinking Component**

Along with the implementation, you must also submit a one-page PDF document explaining the broader significance of your MCP system.



Your PDF must answer the following questions:



What problem does your MCP system solve?



Which industry or market does it target?



Why is MCP a good architecture for solving this problem?



What is the value proposition for users?



If this system were developed into a real product, who would pay for it and why?



In your opinion, which industry could be significantly disrupted by systems like this?



The purpose of this section is to encourage you to think beyond the code and understand how AI systems integrated with tools can transform industries.



**#####Deliverables**

You must submit the following:



Code repository (GitHub or similar) containing:



MCP server implementation



MCP client implementation



Instructions to run the system



One-page PDF explaining:



The use case



Target market



Value proposition



Potential industry disruption



Either one of the following:



Option A – Web client



A website where the instructor can paste their API key and run the system.

Option B – Loom demo



A 5-10 minute Loom video demonstrating your system working locally.

**#######Evaluation Criteria**

Your submission will be evaluated based on:



Correct implementation of MCP server and client



Clarity and usefulness of the exposed tools



Creativity and originality of the application



Quality of the demonstration



Depth of thought in the one-page market analysis



**Goal of This Assignment**

This assignment is designed to help you move from simply using large language models to building real systems where AI interacts with tools and services. The long-term goal is to develop the ability to design AI-native applications that can transform industries, rather than just building simple chatbot interfaces.


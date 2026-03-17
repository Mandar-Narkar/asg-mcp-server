# Strategic Analysis: ASG Securitization Operations Assistant

## 1. What Problem Does This MCP System Solve?

Securitization back-office operations are stuck in a paradox: the data exists, the rules are defined, and the workflow is deterministic — yet analysts spend hours each morning manually pulling deal reports, running waterfall calculations, checking coverage test ratios, and drafting payment direction letters. At TD Securities, this cycle repeats across every trust and conduit on the portfolio, every payment period, under hard cut-off deadlines. The cost is not missing information — it is the friction of translating structured data into operational decisions. This system eliminates that friction by giving an LLM direct, tool-mediated access to deal data, coverage logic, and exception rules so that a complete ops review — summary, waterfall, exceptions, payment status — executes in seconds via natural language.

---

## 2. Which Industry and Market Does It Target?

**Structured finance operations within Canadian and global capital markets.** The immediate market is the back-office and middle-office teams at Schedule I banks, trust companies, and asset managers that administer ABS, ABCP, RMBS, and CLO vehicles. In Canada alone, the ABS market exceeds $200 billion in outstanding issuance. Globally, structured finance administration is a multi-billion-dollar services segment currently dominated by manual processes, legacy trustee platforms, and Excel-based waterfall models.

---

## 3. Why Is MCP the Right Architecture?

MCP is the right architecture because securitization operations are tool-shaped problems, not conversation-shaped ones. Each task — fetch deal data, run a waterfall, evaluate a coverage test — is a discrete, deterministic function with a defined schema. MCP makes these functions first-class primitives that any capable LLM can call, chain, and reason over without bespoke integration code. Compared to a RAG pipeline, MCP returns exact figures rather than retrieved text. Compared to a custom API, MCP is model-agnostic and composable — new tools can be added without retraining or prompt re-engineering. For a regulated environment where auditability and precision matter, the tool-call trace MCP produces is also a natural audit log.

---

## 4. What Is the Value Proposition for Users?

For an operations analyst, the value is reclaimed time and reduced error surface. A morning portfolio review that takes 60–90 minutes of manual report-pulling and cross-referencing collapses to a single prompt. Exception flags that might be missed in a dense report are surfaced automatically. Payment summaries arrive pre-validated against coverage tests, with a clear READY TO SUBMIT or BLOCKED status, before the 11AM trustee cut-off. For operations managers, the value is consistency: every deal is reviewed to the same standard, every period, with a reproducible tool-call record. For compliance and audit functions, every LLM decision is grounded in a structured tool result — not a hallucinated figure.

---

## 5. Who Would Pay for This and Why?

**TAO Solutions** is the natural commercialisation vehicle. With approximately 80% market share in Canadian securitization administration and contracts with every Schedule I bank — TD, RBC, BMO, Scotiabank, CIBC, NBC — TAO already owns the data layer this system runs on. Their February 2026 AI roadmap positions MCP-native tooling as the next capability tier for SecureHub, their flagship administration platform. Rather than building a standalone AI product, TAO can ship this as a **SecureHub Intelligence** premium add-on: the MCP server connects directly to live SecureHub deal data, and clients pay a per-seat or per-deal licence on top of their existing SecureHub subscription. The switching cost is near-zero for existing clients; the incremental revenue per bank is material. For TAO, this is a defensible moat — competitors cannot replicate the tool layer without first replicating the 30-year data relationships underneath it.

---

## 6. Which Industry Could Be Significantly Disrupted?

**Structured finance administration and trustee services.** The trustee and paying-agent function — currently performed by large trust companies charging basis-point fees on pool balances — is largely a data-routing and compliance-verification business. MCP-native systems that automate waterfall computation, exception detection, and payment instruction generation compress the human labour that justifies those fees. As MCP tooling matures, the question shifts from *whether* AI can perform these functions to *which platform owns the tool layer*. Firms that control the data and expose it via MCP will absorb margin from those that do not. The first institution to productise this at scale — likely through an embedded AI layer in an existing administration platform — will structurally reprice what trustee services cost.

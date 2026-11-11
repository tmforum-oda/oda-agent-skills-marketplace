# open-gateway-northbound-api-types-scope.jpeg

**Type:** Layered architecture diagram.
**Source context:** `# Introduction`, after "Open Gateway defines the APIs Exposed by CSPs to fulfill the Open Gateway requirements in the categories below."

**What it shows:**

- **Northbound API Types** (inside a dashed box) are split into two scopes:
  - **TMF Scope** (red dotted outline): **Aggregators / Hyperscalers** use the **Operate APIs**.
  - **CAMARA Scope** (blue dotted outline): the **CAMARA API Consumer** uses the **Service APIs** and the **Service Mgmt. APIs**.
- Below them, a **Telco Service Exposure Platform** sits on top of **Southbound / Technology Specific APIs**, which sit on top of **Network(s)**.
- A second, identical stack on the right (Telco Service Exposure Platform, Southbound / Technology Specific APIs, Network(s)) represents another operator.
- The two exposure platforms are connected by **Federated East ⇔ West APIs**. The two networks are connected by **Network to Network Interconnect (aka) Roaming**.

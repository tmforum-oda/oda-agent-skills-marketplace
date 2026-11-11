# b2b2x-marketplace-ecosystem-context-diagram.png

**Type:** Business context / stakeholder diagram.
**Source context:** `## Context or Background` section of the Introduction, showing the B2B2X marketplace scenario the use case is built around.

**What it shows:**

- At the top, a **Large Enterprise customer with multiple branches**. It "Uses Underlay / Connectivity for each of the branches and hub" (arrow to **MPLS VPN**) and "Uses Overlay services for VPN, SW, Cloud and apps" (arrow to **SD WAN & SAAS Services**).
- **MPLS VPN** and **SD WAN & SAAS Services** both "Uses" a shared **Underlay / Connectivity** box.
- The **B2B2B Telco (MARKETPLACE OWNER)** "Supplies" the Underlay / Connectivity, the MPLS VPN and the SD WAN & SAAS Services.
- Below the marketplace owner, a box of its capabilities: Partner eco System factory, Partner Offer Management, Partner Account Management, Selling & Orchestration, Partner Agreements, Partner Settlements, Disputes & reconciliation, plus **Existing BSS** and **Existing OSS**.
- On the right, a dashed box **Eco System Stakeholders – Business Partners** containing four partner types: Business Partner: Cloud Provider; Business Partner: SAAS Vendor; Business Partners: SD WAN and SASE Vendors; Business Partners: CAAS vendors (shown with a UCaaS logo).
- Six numbered curved lines connect the marketplace owner's capability box to the business partners:
  1. Partner Onboarding with separate Agreements for Operating and Financial Models.
  2. Based on Agreement, onboard the partner services.
  3. Provisioning SD WAN Services, Branch routers, Policies, SAAS licences etc.
  4. Business Partner sends Invoice to marketplace owner.
  5. Marketplace owner initiates Settlements Process based on Agreement.
  6. Dispute management.

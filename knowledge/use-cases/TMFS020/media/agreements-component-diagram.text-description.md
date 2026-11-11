# agreements-component-diagram.png

**Type:** ODA component interaction (block) diagram.
**Source context:** `### Agreements - Component diagram` under "ODA component and canvas interaction diagrams". The text before it stresses that the Agreement is driven by the catalog, so the product offering is configured for the agreement instead of being captured in manual documents and spreadsheets.

**What it shows:** three dashed swimlane boxes — **Marketplace owner**, **Account Manager** and **Customer**.

Inside the Marketplace owner box, **Agreement Management - TMFC039** sits in the centre, connected to four components by labelled API arrows:

- Agreement Management → **Party Management TMFC028** via **TMF632**.
- Agreement Management → **Product Catalog Management - TMFC001** via **TMF 620**.
- Agreement Management → **Product Configuration - TMFC027** via **TMF 679, TMF 760**.
- **Lead & Opportunity Management - TMFC036** → Agreement Management via **TMF 651**.

The **Account Manager** lane has an arrow into Agreement Management labelled **View and Manage the agreement**. A two-way arrow connects the Account Manager lane with the **Customer** lane, showing that the account manager and customer interact directly.

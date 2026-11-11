# notification-delivery-business-process.png

**Type:** Business process / block diagram, titled "Figure 1. Notification delivery across notifying components".
**Source context:** `## Business process view`, after the analysis of requirements C1–C4 that no notifying component can satisfy alone.

**What it shows:**

- **Eight notifying ODA components** (top row, blue), each with its scenario and API, each sending into a shared notification delivery capability:
  - Product Order Delivery and Orchestration Mgmt — S1 order status — TMF622
  - Service Ordering/ Activation — S2 service, outage — TMF641 . TMF640
  - Product Usage Management — S3 spend threshold — TMF635
  - Billing Account Management — S4 bill available — TMF678 . TMF636
  - Party Management/ Payment Management — S5 payment overdue — TMF666 . TMF676
  - Party Privacy Management — S6 consent change — TMF644
  - Partner/Event Management — S7 ecosystem event — event hub of the raising API
  - Product Catalogue Management — S8 price change — TMF620
- **notification delivery** (yellow band), covering "consent ; contact policy ; coordination ; channel handling ; delivery record", broken into twelve delivery steps: 1 Accept; 2 Suppress duplicate; **3 Consent by class (C1 . C2)**; 4 Contact Policy; **5 Coordinate (C3)**; 6 Resolve address; 7 Select channel; 8 Render; 9 Dispatch and retry; 10 Normalize State; **11 Record (C4)**; 12 Terminal state. Steps 3, 5 and 11 are shaded red as steps carrying an unmet requirement.
- Below the band: a **notification** arrow goes to the **Recipient (customer or business partner)**, and a **reply (I1-I3, 2.3)** arrow comes back from the recipient into the band. **Compliance / audit** reads a **quick delivery record** from the band (dotted arrow).
- A red dotted note box lists the "Requirements that no notifying component can satisfy alone (2.4)":
  - C1 uniform consent enforcement — the effective standard is that of the least rigorous implementation.
  - C2 consent differentiated by message class — a regulatory notice is delivered where a marketing one is not.
  - C3 coordination between notifications raised by different components to one recipient.
  - C4 a consolidated delivery record, queryable across all notifying components and channels.
- **Legend:** notifying ODA component (blue); delivery step (orange outline); recipient (green); audit (purple); step carrying an unmet requirement (red).

# communication-interaction-management-component-diagram.png

**Type:** ODA component interaction (block) diagram.
**Source context:** the ODA component and canvas interaction section for the proposed Communication Interaction Management component. The text before it notes: one exposed API (TMF681) consumed by every notifying component; no mandatory dependency (every consumed interface is optional, because a notifying component may give an explicit delivery address instead of a party reference); and the inbound direction is not an ODA interface. Party Interaction Management is drawn separately because the relationship is reciprocal (see Table 23).

**What it shows:**

- In the centre, **Communication Interaction Management (proposed — no identifier)**, in the **Engagement Management** functional block. Above it, the API it **exposes**: **TMF681 Communication Management**, marked **MANDATORY**.
- On the left, **Core Commerce Management - notifying components**: Product Order Delivery and Orchestration Mgmt (TMFC003), Service Order Management (TMFC007), Product Usage Management (TMFC040), Billing Account Management (TMFC024), Payment Management (TMFC029), Product Catalog Management (TMFC001), Party Management (TMFC027). They call the central component via **TMF681 POST /communicationMessage**.
- Below it, **Channel transports (non-ODA)**, "terminated by the component; outbound and inbound". The central component sends **dispatch** to them and receives **inbound reply** from them.
- Upper right, **Party Interaction Management · TMFC023** (Engagement Management), reached by a dashed arrow labelled **TMF683 POST /partyInteraction**.
- Right, a group headed **consumed by Notification Management — all optional**, reached by a dashed arrow labelled **consumed all optional**: Party Management · TMF632, Customer Management · TMF629, Privacy Management · TMF644 (all Party Management block), and Account Management · TMF666, Product Inventory · TMF637, Usage Management · TMF635, Document Management · TMF667 (Core Commerce Management block).
- **Legend:** colour follows the functional block — Engagement Management (purple), Party Management (red), Core Commerce Management (white with black outline), non-ODA (blue), proposed component (dashed purple, italic), exposed API (yellow). Solid arrow = call; dashed arrow = optional dependency.

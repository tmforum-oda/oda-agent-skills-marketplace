# communication-delivery-state-lifecycle.png

**Type:** State transition diagram.
**Source context:** the information view section on the delivery lifecycle of a communication. The text before it says the diagram shows the five states and their transitions, with the conditions on the transition to failed, and marks two properties the published model does not represent: reason for non-delivery (Q1) and channel and route used (Q2).

**States** (legend: non-terminal state in blue, terminal - delivered in green, terminal — not delivered in red): **initial** and **inProgress** (non-terminal), **completed** (terminal, delivered), **failed** (terminal, not delivered) and **cancelled**.

**Transitions:**

- initial → inProgress: **accepted**.
- initial → cancelled: **suppressed by consent or contact policy**.
- inProgress → cancelled: **cancelled before dispatch**.
- inProgress → completed: **delivery confirmed**.
- inProgress → failed: **terminal disposition**.

**Annotations:**

- Linked to failed: "Transition to failed occurs when · maximum hold time is exceeded · all permitted routes and channels are exhausted · the contact medium is permanently unusable".
- Red note linked to failed: "Not represented in TMF681 v4.0.0 the reason for non-delivery (5.1.4, postcondition Q1)".
- Red note linked to inProgress: "Not represented in TMF681 v4.0.0 the channel and address actually used where the route is substituted (5.1.4, postcondition Q2)".
- Red note: "No event schemas are defined on the TMF681 /hub, so no transition above can be subscribed to. Delivery state is available by query only. (5.1.3, requirement C4)".

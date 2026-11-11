# similar-incidents-problem-ticket-agent-ui-mockup.png

**Type:** UI screen-flow mockup (wireframe).
**Source context:** the second scenario, where a Helpdesk Agent, prompted by the system or on their own, spots similar incidents reported by multiple customers in the same region and raises a Problem Ticket. It follows the scenario table (pre-conditions, begins when, description, ends when, post-conditions).

**Screens, in order:**

1. A dashed box offering two starting points, joined by **OR**:
   - **System Prompt to Agent**: "Similar problem detected!!! Multiple customers in this region have reported similar problem. Would you like to view similar ticket." Buttons: View, Dismiss.
   - **Agent-initiated investigation**: "Agent searches for the similar incident in the same region. Filters: Region, Service, Error code, Time Range etc." It lists tickets TT-123456XYZ, TT-123457XYZ and TT-123458XYZ. Button: View All.
2. **Identify Similar Problem**: "Helpdesk Agent Identifies multiple customer have reported similar problem in this region have reported similar problem". Buttons: Proceed, Dismiss.
3. **Creates Problem Ticket** form: Type: Problem; Severity: Critical; Product Service: Mobile Plan 1234XXX; a Description field. Buttons: Proceed, Dismiss.
4. **Notification**: "You ticket number is PR-123456ABC. Problem Ticket created. Would you like to proceed with linking the tickets". Buttons: Proceed, Dismiss.
5. **Link related incident tickets**: TT-123456XYZ, TT-123457XYZ, TT-123458XYZ, Etc. Buttons: Proceed, Dismiss.
6. **Notification**: "Problem Ticket PR-123456ABC assigned to Technical Team for Root Cause Analysis and Resolution". Button: Close.

---
id: TMFC023
type: component
name: Party Interaction Management
version: 1.1.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC023_Party_Interaction_Management_v1.1.1.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 732081b471bbb14cd2172c71e004e9dfd44419b3e2d55932d8e6fade0852f39b
  raw_path: references/components/TMFC023/TMFC023_Party_Interaction_Management_v1.1.1.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF662
      name: entity-catalog-management-api
    - id: TMF667
      name: document-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF681
      name: communication-management-api
    - id: TMF683
      name: party-interaction-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS001
      name: New Party – Create your accounts
    - id: TMFS002
      name: Browse B2C Catalogue and Check Fiber Technical Eligibility
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS006
      name: Legal Guardian
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
    - id: TMFS031
      name: Problem Management
yaml_spec_version: 1.1.2
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Party<br>Interaction<br>Management | TMFC023 | Party Interaction deals with the initial greeting and<br>welcoming of a new contact. This will typically be<br>the first component in a customer experience<br>journey, shared by unassisted (self-service, retail<br>kiosk) or assisted (call center, retail store) channels.<br>It will identify known Parties or new Parties and react<br>appropriately to propose available actions. It<br>records all the interactions for the Parties from all<br>channels. | Party<br>Management |

![](media/party-interaction-management-architecture.png)
*([PlantUML source](media/party-interaction-management-architecture.puml))*

# 2. eTOM Processes, SID Data

Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.5 | 2 | Customer<br>Interaction<br>Management | Manage interactions between the customer and the<br>enterprise. Interactions can be triggered by the<br>customer or by the enterprise |
| 1.3.5.1 | 3 | Create Customer<br>Interaction | Create a record that logs the customer interaction. |
| 1.3.5.2 | 3 | Update Customer<br>Interaction | Update the customer interaction. |
| 1.3.5.3 | 3 | Close Customer<br>Interaction | Close the customer interaction. |
| 1.3.5.4 | 3 | Log Customer<br>Interaction | Record and maintain all information about the<br>customer interaction. |
| 1.3.5.6 | 3 | Track and Manage<br>Customer<br>Interaction | Ensure that Customer Interactions are managed and<br>tracked efficiently. |
| 1.3.5.7 | 3 | Report Customer<br>interaction | Monitor the status of a customer interaction. |
| 1.6.9 | 2 | Business Partner<br>Interaction<br>Management | Manage interactions between parties and the<br>enterprise. Interactions can be triggered by the<br>enterprise (as a result of a query or complaint) or by a<br>Business Partner (for example sending bills or other<br>notifications.) |
| 1.6.9.1 | 3 | Log Business<br>Partner Interaction | Record and maintain all information about the<br>Business Partner interaction. |
| 1.6.9.3 | 3 | Track and Manage<br>Business Partner<br>Interaction | Ensure that Business Partner Interactions are<br>managed and tracked efficiently to meet the Business<br>Partner interaction policies and SLA requirements. |
| 1.6.9.5 | 3 | Analyze & Report<br>Business Partner<br>Interactions | Perform all required analysis on closed requests and<br>on Business Partner contacts and generate related<br>reports |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Communication Interaction ABE |   |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-communication-interaction-links.png)
*([PlantUML source](media/etom-sid-communication-interaction-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 93 | Customer Behavior<br>Tracking | Customer Behavior Tracking<br>function monitor the customer<br>behavior through the customer<br>interaction, public communication,<br>and use of products. | Welcome and<br>Interaction | Customer<br>Interaction<br>Management |
| 163 | Contact Queuing | Contact Queuing; Contact Queuing<br>provides the means to queue the<br>contact until such time that a<br>suitable agent comes available to<br>work the contact. | Welcome and<br>Interaction | Customer<br>Interaction<br>Management<br>Queue<br>Management |
| 165 | Customer Support<br>Collaboration<br>Access | Customer Support Collaboration<br>Access provides the means for<br>customer to agent or agent to<br>support online chatting | Welcome and<br>Interaction | Customer<br>Interaction<br>Management |
| 168 | Voice Channel<br>Contact Routing | Voice Channel Contact Routing<br>function provides the means for a<br>customer to speak to a service<br>representative, including the<br>mechanism to query the customer<br>(e.g. – IVR) on the nature of their<br>request, and routing of the contact<br>to the best available agent with the<br>skills required for the contact and<br>presents to the agent selected call<br>information. | Welcome and<br>Interaction | Customer<br>Interaction<br>Management<br>Voice Channel<br>Contact<br>Routing |
| 189 | Customer<br>Interaction<br>Information<br>Capturing | Customer Interaction Information<br>Capturing captures customer<br>interaction event data from all<br>channels (agent interaction/notes,<br>web/device click analytics, retail<br>transactions, etc.), including<br>receiving information from<br>Customer Interaction Collection &<br>Storage | Welcome and<br>Interaction | Customer<br>Interaction<br>Management |
| 191 | Customer<br>Relationship/Context<br>Event Data<br>Accumulation | Customer Relationship/Context<br>Event Data Accumulation provides<br>an ability to accumulate and map<br>customer interaction event data<br>from all channels (agent<br>interaction/notes, web/device click<br>analytics, retail transactions, etc.),<br>including received information from<br>Customer Interaction Collection &<br>Storage | Welcome and<br>Interaction | Customer<br>Interaction<br>Management |
| 196 | Customer<br>Interaction Logging | Customer Interaction Logging<br>provides collection and storage of<br>all contact events with the<br>customer via all channels whether<br>unassisted (self service, retail<br>kiosk) or assisted (call center, retail<br>store). All types of interactions,<br>including interaction history order<br>history, trouble ticket history,<br>billing collection history, case<br>management, etc...<br>The Store of any communications in<br>any current or future form including<br>Fax, IVR, email, Page, text, online<br>chat, social media, and postal mail.<br>The storage of all inbound and<br>outbound interactions with the<br>customer. | Welcome and<br>Interaction | Customer<br>Interaction<br>Management |
| 239 | Recommendation to<br>Customer<br>Notification | Recommendation to Customer<br>Notification provides necessary<br>hooks to reach out to the customer<br>via preferred channel such as SMS,<br>email or Social media<br>For Inbound, Self-Service or<br>Call Center touch points can get<br>recommendation and a guided<br>action flow to complete the<br>suitable customer treatment (ex.<br>Credit Adjustment handled by<br>agent, or bill dispute initiation via<br>self-service) | Welcome and<br>Interaction | Customer<br>Interaction<br>Management<br>Customer<br>Context<br>Management |
| 1041 | Partner Interaction<br>Journalizing | Partner Interaction Journalizing<br>provides collection & storage of all<br>contact events with the partner via<br>all channels whether unassisted<br>(self service, retail kiosk) or<br>assisted (call center, retail store). | Business<br>Partner<br>Welcome and<br>Interaction | Business<br>Partner<br>Interaction<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF683 | Party Interaction Management | Mandatory | partyInteraction:<br>• GET<br>• GET /id<br>• POST<br>• PATCH<br>• DELETE |
| TMF701 | Process Flow Management | Optional | processFlow:<br>• POST<br>• GET<br>• GET /id<br>• DELETE<br>taskFlow:<br>• PATCH<br>• GET<br>• GET /id |
| TMF688 | Event | Optional | listener:<br>• POST<br>hub:<br>• POST<br>• DELETE |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF632 | Party Management | Optional | Get |
| TMF669 | Party Role Management | Optional | Get |
| TMF672 | Users Roles & Permissions | Optional | Get |
| TMF662 | Entity Catalog Management | Optional | Get |
| TMF667 | Document Management | Optional | Get |
| TMF681 | Communication Management | Optional | Optional |
| TMF701 | Process Flow Management | Optional | Get, Post, Patch |
| TMF688 | Event | Optional | Get |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component. While we are building this over the lifespan of this document, the file can be found here as well: TMForum-ODA-Ready-for-publication/1Beta2/TMFC023- PartyInteractionManagement/TMFC023-PartyInteractionManagement.yaml at main · tmforum-rand/TMForum-ODA-Ready-for-publication (github.com)

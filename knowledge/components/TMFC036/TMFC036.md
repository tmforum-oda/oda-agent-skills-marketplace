---
id: TMFC036
type: component
name: Lead And Opportunity Management
version: 1.2.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC036_Lead_and_Opportunity_Management_v1.2.1.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 8143ffd9a2ee512224b4a2884eefecbecbee37422eaf34a08a5b7c4498aabc2b
  raw_path: references/components/TMFC036/TMFC036_Lead_and_Opportunity_Management_v1.2.1.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF622
      name: product-ordering-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF648
      name: quote-management-api
    - id: TMF651
      name: agreement-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF699
      name: sales-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
yaml_spec_version: 1.2.0
---

# 1. Overview

| Component Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Lead and<br>Opportunity<br>Management | TMFC036 | Lead and Opportunity Management<br>component provides the functionality for<br>lead and opportunity capture,<br>qualification, reporting, and support<br>during the pre-sales stage. | Party Management |

![](media/lead-and-opportunity-management-architecture.png)
*([PlantUML source](media/lead-and-opportunity-management-architecture.puml))*

# 2. eTOM Processes, SID Data

Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.1.11 | 2 | Contact/Lead/Prospect<br>Management | Develop the appropriate relationships<br>with contacts, leads, and prospects<br>with the intent to convert them to<br>consumers, such as customers, or<br>providers, such as partners, of an<br>enterprise's offerings. |
| 1.1.11.1 | 3 | Manage Sales Contact | Manage all sales contacts between<br>potential or existing parties and the<br>enterprise. |
| 1.1.11.2 | 3 | Manage Sales Lead | Collect and administer a sales lead and<br>the associated probabilities of the lead<br>becoming a prospect. |
| 1.1.11.3 | 3 | Manage Sales Prospect | Match a sales prospect with the most<br>appropriate products and ensure that a<br>prospect is handled appropriately. |
| 1.1.9 | 2 | Selling | Responsible for managing prospective<br>customers, for qualifying and educating<br>customers, and matching customer<br>expectations<br>Managing prospective parties with<br>whom an enterprise may do business,<br>such as potential existing or new<br>customers and partners, for qualifying<br>and educating them, and ensuring their<br>expectations are met. |
| 1.1.9.1 | 3 | Qualify Selling<br>Opportunity | Ensure that a sales prospect is<br>qualified in terms of any associated risk<br>and the amount of effort required to<br>achieve a sale. |
| 1.1.9.3 | 3 | Acquire Sales Prospect<br>Data | Capture and record all pertinent sales<br>prospect data required for qualifying an<br>opportunity and for the initiation,<br>realization, and deployment of the<br>agreed sales proposal. |
| 1.1.7 | 2 | Market Sales Support &<br>Readiness | Market Sales Support & Readiness<br>processes ensure the support<br>capability is in place to allow the CRM<br>Fulfillment, Assurance and Billing<br>processes to operate effectively. |
| 1.1.7.2 | 3 | Support Selling | Administer and manage the operation<br>of the various sales channels and to<br>ensure that there is capability (for<br>example, information, materials,<br>systems, and resources) to support<br>the Selling processes. |
| 1.1.7.5 | 3 | Manage Sales Accounts | Manage the sales accounts assigned to<br>the sales channel on a day-day basis. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified. ** Sales Lead and Sales Opportunity are currently BEs in Sales Lead and Opportunity ABE Level 1 but refer to SID JIRA asking to create 2 ABEs Level 2.

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Sales Lead and Opportunity ABE | Sales Lead ** |
|   | Sales Opportunity ** |

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-lead-opportunity-links.png)
*([PlantUML source](media/etom-sid-lead-opportunity-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function<br>Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 394 | Sales Aids<br>Support | Sales Aids Support provides job<br>aids functions to access active<br>aids like template or wizard types<br>of context-aware scripting to e.g.<br>aid lead qualification as an<br>example. | Sales<br>Management | Opportunity<br>Management |
| 372 | Sales<br>Opportunity<br>Management | Sales Opportunity Management<br>creates, manages, and develop<br>sales opportunities for<br>customers. | Sales<br>Management | Opportunity<br>Management |
| 375 | Funnel<br>Assigning | Funnel Assigning provides the<br>necessary functionality to assign<br>sales personnel to leads within a<br>given funnel/pipeline. | Presales<br>Management | Sales Lead<br>Management |
| 374 | Funnel<br>Creation | Funnel Creation provides the<br>necessary functionality to create<br>a new sales funnel or pipeline | Presales<br>Management | Sales Lead<br>Management |
| 376 | Funnel Leads<br>Tracking | Funnel Leads Tracking provides<br>the necessary functionality to<br>track and manage the funnel<br>process of the various leads and<br>opportunities. | Presales<br>Management | Sales Lead<br>Management |
| 726 | Sales Lead<br>Capturing | Sales Lead Capturing handles the<br>generation of leads. A lead can be<br>generated from many sources and<br>customer interactions including<br>the result of a targeted marketing<br>campaign. Potential customer<br>information is obtained from<br>external sources or from<br>internally generated data. | Presales<br>Management | Sales Lead<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. List of Events (generated & consumed )- The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional |   | Operations |
| --- | --- | --- | --- | --- |
| TMF699 | Sales Management API | Mandatory | salesLead:<br>- GET<br>- GET /id<br>- POST<br>- PATCH |   |
| TMF701 | Process Flow Management | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id |   |
| TMF688 | Event Management | Optional |   |   |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- |
| TMF632 | Party Management | Optional | individual:<br>- GET<br>- GET/id<br>organization:<br>- GET<br>- GET/id | n/a |
| TMF620 | Product Catalog<br>Management | Optional | productOffering:<br>- GET<br>- GET/id<br>productOfferingPrice:<br>- GET<br>- GET/id | n/a |
| TMF651 | Agreement<br>Management | Optional | agreement:<br>- GET<br>- GET/id<br>agreementSpecification:<br>- GET<br>- GET/id | n/a |
| TMF648 | Quote Management | Optional | quote:<br>- GET<br>- GET /id | n/a |
| TMF669 | Party Role<br>Management | Optional | partyRole:<br>- GET<br>- GET/id | n/a |
| TMF701 | Process Flow<br>Management | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id | n/a |
| TMF688 | Event Management | Optional | Get, Get Id |   |
| TMF622 | Product Order Mgmt | Optional | productOrder:<br>- GET<br>- GET /id | n/a |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component Directory for the machine-readable component specification file for this component.

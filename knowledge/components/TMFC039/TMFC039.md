---
id: TMFC039
type: component
name: Agreement Management
version: 1.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC039_Agreement_Management_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 4265e509a65c86613aba70d3049c0f82f104e74ae8bfa34e7aa9a416af0fcefa
  raw_path: references/components/TMFC039/TMFC039_Agreement_Management_v1.1.0.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF651
      name: agreement-management-api
    - id: TMF667
      name: document-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS019
      name: TMFS019
    - id: TMFS019A
      name: "Part I: Partner On-boarding with Agreement Management"
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.1.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Agreement<br>Management | TMFC039 | Agreement Management component is<br>responsible for creating, storing, editing,<br>and tracking agreed arrangements with<br>related terms and conditions over a<br>lifecycle. The component manages<br>offers, records acceptance, and<br>associated considerations and<br>intentions to establish agreements as<br>legally binding.<br>As well this components provides<br>workfows and templates that facilitates<br>collaboration, communication, and<br>negotiation of agreements between<br>parties, and administers the specificities<br>related to translate agreements into<br>contracts, when it is required. It<br>provides a secure storage, version<br>control, compliance management, and<br>renewal notifications for agreements. | Party<br>Management |

![](media/agreement-management-architecture.png)
*([PlantUML source](media/agreement-management-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this component is responsible for are:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.6.5 | L2 | Party<br>Agreement<br>Management | Party Agreement Management manages all<br>aspects of agreements with parties, including<br>customers. Agreements include:<br>• Purchasing agreements for products,<br>services, and resources that meet the<br>enterprise’s needs<br>• On-boarding agreements for a Party's<br>offerings<br>• Service Level Agreements with one or<br>more other parties<br>• Agreements to use a Party as a sales<br>channel<br>• Reusable template agreements that<br>can be used to create any of the<br>above. |
| 1.7.14 | L2 | Enterprise<br>Governance | Enterprise Governance business process<br>manage activities that ensure accountability<br>and control of the strategic direction of the<br>organization. |
| 1.7.14.5 | L3 | Manage<br>Contract | Manage Contract business activity is in charge<br>of managing agreements, from their creation<br>through to their execution by chosen party, as<br>well as the termination of contracts.<br>Manage Contract business activity cover tasks<br>that include managing contract creation,<br>execution of contracts, analysis of contracts to<br>maximize operational and financial<br>performance and reducing financial risk. |

## 2.2. SID ABEs

SID ABEs this component is responsible for are:

eTOM L2 - SID ABEs links

| SID ABE Level 1 | SID ABE L1 Definition | SID ABE Level 2 (or set of BEs) | SID ABE L2 Definition |
| --- | --- | --- | --- |
| Agreement<br>ABE | One form of business<br>interaction in which Parties<br>(for example, Service<br>Providers or Customers)<br>engage is an agreement. An<br>agreement is a contract or<br>arrangement, either written<br>or verbal and sometimes<br>enforceable by law, such as<br>a service level agreement or<br>a customer price agreement.<br>An agreement involves a<br>number of other business<br>entities, such as Products,<br>Services, and/or<br>Resources. | Agreement | A type of<br>BusinessInteraction that<br>represents a contract or<br>arrangement, either written<br>or verbal and sometimes<br>enforceable by law. |
|   |   | AgreementItem | The purpose for an<br>Agreement expressed in<br>terms of a Product, Service,<br>Resource, and/or their<br>respective specifications,<br>inherited from<br>BusinessInteractionItem. |
|   |   | AgreementTermO<br>rCondition | Aspects of the Agreement<br>not formally specified<br>elsewhere in the Agreement<br>and that cannot be captured<br>elsewhere in a formal<br>notation, or automatically<br>monitored and require a<br>more human level of<br>management. |
|   |   | AgreementAuthori<br>zation | BusinessParticpant<br>responsible for approving an<br>Agreement. |
|   |   | AgreementApprov<br>al | A group of<br>AgreementAuthorizations<br>required from the<br>BusinessParticipants<br>involved in the Agreement. |

![](media/etom-sid-agreement-links.png)
*([PlantUML source](media/etom-sid-agreement-links.puml))*

## 2.3. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 1026 | Partner<br>Collaboration<br>Constraints<br>Collection | Partner Collaboration<br>Constraints Collection function<br>collect external and internal<br>constraints that can impact a<br>partner collaboration. The<br>partner strategy definition is<br>impacted by various factors,<br>like partner’s geographical<br>location, governmental<br>regulatory, product and<br>services offered etc. The<br>function also provides<br>capability to consider security<br>and financial risks,<br>environmental and legal issues<br>and existing agreements etc. | Purchasing<br>Strategy<br>Management | Purchasing<br>Strategy<br>Definition |
| 1045 | Partner<br>Agreement<br>Tracking | Partner Agreement Tracking<br>function keeps the association<br>of the partner product offerings<br>with the agreements and tracks<br>anomalies for single products<br>or group of products of the<br>partner. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1043 | Partner<br>Agreement<br>Storage and<br>Searching | Partner Agreement Storage<br>and Searching function provide<br>the ability to view Partner's<br>existing agreements, search for<br>partner agreements based on<br>meta-data and to search text<br>strings within agreements. The<br>data can also be mined for<br>partner strategy, negotiation,<br>workflow, and interaction<br>purposes. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1044 | Partner<br>Agreement<br>Implementation | Agreement Implementation<br>function provides support for<br>the implementation of the<br>agreement’s terms and<br>conditions to be used by<br>related organizations during<br>operations. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1042 | Partner<br>Agreement<br>Creation | Partner Agreement Creation<br>function provide the<br>functionality to automate the<br>creation of an agreement<br>based on templates or from<br>scratch. The function allows us<br>to create and maintain<br>predefined agreement options<br>and templates with terms and<br>conditions (e.g., pricing<br>information, payment clauses,<br>legal texts, etc.) for different<br>purposes and services. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1180 | Customer<br>Framework<br>Agreement<br>Approval | Customer Framework<br>Agreement Approval Function<br>manages all approval of Party<br>Roles involved in the<br>Framework Agreement<br>(Customer Roles as well as<br>CSP roles). | Sales<br>Management | Framework<br>Agreement<br>Management |
| 1179 | Customer<br>Framework<br>Agreement<br>Definition | The Customer Framework<br>Agreement Definition Function<br>consists in defining the<br>agreement that describes the<br>commitments and company<br>features valid for associated<br>customer orders.<br>It defines a subset of catalog<br>offers and products which will<br>be marketed to a customer with<br>particular conditions<br>(configurations of product,<br>rates, discounts, SLA such as<br>availability rate, restoration time<br>guaranties, and associated<br>penalties for the CSP). | Sales<br>Management | Framework<br>Agreement<br>Management |
| 363 | Product<br>Agreement<br>Storage | Product Agreement Storage<br>provides functionality<br>necessary to store and make<br>available the Product<br>Agreements.<br>This function allows:<br>• to instantiate or update<br>Product Agreement<br>approved by the customer<br>with their party involved,<br>their configuration, their<br>approvals and their status,<br>• to update Product<br>Agreements status,<br>• to search and read Product<br>Agreements. | Product<br>Agreement<br>Management | Product<br>Agreement<br>Storage |
| 361 | Product<br>Agreement<br>Implementation | Product Agreement<br>Implementation function<br>provides functionality pertaining<br>to the implementation of the<br>Product Agreement (a.k.a.<br>contract) across fulfillment,<br>assurance, and billing<br>according to Product<br>Agreement Specification.<br>A Product Agreement<br>represents the approval by the<br>Customer and the Vendor of all<br>term or conditions of a<br>ProductOffering. | Product<br>Management | Product<br>Agreement<br>Implementation |
| 653 | Contract<br>Management | Contract Management,<br>including establishment,<br>modification, and termination. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1042 | Partner<br>Agreement<br>Creation | Partner Agreement Creation<br>function provides the<br>functionality to automate the<br>creation of an agreement<br>based on templates or from<br>scratch. The function allows to<br>create and maintain predefined<br>agreement options and<br>templates with terms and<br>conditions (e.g., pricing<br>information, payment clauses,<br>legal texts, etc.) for different<br>purposes and services. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1043 | Partner<br>Agreement<br>Storage and<br>Searching | Partner Agreement Storage<br>and Searching function<br>provides the ability to view<br>Partner's existing agreements,<br>search for partner agreements<br>based on meta-data and to<br>search text strings within<br>agreements. The data can also<br>be mined for partner strategy,<br>negotiation, workflow and<br>interaction purposes. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1044 | Partner<br>Agreement<br>Implementation | Agreement Implementation<br>function provides support for<br>the implementation of the<br>agreement’s terms and<br>conditions to be used by<br>related organizations during<br>operations. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |
| 1045 | Partner<br>Agreement<br>Tracking | Partner Agreement Tracking<br>function keeps the association<br>of the partner product offerings<br>with the agreements and tracks<br>anomalies for single products<br>or group of products of the<br>partner. | Business<br>Partner<br>Management | Business<br>Partner<br>Agreement<br>Management |

# 3. TMF OPEN APIs & events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF651 | Agreement<br>Management API | Mandatory | agreement:<br>- GET<br>- GET/id<br>- POST<br>- PATCH/id<br>- DELETE/id<br>agreementSpecification:<br>- GET<br>- GET/id<br>- POST<br>- PATCH/id<br>- DELETE/id |
| TMF669 | Process Flow<br>Management API | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id |
| TMF688 | Event | Optional | n/a |

NOTE: "Resources Model coverage" element has been added to the table

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

The APIs called by this component and provided by other components are:

| API ID | API Name | Mandatory / Optional | Operation | Rationale |
| --- | --- | --- | --- | --- |
| TMF632 | Party<br>Management<br>API | Mandatory | individual:<br>- GET<br>- GET/id<br>organization:<br>- GET<br>- GET/id | From TMF651_Agreement<br>resource schema, where<br>Agreement vs<br>RelatedPArty relationship<br>is listed as 1,..* |
| TMF672 | User Roles &<br>Permissions | Mandatory | get |   |
| TMF669 | Party Role<br>Management<br>API | Optional | partyRole:<br>- GET<br>- GET/id | n/a |
| TMF620 | Product<br>Catalog<br>Management<br>API | Optional | productOffering:<br>- GET<br>- GET/id<br>productOfferingPrice:<br>- GET<br>- GET/id | n/a |
| TMF637 | Product<br>Inventory<br>API | Optional | product:<br>- GET<br>- GET/id | n/a |
| TMF667 | Document<br>Management<br>API | Optional | document:<br>- GET<br>- GET/id | n/a |
| TMF701 | Process<br>Flow<br>Management<br>API | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id | n/a |
| TMF688 | Event | Optional | get |   |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

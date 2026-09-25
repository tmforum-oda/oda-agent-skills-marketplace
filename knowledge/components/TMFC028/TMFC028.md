---
id: TMFC028
type: component
name: Party Management
version: 2.1.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC028_Party_Management_v2.1.1.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 306c234a26a1104e2484d2812936687723fd387741180550ac9229134fca3bc6
  raw_path: references/components/TMFC028/TMFC028_Party_Management_v2.1.1.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF688
      name: event-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS001
      name: New Party – Create your accounts
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS005
      name: Billing - Fiber Contract
    - id: TMFS006
      name: Legal Guardian
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
    - id: TMFS031
      name: Problem Management
yaml_spec_version: 2.1.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Party<br>Management | TMFC028 | The Party Management component is responsible<br>for the capture, validation, and management of<br>Parties. A Party may be an individual or<br>organization that has a relationship with an<br>enterprise. In this context it is responsible for the<br>end-to-end lifecycle of: Individual, Organization<br>and its related sub-entities, Contact Medium,<br>Currency and tax exemption certificates,<br>Identification, and Community. | Party<br>Management |

![](media/party-management-architecture.png)
*([PlantUML source](media/party-management-architecture.puml))*

# 2. eTOM Processes, SID Data

Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.16 | 2 | Customer<br>Inventory<br>Management | Establish, manage, and administer the enterprise's<br>customer inventory, as embodied in the Customer<br>Inventory Database, and monitor and report on the<br>usage and access to the customer inventory, and<br>the quality of the data maintained in it.<br>Note: validate if the "Customer Inventory<br>Shortcomings" (L3) should be into the scope of this<br>component. |
| 1.3.6 | 2 | Customer<br>Information<br>Management | Manage customer information after customer<br>contracts or associated service orders have been<br>finalized and during the order completion<br>phase. Ensure that any customer information<br>required by other CRM processes is updated as part<br>of the customer order completion.<br>Note: validate with eTOM team why CIM is an L2 and<br>not an L3 of Customer Inventory Mgmt. |
| 1.3.4 | 2 | Customer<br>Relationship<br>Management | Manage the relationship of the Customer and the<br>enterprise. |
| 1.3.4.2 | 3 | Establish<br>Customer<br>Relationship | Verify the customer identity and manage the<br>customer identity across the Enterprise. |
| 1.3.4.3 | 3 | Re-establish<br>Customer<br>Relationship | Re-establish customer relationship. |
| 1.3.4.4 | 3 | Terminate<br>Customer<br>Relationship | Manage termination as appropriate |
| 1.6.3 | 2 | Party<br>Relationship | Manage the lifecycles of parties with whom the<br>enterprise has a relationship. Relationship with new<br>parties may be required to broaden the services an<br>enterprise offers, to improve performance, for |
|   |   | Development &<br>Retirement | outsourcing and out-tasking requirements, and so<br>forth. |
| 1.6.3.1 | 3 | Party<br>Relationship<br>Management | Support the lifecycles (development and retirement)<br>of an enterprise's relationships with parties. |
| 1.6.3.1.5 | 4 | Collect Party<br>data | Collect data about a Party and/or a Party playing a<br>role. Data includes basic Party data, identification<br>data, contact data, and additional attributes. |
| 1.6.21 | 2 | Party Inventory<br>Management | Manage the administration of the enterprise's Party<br>inventory. |
| 1.7.7 | 2 | Human<br>Resources<br>Management | This process element represents part of the overall<br>enterprise, modeled in business process terms, and<br>can be applied (ie “instantiated") with other similar<br>process elements for application within a specific<br>organization or domain.<br>The Human Resources Management process<br>grouping provides the human resources<br>infrastructure for the people resources that the<br>enterprise uses to fulfil its objectives. |
| 1.7.7.2 | 3 | Develop the<br>Workforce | This process element represents part of the overall<br>enterprise, modeled in business process terms, and<br>can be applied (ie “instantiated") with other similar<br>process elements for application within a specific<br>organization or domain.<br>Support the definition of the organization of the<br>enterprise and coordinate its reorganizations. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| Party | • Party<br>• Contact Medium<br>• Currency and tax exemption certificates<br>• Party Identification<br>• Community |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-party-links.png)
*([PlantUML source](media/etom-sid-party-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 369 | Customer Data<br>Fencing | Customer Data Fencing<br>provides a security function<br>that will allow e.g., VNO<br>agents or Dealers to view<br>only their own customers.<br>In some cases, the network<br>provider will use the same<br>BSS environment to serve<br>several VNOs (multi<br>tenancy) | Customer<br>Information<br>Support | Customer<br>Information<br>Management |
| 225 | Customer Details<br>Management | Customer Details<br>Management; Managing<br>customer details - E.g.,<br>name, contact persons for<br>this customer, account<br>managers for this<br>customer, addresses<br>(residence, billing, service<br>address, etc.), contact<br>phone numbers (landline,<br>mobile, fax, etc.) | Customer<br>Information<br>Support | Customer<br>Information<br>Management |
| 400 | Customer<br>Information<br>Management | Customer Information<br>Management is a generic<br>function for customer<br>information that also<br>includes functionality for<br>data fencing if accessed by<br>Partner's online access<br>function to make them self-<br>sufficient and avoid the<br>need for them to call the<br>call center for Customer<br>creation and management. | Customer<br>Information<br>Support | Customer<br>Information<br>Management |
| 282 | Customer<br>Information<br>Presentation | Customer Information<br>Presentation displays<br>relevant customer<br>information, such as name,<br>account and lifetime value<br>on a persistent customer<br>dashboard. | Customer<br>Information<br>Support | Customer<br>Information<br>Management |
| 226 | Customer<br>Preferences<br>Administration | Customer Preferences<br>Administration<br>administrates customer<br>proprietary information<br>preferences (CPNI), email<br>versus US Mail, how to be<br>contacted (based on type of<br>communication), web look<br>and feel, do not solicit me.<br>Personalization allows<br>delivery of services that<br>more closely match the<br>customer's need. | Customer<br>Information<br>Support | Customer<br>Information<br>Management |
| 364 | Customer/Prospect<br>Data Acquisition | Customer/Prospect Data<br>Acquisition obtains all<br>necessary information to<br>make a sale. The prospect<br>could be a new or current<br>customer.<br>Customer/Prospect Data<br>Acquisition includes<br>information about the<br>service location, billing<br>address, demographic<br>information about the<br>customer, any existing<br>products and services the<br>customer currently has, as<br>well as the customer's<br>needs (requirements). | Customer<br>Information<br>Support | Customer<br>Information<br>Management |
| 92 | Customer Relation<br>Map Exposure | Customer Relation Map<br>Exposure maps the<br>customer relation/context<br>to systems such as call<br>center or self-service touch | Customer<br>Information<br>Support | Personalize<br>Customer<br>Profile |
| 233 | Customer Actions<br>Profile Updating | Customer Actions Profile<br>Updating updates customer<br>profiling based on implicit<br>and explicit actions,<br>transactions (ex., deriving<br>actual channel preference<br>from a customer whose<br>implicit preference is SMS,<br>not email) | Customer<br>Information<br>Support | Collect &<br>Qualify<br>Customer<br>Information |
| 195 | Customers<br>Hierarchy and<br>Group Management | Customer Hierarchy and<br>Group Management<br>function stores the<br>customer hierarchy and/or<br>groups such as company,<br>relationships and<br>household structures.<br>Manages complex<br>customer relationships<br>such as an individual who<br>performs multiple roles, or<br>hierarchies such as<br>complex Corporate<br>structures. This function<br>should be able to deal with<br>several levels of complexity<br>from single service<br>accounts to multinational<br>corporations. Hierarchies<br>are defined by an account<br>type and its relationships<br>with parent and child<br>accounts. | Customer<br>Information<br>Support | Collect &<br>Qualify<br>Customer<br>Information |
| 122 | Customer<br>Information<br>Searching | Customer Information<br>Searching search the<br>existing customer base<br>using various criteria<br>(name, address, subscriber<br>number, equipment id,<br>billing account number,<br>etc.) and find the customer<br>record to add the order<br>(using Customer<br>Information Management). | Customer<br>Information<br>Support | Collect &<br>Qualify<br>Customer<br>Information |
| 91 | Customer Profile<br>Updating | Customer Profile Updating<br>function concerns the<br>management of our<br>knowledge of the individual<br>customer to keep or<br>produce an up-to-date,<br>accurate and legally<br>compliant Customer<br>information.<br>It will incorporate into the<br>customer profile, all<br>relevant information<br>gathered through all<br>contacts with the customer | Customer<br>Information<br>Support | Collect &<br>Qualify<br>Customer<br>Information |
| 121 | Registration | Customer Registration<br>registers a new customer if<br>this is a new customer<br>(using Customer<br>Information Management). | Customer<br>Information<br>Support | Collect &<br>Qualify<br>Customer<br>Information |
| 124 | Guided Customer<br>Information<br>Capturing | Guided Customer<br>Information Capturing<br>provides a step-by-step<br>guide at the channel to<br>capture the specific<br>information items to be<br>collected (e.g. customer<br>identification, required<br>product / order and the<br>pertinent data for the<br>order). Including Validation<br>guidance – for each<br>information element, may<br>provide set of valid input | Customer<br>Information<br>Support | Collect &<br>Qualify<br>Customer<br>Information |
| 1036 | Partner Profile<br>Enquiry and<br>Filtering | Partner Profile Enquiry and<br>Filtering function provide<br>the necessary<br>functionalities to inquire<br>stored profiles including<br>filtering to both ensure<br>access based on authority<br>levels and for the<br>convenience for the reader. | Business<br>Partner<br>Management | Business<br>Partner<br>Inventory<br>Management |
| 1037 | Partner Profile<br>Storage | Partner Profile Storage<br>function secure data<br>availability and integrity for<br>the partner profile<br>management. | Business<br>Partner<br>Management | Business<br>Partner<br>Inventory<br>Management |
| 746 | Partner Workflow<br>Management | Partner Workflow<br>Management function<br>provide workflow and<br>orchestration for<br>supplier/partner<br>management activities. | Business<br>Partner<br>Management | Business<br>Partner<br>Inventory<br>Management |
| 1032 | Partner Group and<br>Hierarchy Definition | Partner Group and<br>Hierarchy Assigning assigns<br>partners to relevant groups<br>and hierarchies and make<br>the grouping available to<br>the concerned<br>organizations within the<br>enterprise | Business<br>Partner<br>Management<br>Business<br>Partner<br>Welcome and<br>interaction | Business<br>Partner Support<br>& Readiness |
| 1033 | Partner Group and<br>Hierarchy Assigning | Partner Group and<br>Hierarchy Definition defines<br>and creates partner group<br>types and hierarchy criteria<br>in line with the partner<br>strategy to support partner<br>collaboration with the<br>different organization of the<br>enterprise. | Business<br>Partner<br>Management<br>Business<br>Partner<br>Welcome and<br>interaction | Business<br>Partner Support<br>& Readiness |
| 1035 | Partner Preferences<br>Management | Partner Preferences<br>Management function<br>provide the necessary<br>functionalities to manage<br>partner preferences and<br>partner information details<br>in collaboration with the<br>partner. This includes<br>management of the stored<br>profile information<br>including creation, updating<br>and deletion as well as<br>lifecycle management by<br>supervision of validity and<br>recency. | Business<br>Partner<br>Management<br>Business<br>Partner<br>Welcome and<br>interaction | Business<br>Partner Support<br>& Readiness |
| 1034 | Partner Profile<br>Management | Partner Profile Management<br>function provide the<br>necessary functionalities to<br>manage partner information<br>details for internal usages.<br>This includes management<br>of the stored profile<br>information including<br>creation, updating and<br>deletion as well as lifecycle<br>management by<br>supervision to keep<br>information valid and up to<br>date. | Business<br>Partner<br>Management | Business<br>Partner Support<br>& Readiness |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Opeartions |
| --- | --- | --- | --- |
| TMF632 | Party Management | Mandatory | individual:<br>- GET<br>- GET/id<br>- POST<br>- PATCH/id<br>- DELETE/id<br>organization:<br>- GET<br>- GET/id<br>- POST |

| API ID | API Name | Mandatory / Optional |   | Opeartions |
| --- | --- | --- | --- | --- |
|   |   |   | - PATCH/id<br>- DELETE/id | - PATCH/id |
| TMF688 | Event Management | Optional |   |   |
| TMF701 | Process Flow Management | Optional |   | processFlow:<br>- GET<br>- GET/id<br>- POST<br>- DELETE/id<br>taskFlow:<br>- GET<br>- GET/id<br>- PATCH/id |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations | Rationale |
| --- | --- | --- | --- | --- |
| TMF672 | User Roles And<br>Permissions | Mandatory | Get | n/a |
| TMF669 | Party Role<br>Management | Optional | partyRole:<br>- GET<br>- GET /id | n/a |
| TMF701 | Process Flow<br>Management | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id | n/a |
| TMF688 | Event Management | Optional | Get | n/a |
| TMF675 | Geographic Location<br>Mgmt. | Optional | geographicLocation:<br>- GET<br>- GET /id | n/a |
| TMF674 | Geographic Site<br>Mgmt. | Optional | geographicSite:<br>- GET<br>- GET /id | n/a |
| TMF673 | Geographic Address<br>Mgmt. | Optional | geographicAddress:<br>- GET<br>- GET /id | n/a |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component.

---
id: TMFC005
type: component
name: Product Inventory
version: 1.0.3
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC005_Product_Inventory_v1.0.3.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 6b7c6fab4cef4d130f1c022b70b0ea28c72783c58f5ff608ee6387da0526cad7
  raw_path: references/components/TMFC005/TMFC005_Product_Inventory_v1.0.3.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF622
      name: product-ordering-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF638
      name: service-inventory-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF651
      name: agreement-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS005
      name: Billing - Fiber Contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS009
      name: Usage and Balance Management
    - id: TMFS011
      name: Order Fallout Management
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS021
      name: Orchestration of a Multi Party, Multi domain Sales Order
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.0.4
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Product<br>Inventory | TMFC005 | The Product Inventory component is<br>responsible for storage and exposure of<br>products that are assigned to and used by<br>Parties. This component has functionality<br>that enables creation of inventory items,<br>inventory organization, inventory search or<br>filter, inventory monitoring and tracking,<br>inventory control and inventory auditing. The<br>minimum check to be performed upon<br>inventory item creation or update is for global<br>consistency with related Product Catalog<br>information. | Core<br>Commerce<br>Management |

![](media/product-inventory-architecture.png)
*([PlantUML source](media/product-inventory-architecture.puml))*

# 2. eTOM Processes, SID

Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.2.11 | L2 | Product<br>Inventory<br>Management | Product Inventory Management is responsible to<br>establish, manage and administer the enterprise's<br>product inventory, as embodied in the Product<br>Inventory repository, and monitor and report on the<br>usage and access to the product inventory, and the<br>quality of the information maintained in it. |
| 1.1.19 | L2 | Loyalty Program<br>Management | Define all aspects of a loyalty program, such as<br>requirements and objectives of a loyalty program,<br>determine the benefits to participants. Develop a<br>program, prototype it, test it, rollout/launch it, amend<br>and evaluate it, and terminate it when it is no longer<br>viable for an enterprise.<br>Manage all operational aspects of running a loyalty<br>program. Enable parties to become a members of a<br>program, earn currency and rewards, and redeem<br>currency. Manage a loyalty program account, leave a<br>program, and provide operational reports. |
| 1.1.19.2 | L3 | Loyalty Program<br>Operation | Manage all operational aspects of running a loyalty<br>program. Enable parties to become a members of a<br>program, earn currency and rewards, and redeem<br>currency. Manage a loyalty program account, leave a<br>program, and provide operational reports. |
| 1.1.19.2.5 | L4 | Manage Loyalty<br>Program<br>Account | Update a loyalty program account and make changes<br>to loyalty program participant information. Expire,<br>reinstate, transfer in/out, adjust, a loyalty<br>participant's account currency. Prepare and send a<br>loyalty program communication to a participant or for<br>internal use by an enterprise. |
| 1.1.19.2.7 | L4 | Provide Loyalty<br>Program<br>Operation<br>Report | Generate a loyalty program operation report, such as<br>various loyalty program status reports, trend analysis,<br>and reports that identify suspected abuse of a loyalty<br>program. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| Product |   |
| Loyalty | Loyalty Program |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-product-loyalty-links.png)
*([PlantUML source](media/etom-sid-product-loyalty-links.puml))*

## 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 180 | Assigned Products<br>Maintenance | Assigned Products<br>Maintenance permits defining<br>and update :<br>- product characteristics<br>- links with the related service<br>or resource (handsets, SIM<br>cards, ...) needed to deliver the<br>product, ... | ProductReposito<br>ry Management | ProductInventory<br>Repository<br>Management |
| 197 | Customer Product<br>Storage | Customer Product Storage<br>provides the functionality<br>necessary to store and make<br>available the Products./<br>services presently being used<br>by the customer.<br>This function allows:<br>• to instantiate or update<br>offers and products ordered<br>by the customer, whatever<br>their type (network product,<br>bundle, device, …) or their<br>marketing mode (rented,<br>sold, …), with their<br>configuration, their tariffs<br>and discounts, and their<br>status (initialized with a<br>creation order)<br>• to update Products status<br>• to search and read Offer<br>and Product installed base<br>(subscribed offers,<br>configuration of installed<br>products, installed tariffs<br>and discount, statuses, …). | ProductReposito<br>ry Management | ProductInventory<br>Repository<br>Management |
| 198 | Customer Loyalty<br>Score Balance<br>Management | Customer Loyalty Score<br>Balance Management function<br>calculates the score according<br>to accumulation/decrease<br>rules. When a customer<br>subscribes to the loyalty<br>program with more than one<br>SIM or other ‘traffic objects’,<br>the Score Management<br>accumulates the points into a<br>single balance. The loyalty<br>score could decrease for one<br>of the following events: prize<br>purchase, points expiry or<br>points deletion by Call Centre.<br>The functionality may also<br>include the visualization of<br>Score details (date,<br>description event type, points,<br>final score) via different<br>contact Channels (e.g. via<br>Web, IVR, Call Centre). | ProductReposito<br>ry Management | Loyalty Account<br>Management |
| 237 | Customer Loyalty<br>Communication | Customer Loyalty<br>Communication function<br>sends information related to<br>Loyalty Programs (Point<br>Balance, Prize Request status,<br>renewed Loyalty Code) to<br>external components in push<br>and pull modes. | ProductReposito<br>ry Management | Loyalty Account<br>Management |
| 361 | Contract<br>Implementation Pro<br>duct Agreement<br>Implementation | Contract Implementation<br>function provide functionality<br>pertaining to the<br>implementation of the<br>contract across fulfillment,<br>assurance, and billing.<br>Product Agreement<br>Implementation function<br>provides functionality<br>pertaining to the<br>implementation of the<br>Product Agreement (a.k.a.<br>contract) across fulfillment,<br>assurance, and billing<br>according to Product<br>Agreement Specification.<br>A Product Agreement<br>represents the approval by<br>the Customer and the Vendor<br>of all term or conditions of a<br>ProductOffering. | ProductReposito<br>ry Management | ProductInventory<br>Agreement<br>Management |
| 362 | Contract Searching | Contract Searching function<br>provides the ability to search<br>for customer contracts based<br>on meta-data and to search<br>text strings within contracts<br>and view customer's existing<br>and previous contracts, | Product<br>Repository<br>Management | Product<br>Inventory<br>Management |
| 363 | Contract Storage<br>Product Agreement<br>Storage | Contract Storage provides the<br>central repository for contract<br>storage as well as the<br>associated contract meta-<br>data. This data can be mined<br>for Campaigns and Lead<br>Generation.<br>Product Agreement Storage<br>provides functionality<br>necessary to store and make<br>available the Product<br>Agreements.<br>This function allows:<br>• to instantiate or update<br>Product Agreement approved<br>by the customer with their<br>party involved, their<br>configuration, their<br>approvals and their status,<br>• to update Product<br>Agreements status,<br>• to search and read Product<br>Agreements. | ProductReposito<br>ry Management | ProductInventory<br>Agreement<br>Management |
| 1201 | Product<br>Configuration<br>Check | Product Configuration Check<br>Function Checks for each<br>Product submitted if all<br>Product configuration rules<br>have been respected such as<br>prerequisite, incompatibility<br>rules between<br>ProductSpecifications or<br>mandatory characteristics. | Product<br>Management | Product<br>Repository<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
| --- | --- | --- | --- | --- | --- |
| TMF637 | Product Inventory<br>Management | 4 | Mandatory | Product | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF688 | Event Management | 4 | Optional | listener | POST |
|   |   |   |   | hub | POST<br>DELETE |
| TMF701 | Process Flow<br>Management | 4 | Optional | processFlow | GET<br>GET /ID<br>POST<br>DELETE |
|   |   |   |   | taskFlow | GET<br>GET /ID<br>PATCH |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operation |
| --- | --- | --- | --- | --- | --- |
| TMF666 | Account<br>Management | 4 | Optional | billingAccount | Get<br>Get /id |
| TMF669 | Party Role<br>Management | 4 | Optional | partyRole | Get<br>Get /id |
| TMF632 | Party | 4 | Optional | individual | Get<br>Get /id |
|   |   |   |   | organization | Get<br>Get /id |
| TMF672 | User Roles And<br>Permissions | 4 | Optional | permission | Get<br>Get /id |
| TMF673 | Geographic Addre<br>ss Management | 4 | Optional | geographicAddress | Get<br>Get /id |
|   |   |   |   | geographicSubAddre<br>ss | Get<br>Get /id |
| TMF674 | Geographic Site<br>Management | 4 | Optional | geographicSite | Get<br>Get /id |
| TMF675 | Geographic<br>Location | 4 | Optional | geographicLocation | Get<br>Get /id |
| TMF651 | Agreement<br>Management | 4 | Optional | agreement | Get<br>Get /id |
| TMF639 | Resource<br>Inventory<br>Management | 4 | Optional | resource | Get<br>Get /id |
| TMF638 | Service Inventory<br>Management | 4 | Optional | service | Get<br>Get /id |
| TMF620 | Product Catalog<br>Management | 4 | Mandatory | productSpecification | Get<br>Get /id |
|   |   |   |   | productOffering | Get<br>Get /id |
|   |   |   |   | productOfferingPrice | Get<br>Get /id |
| TMF622 | Product Ordering | 4 | Optional | productOrder | Get<br>Get /id |
| TMF637 | Product Inventory | 4 | Optional | product | Get<br>Get /id<br>Post<br>Patch<br>Delete |
| TMF688 | Event<br>Management | 4 | Optional | event | Get<br>Get /id |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component Map on the TM Forum website for the machine- readable component specification files for this component.

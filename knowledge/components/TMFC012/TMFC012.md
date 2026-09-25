---
id: TMFC012
type: component
name: Resource Inventory
version: 2.1.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC012_Resource_Inventory_v2.1.1.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: f4ddd532c8ed4c1a56e0c42beb637b9f1537bf3c4ce1fc613850452d991feecb
  raw_path: references/components/TMFC012/TMFC012_Resource_Inventory_v2.1.1.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF685
      name: resource-pool-management-api
    - id: TMF701
      name: process-flow-management-api
    - id: TMF716
      name: resource-reservation
  use_cases:
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS011
      name: Order Fallout Management
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS025
      name: Cloud Native Function Management
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 2.2.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Resource<br>Inventory | TMFC012 | The Resource Inventory component owns<br>accounting for resources (all inputs - including<br>stock, parts, assets, production components etc.)<br>that are owned and/or held for allocation and/or<br>use by the organization. The Resource Inventory<br>component has functionality that includes<br>inventory item creation, inventory organization,<br>inventory search or filter, inventory monitoring and<br>tracking, inventory control (organization, re-stock<br>management etc.) and inventory auditing. The<br>minimum check to be performed at inventory item<br>creation or update is for global consistency with<br>related Resource Catalog information. | Production |

![](media/resource-inventory-architecture.png)
*([PlantUML source](media/resource-inventory-architecture.puml))*

# 2. eTOM Processes and

SID Data Entities

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.5.4 | L2 | Resource<br>Support<br>Readiness | Manage resource infrastructure to ensure that<br>appropriate application, computing and network<br>resources are available and ready to support the<br>Fulfillment, Assurance and Billing processes in<br>instantiating and managing resource instances, and for<br>monitoring and reporting on the capabilities and costs of<br>the individual FAB processes. |
| 1.5.4.5 | L3 | Manage<br>Resource<br>Inventory | Establish, manage and administer the enterprise's<br>resource inventory, as embodied in the Resource<br>Inventory Database, and monitor and report on the usage<br>and access to the resource inventory, and the quality of<br>the data maintained in it |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| Resource ABE | Logical Resource ABE, Physical Resource ABE, Compound<br>Resource ABE |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-resource-links.png)
*([PlantUML source](media/etom-sid-resource-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Aggregate Functions Level 1 | Aggregate Functions Level 2 |
| --- | --- | --- | --- | --- |
| 426 | Physical<br>Implementation<br>Information<br>Capturing | Physical Implementation<br>Information Capturing<br>provide levels of<br>implementation details that<br>tactical planning does not<br>need to specify, such as duct<br>routes and the frame<br>appearances of device ports. | Resource<br>Management | Resource<br>Repository<br>Management |
| 442 | Network<br>Overviews<br>Presentation | Network Overviews<br>Presentation provides a more<br>generalized view of the<br>network than found in<br>resource management. | Resource<br>Management | Resource<br>Repository<br>Management |
| 471 | Resource<br>Repository<br>Updating | Resource Repository<br>Updating function entails<br>update of the resource<br>Repository based on a<br>provided collection of<br>updates. The expectation is<br>that the Repository is<br>updated as requested, but no<br>other side effects are<br>expected (e.g., creating a Sub<br>Network Connection (SNC) in<br>the network). This is a key<br>point concerning this<br>capability. The Repository<br>update request can involve<br>addition (new object),<br>modification (change to an<br>existing object) or deletion<br>(removal of an object). | Resource<br>Management | Resource<br>Repository<br>Management |
| 453 | Resource<br>Configuration<br>Change Logging | Resource Configuration<br>Change Logging - Collects<br>and Records the history of<br>configuration changes | Resource<br>Management | Resource<br>Repository<br>Management |
| 454 | Resource<br>Configuration<br>Management | Resource Configuration<br>Management provides<br>configuration database and<br>management of the<br>configurations of the<br>individual resources | Resource<br>Management | Resource<br>Repository<br>Management |
| 456 | Resource<br>Topology<br>Verification | Resource Topology<br>Verification work with the<br>Inventory Management<br>functions to ensure that the<br>topology reflected in its<br>database is in sync with that<br>in the Inventory Management<br>Systems | Resource<br>Management | Resource<br>Repository<br>Management |
| 468 | Resource<br>Information<br>Model Creation | Resource Information Model<br>creation function allows<br>Service Providers to create<br>information base in the<br>resource inventory of the<br>managed resources along its<br>attributes. This function uses<br>the standardized information<br>model (e.g. TM Forum<br>Information Framework) for<br>the resources to be<br>managed. The specific<br>details will depend on the<br>particular resources (e.g.,<br>particular types of managed<br>elements and equipments)<br>and associated technologies. | Resource<br>Management | Resource<br>Repository<br>Management |
| 470 | Resource<br>Inventory<br>Retrieval | This function allows for client<br>operations support (service<br>assurance and billing<br>systems) to retrieve part or all<br>of the resource inventory<br>known to the target OSS. This<br>feature may allow the<br>following selection criteria:<br>• retrieval of a specified set of<br>one or more sub-trees<br>• exclusion or inclusion of<br>specified object types from<br>the selected sub-tree<br>• further filtering based on<br>attribute matching<br>• retrieval of only the object<br>instances that have been<br>modified after a provided<br>date and time<br>• For the selected objects,<br>this feature may allow the<br>client operations support<br>(service assurance and billing<br>systems) to specify what<br>specific attributes and<br>relationships shall be<br>returned. This (the attributes<br>and relationships to be<br>returned) would be the same<br>for all objects of the same<br>type | Resource<br>Management | Resource<br>Repository<br>Management |
| 471 | Resource<br>Inventory<br>Updating | Resource Inventory Updating<br>function entails update of the<br>resource inventory based on<br>a provided collection of<br>updates. The expectation is<br>that the inventory is updated<br>as requested, but no other<br>side effects are expected<br>(e.g., creating a Sub Network<br>Connection (SNC) in the<br>network). This is a key point<br>concerning this capability.<br>The inventory update request<br>can involve addition (new<br>object), modification (change<br>to an existing object) or<br>deletion (removal of an<br>object). | Resource<br>Management | Resource<br>Repository<br>Management |
| 472 | Resource<br>Inventory<br>Update<br>Notification | Resource Inventory Update<br>Notification function entails<br>the generation of inventory<br>update notifications based<br>on changes to the<br>inventory: Notifications<br>concerning object creation,<br>object deletion and attribute<br>value changes to other<br>systems.<br>• Single Entity Notifications –<br>in this variation of the<br>feature, each notification<br>pertains to only one entity,<br>e.g., an equipment instance<br>• Multi-entity Notifications –<br>in this variation of the<br>feature, a single notification<br>may report on inventory<br>changes for multiple entities.<br>• Notification Suppression –<br>in this variation of the<br>feature, each notification<br>pertains to only one entity. | Resource<br>Management | Resource<br>Repository<br>Management |
| 562 | Voucher<br>Reporting | Voucher Reporting function<br>for querying and reporting of<br>voucher related data | Resource<br>Management | Resource<br>Repository<br>Management |
| 564 | Voucher Life<br>Cycle<br>Management | Voucher Life Cycle<br>Management including<br>activation, locking,<br>expiration and maintenance<br>of purchased vouchers. | Resource<br>Management | Resource<br>Repository<br>Management |
| 738 | Resource Data<br>Inventory<br>Synchronization | Resource Data Inventory<br>Synchronization is the<br>function that ensure OSS<br>Inventory data generated in<br>each function is available to<br>other functions as required. | Resource<br>Management | Resource<br>Repository<br>Management |
| 436 | Number Aging | Manages the aging of<br>numbers before they can be<br>re-assigned. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 437 | Number<br>Assigning | Number Assigning manages<br>the assignment of numbers<br>for usage. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 439 | Number<br>Searching | Number Searching provides<br>the means to search the<br>number inventory. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 440 | Number<br>Tracking and<br>Reporting | Provides functionality to<br>track numbers and perform<br>number reporting. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 743 | Number<br>Portability<br>Orchestration | Number Portability<br>Orchestration is a<br>communication mechanism<br>that ensures the Resource<br>Number orders activation<br>according to a criteria set,<br>allowing in this way the<br>correct execution of orders. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 744 | Number<br>Portability Risk<br>& Effectiveness<br>Management | Number Portability Risk &<br>Effectiveness Management<br>for determine of threats, risks<br>and control of fulfillment, in<br>order to comply with the<br>execution of all Resource<br>Number Portability orders. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 745 | Number<br>Portability<br>Validation | Number Portability Validation<br>can perform calculations that<br>determine whether the<br>information received is<br>reliable, safe and contains<br>the minimum information<br>required during<br>implementation, enabling<br>with this the Resource<br>Number Portability orders<br>rejection for those who do<br>not comply with the defined<br>criteria. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 1062 | Number<br>Acquisition | Number Acquisition<br>manages the capturing of<br>numbers for the number<br>inventory. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 1249 | Number Porting | Number Porting implements<br>the changes to transfer the<br>management of a number<br>from one Service Provider to<br>another, and on request<br>provides status on the<br>implementation of the<br>changes. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 438 | Number<br>Reservation | Provides the functionality to<br>manage the reservation of<br>numbers. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |
| 435 | Number<br>Inventory<br>Establishing | Number Inventory<br>Establishing manages the<br>establishment of a number<br>inventory. | Resource<br>Management | Regulated<br>Logical<br>Resources<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operation |
| --- | --- | --- | --- | --- | --- |
| TMF639 | TMF639 Resource<br>Inventory | 4 | Mandatory | resource | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF688 | TMF688 Event | 4 | Optional | listener | POST |
|   |   |   |   | hub | POST<br>DELETE |
| TMF701 | TMF701 Process<br>Flow | 4 | Optional | processFlow | GET<br>GET /ID<br>POST<br>DELETE |
|   |   |   |   | taskFlow | GET<br>GET /ID<br>PATCH |

## 3.2. Dependant APIs

The following diagram illustrates API/Resource/Operation potentially used by the resource inventory component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations | Rationales |
| --- | --- | --- | --- | --- | --- | --- |
| TMF634 | Resource<br>Catalog<br>Management | 4.1 | Mandatory | resourceSpecific<br>ation | Get<br>get /ID | Consistency<br>check. |
| TMF669 | Party Role<br>Management | 4 | Optional | partyRole | Get<br>get /ID |   |
| TMF632 | Party<br>Management | 4 | Optional | induvidual /<br>organization | Get<br>get /ID |   |
| TMF673 | Geographic Ad<br>dress<br>Management | 4 | Optional | geographicAddre<br>ss | Get |   |
|   |   |   |   | geographicSubAd<br>dress | Get<br>get /ID |   |
| TMF674 | Geographic<br>Site<br>Management | 4 | Optional | geographicSite | Get<br>get /ID |   |
| TMF675 | Geographic<br>Location | 4 | Optional | geographicLocati<br>on | Get<br>get /ID |   |
| TMF672 | User Roles And<br>Permissions | 4 | Optional | permission | Get<br>get /ID |   |
| TMF639 | Resource<br>Inventory<br>Management | 4 | Optional | resource | Get<br>get /ID<br>Post,<br>Patch<br>Delete |   |
| TMF688 | Event | 4 | Optional | event | Get, Post |   |

## 3.3. Events

The following diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component Map on the TM Forum website for the machine- readable component specification files for this component.

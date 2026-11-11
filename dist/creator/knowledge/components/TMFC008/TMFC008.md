---
id: TMFC008
type: component
name: Service Inventory
version: 1.2.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC008_Service_Inventory_v1.2.1.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 8bf1478239b33dbc54f2c0ab77ae828839b19e66a84d6d08b620ed95a2f3223f
  raw_path: references/components/TMFC008/TMFC008_Service_Inventory_v1.2.1.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF633
      name: service-catalog-management-api
    - id: TMF638
      name: service-inventory-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF641
      name: service-ordering-management-api
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
    - id: TMFS004
      name: Order Delivery – Fiber contract
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
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
yaml_spec_version: 1.2.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Service<br>Inventory | TMFC008 | The Service Inventory component is responsible<br>for storage and exposure of CFS (Customer Facing<br>Services) that are associated to Product Inventory<br>items. It is also responsible for RFS (Resource<br>Facing Service) definition, mapping between CFS<br>and RFS and mapping with infrastructure/network<br>resources. The Service Inventory component has<br>functionality that enables creation of inventory<br>items, inventory organization, inventory search or<br>filter, inventory monitoring and tracking, inventory<br>control and inventory auditing. The minimum<br>check to be performed at inventory item creation<br>or update is for global consistency with related<br>Service Catalog information. | Production |

![](media/service-inventory-architecture.png)
*([PlantUML source](media/service-inventory-architecture.puml))*

# 2. eTOM Processes SID

Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.4.4 | L2 | Service Support<br>Readiness | Manage service infrastructure, ensuring that the<br>appropriate service capacity is available and ready<br>to support the SM&O Fulfillment, Assurance and<br>Billing processes |
| 1.4.4.1 | L3 | Manage Service<br>Inventory | Establish, manage, and administer the enterprise's<br>service inventory, as embodied in the Service<br>Inventory Database, and monitor and report on the<br>usage and access to the service inventory, and the<br>quality of the data maintained in it. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| Service ABE |   |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-service-links.png)
*([PlantUML source](media/etom-sid-service-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Aggregate Functions Level 1 | Aggregate<br>Functions Level 2 |
| --- | --- | --- | --- | --- |
| 576 | Service Data<br>Retrieval | Service Data Retrieval<br>provides retrieval of<br>appropriate inventory<br>data for example in the<br>context of service end to<br>end testing. | Service<br>Management | Service Repository<br>Management |
| 593 | ServiceInventory<br>Repository<br>Updating | ServiceInventory<br>Repository Updating<br>updates information in the<br>service inventory<br>according to the<br>configuration of specific<br>services | Service<br>Management | ServiceInventory<br>Repository<br>Management |
| 628 | Service to<br>Resource<br>Relationship<br>Management | Service to Resource<br>Relationship Management<br>provides Creation, Update<br>and Deletion of the<br>relations of stand-alone<br>physical or logical<br>resources whose<br>assignment is critical to<br>service's fulfillment, and<br>whose tracking is critical<br>to service operations,<br>assurance, and billing, as<br>well as, resources, which<br>represent a larger<br>resource structure<br>supporting the service,<br>often referred to as an<br>Access Point. | Service<br>Management | ServiceInventory<br>Repository<br>Management |
| 629 | Service to<br>Resource<br>Relationship<br>Synchronization | Service to Resource<br>Relationship<br>Synchronization function<br>entails reconciliation of<br>the data in a Service<br>Inventory Management<br>system with inventory<br>discovered from other<br>sources and synchronizes<br>mismatched service<br>inventory records. | Service<br>Management | ServiceInventory<br>Repository<br>Management |
| 630 | Service-<br>Resource<br>Relationship<br>Management<br>Notifications | Service-Resource<br>Relationship Management<br>Notifications; Notification<br>of Service-Resource<br>Relationship Management<br>actions to relevant<br>stakeholders | Service<br>Management | Service Reporting<br>Service Repository<br>Management |
| 964 | Onboarded<br>Service<br>Integration<br>Configuration | Onboarded Service<br>Integration Configuration<br>function will configure<br>the on boarded service<br>and the relevant systems<br>to establish integration<br>automatically, when<br>requested. There are<br>several system services<br>in the infrastructure that<br>needs to be aware and<br>integrated with the new<br>service. | Service<br>Management | Service Repository<br>Management |
| 965 | Service Instance<br>Lifecycle<br>Management | Service Instance Lifecycle<br>Management function will<br>control the starting of new<br>instances and closing of<br>instances of a service as<br>well as other activity<br>states of the service<br>instances.<br>Software based Services’<br>performance and<br>availability may be<br>controlled by managing<br>multiple instances of the<br>service with multiple<br>states of activity. | Service<br>Management | ServiceInventory<br>Repository<br>Management |
| 1344 | Service<br>Topology<br>Discovery | Service Topology<br>Discovery function<br>provides the required<br>capability to discover<br>how resources (e.g.<br>network) are related to<br>each other in providing a<br>service. | Service<br>Management | Service Repository<br>Management |

# 3. TMF OPEN APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
| --- | --- | --- | --- | --- | --- |
| TMF638 | Service Inventory<br>Management | 4 | Mandatory | service | Get<br>Get /ID<br>POST<br>PATCH<br>DELETE |
| TMF701 | Process Flow | 4 | Optional | processFlow | Get<br>Get /ID<br>POST<br>DELETE |
|   |   |   |   | taskFlow | Get<br>Get /ID<br>PATCH |
| TMF688 | Event | 4 | Optional | listener | POST |
|   |   | 4 |   | hub | POST<br>DELETE |

## 3.2. Dependant APIs

The following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resources | Operations |
| --- | --- | --- | --- | --- | --- |
| TMF639 | Resource Inventory<br>Management | 4 | Optional | resource | Get<br>Get /ID |
| TMF669 | Party Role<br>Management | 4 | Optional | partyRole | Get<br>Get /ID |
| TMF632 | Party Management | 4 | Optional | induvidual /<br>organization | Get<br>Get /ID |
| TMF672 | User Roles<br>Permission | 4 | Optional | permission | Get<br>Get /ID |
| TMF673 | Geographic Address<br>Management | 4 | Optional | geographicAddress | Get<br>Get /ID |
|   |   |   |   | geographicSubAddress | Get<br>Get /ID |
| TMF674 | Geographic Site<br>Management | 4 | Optional | geographicSite | Get<br>Get /ID |
| TMF675 | Geographic<br>Location | 4 | Optional | geographicLocation | Get<br>Get /ID |
| TMF633 | Service Catalog<br>Management | 4 | Mandatory | serviceSpecification | Get<br>Get /ID |
| TMF641 | Service Ordering | 4 | Optional | serviceOrder | Get<br>Get /ID |
| TMF638 | Service Inventory<br>Management | 4 | Optional | service | Get<br>Get /ID,<br>Post,<br>Patch,<br>Delete |
| TMF688 | Event | 4 | Optional | event | Get<br>Get /ID,<br>Post |

## 3.3. Events

The following diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component Map on the TM Forum website for the machine- readable component specification files for this component.

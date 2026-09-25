---
id: TMFC007
type: component
name: Service Order Management
version: 1.2.2
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC007_Service_Order_Management_v1.2.2.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 5f14a8010a91a94591302a0fc65884175653e66ed9f0653432eb214bb9ef219c
  raw_path: references/components/TMFC007/TMFC007_Service_Order_Management_v1.2.2.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF633
      name: service-catalog-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF638
      name: service-inventory-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF640
      name: service-activation-management-api
    - id: TMF641
      name: service-ordering-management-api
    - id: TMF645
      name: service-qualification-management-api
    - id: TMF646
      name: appointment-management-api
    - id: TMF652
      name: resource-order-management-api
    - id: TMF653
      name: service-test-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF681
      name: communication-management-api
    - id: TMF697
      name: work-order-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS010
      name: ODA Flow with NaaS Support
    - id: TMFS011
      name: Order Fallout Management
    - id: TMFS012
      name: Product Catalog - Launching a New Product Offering
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS021
      name: Orchestration of a Multi Party, Multi domain Sales Order
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 2.0.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Functional Block |
| --- | --- | --- | --- |
| Service Order<br>Management | TMFC007 | Service Order Management (SOM)<br>component is the entry point to the<br>Production Domain. It oversees delivery of<br>Customer-Facing-Service (CFS) resources<br>(network and service platform equipment).<br>The SOM exposes the API ServiceOrder. It is<br>triggered when the Product Order Delivery<br>Orchestration And Management<br>component calls this API to request CFS<br>delivery. To achieve delivery of a CFS, the<br>SOM orchestrates the CFS delivery process<br>which identifies possible RFS and chooses<br>one, using the catalog and technical<br>inventory. It selects the resources (servers,<br>equipment, etc.) and their instances, and<br>requests the Resource Order Management<br>(ROM) component to update selected<br>resource instances to deliver CFS.<br>Requests sent to the ROM contain the CFS<br>and the list of configured resource<br>instances to be updated. | Production |

![](media/service-order-management-architecture.png)
*([PlantUML source](media/service-order-management-architecture.puml))*

# 2. eTOM Processes, SID

Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this component is responsible for are:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.4.5 | L2 | Service<br>Configuration &<br>Activation | Allocation, implementation, configuration,<br>activation and testing of specific services to<br>meet customer requirements. |
| 1.4.5.1 | L3 | Design Solution | Develop an end-end specific service design which<br>complies with a particular customer's requirement |
| 1.4.5.2 | L3 | Allocate Specific<br>Service Parameters to<br>Services | Issue service identifiers for new services. |
| 1.4.5.3 | L3 | Track & Manage<br>Service Provisioning | Ensure service provisioning activities are assigned,<br>managed and tracked efficiently. |
| 1.4.5.4 | L3 | Implement, configure<br>& activate service | Implement, configure and activate the specific<br>services allocated against an issued service order. |
| 1.4.5.6 | L3 | Issue Service Order | Issue correct and complete service orders |
| 1.4.5.7 | L3 | Report service<br>provisioning | Monitor the status of service orders, provide<br>notifications of any changes and provide<br>management reports. |
| 1.4.5.8 | L3 | Close Service Order | Close a service order when the service<br>provisioning activities have been completed |
| 1.5.5 | L2 | Resource Order<br>Management | Resource Order Management business process<br>directs and controls ordering, scheduling, and<br>allocation of resources (such as materials,<br>equipment, and personnel) within the business. |
| 1.5.5.6 | L3 | Manage Resource<br>Order Capture | Manage Resource Order Capture is responsible for<br>directing and controlling the capture and<br>collection of resource orders from internal and<br>external customers. |
| 1.5.5.6.1 | L4 | Initiate Resource<br>Order Capture * | Initiate Resource Order Capture business activity<br>is responsible for the initial activity of capturing<br>and collecting resource orders from internal and<br>external customers. |
| 1.5.5.7 | L3 | Manage Resource<br>Work Order | Manage Resource Order Work business activity<br>directs and controls all work that are required to<br>fulfill an approved resource order by ensuring the<br>work related to the order is planned, executed and<br>closed in a timely and efficient manner. |
| 1.5.5.7.1 | L4 | Initiate Resource<br>Work Order * | Initiate Resource Work Order business activity<br>starts a new work order for a specific resource<br>along with all work orders tasks, roles and<br>supporting resources that are need. |

*to notice, only these L4 of these L3 and L2 are covered by TMFC007.

## 2.2. SID ABEs

SID ABEs this component is responsible for are:

| SID ABE<br>Level 1 | SID ABE L1 Definition | SID ABE Level 2 (or set of BEs)* | SID ABE<br>Level 2<br>Definition |
| --- | --- | --- | --- |
| Service<br>Order | The Service Order ABE contains entities that<br>represent a type of Request that decomposes a<br>Customer Order's products into the services<br>associated with a ServiceOrder through which<br>the products are realized. |   |   |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified. As for TMFC003 Product Order Delivery Orchestration and Management, we also need to describe Orchestration Plan and delivery process to manage here at Service Order level. Refer to Jira paragraph at the end of the document.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-service-order-links.png)
*([PlantUML source](media/etom-sid-service-order-links.puml))*

## 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 571 | Service<br>Delivery Due<br>Date<br>Calculation | Service Delivery Due Date<br>Calculation functions calculates<br>the service delivery due date<br>using network capacity, access<br>provider selection and work<br>center intelligence (including<br>workload and capacity). | Service Order<br>Management | Service Order<br>Initialization |
| 1061 | Service Order<br>Initiation | Service Order Initiation function<br>issues valid and complete<br>service orders. | Service Order<br>Management | Service Order<br>Initialization |
| 1219 | Service Order<br>Request<br>Consistency<br>Check | The Service Order Request<br>Consistency Check Function<br>allows, when receiving a Service<br>Order request prepared and<br>transmitted by another system,<br>to check its consistency. | Service Order<br>Management | Service Order<br>Initialization |
| 1220 | Internal<br>Service Order<br>Initialization | The Internal Service Order<br>Initialization Function permit to<br>initialize Customer Facing<br>Service Orders (a.k.a. CFS<br>Orders) for operator internal<br>needs, for example to change<br>(part of) a technical solution and<br>migrate operational Installed<br>CFS on the new solution<br>elements (ex: VOIP H323 -><br>VOIP SIP). | Service Order<br>Management | Service Order<br>Initialization |
| 592 | Service<br>Parameters<br>Reservation | Service Parameters Reservation<br>reserves the right service<br>parameters based on service<br>specification and service<br>inventory for a service order | Service Order<br>Management | Service<br>Availability |
| 584 | Service<br>Activation<br>Planning | Service Activation Planning<br>provides planning of service<br>activation to access, plan and<br>gather additional information for<br>service activation | Service Order<br>Management | Service Order<br>Orchestration |
| 588 | Service<br>Orchestration<br>Configuration | Service Orchestration<br>Configuration function provides<br>composition of a service<br>configuration plan according to<br>the required service actions and<br>sent to Service Order<br>Orchestration and/or Service<br>Activation Management | Service Order<br>Management | Service Order<br>Orchestration |
| 591 | Service<br>Parameters<br>Allocation | Service Parameters Allocation<br>provides allocation of the right<br>service parameters to fulfill<br>service orders | Service Order<br>Management | Service Order<br>Orchestration |
| 596 | Service Order<br>Transfer<br>Supervision | Oversees the transfer of Service<br>Order Requests to appropriate<br>resource providers. | Service Order<br>Management | Service Order<br>Orchestration |
| 598 | Service Order<br>Orchestration | The Service Order Orchestration<br>function provides workflow and<br>orchestration capabilities for a<br>dedicated Service (CFS) Order.<br>Orchestration is needed when:<br>• the technical solution<br>includes the expansion of<br>the operator Installed<br>Resources or the purchase<br>of a partner product (ex:<br>local loop purchase)<br>• a work order is necessary<br>at the delivery address or<br>somewhere in the operator<br>network<br>• part of the delivery process<br>or checks needs to be<br>delegated to another<br>Service Order Manager<br>• contributing or support<br>systems must be informed<br>Example: to deliver a VOIP<br>service, it will orchestrate<br>actions on Access Network<br>Factory, VOIP service platform<br>and CPE.<br>Service Order Orchestration will<br>also orchestrate and manage<br>dependencies between related<br>Service Order items of Service<br>Order. | Service Order<br>Management | Service Order<br>Orchestration |
| 734 | Service Data<br>Collection | The Service Data Collection<br>function gathers any needed<br>service data to aid in the<br>verification and issuance of a<br>complete and valid service order<br>as well as data necessary to<br>address dependencies between<br>service and/or resource orders. | Service Order<br>Management | Service Order<br>Orchestration |
| 963 | Service Task<br>Item<br>Decompositio<br>n | Service Task Item<br>Decomposition: By a request for<br>an orchestration of a service the<br>service needs to be analyzed<br>and decomposed into the part-<br>actions necessary to take to<br>fulfill the requested<br>orchestration. The Service may<br>consist of several services and<br>may use a number of<br>Resources. It may also be<br>controlled by several<br>parameters for optional<br>behaviors. This composition of<br>the Service is given by<br>configuration data available<br>from Catalog applications and<br>the Service Capability<br>Orchestration application. | Service Order<br>Management | Service Order<br>Orchestration |
| 968 | Service Work<br>Item<br>Sequence<br>Execution | Service Work Item Sequence<br>Execution function executes<br>each individual item in<br>sequence of the service<br>orchestration to fulfill, or roll<br>back according to a pre-defined<br>configuration, and reports the<br>sequence execution result.<br>Because of the “Service<br>Decomposition” of an<br>orchestration request the result<br>may be several actions that<br>needs to take place in a specific<br>sequence. | Service Order<br>Management | Service Order<br>Orchestration |
| 969 | Service Work<br>Item<br>Sequence<br>Execution<br>Configuration | The “Service Work Item<br>Sequence Execution" function<br>controls so that the sequence is<br>fulfilled or rolled back. The rules<br>for the sequence execution will<br>set the conditions for the<br>fulfillment, or roll-back, and for<br>the reporting and notification.<br>The “Service Task Item<br>Sequence Carry Through<br>configuration" is a management<br>of the application function that<br>defines how the execution of the<br>orchestration sequence will be<br>done. | Service Order<br>Management | Service Order<br>Orchestration |
| 632 | Service<br>Termination<br>Points<br>Determining | Service Termination Points<br>Determining determines the<br>termination points i.e. the<br>appropriate service provider<br>entry point to support the<br>Customer's service request. | Service Order<br>Management | Service<br>Technical<br>Solution<br>Identification |
| 735 | Access<br>Provider<br>Selection | Access Provider Selection<br>function selects an access<br>provider among identified<br>available access providers or<br>access technologies at the given<br>location, based on business<br>rules. | Service Order<br>Management | Service<br>Technical<br>Solution<br>Identification |
| 1141 | Installed<br>Resources<br>Identification | Installed Resources<br>Identification Function identifies<br>the installed resources to<br>update, as part of the chosen<br>technical solution, to deliver the<br>ordered service (CFS).<br>This information enriches the<br>CFS order and the CFS.<br>This choice is based on service<br>catalogue rules (between RFS<br>specification and Resources<br>specification) and it can be<br>necessary to check the installed<br>resources availability,<br>occupancy, etc. via the<br>Resource Availability function.<br>Cloud example: In case of a<br>cloud service, the Service Order<br>Delivery process only identifies<br>the equipment in charge of the<br>management of the cloud<br>infrastructure and it will be<br>informed of the ordered service<br>characteristics. Depending on<br>its own rules, the cloud<br>infrastructure manager will<br>decide or not to immediately<br>allocate and configure all or part<br>of the required resources.<br>So the first usage request of the<br>cloud service can trigger the<br>effective choice and<br>configuration of the necessary<br>resources and these resources<br>can change between usages. In<br>this case the end of the delivery<br>process is assumed by the<br>manager of the cloud<br>infrastructure.<br>Note: This function is globally a<br>part of the technical solution<br>identification. | Service Order<br>Management | Installed<br>Resources<br>Identification |
| 733 | Service Order<br>Decompositio<br>n | The Service Order<br>Decomposition Function allows<br>in the context of a Service Order<br>to prepare Resource Order,<br>Service Order which will be<br>delegated to another system,<br>Supplier Order, Stock Item<br>Order or Work Order with the<br>necessary information (the<br>effective update in the order<br>repositories will be supported by<br>the corresponding Order<br>Repository Management<br>functions).<br>In the case of a Service<br>associated with an existing<br>Internal Resource Type, this<br>function also allows to:<br>• check if a corresponding<br>Installed Resource is<br>operational in the resource<br>installed base, and determine<br>the operation to be performed at<br>Resource level (creation or<br>modification)<br>• eventually group in the same<br>Resource order several ordered<br>services, based on the same<br>Customer Facing Service<br>Specification (a.k.a. CFS<br>specification), and/or identified<br>to be delivered at the same time<br>by the Service Order Delivery<br>Orchestration. | Service Order<br>Management | Service Order<br>Delivery<br>Preparation |
| 1217 | Service Order<br>Needs<br>Identification | The Service Order Needs<br>Identification Function allows in<br>the context of a Service Order to<br>query catalogues and installed<br>bases to identify what needs to<br>be delivered: resource<br>specification and its<br>configuration, service<br>specification (CFSSpec),<br>intervention (WorkSpec),<br>supplier product, related to the<br>ordered service. | Service Order<br>Management | Service Order<br>Delivery<br>Preparation |
| 595 | Service Order<br>Completion | Completes the service order<br>when all resource orders have<br>been completed. | Service Order<br>Management | Service Order<br>Completion |
| 600 | Service Order<br>Validation | The Service Order Validation<br>function validates the service<br>order request based on<br>contract, catalog, and<br>provisioning rules. | Service Order<br>Management | Service Order<br>Completion |
| 583 | Activation<br>Notification | Activation Notification function<br>provides notifications on<br>successful activation and, in<br>cases of exceptions send<br>fallouts to Service Order<br>Orchestration and manage<br>rollbacks activities (if<br>applicable) | Service Order<br>Management | Service Order<br>Repository<br>Management |
| 594 | Service Order<br>Storage | Service order Storage function<br>stores the service order into an<br>appropriate data store. | Service Order<br>Management | Service Order<br>Repository<br>Management |
| 599 | Service Order<br>Tracking | The Service Order Tracking<br>function tracks and manages<br>the events and the lifecycle<br>related to the Service (CFS)<br>Order and to its items (e.g.:<br>service order lines).<br>It gathers Service Order items<br>delivery events from Service<br>Order Orchestration and<br>manages related Service Order<br>lifecycle and Installed CFS<br>lifecycle (via the Installed<br>Service Management function).<br>Depending on the Service Order<br>(or any of its elements) events,<br>and on the implemented<br>business rules, this function can<br>decide to notify other systems<br>(for example in case of delivery<br>problems or delays) – via the<br>business event publication<br>function. | Service Order<br>Management | Service Order<br>Repository<br>Management |
| 597 | Service Order<br>Exposure | Service Order Exposure provides<br>exposure of the status on the<br>overall service order. | Fulfillment<br>Integration<br>Management | Service<br>Fulfillment<br>Access<br>Management |
| 570 | Solution<br>Services<br>Design<br>Management | Solution Services Design<br>Management function supports<br>the end to end service design. It<br>applies engineering rules to<br>determine required network<br>facilities, equipment<br>configurations and the method<br>and access path to the<br>customer site or location of<br>service termination.<br>This function also establishes<br>and manages the detailed<br>design tasks required to issue<br>the work orders. | Service<br>Configuration &<br>Activation | Service<br>Configuration |
| 589 | Cross<br>Services<br>Dependencies<br>Configuration | Cross Services Dependencies<br>Configuration function provides<br>support for appropriately<br>considered cross service<br>dependencies as part of the<br>configuration activities to fulfill a<br>service order | Service<br>Configuration &<br>Activation | Service<br>Configuration |
| 590 | Service<br>Configuration | The Service Configuration<br>function is in charge of<br>configuring the specific service<br>and its parameters as<br>appropriate for the fulfillment of<br>a service order | Service<br>Configuration &<br>Activation | Service<br>Configuration |
| 341 | Service<br>Activation | Service Activation function for<br>services/products sold by<br>affiliates. | Service<br>Configuration &<br>Activation | Service<br>Activation |
| 342 | Mass Service<br>Pre-activation | Mass Service Pre-activation of<br>services to prepare for a swift<br>activation at sales. E.g.,<br>subsequent affiliate sales. | Service<br>Configuration &<br>Activation | Service<br>Activation |
| 585 | Service<br>Configuration<br>Activation | Service Configuration Activation<br>implements and activates the<br>specific service configuration<br>against the service configuration<br>plan (including activation of CPE<br>if part of the service) | Service<br>Configuration &<br>Activation | Service<br>Activation |
| 16 | Fallout<br>Automated<br>Correction | Fallout Automated Correction<br>function tries to automatically<br>fix fallouts in workflows before<br>they go to a human for handling.<br>This includes a Fallout Rules<br>Engine that provides the<br>capability to handling various<br>errors or error types based on<br>built rules. These rules can<br>facilitate autocorrection,<br>correction assistance,<br>placement of errors in the<br>appropriate queues for manual<br>handling, as well as access to<br>various systems. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 17 | Fallout<br>Correction<br>Information<br>Collection | Fallout Correction Information<br>Collection collects relevant<br>information for errors or<br>situations that cannot be<br>handled via Fallout Auto<br>Correction. The intent is to<br>reduce the time required by the<br>technician in diagnosing and<br>fixing the fallout. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 19 | Fallout<br>Manual<br>Correction<br>Queuing | Fallout Manual Correction<br>Queuing function provides the<br>required functionality to place<br>error fallout into appropriate<br>queues to be handled via<br>various staff or workgroups<br>assigned to handle or fix the<br>various types of fallout that<br>occurs during the fulfillment<br>process. This includes the ability<br>to create and configure queues,<br>route errors to the appropriate<br>queues, as well as the ability for<br>staff to access and address the<br>various fallout instances within<br>the queues. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 21 | Fallout<br>Orchestration | The Fallout Orchestration<br>function provides workflow and<br>orchestration capability across<br>Fallout Management. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 24 | Pre-populated<br>Fallout<br>Information<br>Presentation | Pre-populated Fallout<br>Information Presentation<br>automatically position the<br>analyzer on appropriate screens<br>pre-populated with information<br>about the order(s) that's subject<br>for fallout handling. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 756 | Fallout Rule<br>Based Error<br>Correction | Fallout Rule Based Error<br>Correction function provides the<br>capability to handle various<br>errors or error types based on<br>pre-defined rules. These rules<br>can facilitate autocorrection. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 18 | Fallout<br>Management<br>to Fulfillment | Fallout Management to<br>Fulfillment Application<br>Accessing function provides a<br>variety of tools to facilitate | Fallout<br>Management | Fallout<br>Repository<br>Management |
|   | Application<br>Accessing | Fallout Management access to<br>other applications and<br>repositories to facilitate proper<br>Fallout Management. This can<br>include various general access<br>techniques such as messaging,<br>publish and subscribe, etc. as<br>well as specific APIs and<br>contracts to perform specific<br>queries or updates to various<br>applications or repositories<br>within the fulfillment domain. |   |   |
| 20 | Fallout<br>Notification | Fallout Notification function<br>provides the means to alert<br>people or workgroups of some<br>fallout situation. This can be<br>done via a number of means,<br>including email, paging, (Fallout<br>management interface bus) etc.<br>This function is done via<br>business rules. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 22 | Fallout<br>Reporting | Fallout Reporting provides<br>various reports regarding Fallout<br>Management, including<br>statistics on fallout per various<br>times periods (per hour, week,<br>month, etc) as well as<br>information about specific<br>fallout. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 23 | Fallout<br>Dashboard<br>System Log-in<br>Accessing | Fallout Dashboard System Log-<br>in Accessing provides auto<br>logon capability into various<br>applications needed to analyze<br>and fix fallout. | Fallout<br>Management | Fallout<br>Repository<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event. <Note note to be inserted into ODA Component specifications: If a new Open API is required, but it does not yet exist. Then you should include a textual description of the new Open API, and it should be clearly noted that this Open API does not yet exist. In addition, a Jira epic should be raised to request the new Open API is added, and the Open API team should be consulted. Finally, a decision is required on the feasibility of the component without this Open API. If the Open API is critical then the component specification should not be published until the Open API issue has been resolved. Alternatively if the Open API is not critical, then the specification could continue to publication. The result of this decision should be clearly recorded.>

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF641 | Service Ordering<br>Management | Mandatory | serviceOrder:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE<br>cancelServiceOrder:<br>- GET<br>- GET /id<br>- POST |
| TMF701 | Process Flow | Optional | processFlow:<br>- GET<br>- GET /id<br>- POST<br>- DELETE /id<br>taskFlow:<br>- GET<br>- GET /id<br>- PATCH /id |
| TMF688 | Event Management | Optional | d |

## 3.2. Dependant APIs

Following diagram illustrates API/Resource/Operation potentially used by the Service Order Management component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- |
| TMF632 | Party Management<br>API | Optional | individual:<br>- GET<br>- GET /id<br>organization:<br>- GET<br>- GET /id | n/a |
| TMF633 | Service Catalog<br>Management API | Mandatory | serviceSpecification:<br>- GET<br>- GET /id | as<br>illustrated<br>into IG1228<br>per TMFS00 |
| TMF634 | Resource Catalog<br>Management API | Optional | resourceSpecification:<br>- GET<br>- GET /id |   |
| TMF638 | Service Inventory<br>Management API | Mandatory | service:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE | as<br>illustrated<br>into IG1228<br>per TMFS00 |
| TMF639 | Resource Inventory<br>Management API | Optional | resource:<br>- GET<br>- GET /id | n/a |
| TMF640 | Service Activation &<br>Configuration API | Optional | monitor:<br>- GET<br>- GET /id | n/a |
| TMF641 | Service Ordering<br>Management API | Optional | serviceOrder:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE<br>cancelServiceOrder:<br>- GET<br>- GET /id<br>- POST | n7a |
| TMF645 | Service<br>Qualification<br>Management API | Optional | checkServiceQualification:<br>- GET<br>- GET /id<br>- POST<br>- PATCH | n/a |
| TMF646 | Appointment<br>Management API | Optional | appointment:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>searchTimeSlot:<br>- GET<br>- GET /id<br>- POST<br>- PATCH | n/a |
| TMF652 | Resource Ordering<br>Management API | Optional | resourceOrder:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE<br>cancelResourceOrder:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE | n/a |
| TMF653 | Service Test<br>Management API | Optional | serviceTest:<br>- GET<br>- GET /id<br>serviceTestSpecification:<br>- GET<br>- GET /id | n/a |
| TMF669 | Party Role<br>Management API | Optional | partyRole:<br>- GET<br>- GET /id | n/a |
| TMF672 | User Role<br>Permission<br>Management API | Optional | permission:<br>- GET<br>- GET /id | n/a |
| TMF673 | Geographic Address<br>Management API | Optional | geographicAddress:<br>- GET<br>- GET /id<br>geographicSubAddress:<br>- GET<br>- GET /id<br>geographicAddressValidation:<br>- GET<br>- GET /id<br>- POST | n/a |
| TMF674 | Geographic Site<br>Management API | Optional | geographicLocation:<br>- GET<br>- GET /id | n/a |
| TMF675 | Geographic<br>Location<br>Management API | Optional | geographicSite:<br>- GET<br>- GET /id | n/a |
| TMF681 | Communication<br>Management API | Optional | communicationMessage:<br>- GET<br>- GET /id | n/a |
| TMF685 | Resource Pool<br>Management API | Optional | reservation:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE<br>resourcePool:<br>- GET<br>- GET /id |   |
| TMF688 | Event Management<br>API | Optional | event:<br>- GET<br>- GET /id | n/a |
| TMF697 | Work Order<br>Management API | Optional | workOrder:<br>- GET<br>- GET /id | n/a |
| TMF701 | Process Flow<br>Management API | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- PATCH | n/a |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

Event name always follows same pattern: <<Resource>> + <<Type of Event>> + "Event" The type of event could be: • Create : a new resource has been created (following a POST). • Delete: an existing resource has been deleted. • AttributeValueChange: an attribute from the resource has changed - event structure allows to pinpoint the attribute. • InformationRequired: an attribute should be valued for the resource preventing to follow nominal lifecycle - event structure allows to pinpoint the attribute. • StateChange: resource state has changed.

# 4. Machine Readable

Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component.

---
id: TMFC011
type: component
name: Resource Order Management
version: 1.1.2
status: Pre-production
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC011_Resource_Order_Management_v1.1.2.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: d5b94ba095698b5a5260bf7c799d6c128d7cdae1b07a3d1e26f7b4fbe2a6928e
  raw_path: references/components/TMFC011/TMFC011_Resource_Order_Management_v1.1.2.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF646
      name: appointment-management-api
    - id: TMF652
      name: resource-order-management-api
    - id: TMF664
      name: resource-function-activation-management-api
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
    - id: TMF702
      name: resource-activation-management-api
  use_cases:
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS011
      name: Order Fallout Management
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS025
      name: Cloud Native Function Management
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.2.0
---

# 1. Overview

1. TAC-208 IG1171 (update) Component Definition to v4.0.0 and incorporate IG1245 Principles to Define ODA Components

# 2. [TAC-250] IG 1171 Improvements Some observations & recommendations.

- TM Forum JIRA

# 3. [TAC-214] Interface Standardization needs all 3 stages of process to be

developed - TM Forum JIRA

# 4. [TAC-226] Overview - TM Forum JIRA

# 5. ODA-846 Summary of ODA component Template enhancements for 14th

Sep Review

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Resource Order<br>Management | TMFC011 | The Resource Order Management Component<br>manages the end-to-end lifecycle of a resource<br>order request. This includes validating resource<br>availability as well as the resource order request.<br>Other functionality includes resource order<br>assurance, resource order decomposition and<br>resource order tracking, along with orchestrating<br>activation and the test and turn-up<br>processes.Component | Production |

![](media/resource-order-management-architecture.png)
*([PlantUML source](media/resource-order-management-architecture.puml))*

2. eTOM Processes, SID Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

<Note to not be inserted onto ODA Component specifications: If a new ABE is required, but it does not yet exist in SID. Then you should include a textual description of the new ABE, and it should be clearly noted that this ABE does not yet exist. In addition a Jira epic should be raised to request the new ABE is added to SID, and the SID team should be consulted. Finally, a decision is required on the feasibility of the component without this ABE. If the ABE is critical then the component specification should not be published until the ABE issue has been resolved. Alternatively if the ABE is not critical, then the specification could continue to publication. The result of this decision should be clearly recorded.> eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.5.5 | L2 | Resource Order<br>Management | Resource Order Management business process<br>directs and controls ordering, scheduling, and<br>allocation of resources (such as materials,<br>equipment, and personnel) within the business.<br>Resource Order Management includes managing<br>the capture of resource orders, scheduling works to<br>support the resource order, managing the fulfillment<br>of resource orders, picking/packing, shipping,<br>tracking, and closing orders. |
| 1.5.5.6 | L3 | Manage Resource<br>Order Capture | Manage Resource Order Capture is responsible for<br>directing and controlling the capture and collection<br>of resource orders from internal and external<br>customers.<br>The business activity begins with the receipt of an<br>order for resource(s), checks orders for<br>completeness and accuracy, and ensures missing<br>or incorrect information is requested from the<br>customer. |
| 1.5.5.7 | L3 | Manage Resource<br>Work Order | Manage Resource Order Work business activity<br>directs and controls all work that are required to<br>fulfill an approved resource order by ensuring the<br>work related to the order is planned, executed and<br>closed in a timely and efficient manner.<br>Manage Resource Order Work business activity<br>includes activities to "Initiate Resource Work Order",<br>"Create Resource Work Order", "Review Resource<br>Work Order", "Plan Resource Work Order", "Close<br>Resource Work Order", "Analyze Resource Work<br>Order" and "Report Resource Work Order". |
| 1.5.5.8 | L3 | Manage Resource<br>Order Fulfilment | Manage Resource Order Fulfillment business<br>activity directs and controls activities that ensure<br>that resource orders are described, internally<br>satisfied and delivered accordingly.<br>Manage Resource Order Fulfillment business<br>activity will coordinate with various business<br>processes, such as inventory management,<br>purchasing and logistics to ensure that resources<br>are readily available and can be shipped to the<br>customer in a timely manner. |
| 1.5.5.9 | L3 | Manage Resource<br>Order<br>Picking/Packing | Manage Resource Order Picking/Packing business<br>activity directs and controls the preparation of<br>resources for delivery to the customer.<br>Manage Resource Order Picking/Packing business<br>activity will select the resources from inventory,<br>package them accordingly for delivery (based on the<br>shipment method of the resource order), applying<br>the right mark/label/designation. |
| 1.5.5.12 | L3 | Manage Resource<br>Order Tracking | Manage Resource Order Tracking business activity<br>directs and controls the monitoring of resource<br>order status from the time the order is placed to the<br>time is confirmed delivered<br>Manage Resource Order Tracking business activity<br>tracks the status of the resource order, provides<br>updates to all related parties, and ensures that<br>issues are escalated and managed promptly. |
| 1.5.5.13 | L3 | Manage Resource<br>Order Closure | Manage Resource Order Closure business activity<br>directs and controls the closure of an order and<br>finalizing all supporting business activities.<br>Manage Resource Order Closure business activity<br>will support order invoicing, order payment<br>processing, and updating the resource order status<br>based on completion status of the order. |

## 2.2. SID ABEs

<Note not to be inserted into ODA Component specifications: If a new ABE is required, but it does not yet exist in SID. Then you should include a textual description of the new ABE, and it should be clearly noted that this ABE does not yet exist. In addition a Jira epic should be raised to request the new ABE is added to SID, and the SID team should be consulted. Finally, a decision is required on the feasibility of the component without this ABE. If the ABE is critical then the component specification should not be published until the ABE issue has been resolved. Alternatively if the ABE is not critical, then the specification could continue to publication. The result of this decision should be clearly recorded.> SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Resource Order ABE | - |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-resource-order-links.png)
*([PlantUML source](media/etom-sid-resource-order-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function<br>Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 448 | Resource<br>Availability<br>Validation | Resource Availability<br>Validation function validates<br>that the resource or resources<br>specified on the resource<br>order are available at the<br>specified customer/service<br>location and feasible from a<br>network point of view. This<br>includes the following:<br>• Resource address validation<br>• Resource availability<br>validation<br>• Resource feasibility<br>validation<br>• Establishment of service<br>termination points<br>• Determination of delivery<br>interval<br>It includes checking<br>appropriate network facility<br>route(s) according to<br>engineering rules. | ResourceOrder<br>Management | Resource<br>Availability<br>Management |
| 568 | Resource<br>Availability<br>Checking | Resource Availability Checking<br>determines facility and<br>equipment availability needed<br>for service<br>designing/assigning. It checks<br>appropriate network facility<br>route(s) according to<br>engineering rules. | ResourceOrder<br>Management | Resource<br>Availability<br>Management |
| 569 | Network<br>Facility<br>Selection | Network Facility Selection<br>function selects and assigns<br>appropriate network facility<br>route(s) and configures facility<br>equipment per engineering<br>rules as well as obtains new<br>assets from network plan and<br>build (capacity management) if<br>required. | ResourceOrder<br>Management | Resource<br>Availability<br>Management |
| 490 | Resource Order<br>Data Collection | Resource Order Data<br>Collection function gathers<br>any needed resource data to<br>aid in the verification and<br>issuance of a complete and<br>valid resource order. | Resource<br>Order<br>Management | Resource<br>Order<br>Completion |
| 491 | Resource Order<br>Initiation | Resource Order Initiation<br>function issues valid and<br>complete resource orders, and<br>stores the order into an<br>appropriate data store. As part<br>of order publication, additional<br>data might be obtained or<br>derived to support<br>downstream functions that are<br>not provided in the resource<br>order request. | Resource<br>Order<br>Management | Resource<br>Order<br>Completion |
| 495 | Resource Order<br>Completion | Resource Order Completion<br>completes the resource order<br>when all activities have been<br>completed. | Resource<br>Order<br>Management | Resource<br>Order<br>Completion |
| 503 | Resource Order<br>Validation | The Resource Order Validation<br>function validates the resource<br>order request based on<br>contract, catalog, and<br>provisioning rules. | Resource<br>Order<br>Management | Resource<br>Order<br>Completion |
| 452 | Resource<br>Commissioning | Resource Commissioning<br>supports the commissioning<br>process of a resource and<br>ensuring that operational<br>status' are configured. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 492 | Resource Order<br>Management | This function provides<br>workflow and orchestration<br>capability for the Resource<br>order fulfillment. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 493 | Resource Order<br>Dependency<br>Management | Manages dependencies across<br>resource orders by triggering<br>and follow up as needed. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 494 | Resource Order<br>Jeopardy<br>Tracking | Raises jeopardies as<br>appropriate if specified dates<br>and workflow milestones are<br>not met, and escalates<br>jeopardies to appropriate<br>management levels. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 529 | Tactical<br>Resource<br>Planning | Detailed design of resources<br>against the existing networked<br>resource at all technology<br>layers, ensuring that the<br>designed resource is actually<br>deployed and for accurately<br>recording the resultant<br>inventory. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 958 | Resource Task<br>Decomposition | By request for an orchestration<br>of a resource the Task Item<br>needs to be analyzed and<br>decomposed into the part-<br>actions necessary to take to<br>fulfill the requested resource<br>orchestration. The resource<br>task item may consist of<br>several resource tasks and<br>may use a number of<br>Resources. It may also be<br>controlled by several<br>parameters for optional<br>behaviors. This composition of<br>the Resource is given by<br>configuration data available<br>from Catalog applications and<br>the Resource Capability<br>Orchestration application. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 961 | Resource Work<br>Item Sequence<br>Execution | Because of the “Resource Task<br>Item Decomposition” of an<br>orchestration request the<br>result may be several actions<br>that needs to take place in a<br>specific sequence. The<br>“Resource Work Item<br>Sequence Execution” function<br>executes each individual item<br>in sequence to fulfill, or roll<br>back according to a pre-<br>defined configuration, and<br>reports the sequence carry<br>through result. | Resource<br>Order<br>Management | Resource<br>Order<br>Orchestration |
| 496 | Resource Order<br>Tracking | Resource Order Tracking<br>tracks the various resource<br>orders until completed. | Resource<br>Order<br>Management | Resource<br>Order<br>Tracking &<br>Business<br>Value<br>Development |
| 497 | Resource Order<br>Status<br>Reporting | Resource Order Status<br>Reporting provides status<br>reports on the resource order. | Resource<br>Order<br>Management | Resource<br>Order<br>Tracking &<br>Business<br>Value<br>Development |
| 488 | Resource<br>Parameter<br>Allocation | Resource Parameters<br>Allocation allocates the right<br>resource parameters to fulfill<br>resource orders. | Resource<br>Management | Resource<br>Allocation |
| 487 | Resource<br>Parameter<br>Reservation | Resource Parameters<br>Reservation reserves the right<br>resource parameters based on<br>resource specification and<br>resource inventory. | Resource<br>Management | Resource<br>Allocation |
| 16 | Fallout<br>Automated<br>Correction | Fallout Automated Correction<br>function tries to automatically<br>fix fallouts in workflows before<br>they go to a human for<br>handling. This includes a<br>Fallout Rules Engine that<br>provides the capability to<br>handling various errors or error<br>types based on built rules.<br>These rules can facilitate<br>autocorrection, correction<br>assistance, placement of<br>errors in the appropriate<br>queues for manual handling,<br>as well as access to various<br>systems. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 17 | Fallout<br>Correction<br>Information<br>Collection | Fallout Correction Information<br>Collection collects relevant<br>information for errors or<br>situations that cannot be<br>handled via Fallout Auto<br>Correction. The intent is to<br>reduce the time required by<br>the technician in diagnosing<br>and fixing the fallout. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 19 | Fallout Manual<br>Correction<br>Queuing | Fallout Manual Correction<br>Queuing function provides the<br>required functionality to place<br>error fallout into appropriate<br>queues to be handled via<br>various staff or workgroups<br>assigned to handle or fix the<br>various types of fallout that<br>occurs during the fulfillment<br>process. This includes the<br>ability to create and configure<br>queues, route errors to the<br>appropriate queues, as well as<br>the ability for staff to access<br>and address the various fallout<br>instances within the queues. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 21 | Fallout<br>Orchestration | The Fallout Orchestration<br>function provides workflow<br>and orchestration capability<br>across Fallout Management. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 24 | Pre-populated<br>Fallout<br>Information<br>Presentation | Pre-populated Fallout<br>Information Presentation<br>automatically position the<br>analyzer on appropriate<br>screens pre-populated with<br>information about the order(s)<br>that's subject for fallout<br>handling. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 756 | Fallout Rule<br>Based Error<br>Correction | Fallout Rule Based Error<br>Correction function provides<br>the capability to handle<br>various errors or error types<br>based on pre-defined rules.<br>These rules can facilitate<br>autocorrection. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 18 | Fallout<br>Management to<br>Fulfillment<br>Application<br>Accessing | Fallout Management to<br>Fulfillment Application<br>Accessing function provides a<br>variety of tools to facilitate<br>Fallout Management access to<br>other applications and<br>repositories to facilitate proper<br>Fallout Management. This can<br>include various general access<br>techniques such as<br>messaging, publish and<br>subscribe, etc. as well as<br>specific APIs and contracts to<br>perform specific queries or<br>updates to various<br>applications or repositories<br>within the fulfillment domain. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 20 | Fallout<br>Notification | Fallout Notification function<br>provides the means to alert<br>people or workgroups of some<br>fallout situation. This can be<br>done via a number of means,<br>including email, paging,<br>(Fallout management interface<br>bus) etc. This function is done<br>via business rules. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 22 | Fallout<br>Reporting | Fallout Reporting provides<br>various reports regarding<br>Fallout Management, including<br>statistics on fallout per various<br>times periods (per hour, week,<br>month, etc) as well as<br>information about specific<br>fallout. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 23 | Fallout<br>Dashboard<br>System Log-in<br>Accessing | Fallout Dashboard System<br>Log-in Accessing provides auto<br>logon capability into various<br>applications needed to analyze<br>and fix fallout. | Fallout<br>Management | Fallout<br>Repository<br>Management |

3. TM Forum Open APIs & Events The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event. <Note note to be inserted into ODA Component specifications: If a new Open API is required, but it does not yet exist. Then you should include a textual description of the new Open API, and it should be clearly noted that this Open API does not yet exist. In addition, a Jira epic should be raised to request the new Open API is added, and the Open API team should be consulted. Finally, a decision is required on the feasibility of the component without this Open API. If the Open API is critical then the component specification should not be published until the Open API issue has been resolved. Alternatively if the Open API is not critical, then the specification could continue to publication. The result of this decision should be clearly recorded.>

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF652 | TMF652 Resource Order<br>Management | Mandatory | resourceOrder:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE<br>cancelResourceOrder:<br>- GET<br>- GET /id<br>- POST |
| TMF701 | TMF701 Process Flow | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id |
| TMF688 | TMF688 Event | Optional |   |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation potentially used by the product catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- |
| TMF702 | Resource<br>Activation<br>Management<br>API | Mandatory | resource:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE<br>monitor:<br>- GET<br>- GET /id | Resource order<br>must perform<br>resource activation<br>/ condfiguration<br>across specified<br>order resources. |
| TMF634 | Resource<br>Catalog<br>Management<br>API | Mandatory | resourceSpecification:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE | consistency<br>checks. |
| TMF664 | Resource<br>Function<br>Activation<br>Management<br>API | Mandatory | resourceFunction:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE | Resource order<br>must perform<br>resource activation<br>/ condfiguration<br>across specified<br>order resources. |
| TMF639 | Resource<br>Inventory<br>Management<br>API | Mandatory | resource:<br>- GET<br>- GET /id<br>- POST<br>- PATCH<br>- DELETE | consistency check. |
| TMF632 | Party<br>Management<br>API | Optional | individual:<br>- GET<br>- GET /id<br>organization:<br>- GET<br>- GET /id | n/a |
| TMF697 | Work Order<br>Management<br>API | Optional | workOrder:<br>- GET<br>- GET /id | n/a |
| TMF673 | Geographic<br>Address<br>Management<br>API | Optional | geographicAddress:<br>- GET<br>- GET /id | n/a |
| TMF674 | Geographic<br>Site<br>Management<br>API | Optional | geographicSite:<br>- GET<br>- GET /id | n/a |
| TMF675 | Geographic<br>Location<br>Management<br>API | Optional | geographicLocation:<br>- GET<br>- GET /id | n/a |
| TMF688 | TMF688 Event | Optional |   | n/a |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

4. Machine Readable Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component.

5. References

## 5.1. TMF Standards related versions

| Standard | Version(s) |
| --- | --- |
| SID | 24.0 |
| eTOM | 24.0 |
| Functional Framework | 24.0 |

## 5.2. Further resources

1. IG1228: please refer to IG1228 for defined use cases with ODA components interactions.

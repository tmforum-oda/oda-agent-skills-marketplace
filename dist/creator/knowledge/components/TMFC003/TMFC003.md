---
id: TMFC003
type: component
name: Product Order Delivery Orchestration And Management
version: 2.0.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC003_Product_Order_Delivery_Orchestration_and_Management_v2.0.0.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: f69f583be6de3e93787d8aa5f4301317641b2acd24dae040da3b79ecb7b32dca
  raw_path: references/components/TMFC003/TMFC003_Product_Order_Delivery_Orchestration_and_Management_v2.0.0.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF622
      name: product-ordering-management-api
    - id: TMF633
      name: service-catalog-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF638
      name: service-inventory-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF641
      name: service-ordering-management-api
    - id: TMF652
      name: resource-order-management-api
    - id: TMF669
      name: party-role-management-api
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
    - id: TMFS012
      name: Product Catalog - Launching a New Product Offering
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS021
      name: Orchestration of a Multi Party, Multi domain Sales Order
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.1.1
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Product Order<br>Delivery<br>Orchestration<br>and<br>Management | TMFC003 | This component is in charge of the<br>orchestration of the delivery of Product Orders<br>(status accepted).<br>Based on the Product specification level of<br>information available in the Product Catalog<br>(ex: prerequisite links between product<br>specifications, links between product and CFS<br>specifications, ...):<br>• it determines in which order the<br>product specification level order items<br>need to be delivered,<br>• and to which CFS (or Resource)<br>specification each ordered product<br>corresponds,<br>• and prepares and addresses each<br>related service (or resource) order to<br>the production system in charge.<br>During the delivery process execution, this<br>component is in charge of the evolution of the<br>status of the product specification level order<br>items, and of the related product items . So, it<br>triggers the updates of the related inventories. | Core<br>Commerce<br>Management |

![](media/product-order-delivery-architecture.png)
*([PlantUML source](media/product-order-delivery-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.3 | L2 | Customer<br>Order Handling<br>Customer<br>Order<br>Processing<br>Management | Customer Order Handling processes are responsible<br>for accepting and issuing orders. They deal with pre-<br>order feasibility determination, credit authorization,<br>order issuance, order status and tracking, customer<br>update on order activities and customer notification<br>on order completion.<br>Responsibilities of the Order Handling processes<br>include:<br>• Testing the completed offering to ensure it is<br>working correctly;<br>• Updating of the Customer Inventory Database<br>to reflect that the specific product offering has<br>been allocated, modified or cancelled;<br>• Assigning and tracking customer provisioning<br>activities;<br>• Managing customer provisioning jeopardy<br>conditions<br>• Reporting progress on customer orders to<br>customer and other processes.<br>Customer Order Processing Management<br>business process directs and controls all<br>activities that operationally realize orders for<br>customer.<br>Customer Order Processing Management assures<br>the capture, processing, fulfillment, "shipping",<br>delivery and reporting of customer orders from<br>feasibility assessment, purchasing, payment,<br>fulfillment and follow up with the customer for<br>closure. |
| 1.3.3.12 | L3 | Manage<br>Customer<br>Order<br>Fulfillment | Manage Customer Order Fulfillment business<br>activity directs and controls all activities that<br>provision and activate orders marked for<br>fulfillment.<br>Manage Customer Order Fulfillment ensure<br>customer orders are organized and arranged<br>(orchestrated), and tracked to meet committed<br>ordering terms. |
| 1.3.3.8<br>1.3.3.12.1 | L3 L4 | Manage<br>Customer Order<br>Fallout | This process defines tasks involved in handling<br>fallouts (exceptions) generated in the order fulfillment<br>lifecycle. It deals with identifying, assigning,<br>managing, monitoring and reporting order fallouts<br>Manage Customer Order Fallout business activity<br>controls orders that have failed during the<br>fulfillment stage of a customer order process. |
| 1.3.3.9 | L3 | Customer Order<br>Orchestration | Customer Order Orchestration ensures customer<br>order provisioning activities are orchestrated,<br>managed and tracked efficiently to meet the agreed<br>committed availability date. |
| 1.3.3.13 | L3 | Manage<br>Customer<br>Order Delivery | Manage Customer Order Delivery business<br>activity directs and controls activities that deliver<br>orders according to the requirement of the<br>customer. |
| 1.2.9 | L2 | Product Offering<br>Purchasing | Make an inbound/outbound purchase of one or more<br>product offerings, change an offering being<br>purchased, review an entire purchase, and other<br>processes that manage the lifecycle of a purchase of<br>one or more product offerings. |
| 1.2.9.5 | L3 | Complete<br>Product Offering<br>Purchase | Complete a product offering purchase which may<br>trigger other processes, such as ones that accept<br>payment and deliver the purchased offerings.<br>L4 - 1.2.9.5.3 - Coordinate Product Offering<br>Purchase Provisioning<br>Coordinate any necessary provisioning activities<br>for inbound product offering purchases by<br>generating the service order and resource order<br>creation request(s) to Issue Service Orders and<br>Issue Resource Orders<br>L4 - 1.2.9.5.4 - Initiate Additional Product Offering<br>Purchase(s)<br>Prepare product offering purchases in the form of<br>product offering orders for each product offering<br>fulfilled by another party. |
| 1.2.27 | L2 | Product Order<br>Management | Product Order Management business direct and<br>control processes that capture, track, fulfil,<br>deliver and close product order requests. |
| 1.2.27.2 | L3 | Manage<br>Product Order<br>Fulfillment | Manage Product Order Fulfillment business<br>activity is responsible for directing and<br>controlling for product orders, the configuration<br>of product order fulfillment steps, managing the<br>product order fulfillment profile, managing the<br>product order picking and packing, managing<br>product order shipment, managing product order<br>returns, tracking product order fulfillment, and<br>closing fulfillment of product orders. |
| 1.2.27.3 | L3 | Manage<br>Product Order<br>Delivery | Manage Product Order Delivery business activity<br>directs and controls the activities to validate<br>products in the product order.<br>Manage Product Order Delivery business activity<br>ensures product can be successfully be supplied<br>to consignee of the product order to enable<br>complete the product order process. |
| 1.4.5 | L2 | Service<br>Configuration &<br>Activation | Allocation, implementation, configuration, activation<br>and testing of specific services to meet customer<br>requirements. |
| 1.4.5.6 | L3 | Issue Service<br>Order | Issue correct and complete service orders. |
| 1.4.5.6.1 | L4 | Assess Service<br>Request | This process assesses the information contained in<br>the customer order, through a service order request,<br>relating to the purchased product offering, initiating<br>service process or party initiated request, to<br>determine the associated service orders that need to<br>be issued. |
| 1.5.6 | L2 | Resource<br>Provisioning | Allocation, installation, configuration, activation and<br>testing of specific resources to meet the service<br>requirements, or in response to requests from other<br>processes to alleviate specific resource capacity<br>shortfalls, availability concerns or failure conditions. |
| 1.5.6.7 | L3 | Issue Resource<br>Order | Issue correct and complete resource orders.<br>L4 - 1.5.6.7.1 - Assess Resource Request<br>This process assesses the information contained<br>in the service order, through a resource order<br>request, initiating resource process request or<br>supplier/partner initiated request, to determine the<br>associated resource orders that need to be issued. |
| 1.5.5 | L2 | Resource Order<br>Management | Resource Order Management business process<br>directs and controls ordering, scheduling, and<br>allocation of resources (such as materials,<br>equipment, and personnel) within the business. |
| 1.5.5.6 | L3 | Manage<br>Resource Order<br>Capture | Manage Resource Order Capture is responsible<br>for directing and controlling the capture and<br>collection of resource orders from internal and<br>external customers. |
| 1.5.5.6.1 | L4 | Initiate<br>Resource Order<br>Capture | Initiate Resource Order Capture business activity<br>is responsible for the initial activity of capturing<br>and collecting resource orders from internal and<br>external customers.<br>This business activity begins with the<br>identification of the needed resources, either by a<br>"customer" and facilitating creating the request<br>for the resources. This business activity will<br>gather the necessary information to complete the<br>request order, such as the type and quantity of<br>resources needed, delivery location, and any<br>special instructions. |
| 1.6.8 | L2 | Business<br>Partner Order<br>Management | Track, monitor and report on an order to another<br>Business Partner to ensure that the interactions<br>are in accordance with the agreed commercial<br>agreements with the other Business Partner. |
| 1.6.8.5 | L3 | Issue Business<br>Partner Order | Generate a correctly formatted and specified<br>Business Partner order and issue this to the<br>selected Business Partner. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| none |   |

Note: SID doesn't currently describe Orchestration Plan and delivery process to manage at Product Order level. This could be added at least as specialization from Project ABE or Workflow ABE. Refer to JIRA paragraph at the end of the document.

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-product-order-links.png)
*([PlantUML source](media/etom-sid-product-order-links.puml))*

## 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 16 | Fallout Automated<br>Correction | Fallout Automated Correction function tries to<br>automatically fix fallouts in workflows before they<br>go to a human for handling.<br>This includes a Fallout Rules Engine that<br>provides the capability to handling various errors<br>or error types based on built rules. These rules<br>can facilitate autocorrection, correction<br>assistance, placement of errors in the<br>appropriate queues for manual handling, as well<br>as access to various systems. | Fallout Management | Fallout Correction<br>Management |
| 17 | Fallout Correction<br>Information Collection | Fallout Correction Information Collection collects<br>relevant information for errors or situations that<br>cannot be handled via Fallout Auto Correction.<br>The intent is to reduce the time required by the<br>technician in diagnosing and fixing the fallout. | Fallout Management | Fallout Correction<br>Management |
| 18 | Fallout Management to<br>Fulfillment Application<br>Accessing | Fallout Management to Fulfillment Application<br>Accessing function provides a variety of tools to<br>facilitate Fallout Management access to other<br>applications and repositories to facilitate proper<br>Fallout Management. This can include various<br>general access techniques such as messaging,<br>publish and subscribe, etc. as well as specific<br>APIs and contracts to perform specific queries or<br>updates to various applications or repositories<br>within the fulfillment domain. | Fallout Management | Fallout Repository<br>Management |
| 19 | Fallout Manual<br>Correction Queuing | Fallout Manual Correction Queuing function<br>provides the required functionality to place error<br>fallout into appropriate queues to be handled via<br>various staff or workgroups assigned to handle or<br>fix the various types of fallout that occurs during<br>the fulfillment process. This includes the ability to<br>create and configure queues, route errors to the<br>appropriate queues, as well as the ability for staff<br>to access and address the various fallout<br>instances within the queues. | Fallout Management | Fallout Correction<br>Management |
| 20 | Fallout Notification | Fallout Notification function provides the means<br>to alert people or workgroups of some fallout<br>situation. This can be done via a number of<br>means, including email, paging, (Fallout<br>management interface bus) etc. This function is<br>done via business rules. | Fallout Management | Fallout Repository<br>Management |
| 21 | Fallout Orchestration | The Fallout Orchestration function provides<br>workflow and orchestration capability across<br>Fallout Management. | Fallout Management | Fallout Correction<br>Management |
| 22 | Fallout Reporting | Fallout Reporting provides various reports<br>regarding Fallout Management, including<br>statistics on fallout per various times periods (per<br>hour, week, month, etc) as well as information<br>about specific fallout. | Fallout Management | Fallout Repository<br>Management |
| 23 | Fallout Dashboard<br>System Log-in<br>Accessing | Fallout Dashboard System Log-in Accessing<br>provides auto logon capability into various<br>applications needed to analyze and fix fallout | Fallout Management | Fallout Repository<br>Management |
| 24 | Pre-populated Fallout<br>Information<br>Presentation | Pre-populated Fallout Information Presentation<br>automatically position the analyzer on<br>appropriate screens pre-populated with<br>information about the order(s) that's subject for<br>fallout handling. | Fallout Management | Fallout Correction<br>Management |
| 174 | Customer Order Error<br>Resolution Support | Customer Order Error Resolution Support<br>provides to view pool of orders resulted in error<br>or stuck orders and enable the Customer Support<br>to act accordingly (e.g., resend the request, notify<br>the user with recommended action) | Customer Order<br>Management | Customer Order<br>Repository Management |
| 175 | Customer Support<br>Jeopardy Notification | Customer Support Jeopardy Notification provide<br>to view jeopardy notifications queue and enable<br>the Customer Support to act accordingly (e.g.,<br>notify customer on due date delay) | Customer Order<br>Management | Customer Order<br>Repository Management |
| 723 | Customer Order Item<br>Decomposition | Customer Order Item Decomposition prepares<br>the customer order structure for breakdown into<br>customer order items. |   |   |
| 214 | Customer Order<br>Orchestration | The Customer Order Orchestration function<br>provides workflow and orchestration capabilities<br>at the Product Order Item level for a dedicated<br>Customer Order.<br>Customer Order Orchestration function identifies<br>Service Order Items (CFS level) according to<br>Order Items of the Customer Order, sequences<br>Service Order Items and distributes the Service<br>Order requests to appropriate systems. For<br>example : Service Order Management (SOM),<br>potential 3rd parties, ...<br>This identification of Service Order Items relies<br>on :<br>- the articulation between ProductSpecifications<br>and CFSSpec described in the Catalogue<br>Repository<br>- the articulation between Product Operations<br>and CFS Operations described in the Catalogue<br>Repository<br>- existing installed CFS<br>- the potential rules of choice if several CFS can<br>fit in with the product.<br>Orchestration can take into account :<br>- constraints between Customer Product Order<br>Items inside the Customer Product Order, or<br>successive Customer Orders including<br>modification or cancellation (in-flight changes)<br>- any type of business rules based on information<br>even external to the Customer Product Order.<br>For example : high level of priority for VIP<br>customers<br>- Triggering of exception process or delivery<br>planning update, depending on Customer<br>Product Order or Service Order events. | Customer Order<br>Management | Customer Order<br>Orchestration |
| 215 | Retro-active order<br>orchestration | Retro-active Order Orchestration provides<br>submission of a retroactive order with a past<br>effective date (e.g., retroactive price plan<br>change) and the handling of manual intervention<br>requests (for order fallouts). | Customer Order<br>Management | Customer Order<br>Orchestration |
| 217 | Customer Order<br>Establishment<br>Tracking | Customer Order Establishment Tracking<br>provides the functionality necessary to track<br>and manage the distributed requests<br>decomposed by Customer Order<br>Orchestration. | Customer Order<br>Management | Customer Order<br>Repository Management |
| 342 | Mass Service/product<br>pre-activation | Mass service/product pre-activation function. To<br>prepare for a swift activation at sales affiliate<br>services/products may be pre-activated. | Service Configuration &<br>Activation | Service Activation |
| 743 | Number Portability<br>Orchestration | Number Portability Orchestration communication<br>mechanism that ensures the orders' activation<br>according to criteria set, allowing in this way the<br>correct execution of orders | Resource Management | Regulated Logical<br>Resources Management |
| 724 | Customer Order Work<br>Item Decomposition | Customer Order Work Item Decomposition<br>decomposes customer order items into a set<br>of customer order work items. | Customer Order<br>Management | Customer Order<br>Orchestration |
| 756 | Fallout Rule Based<br>Error Correction | Fallout Rule Based Error Correction function<br>provides the capability to handle various errors or<br>error types based on pre-defined rules. These<br>rules can facilitate autocorrection, correction<br>assistance, placement of errors in the<br>appropriate queues for manual handling, as well<br>as access to various systems via the Fallout<br>Interface Bus. | Fallout Management | Fallout Correction<br>Management |
| 1070 | Orchestration<br>Customer Order Error<br>Resolution | Orchestration Customer Order Error<br>Resolution provides to view pool of orders<br>resulted in error or stuck orders during<br>orchestration and enable the Customer<br>Support to act accordingly.<br>For example, a delay change because of<br>resource unavailability or appointment not<br>respected may trigger the resend of the<br>request or notify the user with recommended<br>action. | Customer Order<br>Management | Customer Order<br>Orchestration |
| 1202 | Delivery Items<br>Identification | The Delivery Items Identification function<br>allows in the context of a customer order to<br>consult catalogs and installed bases to<br>identify what needs to be delivered: Service<br>Specification (CFS Spec) and its<br>configuration, Stock Item, Supplier Product,<br>Work Spec, related to the ordered product. | Customer Order<br>Management | Customer Order Delivery<br>Preparation |
| 1203 | Order Preparation | The Order Preparation Function allows in the<br>context of a customer order to prepare a<br>Service Order, Supplier Order, Stock Item<br>Order or Work Order with the necessary<br>information.<br>In the case of a Product associated with an<br>Internal Service (Know-How), this function<br>also allows to:<br>• check if a corresponding Installed CFS is<br>operational in the Service Installed Base, and<br>so determine the operation at CFS level<br>(creation or modification)<br>• possibly group in the same Service Order<br>several ordered product, based on the same<br>CFS specification, and/or identified to be<br>delivered at the same time by the Customer<br>Order Delivery Orchestration. | Customer Order<br>Management | Customer Order Delivery<br>Preparation |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Resource | Operations |
| --- | --- | --- | --- | --- |
| TMF701 | Process Flow | Optional | processFlow | GET<br>GET /id<br>POST<br>DELETE /id |
|   |   |   | taskFlow | GET<br>GET /id<br>PATCH /id |
| TMF688 | Event | Optional |   |   |

## 3.2. Dependent APIs

The following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Resource | Operations | Rationales |
| --- | --- | --- | --- | --- | --- |
| TMF620 | Product<br>Catalog<br>Management<br>API | Mandatory | productSpecification | GET<br>GET /id | as illustrated<br>in IG1228,<br>TMFS004,<br>TMFS008<br>and<br>TMFS014 |
| TMF622 | Product<br>Ordering<br>Management<br>API | Mandatory | productOrder | GET /id<br>PATCH /id | as illustrated<br>in IG1228,<br>TMFS004,<br>TMFS008<br>and<br>TMFS014 |
| TMF637 | Product<br>Inventory<br>Management<br>API | Mandatory | product | GET<br>GET /id<br>PATCH /id | as illustrated<br>in IG1228,<br>TMFS004,<br>TMFS008<br>and<br>TMFS014 |
| TMF633 | Service<br>Catalog<br>Management<br>API | Optional | serviceSpecification | GET<br>GET /id |   |
| TMF638 | Service<br>Inventory<br>Management<br>API | Optional | service | GET<br>GET /id |   |
| TMF641 | Service<br>Ordering<br>Management<br>API | Mandatory | serviceOrder | POST<br>GET /id | as illustrated<br>in IG1228,<br>TMFS004,<br>TMFS008<br>and<br>TMFS014 |
| TMF634 | Resource<br>Catalog<br>Management<br>API | Optional | resourceSpecification | GET<br>GET /id |   |
| TMF639 | Resource<br>Inventory<br>Management<br>API | Optional | resource | GET<br>GET /id |   |
| TMF652 | Resource<br>Ordering<br>Management<br>API | Optional | resourceOrder | POST<br>GET /id |   |
| TMF701 | Process<br>Flow | Optional | processFlow | GET<br>GET /id<br>POST<br>DELETE<br>/id |   |
|   |   |   | taskFlow | GET<br>GET /id<br>PATCH /id |   |
| TMF688 | TMF688<br>Event | Optional |   |   |   |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component Map on the TM Forum website for the machine-readable component specification files for this component.

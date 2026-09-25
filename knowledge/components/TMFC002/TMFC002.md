---
id: TMFC002
type: component
name: Product Order Capture And Validation
version: 2.1.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC002_Product_Order_Capture_Validation_v2.1.1.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 6854cf686a5635492e7415534c66b2991dd3611968229da22b46947e43b28baf
  raw_path: references/components/TMFC002/TMFC002_Product_Order_Capture_Validation_v2.1.1.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF638
      name: service-inventory-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF646
      name: appointment-management-api
    - id: TMF648
      name: quote-management-api
    - id: TMF651
      name: agreement-management-api
    - id: TMF663
      name: shopping-cart-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF676
      name: payment-management-api
    - id: TMF679
      name: product-offering-qualification-management-api
    - id: TMF683
      name: party-interaction-management-api
    - id: TMF687
      name: stock-management-api
    - id: TMF701
      name: process-flow-management-api
    - id: TMF716
      name: resource-reservation
    - id: TMF760
      name: product-configuration-management-api
  use_cases:
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS009
      name: Usage and Balance Management
    - id: TMFS012
      name: Product Catalog - Launching a New Product Offering
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS021
      name: Orchestration of a Multi Party, Multi domain Sales Order
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 2.1.0
---

# 1. Overview

| Component Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Product Order<br>Capture and<br>Validation | TMFC002 | This component captures what a customer<br>wants to order based on the CSP's Product<br>Catalog. It enables configuration of the<br>product offerings and products desired,<br>provides quotes, checks the eligibility of the<br>customer order, and completes it with<br>information needed such as the related<br>parties or associated billing account and the<br>delivery appointment. This component owns<br>quote management, order capture and<br>validation, using dedicated components (eg<br>Offering Configurator, Service Qualification,<br>Party Management) when needed. After the<br>delivery of the customer product order items,<br>this component is also in charge of the<br>commercial closure of the order. It includes<br>update of the Product Inventory (status and<br>starting/end date of tariffs and discounts) and<br>potential commercial rules control (eg receipt<br>of the contract document signed by the<br>customer). | Core Commerce |

![](media/product-order-capture-validation-architecture.png)
*([PlantUML source](media/product-order-capture-validation-architecture.puml))*

# 2. eTOM Processes, SID

Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for are:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.1.9 | L2 | Selling | Responsible for managing prospective customers,<br>for qualifying and educating customers, and<br>matching customer expectations.<br>Managing prospective parties with whom an<br>enterprise may do business, such as potential<br>existing or new customers and partners, for<br>qualifying and educating them, and ensuring their<br>expectations are met. |
| 1.1.9.2 | L3 | Develop Sales<br>Proposal | Develop a sales proposal to respond to the<br>customer’s requirements<br>Develop a sales proposal to respond to a sales<br>prospect's requirements. |
| 1.1.9.5 | L3 | Negotiate<br>Sales/Contract | Close the sale with terms that are understood by<br>the customer and are mutually agreeable to both<br>the customer and the service provider.<br>Close the sale with terms that are understood by<br>the sales prospect, which now becomes a<br>customer or some other partythat make an<br>enterprise's offerings to the market, such as a<br>partner, and are mutually agreeable to both the<br>customer or party and an enterprise. |
| 1.2.9 | L2 | Product Offering<br>Purchasing | Make an inbound/outbound purchase of one or<br>more product offerings, change an offering being<br>purchased, review an entire purchase, and other<br>processes that manage the lifecycle of a purchase<br>of one or more product offerings. |
| 1.2.27 | L2 | Product Order<br>Management | Product Order Management business direct and<br>control processes that capture, track, fulfil,<br>deliver and close product order requests.<br>Product Order Management begins with the<br>capture of a product order request based on a<br>party (Customer, Business Partner, Employee<br>etc.), and processes, tracks and reports the<br>products from order capture to fulfillment,<br>shipping the order, and managing cancellation<br>and returns. |
| 1.2.27.1 | L3 | Manage Product<br>Order Capture | Manage Product Order Capture business<br>activity direct and control the creation of<br>product orders, validate product orders against<br>feasibility and/or availability checks, and<br>ensure product orders are complete for onward<br>business processing.<br>Manage Product Order Capture assures for<br>completeness, the Product Order requirements<br>needed for successfully processing, delivering<br>and managing returns of orders. |
| 1.2.27.4 | L3 | Manage Product<br>Order<br>Cancellation | Manage Product Order Cancellation business<br>activity directs and controls the product order<br>cancellation requests. |
| 1.2.27.5 | L3 | Manage Product<br>Order<br>Management<br>Reports | Manage Product Order Management Reports<br>business activity directs and controls<br>monitoring of product order management<br>activities, notify product order management<br>status and reporting product order management<br>activities. |
| 1.3.3 | L2 | Customer Order<br>Handling<br>Customer Order<br>Processing<br>Management | Responsible for accepting and issuing orders.<br>Customer Order Processing Management<br>business process directs and controls all<br>activities that operationally realize orders for<br>customer.<br>Customer Order Processing Management<br>assures the capture, processing, fulfillment,<br>"shipping", delivery and reporting of customer<br>orders from feasibility assessment, purchasing,<br>payment, fulfillment and follow up with the<br>customer for closure. |
| 1.3.3.1 | L3 | Determine<br>Customer Order<br>Feasibility | Check the availability and/or the feasibility of<br>providing and supporting standard and customized<br>product offerings where specified to a customer. |
| 1.3.3.2 | L3 | Authorize Credit | Assess a customer's credit worthiness in support<br>of managing customer risk and company exposure<br>to bad debt |
| 1.3.3.4 | L3 | Complete<br>Customer Order | Manage customer information and interactions<br>after customer contracts or associated service<br>orders have been finalized and during the order<br>completion phase |
| 1.3.3.5 | L3 | Issue Customer<br>Orders | Issue Correct and complete customer orders |
| 1.3.3.6 | L3 | Report Customer<br>Order Handling | Monitor the status of customer orders, provide<br>notifications of any changes, and provide<br>management reports |
| 1.3.3.7 | L3 | Close Customer<br>Order | Close a customer order when the customer<br>provisioning activities have been completed.<br>Monitor the status of all open customer orders and<br>recognize that a customer order is ready to be<br>closed when the status is changed to completed. |
| 1.3.3.8 | L3 | Manage Order<br>Fallout | This process defines tasks involved in handling<br>fallouts (exceptions) generated in the order<br>fulfillment lifecycle. It deals with identifying,<br>assigning, managing, monitoring, and reporting<br>order fallouts. |
| 1.3.3.10 | L3 | Manage<br>Customer Order<br>Placement | Manage Customer Order Placement business<br>activity directs and controls the capture of<br>information to enable create customer order,<br>change customer order and validate customer<br>order based on ordering information from<br>customer. |
| 1.3.3.15 | L3 | Manage<br>Customer Order<br>Completion | Manage Customer Order Completion business<br>activity controls activities to confirm that an<br>order has been successfully delivered/shipped<br>to the customer. |
| 1.3.3.16 | L3 | Manage<br>Customer Order<br>Management<br>Report | Manage Customer Order Management Report<br>business activity provides detailed account of<br>Customer Order Management activities,<br>representing state and status of customer<br>orders across the customer order lifecycle.<br>Manage Customer Order Management Report<br>provides monitoring, tracking and customer<br>order status updates/notification as needed to<br>all stakeholders linked to the customer ordering<br>and fulfillment activities. |
| 1.3.3.17 | L3 | Manage<br>Customer Order<br>Closure | Manage Customer Order Closure business<br>activity ensures that customer has confirmed<br>the delivery of a completed customer order.<br>Manage Customer Order Closure business<br>activity closes-the-loop of between the<br>Customer Order Completion process and the<br>confirmation by the Customer. This business<br>activity includes tasks to communicate and<br>confirm delivery to customer; cancellation of<br>any open line items in the customer order; and<br>reports the customer order completion to<br>related stakeholders. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for are:

| SID ABE Level 1 | SID ABE L1 Definition | SID ABE Level 2 (or set of BEs) | SID ABE L2 Definition |
| --- | --- | --- | --- |
| Customer<br>Product<br>Order | Handles single customer orders<br>and the various types thereof, such<br>as regulated and non-regulated<br>orders. | SalesQuote |   |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified. Note: The Product Order Capture & Validation component will also trigger creation and update of Product but this information is managed by a dedicated component TMFC005 - Product Inventory.

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-order-links.png)
*([PlantUML source](media/etom-sid-order-links.puml))*

## 2.4. Functional Framework Functions

1 TMFC027 Product Configurator covers the part related to Product Catalog rules checking. Only stock control part is done by TMFC002 Product Order Capture & Validation. 2 TMFC027 Product Configurator covers the part related to Product Catalog rules checking at commercial and functional eligibility levels. Only technical eligibility controls are triggered by TMFC002 Product Order Capture & Validation.

| Function<br>ID | Functional Framework Function | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 16 | Fallout Automated<br>Correction | Fallout Automated Correction function<br>tries to automatically fix fallouts in<br>workflows before they go to a human for<br>handling.<br>This includes a Fallout Rules Engine that<br>provides the capability to handling<br>various errors or error types based on<br>built rules. These rules can facilitate<br>autocorrection, correction assistance,<br>placement of errors in the appropriate<br>queues for manual handling, as well as<br>access to various systems. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 17 | Fallout Correction<br>Information<br>Collection | Fallout Correction Information<br>Collection collects relevant information<br>for errors or situations that cannot be<br>handled via Fallout Auto Correction. The<br>intent is to reduce the time required by<br>the technician in diagnosing and fixing<br>the fallout. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 18 | Fallout<br>Management to<br>Fulfillment | Fallout Management to Fulfillment<br>Application Accessing function provides<br>a variety of tools to facilitate Fallout<br>Management access to other | Fallout<br>Management | Fallout<br>Repository<br>Management |
|   | Application<br>Accessing | applications and repositories to<br>facilitate proper Fallout<br>Management. This can include various<br>general access techniques such as<br>messaging, publish and subscribe, etc.<br>as well as specific APIs and contracts to<br>perform specific queries or updates to<br>various applications or repositories<br>within the fulfillment domain. |   |   |
| 19 | Fallout Manual<br>Correction Queuing | Fallout Manual Correction Queuing<br>function provides the required<br>functionality to place error fallout into<br>appropriate queues to be handled via<br>various staff or workgroups assigned to<br>handle or fix the various types of fallout<br>that occurs during the fulfillment<br>process. This includes the ability to<br>create and configure queues, route<br>errors to the appropriate queues, as<br>well as the ability for staff to access and<br>address the various fallout instances<br>within the queues. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 20 | Fallout Notification | Fallout Notification function provides<br>the means to alert people or<br>workgroups of some fallout situation.<br>This can be done via a number of<br>means, including email, paging, (Fallout<br>management interface bus) etc. This<br>function is done via business rules. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 21 | Fallout<br>Orchestration | The Fallout Orchestration function<br>provides workflow and orchestration<br>capability across Fallout Management. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 22 | Fallout Reporting | Fallout Reporting provides various<br>reports regarding Fallout Management,<br>including statistics on fallout per<br>various times periods (per hour, week,<br>month, etc.) as well as information<br>about specific fallout. | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 23 | Fallout Dashboard<br>System Log-in<br>Accessing | Fallout Dashboard System Log-in<br>Accessing provides auto logon<br>capability into various applications<br>needed to analyze and fix fallout | Fallout<br>Management | Fallout<br>Repository<br>Management |
| 24 | Pre-populated<br>Fallout Information<br>Presentation | Pre-populated Fallout Information<br>Presentation automatically position the<br>analyzer on appropriate screens pre-<br>populated with information about the<br>order(s) that's subject for fallout<br>handling. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 120 | Customer Order<br>Capturing | Customer Order Capturing provides<br>access to Order capture and negotiation<br>capabilities or receives the captured<br>Customer Order data from channels.<br>Takes care of persistence using<br>Customer Order Lifecycle Management.<br>Including support of contract printing,<br>integration with a locally installed cash<br>management/cash register and a retail<br>inventory system for order completion<br>and ordered product versioning. | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 172 | Customer Order<br>Reporting | Customer Order Reporting function<br>provides front end support for Business,<br>Financial and Operational reporting and<br>analyzing of the ordering activities. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 174 | Ordering Customer<br>Order Error<br>Resolution Support | Ordering Customer Order Error<br>Resolution Support provides to view<br>pool of orders resulted in error or stuck<br>orders and enable the Customer<br>Support to act accordingly(e.g., resend<br>the request, notify the user with<br>recommended action)<br>For example, a configuration<br>incompatibility with functional or<br>commercial constraint, product<br>unavailability according to the<br>configuration may trigger the resend<br>of the request or notify the user with<br>recommended action. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 175 | Customer Support<br>Jeopardy<br>Notification | Customer Support Jeopardy<br>Notification provide to view jeopardy<br>notifications queue and enable the<br>Customer Support to act accordingly<br>(e.g. notify customer on due date<br>delay). | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 176 | Customer Order<br>Capturing Access | Customer Order Capturing Access<br>provides front end support for the<br>Customer Order Capturing functions<br>defined by the order management. | Fulfillment<br>Integration<br>Management | Customer<br>Fulfillment<br>Access<br>Management |
| 177 | Customer Order<br>Take-over<br>Management | Customer Order Take-over Management<br>provides an ability to take over<br>governance of orders handled by other<br>channels (e.g., self-service) amend and<br>relinquish while preserving all the<br>captured data. | Customer<br>Order<br>Management | Customer<br>Order<br>Completion |
| 178 | Customer Order<br>Administration | Customer Order Administration provide<br>to view all outstanding orders, progress<br>and history displays | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 181 | Product Order Data<br>Collection | Product Order Data Collection provides<br>an aid in verification and issuance of a<br>complete and valid customer order.<br>This function checks delivery<br>address, link with a payment, a billing<br>account, a certified holder, etc. | Customer<br>Order<br>Management | Customer<br>Order<br>Completion |
| 204 | Customer<br>OrderCompletion E<br>ntry Finalization | The Customer OrderCompletion Entry<br>Finalization function<br>enablescompletion and finalization of<br>the Customer Order with collection of<br>Customer Data or installed base data<br>according to the Catalog. It allows to<br>complete the configuration element not<br>necessary for the quotation. The<br>complements could also concern links<br>with actors, dates, address, billing<br>account. | Customer<br>Order<br>Management | Customer<br>Order<br>Completion |
| 205 | Customer Order<br>Eligibility Validation | Customer Order Eligibility Validation<br>function validates that the Offer &<br>products specified on the Customer<br>Order, are eligible from a commercial<br>and functional point of view.<br>It includes:<br>• Commercial Eligibility with<br>commercial compatibility with the<br>already customer installed Offers<br>• Functional Eligibility with the<br>customer's already installed Products.<br>• Customer Credit Eligibility check,<br>considering the payment history and the<br>credit scores for a Customer, only the<br>predictive credit score for a Prospective<br>Customer.<br>The technical feasibility is covered by<br>the Service Availability function.<br>• Commercial Eligibility with<br>commercial compatibility with<br>the already customer installed<br>Products (corresponding to<br>ProductOffering)<br>• Functional Eligibility with the<br>customer's already installed<br>Products (corresponding to<br>ProductSpecification). | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 208 | Customer Order<br>Change<br>Management | Customer Order Change Management<br>amend pending order resulted from<br>customer change requests or<br>provisioning system limitation and<br>revalidate the order. | Customer<br>Order<br>Management | Customer<br>Order Change<br>Management |
| 209 | Customer Order<br>Cancellation | Customer Order Cancellation can<br>optionally support Cancel for order<br>completed by Service Order<br>Management (this capability is<br>dependent on the Service Order<br>Management system’s ability to roll<br>back service provisioning). This<br>function assesses the feasibility of<br>order cancellation and the potential<br>charge to the customer. If the<br>cancellation is confirmed, it proceeds<br>with the cancellation. | Customer<br>Order<br>Management | Customer<br>Order<br>Validation |
| 211 | Customer Order<br>Activity Supervision | Customer Order Activity Supervision<br>governs the control of the order<br>amongst the ordering channels. This<br>allows keeping the order data<br>consistency, sharing the order data<br>among order application channels, and<br>alternating the control between them. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 212 | Customer Order<br>Versioning | Customer Order Versioning maintains<br>order versioning including Tracking &<br>Logging of the changes made to a<br>purchased product. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 213 | Pending Customer<br>Orders<br>Maintenance | Pending Customer Orders Maintenance<br>saves the order/quote for future<br>processing (in case the customer is not | Customer<br>Order<br>Management | Customer<br>Order |
|   |   | sure if they want to go through with the<br>order at this point) |   | Repository<br>Management |
| 217 | Customer Order<br>Establishment<br>Tracking | Customer Order Establishment Tracking<br>provides the functionality necessary to<br>track and manage the distributed<br>requests decomposed by Customer<br>Order Distribution.This capability needs<br>to be provided in both an ability to query<br>in real time and a publish/subscribe<br>mechanism to enable the use of the<br>information wherever required. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 236 | Customer Loyalty<br>SubscriptionManag<br>ement<br>Configuration | Customer Loyalty<br>SubscriptionManagement<br>Configuration function manages<br>information for subscription and<br>deactivation to a Loyalty<br>program.Subscription<br>management includes:<br>- checking customer requirements<br>- assigning one or more subgroups to<br>which the customer belongs<br>- assigning welcome points & send<br>welcome messages<br>- generate the unique Loyalty-identifier<br>Loyalty Subscription Management can<br>assign multiple traffic channels to<br>loyalty subscriptions (sim-cards, PBX,<br>Call Data Network etc.) | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 259 | External Call Center<br>Access | External Call Center Access provides<br>access to call center self-empowered<br>fulfillment function providing an internet<br>technology driven interface for the<br>customer to undertake a variety of<br>fulfillment functions directly for<br>themselves. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 262 | Product<br>Availability<br>Checking 1 | Product Availability Checking<br>function provide an internet<br>technology driven interface for the<br>customer to undertake a product<br>availability check.<br>E.g., that the product offering is active<br>for sales, the equipment(s) specified<br>in the customer order are on stock. | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 272 | Order Status<br>Viewing | Order Status Viewing provides self-<br>empowered fulfillment function of an<br>internet technology driven interface for<br>the customer to undertake Order status<br>enquiry. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 277 | Shopping Cart<br>Purchasing Access | Shopping Cart Purchasing Access<br>function provide an internet technology<br>driven interface to the customer to<br>undertake self-service purchase. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 317 | Product Availability<br>Area Checking | Product Availability Area Checking<br>checks if CSP marketed products are<br>availability in the customer area |   |   |
| 343 | Mass Transaction<br>Ordering | Mass Transaction Ordering feed<br>function of new orders. For bulk sales by<br>e.g., affiliates and corporate customer<br>self-empowered fulfillment provided<br>e.g., by an internet technology driven<br>interface for bulk ordering. | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 359 | Contract and SLA<br>creation | Contract and SLA Creation provides<br>contract generation as well as<br>appropriate service level agreements<br>(SLAs) generation |   |   |
| 366 | Customer Order<br>Management | Customer Order Management provides<br>an online access function to specific<br>orders, to be used for management,<br>monitoring and tracking for customer<br>support and external agents for Upgrade<br>of customer’s products/services. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 379 | Product<br>Customization<br>Offering<br>Management | Product Customization Offering<br>Management provides the necessary<br>functionality to manage the customer<br>personalized proposals, taking into<br>account the customer location, needs,<br>current products, as well as the service<br>provider's products, sales emphasis<br>and targets, etc. | Sales<br>Management | Opportunity<br>Management |
| 387 | Sales Metrics<br>Calculation | Sales Metrics Calculation provides<br>sales metrics calculation according to<br>pre-defined metrics rules |   |   |
| 388 | Sales Order<br>Reporting | Sales Order Reporting provides<br>reporting of order handoff. | Sales<br>Reporting | Sales<br>Performance<br>Management |
| 716 | Order Data<br>Enrichment | Order Data Enrichment function acquire<br>missing order data from surrounding<br>systems (often values taken from<br>catalogs and inventories, billing, fraud,<br>etc.) or from external 3rd party systems<br>(like country's common address or<br>credit check system). | Customer<br>Order<br>Management | Customer<br>Order<br>Completion |
| 717 | Calculated Order<br>Data Enrichment | Calculated Order Data Enrichment<br>calculates missing order data values<br>on-the-fly from existing data and<br>ordering rules. E.g., Contract end dates,<br>Discounted period, etc. | Customer<br>Order<br>Management | Customer<br>Order<br>Completion |
| 718 | Customer Order<br>Validation | Customer Order Validation Function<br>ensures that the qualified order is valid<br>in any moment of order lifecycle,<br>usually as data become available.<br>Validation ensures early fallout which is<br>less costly than encountering errors in<br>later stages of order handling. | Customer<br>Order<br>Management | Customer<br>Order<br>Validation |
| 719 | Customer Order<br>Storage | The Customer Order Storage function<br>stores the valid and complete customer<br>orders into an appropriate data storage. | Customer<br>Order<br>Management | Customer<br>Order<br>Repository<br>Management |
| 720 | Customer Order<br>Searching | Customer Order Searching function<br>makes the customer orders available to<br>other applications. |   |   |
| 727 | Product Offer to<br>Customer<br>Verification 2 | Product Offer to Customer<br>Verification enables and verifies the<br>configuration of the commercial offer<br>chosen by the customer. | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 756 | Fallout Rule Based<br>Error Correction | Fallout Rule Based Error Correction<br>function provides the capability to<br>handle various errors or error types<br>based on pre-defined rules. These rules<br>can facilitate autocorrection, correction<br>assistance, placement of errors in the<br>appropriate queues for manual<br>handling, as well as access to various<br>systems via the Fallout Interface Bus. | Fallout<br>Management | Fallout<br>Correction<br>Management |
| 934 | Sales Negotiation<br>Support | Sales Negotiation Support provides<br>support for negotiating the sale by<br>providing multiple quotations as<br>needed, taking into account the<br>customer data, customer qualification,<br>and offers made. Functionality includes<br>access to products, product pricing,<br>scheduling of appointments if a<br>dispatch is necessary, etc.<br>Sales Negotiation generates an order or<br>service request. A Customer order<br>request.<br>Customer order request generation –<br>send solution design details to update<br>proposal product order in Customer<br>Order Management systems<br>Service order request generation – send<br>solution design details to update service<br>order in Service Order Management<br>systems (after customer agreement –<br>part of handoff to fulfillment) | Sales<br>Management | Opportunity<br>Management |
| 1063 | Sales Quote<br>Management | Sales Quote Management creates and<br>manages quotes, including internal<br>approval. | Sales<br>Management | Opportunity<br>Management |
| 1071 | Customer Credit<br>Eligibility<br>Validation | Customer Credit Eligibility Validation<br>function checks the Customer Credit<br>Eligibility, considering the payment<br>history and the credit scores for a<br>Customer, only the predictive credit<br>score for a Prospective Customer. | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 1109 | Customer Order<br>Quote Calculation | Customer Order Quote Calculation<br>Function enables the elaboration of<br>an estimate, including configuration,<br>pricing and feasibility elements,<br>thanks to the specific configuration,<br>eligibility and valuation functions,<br>identifying the various relevant<br>interlocutors (through the Sales<br>Interlocutors Management function),<br>the scenarios to be realized and the<br>lot. | Customer<br>Order<br>Management | Customer<br>Order<br>Quotation |
| 1110 | Customer Order<br>Quote Creation | Customer Order Quote<br>Materialization Function materializes<br>via a document and/or associated to a<br>simplified identification mean (QR<br>code, bar code) to ease later<br>interactions and identification of the<br>quotation, and sent to the customer. | Customer<br>Order<br>Management | Customer<br>Order<br>Quotation |
| 1123 | Product Order<br>Initialization | The Product Order Initialization<br>Function creates the Product Order<br>and initializes it with the operations<br>and default configuration on the<br>mandatory products of the selected<br>offer, or target offer in case of<br>migration. | Product<br>Configuratio<br>n &<br>Activation | Offer and<br>Product<br>Configuratio<br>n |
| 1200 | Customer Loyalty<br>Subscription<br>Activation | Customer Loyalty Subscription<br>Activation function manages Loyalty<br>programs activation and deactivation.<br>It includes<br>- assigning one or more subgroups to<br>which the customer belongs<br>- assigning welcome points & send<br>welcome messages<br>- generate the unique Loyalty-<br>identifier | Product<br>Configuratio<br>n &<br>Activation | Product<br>Activation |
| 1325 | Customer Order<br>Distribution | Customer Order Distribution function<br>enables distributing finalized<br>customer orders to any parties and<br>systems that need the order<br>information and/or the notification<br>that the order has been finalized. | Customer<br>Order<br>Management | Customer<br>Order<br>Completion |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
| --- | --- | --- | --- | --- | --- |
| TMF622 | Product<br>Ordering<br>Management | 4 | Mandatory | productOrder | GET<br>GET /id<br>POST<br>PATCH<br>DELETE |
|   |   |   |   | cancelProductOrder | GET<br>GET /id<br>POST |
| TMF648 | Quote<br>Management | 4 | Optional | quote | GET<br>GET /id<br>POST<br>PATCH<br>DELETE |
| TMF663 | Shopping Cart<br>Management | 4 | Optional | shoppingCart | GET<br>GET /id<br>POST<br>PATCH<br>DELETE |
| TMF688 | TMF688 Event |   | Optional |   |   |
| TMF701 | Process Flow<br>Management | 4 | Optional | processFlow | GET<br>GET /id<br>POST<br>DELETE |
|   |   |   |   | taskFlow | GET<br>GET /id<br>PATCH |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

The APIs called by this component and provided by other components are:

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operation | Rationales |
| --- | --- | --- | --- | --- | --- | --- |
| TMF620 | Product<br>Catalog<br>Management | v4 | Mandatory | productCategory | Get, Get<br>/id | minimum<br>consistenc<br>y check |
|   |   |   |   | productOffering | Get, Get<br>/id |   |
|   |   |   |   | productOfferingPrice | Get, Get<br>/id |   |
|   |   |   |   | productSpecification | Get, Get<br>/id |   |
| TMF629 | Customer<br>Management | v4 | Optional |   | Get |   |
| TMF632 | Party<br>Management | v4 | Optional | individual | Get, Get<br>/id |   |
|   |   |   |   | organization | Get, Get<br>/id |   |
| TMF637 | Product<br>Inventory<br>Management | v4 | Mandatory | product | Get, Get<br>/id, Post,<br>Patch | minimum<br>consistenc<br>y check<br>(case of<br>update of<br>an existing<br>product) |
| TMF638 | Service<br>Inventory<br>Management | v4 | Optional | service | Get, Get<br>/id |   |
| TMF639 | Resource<br>Inventory<br>Management | v4 | Optional | resource | Get, Get<br>/id |   |
| TMF645 | Service<br>Qualification<br>Management | v4 | Optional | checkServiceQualifica<br>tion | Get, Get<br>/id, Post,<br>Patch |   |
|   |   |   |   | queryServiceQualificat<br>ion | Get, Get<br>/id, Post,<br>Patch |   |
| TMF646 | Appointment<br>Management | v4 | Optional | appointment | Get, Get<br>/id, Post,<br>Patch,<br>Delete |   |
|   |   |   |   | searchTimeSlot | Get, Get<br>/id, Post,<br>Patch,<br>Delete |   |
| TMF651 | Agreement | v4 | Optional | agreement | Get, Get<br>/id |   |
| TMF666 | Account<br>Management | v4 | Optional | billingAccount | Get, Get<br>/id |   |
| TMF669 | Party Role<br>Management | v4 | Optional | partyRole | Get, Get<br>/id |   |
| TMF672 | TMF672 User<br>Role<br>Permission API |   | Optional |   | Get |   |
| TMF673 | Geographic<br>Address<br>Management | v4 | Optional | geographicAddress | Get, Get<br>/id |   |
|   |   |   |   | geographicSubAddres<br>s | Get, Get<br>/id |   |
|   |   |   |   | geographicAddressVal<br>idation | Get, Get<br>/id, Post,<br>Patch |   |
| TMF674 | Geographic Site<br>Management | v4 | Optional | geographicSite | Get, Get<br>/id |   |
| TMF676 | Payment<br>Management | v4 | Optional | payment | Get, Get<br>/id |   |
| TMF679 | Product<br>Offering<br>Qualification<br>Management | v4 | Optional | productOfferingQualifi<br>cation | Get, Get<br>/id, Post,<br>Patch |   |
| TMF683 | Party<br>Interaction Mgt | v4 | Optional | partyInteraction | Get, Get<br>/id |   |
| TMF685 | Resource Pool<br>Management |   | Optional |   | Get, Post,<br>Patch |   |
| TMF687 | Stock<br>Management | v4 | Optional | checkProductStock | Get, Get<br>/id, Post,<br>Delete |   |
|   |   |   |   | queryProductStock | Get, Get<br>/id, Post,<br>Delete |   |
|   |   |   |   | reserveProductStock | Get, Get<br>/id, Post,<br>Delete |   |
|   |   |   |   | productStock | Get, Get<br>/id |   |
| TMF688 | TMF688 Event | v4 | Optional |   | Get, Post |   |
| TMF701 | Process Flow<br>Management | v4 | Optional | processFlow | Get, Get<br>/id, Post,<br>Patch |   |
|   |   |   |   | taskFlow | Get, Get<br>/id, Post,<br>Patch |   |
| TMF716 | Resource<br>Reservation | v4 | Optional | resourceReservation | Get, Get<br>/id, Post,<br>Patch,<br>Delete |   |
|   |   |   |   | cancelResourceReser<br>vation | Get, Get<br>/id, Post |   |
| TMF760 | Product<br>Configuration<br>Management | v5 | Optional | checkProductConfigur<br>ation | Get, Get<br>/id, Post |   |
|   |   |   |   | queryProductConfigur<br>ation | Get, Get<br>/id, Post |   |

NOTE: Geographic Location Management API (TMF675) is available in preview version. As soon as the interface will be published it will be added to the table. NOTE: new API TMF716 Resource Reservation v4 taken into account to replace TMF685 Resource Pool Management.

## 3.3. Events

The diagram illustrates the Events which the component publishes and the Events that the component subscribes to and then receives. Both lists are derived from the APIs listed in the preceding sections. The type of event could be: • Create: a new resource has been created (following a POST). • Delete: an existing resource has been deleted. • AttributeValueChange: an attribute from the resource has changed - event structure allows to pinpoint the attribute. • InformationRequired: an attribute should be valued for the resource preventing to follow nominal lifecycle - event structure allows to pinpoint the attribute. • StateChange: resource state has changed.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component Map on the TM Forum website for the machine-readable component specification files for this component.

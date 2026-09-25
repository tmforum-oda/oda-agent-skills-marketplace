---
id: TMFC031
type: component
name: Bill Calculation
version: 2.0.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC031_Bill_Calculation_Management_v2.0.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: f7794beaaa2924ac2d2652b56331bba38f22e6878e0948b04a1ce96ecb428fd4
  raw_path: references/components/TMFC031/TMFC031_Bill_Calculation_Management_v2.0.0.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF635
      name: usage-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF678
      name: customer-bill-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS005
      name: Billing - Fiber Contract
yaml_spec_version: 3.0.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Bill<br>Calculation | TMFC031 | The Bill Calculation processes all<br>charges against billing accounts during<br>bill cycles. Bill Calculation can be<br>executed both on a cyclic basis and on<br>demand. It performs calculations with bill<br>compilation of charges, credits, fees &<br>taxes, including pro rata, at various<br>levels, such as product and/or account<br>level that have been generated since the<br>last run for that account, applying<br>promotions and discounts as well. | Core<br>Commerce<br>Management |

![](media/bill-calculation-architecture.png)
*([PlantUML source](media/bill-calculation-architecture.puml))*

# 2. eTOM Processes and SID Data Entities

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.9 | L2 | Customer Bill<br>Invoice<br>Management | Ensure the bill invoice is created, physically<br>and/or electronically produced and<br>distributed to customers, and that the<br>appropriate taxes, discounts, adjustments,<br>rebates and credits for the products and<br>services delivered to customers have been<br>applied. |
| 1.3.9.4 | L3 | Pricing,<br>Discounting,<br>Adjustments &<br>Rebates<br>Application | Ensure that the bill invoice is reflective of all<br>the commercially agreed billable events and<br>any bill invoice adjustments agreed between<br>a Service Provider and the customer. |
| 1.3.9.4.1 | L4 | Obtain Billing Events | Accept billing events that have been collected,<br>translated, correlated, assembled, guided and<br>service rated before determining the information<br>would be applied to the customer’s bill<br>invoice(s). |
| 1.3.9.4.2 | L4 | Apply Pricing,<br>Discounting,<br>Adjustments &<br>Rebates to Customer<br>Account | Determine the customer account or customer<br>specific pricing, charges, discounts, and<br>taxation that should be delivered to the<br>invoice(s) for the customer. |
| 1.3.9.4.3 | L4 | Apply Agreed<br>Customer Bill<br>Adjustment | Apply and review any adjustment agreed in the<br>previous billing period and make these included<br>to the bill invoice. |
| 1.6.15 | L2 | BP Bill/Invoice<br>Management | Business Partner Bill/Invoice Management<br>manages the Business Partner bill/invoice<br>process, controls bills/invoices, manages<br>the lifecycle of bills/invoices. A bill is a<br>notice for payment which is supposed to be<br>preceded by an invoice in most cases. |
| 1.6.15.1 | L3 | BP Bill/Invoice<br>Process<br>Management | Make certain that there is capability so that the<br>Bill Invoice Management processes can<br>operate effectively and design and develop an<br>enterprise's invoicing process. |
| 1.6.15.3 | L3 | BP Bill/Invoice<br>Lifecycle<br>Management | Ensure bills/invoices are created, physically<br>and/or electronically produced and<br>distributed to parties, and that the<br>appropriate taxes, discounts, adjustments,<br>rebates and credits for the products<br>delivered to parties have been applied. |
| 1.6.15.3.1 | L4 | Apply BP Pricing,<br>Discounting,<br>Adjustments &<br>Rebates | Ensure that a bill/invoices is reflective of all the<br>commercially agreed billable events and any<br>bill/invoice adjustments agreed between an<br>enterprise and a BP. |
| 1.6.15.3.5 | L4 | Receive BP<br>Bill/Invoice | Receive and record the bill/invoice from a BP .<br>Compare a BP bill/invoice against all<br>transactions with the BP that would result in a<br>bill/invoice being sent to the enterprise. Manage<br>the interactions between a BP and an<br>enterprise. Approve a BP bill/invoice |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Applied Customer Billing Rate ABE | n/a |
| Applied Party Billing Rate ABE | n/a |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-bill-calculation-links.png)
*([PlantUML source](media/etom-sid-bill-calculation-links.puml))*

## 2.4. Functional Framework Functions

*Discounting may apply to different levels and for this component it refers to end of cycle discounts that cannot be managed or applied in Product Configurator or Product Usage Management.

| Function<br>ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 67 | Usage Summary<br>and Details<br>Presentation | Usage Summary and<br>Details Presentation<br>presents usage summary<br>and details (billed and non-<br>billed) for a specific time<br>period. | Invoice<br>Management | Invoicing |
| 87 | Billing Event<br>Processing Guiding | Billing Event Processing<br>Guiding support for a<br>consistent processing. | Invoice<br>Management | Invoicing |
| 316 | Billing<br>Administration | The Billing Administration<br>function manages the data<br>that are necessary to<br>perform the bill calculation:<br>billing cycle data,<br>management of runs,<br>groups and cycles of<br>invoicing. | Invoice<br>Management | Invoicing |
| 399 | Billing Management<br>Integration | Billing Management<br>Integration provide a<br>Virtual Network Operators<br>online access function to<br>make them self-sufficient<br>for Billing management.<br>Including the use of<br>VNO/Dealer data fencing. | Invoice<br>Management | Invoicing |
| 32 | Billing Initialization | Billing Initialization<br>initializes the bill and<br>sends to the Bill<br>Calculation application the<br>required information for<br>accounts that are going to<br>be processed. | Invoice<br>Management | Invoicing |
| 72 | Billing Account<br>Price Plan<br>Determining | Billing Account Price Plan<br>Determining associates a<br>charge record with the<br>appropriate price plan. | Invoice<br>Management | Billing<br>Account<br>Administration |
| 70 | Charge To Billing<br>Account Distribution | Charge To Billing Account<br>Distribution identifies the<br>related prepaid or postpaid<br>billing account for a given<br>charge (recurring, one<br>time, usage). | Invoice<br>Management | Billing<br>Account<br>Administration |
| 69 | Charge To Billing<br>Account<br>Identification | Charge To Billing Account<br>Identification associates<br>incurred charge to the<br>billing account liable for its<br>payment. | Invoice<br>Management | Billing<br>Account<br>Administration |
| 68 | Charges to Billing<br>Statement<br>Identification | Charges to Billing<br>Statement Identification<br>identifies what charges are<br>to be included in the<br>statement. | Invoice<br>Management | Billing<br>Account<br>Administration |
| 158 | Commitment<br>Tracking Result<br>Determining | Commitment Tracking<br>Result Determining<br>determines the outcome of<br>the evaluation (financial<br>benefits or penalties) in the<br>context of the gathered<br>data for commitment<br>tracking. | Rating and<br>Follow up | Bill<br>Calculation |
| 159 | Commitment<br>Tracking Terms &<br>Conditions<br>Evaluation | Commitment Tracking<br>Terms & Conditions<br>Evaluation evaluates the<br>terms and conditions in the<br>context of the gathered<br>data for commitment<br>tracking. | Rating and<br>Follow up | Bill<br>Calculation |
| 160 | Commitment<br>Tracking Data<br>Collection | Commitment Tracking<br>Data Collection collects<br>data to be used in the<br>evaluation of the terms and<br>conditions to monitor<br>financial commitments<br>between the customer and<br>the provider. | Rating and<br>Follow up | Bill<br>Calculation |
| 256 | Customer Bill<br>Usage and Charges<br>Viewing | Customer Bill Usage and<br>Charges Viewing provides<br>an internet technology<br>driven interface to the<br>customer to undertake<br>Usage and charges<br>comparison and unbilled<br>charges view directly for<br>themselves. | Rating and<br>Follow up | Bill<br>Calculation |
| 89 | Billing Event<br>Aggregation | Billing Event Aggregation<br>is part of the Billing Event<br>Processing to supply<br>aggregated billing events<br>to the Billing System. | Invoice<br>Management | Invoicing |
| 90 | Billing Event<br>Processing<br>Analyzing | Billing Event Processing<br>Analyzing provides billing<br>event analysis and billing<br>event aggregations<br>analysis to control the<br>usage data sent to the<br>Billing System. | Invoice<br>Management | Invoicing |
| 183 | Bill Charges<br>Aggregation | Bill Charges Aggregation<br>function determines<br>charges (including<br>recurring, one time and<br>usage charges) for<br>purchased products and<br>services in a given bill run<br>based on the customer<br>price plan set at time of the<br>customer order/contract<br>negotiation. | Rating and<br>Follow up | Bill<br>Calculation |
| 60 | Split Bill Charge<br>Distribution | Split Bill Charge<br>Distribution provides<br>charge and event<br>distribution to support a<br>split bill. | Rating and<br>Follow up | Tariff<br>Calculation<br>and Rating |
| 184 | Currency<br>Conversion | Currency Conversion<br>identifies the required<br>currency conversion if any<br>needed to appropriately bill<br>the customer. | Rating and<br>Follow up | Bill<br>Calculation |
| 61 | On Demand Bill<br>Calculation | On Demand Bill<br>Calculation function will<br>invoke a bill calculation on<br>demand for e.g. a<br>purchase. | Rating and<br>Follow up | Bill<br>Calculation |
| 300 | Discounts<br>Calculation* | Discounts Calculation<br>determines charge<br>discounts based on pricing<br>plan; including discounts<br>on recurring, one time, and<br>usage charges. Discounts<br>may be applied at different<br>levels such as cross<br>product, cross location, or<br>cross customer (all<br>customers that are part of<br>a given group plan – some<br>affiliation). The discounts<br>can be apportioned across<br>multiple events. | Rating and<br>Follow up | Tariff<br>Calculation<br>and Rating |
| 55 | Price and Discount<br>Calculation* | Price and Discount<br>Calculation applies pricing<br>and discounting rules and<br>algorithms in the context of<br>the assembled information<br>concerning Products (i.e.<br>instances of Product). | Rating and<br>Follow up | Tariff<br>Calculation<br>and Rating |

# 3. TMF OPEN APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF678 | Customer Bill<br>Management | 4 | Mandatory | appliedCustomerBillingRate:<br>• GET<br>• GET /id |
| TMF701 | Process Flow<br>Management | 4 | Optional | processFlow:<br>• GET<br>• GET /id<br>• POST<br>• DELETE /id<br>taskFlow:<br>• GET |

Note: TMF678 only for applied customer bill resource

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation potentially used by the product catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API<br>Version | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- | --- |
| TMF6<br>66 | AccountManagem<br>ent | 4 | Mandatory | billingAccount:<br>GET, GET<br>/id,POST, PATCH<br>/id, DELETE /id<br>billingCycelSpecific<br>ation: GET, GET<br>/id,POST, PATCH | Billing Account<br>and Billing Cycle<br>information<br>required to<br>understand what<br>BillingAccount to<br>apply the |

| API ID | API Name | API Version | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- | --- |
|   |   |   |   | /id, DELETE /id<br>billingFormat: GET,<br>GET /id, POST,<br>PATCH /id,<br>DELETE /id<br>billing<br>PresentationMedia:<br>GET, GET /id,<br>POST, PATCH /id,<br>DELETE /id | customer rate to<br>and the Billing<br>Cycle period. |
| TMF6<br>32 | PartyManagement | 4 | Optional | individual: GET,<br>GET /id<br>organization: GET,<br>GET /id |   |
| TMF6<br>37 | Productinventory | 4 | Mandatory | product: GET, GET<br>/id | To retrieve<br>installed product<br>and price<br>information to<br>determine the<br>applied rate. |
| TMF6<br>20 | Product Catalog | 4 | Optional | productOffering:<br>GET, GET /id<br>productOfferingPric<br>e: GET, GET /id<br>productSpecificatio<br>n: GET, GET /id |   |
| TMF6<br>69 | PartyRoleManage<br>ment | 4 | Optional | partyRole: GET,<br>GET /id |   |
| TMF6<br>35 | Usage<br>Management | 4 | Optional | usage: GET, GET<br>/id<br>usageSpecification:<br>GET |   |
| TMF7<br>01 | ProcessFlowMan<br>agement | 4 | Optional | processFlow: GET,<br>GET /id, POST,<br>PATCH /id |   |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

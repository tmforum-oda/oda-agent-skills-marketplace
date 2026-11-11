---
id: TMFC030
type: component
name: Bill Generation Management
version: 2.2.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC030_Bill_Generation_Management_v2.2.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 29b199b657a5342657c79822614202408adb0585f08ea348a373c1e8daa41e65
  raw_path: references/components/TMFC030/TMFC030_Bill_Generation_Management_v2.2.0.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF667
      name: document-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF676
      name: payment-management-api
    - id: TMF678
      name: customer-bill-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS005
      name: Billing - Fiber Contract
yaml_spec_version: 2.0.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Bill<br>Generation<br>Management | TMFC030 | Bill generation management .manages the<br>party invoice management. It addresses<br>the invoice formatting, presentation and<br>dispatching to the proper means of<br>communication. | Party<br>Management |

# 2. eTOM Processes and SID Data Entities

## 2.1. eTOM business activities

![](media/bill-generation-management-architecture.png)
*([PlantUML source](media/bill-generation-management-architecture.puml))*

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.9 | L2 | Customer Bill<br>Invoice<br>Management | Ensure the bill invoice is created, physically<br>and/or electronically produced and distributed<br>to customers, and that the appropriate taxes,<br>discounts, adjustments, rebates and credits for<br>the products and services delivered to<br>customers have been applied. |
| 1.3.9.2 | L3 | Create Customer<br>Bill Invoice | Production of a timely and accurate invoice in<br>accordance with the specific billing cycles and<br>reflective of the final charges for services,<br>together with any adjustments, delivered to the<br>customer by the Service Provider and<br>respective other parties. |
| 1.3.9.2.1 | L4 | Render & Format<br>Customer Invoice | Render and format the customer bill invoice. |
| 1.3.9.2.2 | L4 | Deliver Electronic<br>Invoice | Deliver the electronic copy of an invoice to<br>customers. |
| 1.3.9.2.3 | L4 | Verify Customer<br>Invoice Quality | Verify Customer invoice quality before<br>distribution to the customer in electronic form<br>and the process responsible for physical invoice<br>production and distribution. |
| 1.3.9.2.4 | L4 | Manage Customer<br>InvoiceQuality<br>Archive | Store the customer invoice for a period of time<br>is to address regulation and/or internal<br>requirements, during which they can be<br>accessed to support any customer or regulator<br>agency inquiries on bill invoices. |
| 1.3.9.3 | L3 | Produce &<br>Distribute<br>Customer Bill | Physical production and distribution of bills<br>to customers in accordance with the<br>specified billing cycle. |
| 1.3.9.3.1 | L4 | Co-ordinate Billing<br>Insertion | Co-ordinate with promotional processes for any<br>billing insertions to be included with the bill. |
| 1.3.9.3.2 | L4 | Establish & Manage<br>Bill Production Cycle | Establish and manage the physical bill<br>production cycle. |
| 1.3.9.3.3 | L4 | Deliver Invoice<br>Information | Deliver the invoice information to the physical<br>production processes. |
| 1.3.9.4 | L3 | Pricing,<br>Discounting,<br>Adjustments &<br>Rebates<br>Application | Ensure that the bill invoice is reflective of all<br>the commercially agreed billable events and<br>any bill invoice adjustments agreed between<br>a Service Provider and the customer. |
| 1.3.9.4.2 | L4 | Apply Pricing,<br>Discounting,<br>Adjustments &<br>Rebates to Customer<br>Account | Determine the customer account or customer<br>specific pricing, charges, discounts, and<br>taxation that should be delivered to the<br>invoice(s) for the customer. |
| 1.6.15 | L2 | BP Bill/Invoice<br>Management | Business Partner Bill/Invoice Management<br>manages the Business Partner bill/invoice<br>process, controls bills/invoices, manages<br>the lifecycle of bills/invoices. A bill is a<br>notice for payment which is supposed to be<br>preceded by an invoice in most cases. |
| 1.6.15.2 | L3 | BP Bill/Invoice<br>Control | Establish and maintain Business Partner bill<br>invoice formats, maintain lists of parties who<br>are eligible for receiving bills/invoices, and<br>define the billing cycles. |
| 1.6.15.2.1 | L4 | Establish & Maintain<br>BP Bill Invoice<br>Format | Establish and maintain BP bill invoice formats,<br>and any interaction with specific parties to<br>modify the format. |
| 1.6.15.2.2 | L4 | Maintain Bill Invoice<br>BP List | Maintain lists of parties who are eligible for<br>receiving bills/invoices. |
| 1.6.15.2.3 | L4 | Define BP Billing<br>Cycle | Define the billing cycles and their dates<br>according to cash flow needs as established by<br>financial management processes. |
| 1.6.15.3.2 | L4 | Create BP<br>Bill/Invoice | Produce a timely and accurate bill/invoice in<br>accordance with a specific billing cycle, on<br>demand after the purchase of an offering, on<br>request by a BP, and so forth. Ensure that a<br>bill/invoice is reflective of the final charges for<br>products, together wit |
| 1.6.15.3.2 | L4 | Create BP<br>Bill/Invoice | Produce a timely and accurate bill/invoice in<br>accordance with a specific billing cycle, on<br>demand after the purchase of an offering, on<br>request by a BP, and so forth. Ensure that a<br>bill/invoice is reflective of the final charges for<br>products, together wit |
| 1.6.15.3.3 | L4 | Distribute BP<br>Bill/Invoice | Provide bills/invoices to one or more parties<br>and ensure the delivery of bills/invoices to one<br>or more parties. |
| 1.6.15.3.4 | L4 | Manage BP<br>Bill/Invoice Archive | Store a BP bill/invoice for a period of time to<br>address regulation and/or internal<br>requirements, during which it can be accessed<br>to support any BP, such as a<br>government/regulator agency or internal BP,<br>inquiries about a bill/invoice. |
| 1.6.15.3.5 | L4 | Receive BP<br>Bill/Invoice | Receive and record the bill/invoice from a BP .<br>Compare a BP bill/invoice against all<br>transactions with the BP that would result in a<br>bill/invoice being sent to the enterprise. Manage<br>the interactions between a BP and an<br>enterprise. Approve a BP bill/invo |
| 1.6.15.3.6 |   | Administer<br>Commercial<br>Arrangement for BP<br>Bill/Invoice Creation<br>Capability | Establish the requirements for, and manage the<br>agreed commercial arrangements with,<br>appropriate outsourced parties of the creation<br>capabilities. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Party Bill ABE | n/a |
| Customer Bill ABE | n/a |

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-bill-links.png)
*([PlantUML source](media/etom-sid-bill-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Sub-Domain<br>Functions<br>Level 1 | Sub- Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 62 | Invoice Items<br>Listing | Invoice Items Listing lists all<br>invoice items for a specific<br>invoice. | Invoice<br>Management | Invoicing |
| 63 | Invoice Listing | Invoice Listing function will list<br>all invoices for a customer both<br>over time and for customers<br>with multiple invoices. | Invoice<br>Management | Invoicing |
| 65 | Bill Image<br>Presentation | Bill Image Presentation<br>provides presentation of an<br>exact bill image or after<br>invoking a transactional<br>document generation function. | Invoice<br>Management | Invoicing |
| 309 | Invoice Balance<br>Calculation | Provides the means to<br>calculate the balance due for<br>an invoice/bill. | Invoice<br>Management | Invoicing |
| 310 | Invoice Charges<br>Compilation | Invoice Charges Compilation<br>assembles charges (including<br>charge distribution- charges<br>incurred by other customers),<br>credits, taxes, fees and<br>adjustments that affect the<br>balance due. | Invoice<br>Management | Invoicing |
| 312 | Invoice Detail<br>Collection | Provides appropriate levels of<br>detail regarding items on the<br>invoice. This detail is provided<br>to revenue reporting and/or Bill<br>Format &; Render. | Invoice<br>Management | Invoicing |
| 311 | Invoice Totals<br>Calculation | Provides subtotals and totals at<br>various levels. | Invoice<br>Management | Invoicing |
| 329 | Invoice Tax<br>Calculation | "Invoice Tax Calculation<br>provides the necessary<br>functionality to calculate taxes,<br>including surcharges and fees,<br>where applicable.<br>This function can occur within<br>the Invoicing application or<br>through the use of an external<br>Tax module." | Invoice<br>Management | Invoicing |

# 3. TMF OPEN APIs & Events

The following part covers the APIs and Events; This part is split in 4: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event. <Note to be inserted into ODA Component specifications: If a new Open API is required, but it does not yet exist. Then you should include a textual description of the new Open API, and it should be clearly noted that this Open API does not yet exist. In addition a Jira epic should be raised to request the new Open API is added, and the Open API team should be consulted. Finally, a decision is required on the feasibility of the component without this Open API. If the Open API is critical then the component specification should not be published until the Open API issue has been resolved. Alternatively if the Open API is not critical, then the specification could continue to publication. The result of this decision should be clearly recorded.>

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF678 | Customer Bill<br>Management | Mandatory | customerBillOnDemand<br>• GET<br>• GET /id<br>• POST<br>customerBill<br>• GET<br>• GET /id<br>• POST<br>• PATCH /id<br>: |
| TMF701 | Process Flow<br>Management | Optional | processFlow:<br>• GET<br>• GET /id<br>• POST<br>• DELETE /id<br>taskFlow:<br>• GET<br>• GET /id<br>• PATCH /id |

## 3.2. Dependant APIs

Following diagram illustrates API/Resource/Operation potentially used by the product catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF666 | Account Management<br>API | Mandatory | billingAccount:<br>• GET<br>• GET /id<br>billingCycleSpecification:<br>• GET<br>• GET /id<br>billFormat:<br>• GET<br>• GET /id<br>billPresentationMedia:<br>• GET<br>• GET /id |
| TMF632 | Party Management<br>API | Optional | individual:<br>• GET<br>• GET /id<br>organization:<br>• GET<br>• GET /id |
| TMF676 | Payment Management<br>API | Optional | payment:<br>• GET<br>• GET /id<br>• POST<br>refund:<br>• GET<br>• GET /id<br>• POST |
| TMF667 | Document<br>Management API | Optional | document:<br>• GET<br>• GET /id<br>• POST |
| TMF637 | Product Inventory<br>Management API | Optional | product:<br>• GET<br>• GET /id |
| TMF669 | Party Role<br>Management API | Optional | partyRole:<br>• GET<br>• GET /id |
| TMF678 | Customer Bill<br>Management API | Mandatory | appliedCustomerBillingRate:<br>• GET<br>• GET /id |
| TMF701 | Process Flow<br>Management API | Optional | processFlow:<br>• POST<br>• GET<br>• GET /id<br>• PATCH /id<br>taskFlow:<br>• GET<br>• GET /id<br>• POST<br>• PATCH /id |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

The type of event could be: • Create : a new resource has been created (following a POST). • Delete: an existing resource has been deleted. • AttributeValueChange: an attribute from the resource has changed - event structure allows to pinpoint the attribute. • InformationRequired: an attribute should be valued for the resource preventing to follow nominal lifecycle - event structure allows to pinpoint the attribute. • StateChange: resource state has changed.

# 4. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

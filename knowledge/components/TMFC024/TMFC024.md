---
id: TMFC024
type: component
name: Billing Account Management
version: 2.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC024_Billing_Account_Management_v2.1.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: f80853849d6aa0fbbe55e8c6832b7d47bedfb74cb7cff169a6271ec1dbb0bd52
  raw_path: references/components/TMFC024/TMFC024_Billing_Account_Management_v2.1.0.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF670
      name: payment-method-management-api
    - id: TMF676
      name: payment-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS005
      name: Billing - Fiber Contract
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 2.1.1
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Billing Account<br>Management | TMFC024 | The billing account management component<br>aims to provide all the needed functionalities<br>to create, configure and modify billing<br>accounts.<br>BAM component has the goal to support and<br>handle the following capabilities/<br>functionalities.<br>• Set-up/ creation of Billing account<br>• Associate payment plan(s)<br>• Associate payment method(s) -<br>optional<br>• Account taxes/ fees exception<br>management<br>• Define account associations<br>• Provide account balance details<br>• Set-up Billing contacts<br>• Set-up Billing preferences (e.g., bill<br>cycle frequency, invoice media type,<br>invoice template option, etc.) | Party<br>Management |

![](media/billing-account-management-architecture.png)
*([PlantUML source](media/billing-account-management-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.10 | L2 | CustomerBill<br>Payments &<br>Receivables<br>Management | Ensure that enterprise revenue is<br>collected through pre-established<br>collection channels and put in place<br>procedures to recover past due<br>payments. |
| 1.3.10.1 | L3 | Manage Customer<br>Billing Account | Ensure effective management of the<br>customer’s billing account as it relates to<br>the products purchased and consumed<br>throughout the appropriate billing cycle. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| Customer Billing Account | Customer Billing Account |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-billing-account-links.png)
*([PlantUML source](media/etom-sid-billing-account-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function<br>Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 77 | Billing<br>Account<br>Information<br>Configuration | Billing Account Information<br>Configuration updates specific<br>billing account information such<br>as customer bill periods, bill<br>media options, etc. | Invoice<br>Management | Billing Account<br>Administration |
| 73 | Billing<br>Account<br>Reporting | Billing Account Reporting;<br>Grouping<br>charges/statement/accounts for<br>the purpose of creating a report | Invoice<br>Management | Billing Account<br>Administration |
| 76 | Billing<br>Account<br>Structure<br>Configuration | Billing Account Structure<br>Configuration modifies billing<br>accounts based on various<br>account constructs. | Invoice<br>Management | Billing Account<br>Administration |
| 75 | Billing<br>Accounts<br>Creation | Billing Accounts Creation<br>provides the ability to create<br>billing accounts based on<br>various account constructs.<br>Account creation can also be<br>automated with orders received | Invoice<br>Management | Billing Account<br>Administration |
| 248 | Customer<br>Billing | Customer Billing Hierarchies<br>Management provide an internet<br>technology driven interface to<br>undertake billing functions | Invoice<br>Management | Billing Account<br>Administration |
|   | Hierarchies<br>Management | directly for management of<br>hierarchies driven billing<br>operations for e.g. corporate<br>customers |   |   |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF666 | Account Management | Mandatory | billingAccount:<br>• GET<br>• GET /id<br>• POST<br>• PATCH<br>• DELETE<br>billingCycleSpecification:<br>• GET<br>• GET /id<br>• POST<br>• PATCH<br>• DELETE<br>billFormat:<br>• GET<br>• GET /id<br>• POST<br>• PATCH<br>• DELETE<br>billPresentationMedia:<br>• GET<br>• GET /id<br>• POST<br>• PATCH<br>• DELETE |
| TMF688 | Event Management | Optional | processFlow:<br>• GET<br>• GET /id<br>• POST<br>• DELETE<br>taskFlow:<br>• GET<br>• GET /id<br>• POST<br>• DELETE |
| TMF701 | Process Flow<br>Management | Optional | listener:<br>• POST<br>hub:<br>• POST<br>• DELETE |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operation | Rationale |
| --- | --- | --- | --- | --- |
| TMF632 | Party Management | Mandatory | - individual:<br>- GET<br>- GET /id<br>-<br>organization:<br>- GET<br>- GET /id | Billing<br>Account must<br>be related to<br>at least one<br>Party |
| TMF669 | Party Role<br>Management | Mandatory | - partyRole:<br>- GET<br>- GET /id | Party Role<br>access based<br>control |
| TMF672 | UserRolesPermissions | Mandatory | Get |   |
| TMF670 | Payment Method<br>Management | Optional | -<br>paymentMethod:<br>- GET<br>- GET /id |   |
| TMF676 | Payment Management | Optional | - payment:<br>- GET<br>- GET /id |   |
| TMF701 | Process Flow<br>Management | Optional | -<br>processFlow:<br>- POST<br>- GET<br>- GET /id<br>- PATCH |   |
| TMF688 | Event Management | Optional | Get |   |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component Directory for the machine-readable component specification file for this component.

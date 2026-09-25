---
id: TMFC050
type: component
name: Product Recommendation Management
version: 1.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC050_Product_Recommendation_Management_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 26b78d5de4214f40c586577db981b3850df0bdaeedaf57ac3718d3bb280d9ac7
  raw_path: references/components/TMFC050/TMFC050_Product_Recommendation_Management_v1.1.0.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF621
      name: trouble-ticket-management-api
    - id: TMF622
      name: product-ordering-management-api
    - id: TMF629
      name: customer-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF635
      name: usage-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF663
      name: shopping-cart-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF671
      name: promotion-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF678
      name: customer-bill-management-api
    - id: TMF679
      name: product-offering-qualification-management-api
    - id: TMF680
      name: recommendation-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS002
      name: Browse B2C Catalogue and Check Fiber Technical Eligibility
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
yaml_spec_version: 1.0.0
---

# 1. Overview

1. TAC-208 IG1171 (update) Component Definition to v4.0.0 and incorporate IG1245 Principles to Define ODA Components

# 2. [TAC-250] IG 1171 Improvements Some observations & recommendations. - TM Forum JIRA

# 3. [TAC-214] Interface Standardization needs all 3 stages of process to be developed - TM Forum JIRA

# 4. [TAC-226] Overview - TM Forum JIRA

# 5. ODA-846 Summary of ODA component Template enhancements for 14th Sep Review

| Component<br>Name | ID | Description | ODA<br>Function<br>Block |
| --- | --- | --- | --- |
| Product Recommend<br>ation Management | TMF<br>C050 | Product Recommendation component is responsible for evaluating and providing product offering/specfication<br>recommendations based on the history and real-time context of a party and marketing strategy. | Intelligence<br>Management |

![](media/product-recommendation-management-architecture.png)
*([PlantUML source](media/product-recommendation-management-architecture.puml))*

2. eTOM Processes, SID Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business<br>Activity<br>Name | Description |
| --- | --- | --- | --- |
| 1.1.9.4 | L2 | Cross/Up Sell | Cross/Up Sell ensures that the value of the relationship between the customer or other party and an enterprise is maximized by selling<br>additional, or more of the existing, product offerings. The ongoing analysis of customer or other party trends, such as usage, problems,<br>complaints, is used to identify when the current offerings may no longer be appropriate or when the opportunity for a larger sale arises. Based<br>on the data collected, more appropriate or other offering(s) may be recommended to the customer or other party. |
| 1.1.9.4.2 | L3 | Recommend<br>Appropriate<br>Product<br>Offering(s) | Recommend Appropriate Product Offering(s) recommends more appropriate or other product offering(s) to the customer or other party that<br>may be based on the results of Analyze Customer or Other Party Trends or based on known other offerings that represent an upsell.<br>For example, a potential new partner may be offered the opportunity to have there logo and contact information added to an enterprise's<br>application that manages a IoT device. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified. Note: There is need to create Product Recommendation Management BE in SID.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-recommendation-links.png)
*([PlantUML source](media/etom-sid-recommendation-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function<br>Name | Function Description | Aggregate<br>Function<br>Level 1 | Aggregate<br>Function<br>Level 2 |
| --- | --- | --- | --- | --- |
| 1196 | Product<br>Specification &<br>Offering<br>Simulation | Product Specification & Offering Simulation Function simulates Product Specification configuration and Product<br>Offerings on the real traffic of the customer thanks to Tariff Calculation and Rating. | Product<br>Operational<br>Analysis | Pushed Offer<br>Management |
| 1195 | Pushed Offer<br>Identification | Pushed Offer Identification Function identifies offers adapted to the customer needs including personalized offers.<br>Based on a customer's individualized knowledge (Marketing one to one), the aim is to elaborate for each customer<br>according to his needs and recent action individualized Product Specifications & Offerings. | Product<br>Operational<br>Analysis | Pushed Offer<br>Management |

3. TM Forum Open APIs & Events The following part covers the APIs and Events; This part is split in 3: List of Exposed APIs - This is the list of APIs available from this component. List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event. <Note note to be inserted into ODA Component specifications: If a new Open API is required, but it does not yet exist. Then you should include a textual description of the new Open API, and it should be clearly noted that this Open API does not yet exist. In addition, a Jira epic should be raised to request the new Open API is added, and the Open API team should be consulted. Finally, a decision is required on the feasibility of the component without this Open API. If the Open API is critical then the component specification should not be published until the Open API issue has been resolved. Alternatively if the Open API is not critical, then the specification could continue to publication. The result of this decision should be clearly recorded.>

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF680 | Recommendation Management | 4 | Mandatory | GET<br>GET/id<br>POST |
| TMF701 | Process Flow API | 4 | Optional | GET<br>GET/id<br>POST |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation potentially used by the product recommendation management component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- | --- |
| TMF620 | Product Catalog Management | 4 | Mandatory | - catalog:<br>- GET<br>- GET /id<br>- category:<br>- GET<br>- GET /id<br>- productSpecification:<br>- GET<br>- GET /id<br>- productOffering:<br>- GET<br>- GET /id<br>- productOfferingPrice:<br>- GET<br>- GET /id |   |
| TMF637 | Product Inventory Management | 4 | Optional | - product:<br>- GET<br>- GET /id |   |
| TMF622 | Product Ordering Management | 4 | Optional | - productOrder:<br>- GET<br>- GET /id |   |
| TMF679 | Product Offering Qualification | 4 | Optional | - productOfferingQualification:<br>- GET<br>- GET /id |   |
| TMF666 | Account Management | 4 | Optional | - billingAccount:<br>- GET<br>- GET /id |   |
| TMF663 | Shopping Cart Management | 4 | Optional | - shoppingCart:<br>- GET<br>- GET /id |   |
| TMF671 | Promotion Management | 4 | Optional | - promotion:<br>- GET<br>- GET /id |   |
| TMF673 | Geographic Address Management | 4 | Optional | - geographicAddressManagement:<br>- GET<br>- GET /id |   |
| TMF675 | Geographic Location Management | 4 | Optional | - geographicLocationManagement:<br>- GET<br>- GET /id |   |
| TMF632 | Party Management | 4 | Optional | - individual:<br>- GET<br>- GET /id<br>- organization:<br>- GET<br>- GET /id |   |
| TMF669 | Party Role Management | 4 | Optional | - partyRole:<br>- GET<br>- GET /id |   |
| TMF678 | Customer Bill Management | 4 | Optional | - customerBill:<br>- GET<br>- GET /id |   |
| TMF621 | Trouble Ticket | 4 | Optional | - troubleTicket:<br>- GET<br>- GET /id |   |
| TMF635 | Usage Management | 4 | Optional | - usage:<br>- GET<br>- GET /id |   |
| TMF645 | Service Qualification Management | 4 | Optional | checkServiceQualification:<br>-Get<br>-Get /id<br>-Post<br>-Patch |   |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

4. Machine Readable Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component or click the link Recommendation_Manag ement V1.1.yaml. 5. References

## 5.1. TMF Standards related versions

| Standard | Version(s) |
| --- | --- |
| SID | 24.0 |
| eTOM | 24.0 |
| Functional Framework | 24.0 |

## 5.2. Jira References

JIRA request for creating the SID entity for queryRecommendationManagement : [ISA-1194] SID Entity for queryRecommendationManagement - TM Forum Jira JIRA request for improving the function description of 1196: [FX-1227] Improvement of the description for function id 1196 - Product Specification & Offering Simulation - TM Forum Jira JIRA request for improving the function description of1195: [FX-1228] Improvement of the description for function id 1195 - Pushed Offer Identification - TM Forum JIRA

## 5.3. Further resources

1. IG1228: please refer to IG1228 for defined use cases with ODA components interactions.

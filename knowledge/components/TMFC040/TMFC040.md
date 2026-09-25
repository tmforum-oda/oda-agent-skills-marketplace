---
id: TMFC040
type: component
name: Product Usage Management
version: 1.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC040_Product_Usage_Management_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: d7b253880df331fd1dbf1a4b82021a697606d6622cf6b7edf96f313e18902323
  raw_path: references/components/TMFC040/TMFC040_Product_Usage_Management_v1.1.0.pdf
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
    - id: TMF669
      name: party-role-management-api
    - id: TMF677
      name: usage-consumption-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS005
      name: Billing - Fiber Contract
    - id: TMFS009
      name: Usage and Balance Management
yaml_spec_version: 1.1.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Product<br>Usage<br>Management | TMFC040 | The Product Usage Components<br>provides standardized mechanisms<br>for product usage management<br>(creation, update, retrieval, import and<br>export of a collection of usages) and<br>Product Rating & Rate Assignment by<br>assigning a value (monetary or other)<br>to an event in the context of a product,<br>a party (customers and partners) and<br>payer. | Core<br>Commerce<br>Management |

![](media/product-usage-management-architecture.png)
*([PlantUML source](media/product-usage-management-architecture.puml))*

# 2. eTOM Processes and SID Data Entities

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.2.16 | L2 | Product Usage<br>Management | The Product Usage management<br>processes encompass the functions<br>required to guide, distribute, mediate,<br>summarize, accumulate, and analyze<br>Product Usage records. These processes<br>may occur in real-time, near real-time (i.e.<br>just at the end of the usage), or may be<br>executed on a periodic basis.<br>Based on Service Usage, this process aims<br>at identifying Product Usage. For example,<br>for a Video on Demand where you can<br>watch a video as many time as you want<br>during 72 hours, several Service Usages<br>might have been tracked (each time the<br>user watches the video) and only one<br>Product Usage will be identified for all<br>Service Usages in the 72 hours after the<br>first watch.<br>The guiding processes ensures that the<br>Product Usage records used in the billing<br>processes are appropriately related to the<br>correct customer billing account and<br>products.<br>The Product Usage records are edited and<br>if necessary reformatted (mediated) to<br>meet the needs of subsequent processes.<br>The billing event records may also be<br>enriched with additional data during this<br>process. |
| 1.2.16.1 | L3 | Product Usages | The Enrich Product Usages processes will<br>augment the product usage records by<br>adding data to the records from sources<br>such as customer, product, or other<br>reference data. |
| 1.2.16.1.1 | L4 | Add Product Usage Data | Add data to the records from sources such<br>as customer, product, or other reference<br>data to augment the product usage<br>records. |
| 1.2.16.1.2 | L4 | Assign Product Usage<br>Price | Assign a price to product usage without<br>consideration of specific product or<br>customer information. The assigned price<br>may be used to enrich the product usage<br>record. |
| 1.2.16.2 | L3 | Guide and Assign<br>Product Usages | The Guide Product Usages processes<br>ensure that the event records used in the<br>billing process relate to the correct<br>customer billing account and products. A<br>specific product usage record may be<br>related to multiple customer billing<br>accounts and subscribed products.<br>Distribution of product usage records to<br>other processes may also occur. |
| 1.2.16.2.1 | L4 | Assign Product Usages | Ensure that the Product Usages used in<br>the billing process relate to the correct<br>Product. |
| 1.2.16.2.2 | L4 | Distribute Product Usage | Distribute billing event records to other<br>processes. |
| 1.2.16.2.3 | L4 | Guide Product Usages | Guide Product Usages process is in charge<br>of identifying Product Usages based on<br>Service Usages.<br>For example, for a Video on Demand<br>where you can watch a video as many time<br>as you want during 72 hours, several<br>Service Usages might have been tracked<br>(each time the user watches the video) and<br>only one Product Usage will be identified<br>for all Service Usages in the 72 hours after<br>the first watch. |
| 1.2.16.3 | L3 | Mediate Product Usages | The Mediate Product Usages process edits<br>and reformats the data record to meet the<br>needs of a recipient application. |
| 1.2.16.3.1 | L4 | Edit Product Usages | Edit the data record for recipient<br>applications. |
| 1.2.16.3.2 | L4 | Reformat Product<br>Usages | Reformat the data record for recipient<br>applications. |
| 1.2.16.4 | L3 | Report Product Usage<br>Records | The purpose of the Report Product Usage<br>Record processes is to generate reports on<br>Product Usage records based on requests<br>from other processes.<br>These processes produce reports that may<br>identify abnormalities, which may be<br>caused by fraudulent activity or related to<br>customer complaints.<br>Investigation of problems related to these<br>product usage records is also part of this<br>process.<br>These processes also support other<br>processes such as customer review of<br>product usages (pre-billing and post-<br>billing). |
| 1.2.16.4.1 | L4 | Generate Product Usage<br>Report | Generate reports on product usage records<br>based on requests from other processes. |
| 1.2.16.4.2 | L4 | Investigate Product<br>Usage Related Problem | Investigate problems related to product<br>usage records. |
| 1.2.16.4.3 | L4 | Support Product Usage<br>Related Process | Support other processes such as customer<br>review of product usages (pre-billing and<br>post-billing). |
| 1.2.17 | L2 | Product Rating & Rate<br>Assignment | The purpose of Product Rating &<br>Assignment is to rate a value (monetary or<br>other) to Product Usage or a set of Product<br>Usages and assign the result to a Product<br>and a Billing Account. The charge may be<br>either a credit or a debit and can be<br>handled either online or offline.<br>Online charging is performed in real-time,<br>requiring an authorization component<br>which may affect how the service is<br>rendered and enables an operator to<br>provide prepaid services to its customers.<br>Whereas offline charging is performed after<br>the service is rendered and is not required<br>to be done in real-time and generally<br>relates to subscription based products. |
| 1.2.17.1 | L3 | Perform Rating | Process responsible for calculating the<br>value of a product usage or a set of product<br>usages, before, during or after the<br>rendering of the service, based on<br>parameters of the request (type, quantity,<br>etc.), parameters of the<br>customer/subscriber (tariffs, price plans,<br>accumulated usage, contracts, etc.) and<br>other parameters (time-of-day, taxes, etc.).<br>The same request maybe rated differently<br>for different subscribers based on their<br>purchased offers or agreements. |
| 1.2.17.2 | L3 | Aggregate Items For<br>Rate Assignment | This process is responsible for<br>accumulating contributing items, which can<br>be quantities, values (monetary or other) or<br>both. Aggregation can occur over time or<br>can be initiated to gather a “snapshot” of<br>the items at a point in time. |
| 1.2.17.3 | L3 | Manage Customer<br>Assignment<br>HierarchyManaging the<br>charging relationships<br>among subscribers. | Customer hierarchies are commonly used<br>for corporate customers, family plans or<br>other type of affinity groups. This process<br>manages the assignment relationships<br>among subscribers, e.g. sharing, inheriting<br>or restricting balances, price plans and<br>discounts. Thereby assuring that a charge<br>is added to or subtracted from the correct<br>account balance. |
| 1.2.17.4 | L3 | Provide Advice of Rate | The activity of Provide Advice of Rate (aka<br>Advice of Charge) is responsible for<br>providing advice on rates, in real-time or<br>offline, an estimate or value of the rate for a<br>specific usage request. The advice is<br>usually based upon performing a full rating<br>process for the request. |
| 1.2.17.5 | L3 | Apply Rate Level<br>Discounts | This process applies discounts to product<br>prices at an individual product level. A<br>discount may be expressed as a monetary<br>amount or percentage, and modifies a price<br>for a product. When a discount is<br>expressed as a percentage, the<br>discounting process determines the<br>discount calculated in relation to the price<br>for the product.<br>The discount may be displayed as a<br>separate entry on the bill or may be<br>combined with the rate for the product to<br>only show as one entry.<br>Discounts may be a one-time event or may<br>have some duration (days, months, life of<br>product, etc.). Discounts may apply to a<br>specific customer or be generally available<br>based on selection of products (for<br>example - bundles). Discounting structures<br>may involve tiers, tapers, or thresholds. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified. ** In the context of this component, it relates to the usage events and not the management of the ProductUsageSpecification. The ProductUsageSpecification is maintained by TMFC001 Product Catalog Management component. *** In the context of Usage; related to UsageProdPriceCharge and related ProdPriceAlteration.

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Product Usage ABE** |   |
| Product Price ABE*** |   |

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-product-usage-links.png)
*([PlantUML source](media/etom-sid-product-usage-links.puml))*

# 3. Functional Framework Functions

** Consumption is exposed through TMF677 and Usage details through TMF635.

| Function<br>ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 253 | Customer Usage<br>and Charges<br>Report Access | Customer Usage and<br>Charges Report Access<br>provides an internet<br>technology driven<br>interface to the<br>customer to access<br>web based reports for<br>(historical) usage and<br>charges directly for<br>themselves. | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Bill Calculation |
| 55 | Price and<br>Discount<br>Calculation | Price and Discount<br>Calculation applies<br>pricing and discounting<br>rules and algorithms in<br>the context of the<br>assembled information<br>concerning Products<br>(i.e. instances of<br>Product). | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 125 | Charging Event<br>Accumulation | Charging Event<br>Accumulation function<br>accumulates events<br>that provide<br>measurements that will<br>be used in the charge<br>calculation (e.g. used<br>allowance). | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 126 | Event<br>Charge/Credit<br>Calculation | Event Charge/Credit<br>Calculation calculates<br>event-level<br>charges/credits (one<br>time, recurring, and<br>usage). | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 127 | Calculated<br>Charges/Credits<br>Proration | Calculated<br>Charges/Credits<br>Proration provides<br>proration of calculated<br>charges/credits. The<br>function handles partial<br>rating of a period. | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 128 | Late Arrival<br>Usage<br>Charges/Credits<br>Recalculation | Late Arrival Usage<br>Charges/Credits<br>Recalculation provides<br>recalculation of<br>charges/credits based<br>on information received<br>later (e.g. from the<br>Service Level<br>Agreement function,<br>delayed call detail<br>record file arrival,<br>delayed order arrival).<br>Recalculation may be<br>necessary: pre-billing<br>(prior to Bill<br>Calculation), during the<br>Bill Calculation process,<br>and/or post-billing. | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 186 | Charging/Rating<br>Recalculation | Charging/Rating<br>Recalculation function<br>recalculates the<br>charges, when<br>appropriate, across<br>product, location, or<br>customer, and<br>considerations based<br>on business rules. | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 300 | Discounts<br>Calculation | Discounts Calculation<br>determines charge<br>discounts based on<br>pricing plan; including<br>discounts on recurring,<br>one time, and usage<br>charges. Discounts<br>may be applied at<br>different levels such as<br>cross product, cross<br>location, or cross<br>customer (all customers<br>that are part of a given<br>group plan – some<br>affiliation). The<br>discounts can be<br>apportioned across<br>multiple events. | Product Usage<br>Management<br>Rating and<br>Follow up | Rating and<br>Follow up<br>Tariff Calculation<br>and Rating |
| 67 | Usage Summary<br>and Details<br>Presentation | Usage Summary and<br>Details Presentation<br>presents usage<br>summary and details<br>(billed and non-billed)<br>for a specific time<br>period.** | Invoice<br>Management | Invoicing |
| 85 | Billing Event<br>Processing<br>Distribution | Billing Event<br>Processing Distribution<br>function for correlation<br>and distribution of<br>usage data for<br>processing of e.g. bill,<br>customer and product.<br>To supply relevant<br>usage data to the<br>Billing System. | Invoice<br>Management | Invoicing |
| 86 | Billing Event<br>Processing<br>Enrichment | Billing Event<br>Processing Enrichment<br>with complementing<br>data e.g. product or<br>location information to<br>supply relevant<br>information to the<br>Billing System. | Invoice<br>Management | Invoicing |

# 4. TMF OPEN APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event. The Product Usage Management Component relate to usage and the API TMF635 Usage Managment is in evolution as it mix concerns on product, service and resource levels. With version 5 of Open APIs, there is a major evolution of Usage APIs so that there will be a distinct usage API per Product, Service, and Resource: • TMF767 Product Usage • TMF727 Service Usage • TMF771 Resource Usage These will replace the existing TMF635 Usage Management that will stop with v4 and not be migrated to v5. The Product Usage Management component relates to the usage on Product Level so in future iterations, the TMF767 will be included.

## 4.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF635 | Usage Management | Mandatory | usage: GET, GET /id, POST,<br>PATCH/id |
| TMF677 | Usage Consumption<br>Management | Mandatory | queryUsageConsumption: GET,<br>GET /id, POST |
| TMF701 | Process Flow<br>Management API | Optional | processFlow: GET, GET /id,<br>POST, DELETE /id<br>taskFlow: GET, GET /id, PATCH<br>/id |

## 4.2. Dependant APIs

Following diagram illustrates API/Resource/Operation potentially used by the product catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations | Rationale |
| --- | --- | --- | --- | --- |
| TMF632 | Party<br>Management | Mandatory | individual: GET, GET<br>/id<br>organization: GET,<br>GET /id | To be able to<br>guide the<br>Product Usage<br>to the<br>appropriate<br>Party and its<br>related<br>products. |
| TMF669 | Party Role<br>Management | Optional | partyRole: GET, GET<br>/id |   |
| TMF620 | Product Catalog<br>Management<br>API | Mandatory<br>Optional | productOffering: GET,<br>GET /id<br>productOfferingPrice:<br>GET, GET /id<br>productSpecification:<br>GET, GET /id |   |
| TMF637 | Product<br>Inventory | Mandatory | product: GET, GET /id | To retrieve<br>installed<br>product and<br>price<br>information to<br>determine the<br>rate to assign. |
| TMF701 | Process Flow<br>Management | Optional | processFlow: GET,<br>GET /id, POST,<br>PATCH |   |

## 4.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 5. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

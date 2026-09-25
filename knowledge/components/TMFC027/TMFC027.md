---
id: TMFC027
type: component
name: Product Configurator
version: 2.1.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC027_ProductConfigurator_v2.1.1.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 4f9e6cd54f5361192ecad29adc52bea0fa76406c5226bfbadcdfde6008c0a833
  raw_path: references/components/TMFC027/TMFC027_ProductConfigurator_v2.1.1.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF622
      name: product-ordering-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF637
      name: product-inventory-management-api
    - id: TMF645
      name: service-qualification-management-api
    - id: TMF651
      name: agreement-management-api
    - id: TMF662
      name: entity-catalog-management-api
    - id: TMF666
      name: account-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF679
      name: product-offering-qualification-management-api
    - id: TMF701
      name: process-flow-management-api
    - id: TMF760
      name: product-configuration-management-api
    - id: TMF921
      name: intent-management-api
  use_cases:
    - id: TMFS002
      name: Browse B2C Catalogue and Check Fiber Technical Eligibility
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS010
      name: ODA Flow with NaaS Support
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS019
      name: TMFS019
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 2.1.1
---

# 1. Overview

| Component Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Product<br>Configurator | TMFC027 | The Product Configurator aims to provide<br>sales representatives and customers with<br>fast and error-free product qualification and<br>product configuration capabilities across all<br>channels.<br>It uses mostly the Product Catalog and the<br>Product Inventory information, and is able<br>to execute and check all types of Product<br>Catalog policy rules (e.g. packaging rules,<br>commercial pre-requisite rules, pricing<br>rules, consistency rules between<br>characteristic values). It can also use Party<br>related information, such as the age of the<br>customer, or specific contextual<br>information, such as the channel.<br>It can be triggered in contexts such as<br>product order capture, shopping cart or<br>quote management. It supports the Product<br>Order Capture and Validation component<br>(TMFC002) to:<br>• Establish commercial offering<br>eligibility, and to provide alternative<br>product offerings in case of<br>ineligible product offering selection<br>• Leads the configuration of selected<br>eligible product offerings according<br>to the context. Product configuration<br>includes computation of<br>characteristics values, allowed<br>values, bundled and related product<br>offering, pricing and discounts | Core Commerce<br>Management |

![](media/product-configurator-architecture.png)
*([PlantUML source](media/product-configurator-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.2.5 | L2 | Product<br>Configuration<br>Management | Configuration Management configures or creates a<br>new version of a configuration for an entity, such as<br>a product,service or resource, as defined by a<br>configuration specification. This process also<br>modifies a configuration and values for configuration<br>parameters, and removes a configuration. |
| 1.2.5.2 | L3 | Manage Product<br>Configuration | Manage Product Configuration business activity is in<br>charge of creating, maintaining, controlling,<br>changing and reporting Product Configuration<br>according to Product Configuration Plans.<br>Manage Product Configuration will establish and<br>maintaining consistency of a product's performance,<br>functional, and physical attributes within the limits<br>defined by product requirements, product design,<br>and operational information throughout the Products<br>Lifecycle. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE L1 Definition | SID ABE Level 2 (or set of BEs)* |   | SID ABE L2<br>Definition |
| --- | --- | --- | --- | --- |
| Product<br>Configurati<br>on | A Product Configuration (also referred to<br>as a Product Profile) defines how a<br>Product operates or functions.<br>A Product Configuration may contain one<br>or more parts, and each part may contain<br>zero or more fields. Each field may have<br>attributes that are statically or dynamically<br>defined. Some of these fields have fixed<br>values, while others provide values from<br>which a choice or choices can be made<br>(e.g. using the EntitySpec/Entity and/or<br>CharacteristicSpec/CharacteristicValue<br>patterns) 1 | ProductConfigurati<br>on | A<br>representati<br>on of how a<br>Product<br>operates or<br>functions in<br>terms of<br>characteristi<br>cs and<br>related<br>Product(s). |   |

1 As in GB922 Product v23.0 document the definition of the ABE Product Configuration is a copy of the Configuration ABE pattern defined in GB922 Common v23.0, it is here adapted to the product level only. *: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-product-configuration-links.png)
*([PlantUML source](media/etom-sid-product-configuration-links.puml))*

## 2.4. Functional Framework Functions

1 TMFC027 Product Configurator covers the part related to Product Catalog rules checking. Stock control part is done by TMFC002 Product Order Capture & Validation 2 TMFC027 Product Configurator covers the part related to Product Catalog rules checking at commercial and functional eligibility levels. Technical eligibility controls are triggered by TMFC002 Product Order Capture & Validation

| Function<br>ID | Functional Framework Function | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 55 | Price & Discount<br>Calculation | Price and Discount<br>Calculation applies<br>pricing and discounting<br>rules and algorithms in<br>the context of the<br>assembled information<br>concerning Products (i.e.<br>instances of Product). | Rating and<br>Follow up | Tariff<br>Calculation<br>and Rating |
| 182 | Inter Product<br>Dependency<br>Identification | Inter-Product<br>Dependency<br>Identification identifies<br>product dependencies,<br>binds new order to<br>purchased product or<br>point to the dependent<br>product required | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 205 | Customer Order<br>Eligibility<br>Validation | Customer Order Eligibility<br>Validation function<br>validates that the Offer &<br>products specified on the<br>Customer Order, are<br>eligible from a<br>commercial and<br>functional point of view.<br>It includes:<br>• Commercial Eligibility<br>with commercial<br>compatibility with the<br>already customer<br>installed Offers<br>• Functional Eligibility<br>with the customer's<br>already installed<br>Products (corresponding<br>to ProductSpecification). | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 207 | Offer and Product<br>Configuration | The Offer and Product<br>Configuration function<br>enables the configuration<br>of the commercial offer<br>chosen by the customer.<br>The configuration<br>recovers the choice of an<br>option, the choice of the<br>characteristics values for<br>the Product Specification<br>including installation<br>preferences...<br>It can be based on<br>product configurator<br>using a rule engine.<br>It can be used at the<br>same time by Selling,<br>Order Establishment or<br>Develop Sales Proposal<br>Business activities. | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 262 | Product Availability<br>Checking 1 | Product Availability<br>Checking function<br>provide an internet<br>technology driven<br>interface for the customer<br>to undertake a product<br>availability check.<br>E.g., that the product<br>offering is active for<br>sales, the equipment(s)<br>specified in the customer<br>order are on stock. | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 274 | Quote Price<br>Support Access | Quote Price Support<br>Access provides self<br>empowered fulfillment<br>function to provide an<br>internet technology<br>driven interface for the<br>customer to get a<br>Quotation price. | Customer<br>Order<br>Management<br>Fulfillment<br>Integration<br>Management | Customer<br>Order<br>Quotation<br>Customer<br>Fulfillment<br>Access<br>Management |
| 278 | Customer SLA<br>Preferences<br>Capturing | Customer SLA<br>Preferences Capturing<br>captures the customer's<br>SLA preferences e.g., as<br>part of the fulfillment. | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 300 | Discount<br>Calculation | Discounts Calculation<br>determines charge<br>discounts based on<br>pricing plan; including<br>discounts on recurring,<br>one time, and usage<br>charges.<br>Discounts may be<br>applied at different levels<br>such as cross product,<br>cross location, or cross<br>customer (all customers<br>that are part of a given<br>group plan – some<br>affiliation). The discounts<br>can be apportioned<br>across multiple events. | Rating and<br>Follow up | Tariff<br>Calculation<br>and Rating |
| 320 | Customer<br>Product Proposal<br>Creation | Customer Product<br>Proposal Creation<br>proposes according to<br>what the customer<br>presently has as part of<br>what can be further<br>provided to the customer<br>including bundling,<br>product proposals, etc. | Product<br>Configuration<br>& Activation | Offer and<br>Product<br>Configuration |
| 379 | Product<br>Customization<br>Offering<br>Management | Product Customization<br>Offering Management<br>provides the necessary<br>functionality to manage<br>the customer<br>personalized proposals,<br>taking into account the<br>customer location,<br>needs, current products,<br>as well as the service<br>provider's products, sales<br>emphasis and targets,<br>etc. | Sales<br>Management | Opportunity<br>Management |
| 727 | Product Offer to<br>Customer<br>Verification 2 | Product Offer to<br>Customer Verification<br>enables and verifies the<br>configuration of the<br>commercial offer chosen<br>by the customer.<br>The configuration consist<br>of technical, functional,<br>and commercial<br>prerequisites and<br>preferences. | Customer<br>Order<br>Management | Customer<br>Order<br>Eligibility<br>Validation |
| 928 | Solution Design<br>Creation | Solution Design Creation<br>function<br>combine/configure the<br>emerged solution based<br>on the existing solution,<br>planned changes and<br>newly designed features<br>(e.g., for site connectivity<br>services)<br>Selecting relevant<br>Products and Services<br>from Catalog – Browse<br>and select entries from a<br>catalog that might be<br>relevant to the set of<br>captured requirements<br>into the design. | Sales<br>Management | Opportunity<br>Management |
| 930 | Automatic Solution<br>Validation | Obtains configuration<br>constraints from the<br>catalog and validates the<br>correctness of the design<br>against them. | Sales<br>Management | Opportunity<br>Management |
| 931 | Solution Pricing | The Solution Pricing<br>function is concerned<br>with assuring that the<br>designs are priced<br>consistent with pricing<br>used for billing. The<br>common product catalog<br>provides an initial price<br>base for the components<br>that are in the solution<br>vs. the existing<br>configuration at the<br>customer location. | Sales<br>Management | Opportunity<br>Management |
| 932 | Calculation Rules<br>Retrieval | Calculation Rules<br>Retrieval function gives<br>support for tariffication<br>rules including<br>discounting rules.<br>It supports that<br>discounting rules and<br>guidelines are provided<br>as to standard levels of<br>discounts/promotions<br>that can be provided to<br>the customer. Special<br>discount arrangements<br>can be obtained by<br>following an escalation<br>process. There is<br>workflow functionality to<br>help manage discount<br>escalation. | Sales<br>Management | Opportunity<br>Management |
| 933 | Price/Cost<br>Optimization<br>Price Optimization | Price Optimization<br>enables sales to<br>effectively evaluate the<br>customer, generate<br>recommendations for<br>price decreases and<br>increases, and set<br>negotiation guidelines<br>based on our cost. This<br>includes the application<br>of non-standard pricing. | Sales<br>Management | Opportunity<br>Management |

# 3. TMF OPEN APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API<br>Name | API<br>Vers<br>ion | Manda tory / Option al | Operations |
| --- | --- | --- | --- | --- |
| TMF679 | Product<br>Offering<br>Qualifica<br>tion | V4 | Mandat<br>ory | productOfferingQu<br>alification:<br>• GET<br>• GET /id<br>• POST<br>• PATCH<br>• DELETE |
| TMF760 | Product<br>Configur<br>ation | V5 | Mandat<br>ory | checkProductQual<br>ification:<br>• GET<br>• GET /id<br>• POST<br>queryProductQuali<br>fication:<br>• GET<br>• GET /id<br>• POST |
| TMF688https://raw.githubusercont<br>ent.com/tmforum-apis/TMF688-<br>Event/master/TMF688-Event-<br>v4.0.0.swagger.json | Event | V4.0.<br>0 | Option<br>al | listener:<br>• POST<br>hub:<br>• POST<br>• DELETE |
| TMF701 | Process<br>Flow | V4.0.<br>0 | Option<br>al | processFlow:<br>• POST<br>• GET<br>• GET /id<br>• DELETE<br>taskFlow:<br>• GET<br>• GET /id<br>• PATCH |

## 3.2. Dependent APIs

The following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- |
| TMF637 | Product<br>Inventory<br>Management<br>API | Mandatory | product:<br>- GET<br>- GET /id | Check required to<br>verify any product<br>inventory related to<br>the party. |
| TMF620 | Product<br>Catalog<br>Management<br>API | Mandatory | catalog:<br>- GET<br>- GET /id<br>category:<br>- GET<br>- GET /id<br>productOffering:<br>- GET<br>- GET /id<br>productOfferingPrice:<br>- GET<br>- GET /id<br>productSpecification:<br>- GET<br>- GET /id | Product configuration<br>must rely on product<br>catalog information. |
| TMF622 | Product<br>Ordering<br>Management<br>API | Mandatory | productOrder:<br>- GET<br>- GET /id | Product configurator<br>must produce a<br>product order. |
| TMF632 | Party<br>Management<br>API | Optional | individual:<br>- GET<br>- GET /id<br>organization:<br>- GET<br>- GET /id | n/a |
| TMF662 | Entity Catalog<br>Management<br>API | Optional | entityCatalog:<br>- GET<br>- GET /id | n/a |
| TMF666 | Account<br>Management<br>API | Optional | billingAccount:<br>- GET<br>- GET /id | n/a |
| TMF669 | Party Role<br>Management<br>API | Optional | partyRole:<br>- GET<br>- GET /id | n/a |
| TMF672 | User Roles<br>Permissions | Optional | permission:<br>- GET<br>- GET /id<br>userRole:<br>- GET<br>- GET /id | n/a |
| TMF673 | Geographic<br>Address | Optional | geographicAddress:<br>- GET<br>- GET /id<br>geographicSubAddress: | n/a |
|   | Management<br>API |   | - GET<br>- GET /id |   |
| TMF674 | Geographic<br>Site<br>Management<br>API | Optional | geographicSite:<br>- GET<br>- GET /id | n/a |
| TMF688 | Event | Optional | event:<br>- GET<br>- GET /id | n/a |
| TMF701 | Process Flow | Optional | processFlow:<br>- POST<br>- GET<br>- GET /id<br>- DELETE<br>taskFlow:<br>- PATCH<br>- GET<br>- GET /id | n/a |
| TMF921 | Intent<br>Management<br>API | Optional | intent:<br>- GET<br>- GET /id | n/a |

NOTE: Geographic Location Management API (TMF675) is available in Beta version. As soon as the interface will be published it will be added to the table and to the overview.

## 3.3. Events

The diagram illustrates the Events which the component publishes and the Events that the component subscribes to and then receives. Both lists are derived from the APIs listed in the preceding sections. The type of event could be: • Create : a new resource has been created (following a POST). • Delete: an existing resource has been deleted. • AttributeValueChange: an attribute from the resource has changed - event structure allows to pinpoint the attribute. • InformationRequired: an attribute should be valued for the resource preventing to follow nominal lifecycle - event structure allows to pinpoint the attribute. • StateChange: resource state has changed.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

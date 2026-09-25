---
id: TMFC001
type: component
name: Product Catalog Management
version: 2.1.2
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC001_Product_Catalog_Management_v2.1.2.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 36aab54807f945e9a4911ab31373282879aa54355cb0cafae074978bb66bb2ef
  raw_path: references/components/TMFC001/TMFC001_Product_Catalog_Management_v2.1.2.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF633
      name: service-catalog-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF651
      name: agreement-management-api
    - id: TMF662
      name: entity-catalog-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF671
      name: promotion-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS002
      name: Browse B2C Catalogue and Check Fiber Technical Eligibility
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS005
      name: Billing - Fiber Contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS009
      name: Usage and Balance Management
    - id: TMFS010
      name: ODA Flow with NaaS Support
    - id: TMFS012
      name: Product Catalog - Launching a New Product Offering
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS019
      name: TMFS019
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 2.1.2
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Product<br>Catalog<br>Management | TMFC001 | The Product Catalog Management component is<br>responsible for organizing the collection of Products<br>and Product Offering specifications that identify and<br>define all requirements of a product or a product<br>offering that can be commercialized. | Core<br>Commerce |

![](media/product-catalog-management-architecture.png)
*([PlantUML source](media/product-catalog-management-architecture.puml))*

# 2. eTOM Processes, SID Data

Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.2.7 | L2 | Product<br>Specification &<br>Offering<br>Development &<br>Retirement | Product Specification & Offering Development<br>& Retirement processes develop and deliver<br>new product specifications as well as<br>enhancements and new features, ready for<br>use by other processes. Additionally, they<br>handle the removal of specifications no<br>longer offered.<br>Product specifications represent the types of<br>services and resources made available as<br>product offerings to the market by an<br>enterprise. The key measures of this process<br>are how effectively the enterprise’s offerings<br>are broadened by these specifications or new<br>specification features. These processes also<br>manage updates and enhancements to<br>product specifications. Business case<br>development tracking and commitment are<br>key elements of this process.<br>They also develop new product offerings and<br>their associated features. Pricing for the<br>offerings is also developed, such as standard<br>pricing and feature-based pricing. The<br>offerings and selected processes are included<br>in product catalogs which are also developed<br>by these processes. |
| 1.2.19 | L2 | Product Catalog<br>Planning<br>Management | Product Catalog Planning Management<br>business process covers a set of business<br>activities that understand and enable<br>establish the plan to define, design and<br>operationalize a catalog in order to meet the<br>needs and objectives of Product cataloging.<br>The Product Catalog Planning Management<br>business process ensure that the organization<br>is able to identify the most appropriate<br>scheme and goal for it catalog. It includes<br>designing the Catalog plan and developing the<br>specification according to Product<br>management requirement. |
| 1.2.20 | L2 | Product Catalog<br>Lifecycle<br>Management | Catalog Lifecycle Management business<br>process covers a set of business activities<br>that enable us to manage the lifecycle of an<br>organizations catalog from design to build<br>according to defined requirements. |
| 1.2.21 | L2 | Product Catalog<br>Operational<br>Readiness<br>Management | Product Catalog Operational Readiness<br>Management business process establishes<br>and administers the support needed to<br>operationalize Product catalogs for ongoing<br>day-to-day business needs.<br>These business activities implement the<br>Product Catalog through Release and Deploy<br>business activities.<br>Release Product Catalog business activity<br>ensure all cross-functional activities needed<br>to support catalog maintenance and<br>operations, such as training and updating the<br>support of the catalog are in place.<br>Release Product Catalog business activity<br>includes identifying stakeholders, catalog<br>integration, catalog federation etc. for any<br>scenario in support of the organizations<br>business goals, including Release conditions<br>that support users, customers and business<br>partners. |
| 1.2.22 | L2 | Product Catalog<br>Content<br>Management | Product Catalog Content Management<br>business process define and provide the<br>business activities that support the day-to-<br>day operations of Product Catalogs in order to<br>realize the business operations goals.<br>Product Catalog Content Management<br>business processes include administering the<br>Product Catalog instance in production,<br>maintaining catalog entries, assuring<br>catalogs, managing catalog access, managing<br>entry lifecycle through versioning, handling<br>catalog entity entry and changes, supporting<br>distribution of catalogs as needed, and<br>supporting user-facing activities. |
| 1.2.23 | L2 | Product<br>Specification<br>Management | Product Specification Management business<br>process leverages captured product<br>requirements to develop, master, analyze,<br>and update documented standard and<br>personalized conditions that must be<br>satisfied by product design and/or delivery.<br>Product Specifications Management can<br>result in establishing, in a centralized way,<br>technical (know-how) standards for products.<br>Such standards provide the organization with<br>a means to control and approve the values<br>and inputs of product specification through<br>structure, review, approval and distribution<br>processes to users (including customers and<br>business partners). |
| 1.6.4 | L2 | Business Partner<br>Offering<br>Development &<br>Retirement | Business Partner Offering Development &<br>Retirement supports the management of on-<br>boarding and off-boarding another Business<br>Partner's product specifications and product<br>offerings that a required to facilitate the<br>business model of the enterprise.<br>It also manages the involvement the<br>enterprise has with a product specification<br>and product offering. For example, the<br>enterprise may accept an order for one of its<br>offerings, but it may be fulfilled by another<br>Business Partner.<br>Note:<br>- Product Specification Development &<br>Retirement and Product Offering<br>Development & Retirement processes are<br>used to manage most of the lifecycle of<br>product specifications and product offerings.<br>This is done to eliminate redundant<br>processes. For example, the Product Offering<br>Pricing processes are used to manage the<br>prices associated with on-boarded product<br>offerings.<br>- This process therefore focuses on managing<br>the relationship that parties, including the<br>enterprise, have with product specifications<br>and product offerings as well as the impact of<br>off-boarding specifications and offerings on a<br>provider's service and resource infrastructure. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Product Offering Specification |   |
| Product Specification |   |
| Product Configuration | ProductConfigSpec BE |
| Product Usage | Product Usage Spec ABE |
| Loyalty | Loyalty Program Specification ABE |
| Party Product Specification & Offering |   |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-product-catalog-links.png)
*([PlantUML source](media/etom-sid-product-catalog-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain<br>Functions Level 2 |
| --- | --- | --- | --- | --- |
| 123 | Product Catalog<br>Browsing | Product Catalog Browsing<br>provides a browsing function<br>to identify products available<br>for purchase by a given<br>customer, provide selected<br>relevant information (e.g. cost,<br>requirements, configurable<br>attributes) to the customer.<br>This information will be used in<br>the step guidance. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 210 | Centralized<br>Ordering Rules<br>Management | Centralized Ordering Rules<br>Management provides<br>centralized business rules for<br>ordering (eligibility,<br>compatibility). | Product<br>Specification<br>& Offering<br>Management | Ordering Rules<br>Development |
| 238 | Customer<br>Loyalty Rules<br>Management | Customer Loyalty Rules<br>Management provides Loyalty<br>Program Rules and customer<br>loyalty profiles management | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 263 | Product<br>Compatibility<br>Checking | Product Compatibility<br>Checking function provide an<br>internet technology driven<br>interface for the customer to<br>check product compatibility. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 360 | Product<br>Agreement<br>Specification<br>Design | Product Agreement<br>Specification Design<br>Function creates and<br>maintains predefined<br>Product Agreement options<br>and templates for Product<br>Offerings. It includes general<br>terms or conditions and<br>approval rules. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 407 | Product<br>Modeling<br>Support | Product Modeling Support<br>supports Lifecycle<br>Management in the design and<br>build phase of the Product<br>Offerings and Product<br>Specifications. | Product<br>Specification<br>& Offering<br>Management | Product Modeling<br>Support |
| 408 | Product<br>Retirement | Product Retirement Function<br>retires obsolete product<br>offering as part of the Lifecycle<br>Management (LM) | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification<br>Lifecycle<br>Management |
| 415 | Product Strategy<br>Linking | Product Strategy Linking links<br>strategy to propositions and<br>links propositions to products | Product<br>Specification<br>& Offering<br>Strategy<br>Definition &<br>Analysis | Product<br>Specification &<br>Offering Strategy<br>Management |
| 416 | Product<br>Propositions<br>Operations<br>Planning | Product Propositions<br>Operations Planning supports<br>the planning of the<br>introduction of propositions for<br>new or updated product<br>offerings and/or product<br>specifications, by planning<br>which operating groups are<br>delivering what of the product<br>proposition and where are the<br>organization and operations<br>touchpoints. | Product<br>Specification<br>& Offering<br>Strategy<br>Definition &<br>Analysis | Product<br>Specification &<br>Offering Strategy<br>Management |
| 417 | Product Strategy<br>to Proposition<br>Alignment | Product Strategy to<br>Proposition Alignment<br>captures and manages details<br>of the business strategy and<br>applies them to the<br>propositions for new or<br>updated product offerings<br>and/or product specifications. | Product<br>Specification<br>& Offering<br>Strategy<br>Definition &<br>Analysis | Product<br>Specification &<br>Offering Strategy<br>Management |
| 418 | Product<br>Strategy/Proposit<br>ions Creation | Product Strategy/Propositions<br>Creation delivers a product<br>strategy and/or propositions<br>for new or updated product<br>offerings and/or product<br>specifications. | Product<br>Specification<br>& Offering<br>Strategy<br>Definition &<br>Analysis | Product<br>Specification &<br>Offering Strategy<br>Management |
| 649 | Product Sourcing<br>Registration | Product Sourcing Registration<br>provides initiation of product<br>instantiation into the service<br>provider product catalog<br>and/or storefront, including<br>product prices. | Business<br>Partner<br>Product<br>Specification<br>and Offering<br>Management | Business Partner<br>Product<br>Specification and<br>Offering Onboarding |
| 650 | Partner Product<br>Certification | Partner Product Certification<br>provides product<br>certification/decertification to<br>be an integrated part of the<br>service provider's value<br>proposition. | Business<br>Partner<br>Product<br>Specification<br>and Offering<br>Management | Business Partner<br>Product Specificatio<br>n and Offering<br>Onboarding |
| 651 | Product<br>Onboarding<br>Support | Product Onboarding Support<br>provides product<br>onboarding, updating, and<br>decommissioning. | Business<br>Partner<br>Product<br>Specification<br>and Offering<br>Management | Business Partner<br>Product<br>Specification and<br>Offering<br>Onboarding |
| 662 | Sourcing<br>Reference Data<br>Collection | Sourcing Reference Data<br>Collection collects definition<br>of products and services,<br>pricing schemes, partner<br>entities and contracts into the<br>system. Easy uploading of<br>reference data from external<br>sources such as XML files. | Business<br>Partner<br>Product<br>Specification<br>and Offering<br>Management | Business Partner<br>Product<br>Specification and<br>Offering Onboarding |
| 721 | Customer Order<br>Rules<br>Configuration | Customer Order Rules<br>Configuration function<br>provides in addition to the<br>Product rules, rules like<br>cross/up sell rules,<br>compatibility rules, eligibility<br>rules, address/service<br>availability rules, etc. Some<br>specific types of rules must be<br>available for all decision-<br>based actions on customer<br>orders. These rules could be:<br>customer fraud check,<br>decomposition rules, priority<br>rules, order duplication<br>prevention rules, complex<br>rules involving multi-system<br>checks, etc. | Product<br>Specification<br>& Offering<br>Management | Ordering Rules<br>Development |
| 722 | Order Rules<br>Retrieval | Order Rules Retrieval function<br>makes the Order Rules<br>available to e.g. customer<br>order related applications. | Product<br>Specification<br>& Offering<br>Management | Ordering Rules<br>Development |
| 897 | Building Access<br>Control | Building Access Control<br>checks, stops or allow<br>physical access to facilities<br>according to access roles and<br>rules. | Identification<br>and<br>Permission<br>Management | Permission Control |
| 900 | Authorization<br>Control<br>Management | Authorization Control Function<br>controls permissions<br>according to roles and related<br>rules. | Identification<br>and<br>Permission<br>Management | Permission Control |
| 1050 | Product<br>Onboarding<br>Management | Product Onboarding<br>Management function<br>supports the management of<br>the onboarding of a Product<br>Offering sourced from an<br>external source e.g. a business<br>partner. | Business<br>Partner<br>Product<br>Specification<br>and Offering<br>Management | Business Partner<br>Product<br>Specification and<br>Offering Onboarding |
| 1053 | Onboarded<br>Product<br>Workflows<br>Definition | Onboarded Product Workflows<br>Definition function identifies<br>appropriate workflows related<br>to the use of the onboarded<br>product in fulfillment,<br>assurance and billing. | Business<br>Partner<br>Product<br>Specification<br>and Offering<br>Management | Business Partner<br>Product<br>Specification and<br>Offering Onboarding |
| 1076 | Product<br>Specification<br>Design | Product Specification Design<br>Function provides the means<br>to describe for every product<br>commercialized through one<br>or several offers:<br>• characteristics of the<br>product, and their possible<br>values (ex: speed, volume,<br>duration, phone number, …)<br>• available operations (ex:<br>create, change of speed)<br>• functional incompatibilities<br>or prerequisites (deducted<br>from CFS specification<br>incompatibilities or pre-<br>requisites)<br>• link with the know-how type<br>(CFS specification) from which<br>the intangible product is a<br>restriction (ex: mobile line,<br>VOIP, …), or directly with the<br>resource type for tangible<br>products (ex: smartphone, SIM<br>Card), or to the Supplier<br>product type in case of<br>purchase products.<br>It includes facilities to design a<br>new Product Specification<br>based on an existing one and<br>integrity rules controls.<br>The Product Catalogue<br>describes, according to<br>strategy, all the tangible and<br>intangible products that can be<br>commercialized through<br>standard offers, loyalty offers.<br>Example:<br>• goodies can be sold or<br>offered as a reward in<br>exchange for fidelity points<br>(same product<br>commercialized through 2<br>offers)<br>• a special discount can be<br>granted through a retention<br>offer<br>• …<br>A Product Specification<br>restricts a Customer Facing<br>Service Specification<br>(CFSSpec). | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 1077 | Product Offering<br>Design | Product Offering Design<br>function provides the means to<br>describe Product Offering,<br>according to marketing<br>strategy:<br>• commercial name<br>• packaging rules of the<br>contract: mandatory offers,<br>optional offers, offers that can<br>be ordered in number (ex: 1 to<br>4 mobile lines)<br>• commercial incompatibilities<br>or prerequisites (ex: necessary<br>to be the holder of a X contract<br>to subscribe Y contract)<br>• available commercial<br>operations (ex: contract<br>migration)<br>• available commitment<br>durations<br>• any commercial criteria such<br>as authorized sales channel or<br>geographic area, customer<br>criteria, …<br>• tariff specifications – and<br>possible alterations. They are<br>associated with the offer, to<br>commercial operations or<br>usage types and can be<br>recurring or one shot. They are<br>expressed as rules that can<br>consider many criteria (ex:<br>commitment duration, product<br>configuration, sales channel,<br>customer’s age, …) and will be<br>evaluated during the order<br>capture process, or during the<br>rating process for usage.<br>It includes facilities to design a<br>new Product Offering based on<br>an existing one and integrity<br>rules controls. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 1078 | Product<br>Specification and<br>Offering Change<br>Auditing | Product Specification and<br>Offering Change Auditing<br>manages the implications of<br>Product Specifications and<br>Offerings changes to<br>determine the consequences<br>of any given change. Product<br>Specifications and Offerings<br>changes may impact other<br>Product Specifications and / or<br>Offerings according to<br>relationships between them.<br>The function logs Product<br>Specifications changes and<br>supports the analysis of<br>relationships between Product<br>Specifications.<br>In addition, it tracks the history<br>of changes in an easy and<br>accessible manner. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 1079 | Product<br>Specification and<br>Offering<br>Repository<br>Management | Product Specification and<br>Offering Repository<br>Management is able to create,<br>modify and delete Product<br>Specification and Offering.<br>This includes the ability to<br>manage the state of an entity<br>during its lifecycle (e.g.<br>planned, deployed, in<br>operation, replaced by,<br>locked…).<br>It includes Product<br>Specifications and Offerings<br>retrieval, integrity rules check<br>and versioning management.<br>It also provides Product<br>Specification and Offering<br>views adapted to the different<br>roles. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 1291 | External<br>Product<br>Specification<br>Development | External Product<br>Specification<br>Development function<br>supports the definition of,<br>and sometimes<br>development related to,<br>Product Specifications to<br>be provided either by a<br>Business Partner via the<br>Service Provider or<br>provided with the Business<br>Partner in conjunction with<br>the Service Provider.<br>This function differs from<br>internal Product<br>Specification<br>Development in that this<br>function addresses both<br>the collaborative aspects<br>of inter-company product<br>specification development<br>and the divisions of<br>responsibilities, costs and<br>benefits among the<br>partners.<br>This function provides the<br>means to describe for<br>every product<br>commercialized through<br>one or several offers:<br>- characteristics of the<br>product, and their possible<br>values (ex: speed, volume,<br>duration, phone number,<br>etc.)<br>available operations (ex:<br>create, change of speed)<br>- functional<br>incompatibilities or<br>prerequisites (deducted<br>from CFS specification<br>incompatibilities or pre-<br>requisites)<br>- link with the know-how<br>type (CFS specification)<br>from which the intangible<br>product is a restriction (ex:<br>mobile line, VOIP, etc.), or<br>directly with the resource<br>type for tangible products<br>(ex: smartphone, SIM<br>Card), or to the Supplier<br>product type in case of<br>purchase products.<br>It includes facilities to<br>design a new Product<br>Specification based on an<br>existing one and integrity<br>rules controls.<br>A Product Specification<br>restricts a Customer<br>Facing Service<br>Specification (CFSSpec). | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 1292 | External<br>Product Offering<br>Development | External Product Offering<br>Development function<br>includes the definition of,<br>and sometimes the<br>creation of, Product<br>Offerings provided either<br>by a Business Partner via<br>the Service Provider or<br>provided with the Business<br>Partner in conjunction with<br>the Service Provider.<br>This function differs from<br>internal Product Offering<br>Development in that this<br>function addresses both<br>the collaborative aspects<br>of inter-company product<br>Offering development and<br>the divisions of<br>responsibilities, costs and<br>benefits among the<br>partners.<br>This function provides the<br>means to describe Product<br>Offerings, according to<br>marketing strategy:<br>- commercial name<br>- packaging rules of the<br>contract: mandatory<br>offers, optional offers,<br>offers that can be ordered<br>in number (ex: 1 to 4<br>mobile lines)<br>- commercial<br>incompatibilities or<br>prerequisites (ex:<br>necessary to be the holder<br>of an X contract to<br>subscribe Y contract)<br>- available commercial<br>operations (ex: contract<br>migration)<br>- available commitment<br>durations<br>- any commercial criteria<br>such as authorized sales<br>channel or geographic<br>area, customer criteria,<br>etc.<br>- tariff specifications and<br>possible alterations. They<br>are associated to the offer,<br>to commercial operations<br>or usage types and can be<br>recurring or one shot. They<br>are expressed as rules that<br>can consider many criteria<br>(ex: commitment duration,<br>product configuration,<br>sales channel, customer's<br>age, etc.) and will be<br>evaluated during the order<br>capture process, or during<br>the rating process for<br>usage.<br>It includes facilities to<br>design<br>a new Product Offering<br>based on an existing one<br>and integrity rules<br>controls. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Development |
| 1293 | Product<br>Specification<br>Recalls Support | Product Specification<br>Recalls Support function<br>supports carrying out follow-<br>through with Service Provider<br>or Business Partner Product<br>Specification Recalls,<br>including notifying<br>customers and, where<br>appropriate, coordinating<br>returns and replacement<br>logistics. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification<br>Lifecycle<br>Management |
| 1341 | Product<br>Specification<br>Change<br>Notification | Product Specification<br>Change Notification function<br>enables notifying systems,<br>stakeholders and involved<br>business partners that a new<br>product specification change<br>is pending. This function is<br>ideally automated but can be<br>a manual notification to<br>those systems and<br>processes that require<br>manual intervention to make<br>a product specification<br>change. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification &<br>Offering<br>Realization |
| 1342 | Product<br>Specification<br>Version Control | Product Specification<br>Version Control function<br>facilitates multiple iterations<br>(versions) of product<br>specifications being kept in<br>production to avoid<br>inconveniencing existing<br>customers of the previous<br>versions. | Product<br>Specification<br>& Offering<br>Management | Product<br>Specification<br>Lifecycle<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF620 | Product Catalog<br>Management API | 4 | Mandatory | catalog: POST, PATCH, GET,<br>GET /id, DELETE<br>category: POST, PATCH, GET,<br>GET /id, DELETE<br>productSpecification: POST,<br>PATCH, GET, GET /id, DELETE<br>productOffering: POST,<br>PATCH, GET, GET /id, DELETE<br>productOfferingPrice: POST,<br>PATCH, GET, GET /id, DELETE<br>exportJob: POST, GET, GET /id,<br>DELETE<br>importJob: POST, GET, GET /id,<br>DELETE |
| TMF671 | Promotion | 4 | Optional | promotion: POST, PATCH, GET,<br>GET /id, DELETE |
| TMF688 | Event | 4.0.0 | Optional | listener: POST<br>hub: POST, DELETE |
| TMF701 | Process Flow | 4 | Optional | processFlow: POST, GET, GET<br>/id, DELETE<br>taskflow: PATCH, GET, GET /id |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF632 | Party Management | 4 | Optional | individual: GET, GET /id |
| TMF632 | Party Management | 4 | Optional | individual: GET, GET /id<br>organisation: GET, GET /id |
| TMF669 | Party Role<br>Management | 4 | Optional | partyRole: GET, GET /id |
| TMF633 | Service Catalog<br>Management | 4 | Optional | serviceSpecification: GET,<br>GET /id |
| TMF634 | Resource Catalog<br>Management | 4 | Optional | resourceSpecification:<br>GET, GET /id |
| TMF651 | Agreement<br>Management | 4 | Optional | agreement: GET, GET /id<br>agreementSpecification:<br>GET, GET /id |
| TMF673 | Geographic Address | 4 | Optional | geographicAddress: GET,<br>GET /id |
| TMF674 | Geographic Site | 4 | Optional | geographicSite: GET, GET<br>/id |
| TMF675 | Geographic Location | 4 | Optional | geographicLocation: GET,<br>GET /id |
| TMF688 | Event | 4.0.0 | Optional | event: GET, GET /id |
| TMF672 | UserRolesPermissions | 4.0.0 | Optional | permission: GET, GET /id |
| TMF620 | Product Catalog<br>Management | 4 | Optional | catalog: POST, PATCH,<br>GET, GET /id, DELETE<br>category: POST, PATCH,<br>GET, GET /id, DELETE<br>productSpecification:<br>POST, PATCH, GET, GET<br>/id, DELETE<br>productOffering: POST,<br>PATCH, GET, GET /id,<br>DELETE<br>productOfferingPrice:<br>POST, PATCH, GET, GET<br>/id, DELETE<br>exportJob: POST, GET, GET<br>/id, DELETE<br>importJob: POST, GET,<br>GET /id, DELETE |

## 3.3. Events

The following diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component.

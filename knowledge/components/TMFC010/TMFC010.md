---
id: TMFC010
type: component
name: Resource Catalog Management
version: 1.3.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC010_Resource_Catalog_Management_v1.3.1.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 8e24251ffcf9b3546e5a0487450c24b32526d3aa1fbb291e73dfe869f8154f10
  raw_path: references/components/TMFC010/TMFC010_Resource_Catalog_Management_v1.3.1.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF662
      name: entity-catalog-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS004
      name: Order Delivery – Fiber contract
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
yaml_spec_version: 1.3.2
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Resource<br>Catalog<br>Management | TMFC010 | The Resource Catalog Management component is<br>responsible for organizing the collection of resource<br>specifications that identify and define all<br>requirements for a resource. The Resource Catalog<br>Management component has the functionality that<br>enables presentation of a customer-facing view, so<br>users are able to browse and select resources they<br>need, as well as a technical view to enable definition<br>and setup of resources contained in the resource<br>catalog. Additional functionalities include capturing<br>new resource specifications, managing resources<br>(registering assets and components and identifying<br>and mapping connections / relationships),<br>administering the lifecycle of resources, describing<br>relationships between resources, reporting on<br>resources and changes to their attributes, and<br>facilitating easy access to identify and assign<br>resources. | Production |

![](media/resource-catalog-management-architecture.png)
*([PlantUML source](media/resource-catalog-management-architecture.puml))*

# 2. eTOM Processes, SID

Data Entities and Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.5.15 | L2 | Resource Catalog<br>Lifecycle<br>Management | Catalog Lifecycle Management business process<br>covers a set of business activities that enable<br>manage the lifecycle of an organizations catalog<br>from design to build according to defined<br>requirements.<br>Catalog Lifecycle Management proves the<br>overarching governance to manage all the stages in<br>the realization and operationalization of the<br>Product/Service/Resource Catalog in support of the<br>organizations business goals. |
| 1.5.16 | L2 | Resource Catalog<br>Operational<br>Readiness<br>Management | Resource Catalog Operational Readiness<br>Management business process establishes and<br>administers the support needed to operationalize<br>Resource catalogs for ongoing day-to-day business<br>needs.<br>These business activities implement the Resource<br>Catalog through Release and Deploy business<br>activities. |
| 1.5.17 | L2 | Resource Catalog<br>Content<br>Management | Resource Catalog Content Management business<br>process define and provide the business activities<br>that support the day-to-day operations of Resource<br>Catalogs in order to realize the business operations<br>goals.<br>Resource Catalog Content Management business<br>processes include administering the Resource<br>Catalog instance in production, maintaining catalog<br>entries, assuring catalogs, managing catalog<br>access, managing entry lifecycle through versioning,<br>handling catalog entity entry and changes,<br>supporting distribution of catalogs as needed, and<br>supporting user-facing activities. |
| 1.5.18 | L2 | Resource Catalog<br>Planning<br>Management | Resource Catalog Planning Management business<br>process covers a set of business activities that<br>understand and enable establish the plan to define,<br>design and operationalize a catalog in order to meet<br>the needs and objectives of Resource cataloging.<br>The Resource Catalog Planning Management<br>business process ensure that the organization is<br>able to identify the most appropriate scheme and<br>goal for it catalog. It includes designing the Catalog<br>plan and developing the specification according to<br>Resource management requirement. |
| 1.5.19 | L2 | Resource<br>Specification<br>Management | Resource Specification Management business<br>process leverages captured resource requirements<br>to develop, master, analyze, and update<br>documented standard conditions that must be<br>satisfied by a resource design and/or delivery.<br>Resource Specifications Management can result in<br>establishing in a centralized way, technical (know-<br>how) standards. Such standards provide the<br>organization with a means to control and approve<br>the values and inputs of specification through<br>structure, review, approval and distribution<br>processes to stakeholders and suppliers. |
| 1.5.3 | L2 | Resource<br>Specification<br>Development &<br>Retirement | Resource Specification Development & Retirement<br>processes develop new, or enhance existing<br>technologies and associated resource types, so that<br>new Products are available to be sold to customers.<br>They use the capability definition or requirements<br>defined by Resource Strategy & Planning They also<br>decide whether to acquire resources from outside,<br>taking into account the overall business policy in<br>that respect. These processes also retire or remove<br>technology and associated resource types, which<br>are no longer required by the enterprise.<br>Resource types may be built, or in some cases<br>leased from other parties. To ensure the most<br>efficient and effective solution can be used,<br>negotiations on network level agreements with other<br>parties are paramount for both building and leasing.<br>These processes interact strongly with Product and<br>Engaged Party Development processes. |
| 1.5.3.4 | L3 | Develop Detailed<br>Resource<br>Specifications | The Develop Detailed Resource Specifications<br>processes develop and document the detailed<br>resource-related technical, performance and<br>operational specifications, and manuals. These<br>processes develop and document the required<br>resource features, the specific technology<br>requirements and selections, the specific<br>operational, performance and quality requirements<br>and support activities, any resource specific data<br>required for the systems and network infrastructure.<br>The Develop Detailed Resource Specifications<br>processes provide input to these specifications. The<br>processes ensure that all detailed specifications are<br>produced and appropriately documented.<br>Additionally, the processes ensure that the<br>documentation is captured in an appropriate<br>enterprise repository. |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Resource Specification ABE |   |
| Resource Performance ABE | Resource Performance Specification BE |
| Resource Usage ABE | ResourceUsageSpec BE |
| Resource Configuration ABE | ResourceConfigSpec BE |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-resource-catalog-links.png)
*([PlantUML source](media/etom-sid-resource-catalog-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 737 | Resource Capability<br>Specification<br>Management | This function involves the<br>creation, editing, storage and<br>retrieval of capability<br>specifications. The capability<br>specifications represent the<br>general, common, and<br>invariant characteristics of<br>resource that may be realized<br>in more than one type of<br>specific resource. Examples of<br>capability are Layer2, Data,<br>radio, and Transport. | Resource<br>Capability<br>Management | Resource<br>Specification<br>Capability<br>Development |
| 467 | Resource Data<br>Transformation /<br>Parsing Rules<br>Configuration | Resource Data<br>Transformation/Parsing Rules<br>Configuration provides tools to<br>set up and maintain resource<br>data parsing rules | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 951 | Resource Catalog<br>Entities Management | Resource Catalog Entities<br>Management identifies<br>resource entities in a common<br>Catalog Management from the<br>Common Domain, or identifies<br>a specific instance of a<br>Catalog Management for<br>resource entities | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 996 | Resource Task Item<br>Policy Control<br>Configuration | Defines and configures the<br>policies which will be<br>implemented during the<br>Resource task item lifecycle. | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 1083 | Resource<br>Specification<br>Repository<br>Management | Resource Specification<br>Repository Management is<br>able to create, modify and<br>delete Resource Specification.<br>This includes the ability to<br>manage the state of an entity<br>during its lifecycle (e.g.<br>planned, deployed, in<br>operation, replaced by locked).<br>It includes Resource<br>Specifications retrieval,<br>integrity rules check and<br>versioning management.<br>It also provides Product<br>Specification and Offering<br>views adapted to the different<br>roles. | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 1088 | Resource<br>Specification to<br>Supplier Product<br>Specification<br>Relationship Design | Resource Specification to<br>Supplier Product Specification<br>Relationship Design identifies,<br>when it corresponds to<br>equipment rented to a<br>Supplier (devices, network<br>equipments, hardware<br>& software, etc). | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 1089 | Resource<br>Specification Action<br>Skill Design | Resource Specification Action<br>Skill Design manages the links<br>to the Skill catalog to identify<br>for each type of resource, or of<br>Action on a resource, which<br>type of skill is necessary to<br>make the intervention. | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 1082 | Resource<br>Specification Change<br>Auditing | Resource Specification<br>Change Auditing manages the<br>implications of Resource<br>Specifications changes to<br>determine the consequences<br>of any given change. Resource<br>Specifications changes may<br>impact other Resource<br>Specifications and Resource<br>Facing Service Specit supports<br>The function logs Resource<br>Specifications changes and<br>supports the analysis of<br>relationships between<br>Resource Specifications.<br>In addition, it tracks the history<br>of changes in an easy and<br>accessible manner. | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 1064 | Logical and Software<br>Resources Designing | Logical and Software<br>Resources Designing supports<br>physical, logical, and software<br>design of resources including<br>definition of configuration<br>variables and initial<br>parameters. | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |
| 1087 | Resource<br>Specification Design | Resource Specification Design<br>manages Resource<br>Specifications including<br>constraints, characteristics,<br>and type of usages.<br>It specifies Physical, Logical<br>and Compound Resource<br>Specifications.<br>It includes resource types that<br>as a Service Provider we don't<br>own or commercialize (ex:<br>mobile phones used by our<br>customers). | Resource<br>Specification<br>Management | Resource<br>Specification<br>Development |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF634 | Resource<br>Catalog<br>Management | 4 | Mandatory | resourceCatalog: POST, PATCH, GET,<br>GET /id, DELETE<br>resourceCategory: POST, PATCH, GET,<br>GET /id, DELETE<br>resourceSpecification: POST, PATCH,<br>GET, GET /id, DELETE<br>resourceCandidate: POST, PATCH, GET,<br>GET /id, DELETE<br>exportJob: POST, GET, GET /id, DELETE<br>importJob: POST, GET, GET /id, DELETE |
| TMF701 | Process Flow<br>Management | 4 | Optional | processFlow: POST, GET, GET /id,<br>DELETEtaskflow: PATCH, GET, GET /id |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation potentially used by the resource catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF634 | Resource<br>Catalog<br>Management | 4 | Optional | resourceCatalog: GET, GET /id<br>resourceCategory: POST,<br>PATCH, GET, GET /id, DELETE<br>resourceSpecification: POST,<br>PATCH, GET, GET /id, DELETE<br>resourceCandidate: POST,<br>PATCH, GET, GET /id, DELETE<br>exportJob: POST, GET, DELETE<br>importJob: POST, GET, DELETE |
| TMF669 | Party Role<br>Management | 4 | Optional | partyRole: GET, GET /id |
| TMF632 | Party | 4 | Optional | individual: GET, GET /id<br>organization: GET, GET /id |
| TMF662 | Entity Catalog<br>Management | 4 | Optional | entitySpecification: GET, GET<br>/id<br>associationSpecififaction: GET,<br>GET /id |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable

Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component.

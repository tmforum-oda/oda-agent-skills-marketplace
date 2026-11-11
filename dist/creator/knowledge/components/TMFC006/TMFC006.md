---
id: TMFC006
type: component
name: Service Catalog Management
version: 1.2.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC006_Service_Catalog_Management_v1.2.1.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: f56efa8d80f4af5dd0a71db8901fed6f026c4181f971485850d24e14709f12bd
  raw_path: references/components/TMFC006/TMFC006_Service_Catalog_Management_v1.2.1.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF633
      name: service-catalog-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF657
      name: service-quality-management-api
    - id: TMF662
      name: entity-catalog-management-api
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
    - id: TMFS021
      name: Orchestration of a Multi Party, Multi domain Sales Order
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.2.0
---

# 2. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Service<br>Catalog<br>Management | TMFC006 | The Service Catalog Management<br>component is responsible for organizing the<br>collection of service specifications that<br>identify and define all requirements of a<br>service that can be performed. This<br>component has the functionality that<br>enables presentation of a customer-facing<br>view so users are able to search and select<br>services they need, as well as a technical<br>view to enable definition and setup of what<br>is needed to deliver service specifications<br>(Customer Facing Service Specifications<br>(CFSSs) and Resource Facing Service<br>Specifications (RFSSs)) contained in the<br>service catalog. The Service Catalog<br>Management component has functionalities<br>that include creation of new service<br>specifications, managing service<br>specifications, administering the lifecycle of<br>services, describing relationships between<br>service specification attributes, reporting on<br>service specifications and their changes,<br>and facilitating easy and systematic<br>indexing and access to services, as well as<br>facilitating automation of the service<br>delivery process. | Production |

![](media/service-catalog-management-architecture.png)
*([PlantUML source](media/service-catalog-management-architecture.puml))*

# 3. eTOM Processes, SID

Data Entities and Functional Framework Functions

## 3.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.4.13 | L2 | Service Catalog<br>Lifecycle<br>Management | Catalog Lifecycle Management business<br>process covers a set of business activities that<br>enable manage the lifecycle of an organizations<br>catalog from design to build according to<br>defined requirements. |
| 1.4.14 | L2 | Service Catalog<br>Operational<br>Readiness<br>Management | Service Catalog Operational Readiness<br>Management business process establishes and<br>administers the support needed to<br>operationalize Service catalogs for ongoing day-<br>to-day business needs. |
| 1.4.15 | L2 | Service Catalog<br>Content<br>Management | Service Catalog Content Management business<br>process define and provide the business<br>activities that support the day-to-day<br>operations of Service Catalogs in order to<br>realize the business operations goals. |
| 1.4.16 | L2 | Service Catalog<br>Planning<br>Management | Service Catalog Planning Management business<br>process covers a set of business activities that<br>understand and enable establish the plan to<br>define, design and operationalize a catalog in<br>order to meet the needs and objectives of<br>Service cataloging.<br>The Service Catalog Planning Management<br>business process ensure that the organization<br>is able to identify the most appropriate scheme<br>and goal for it catalog. It includes designing the<br>Catalog plan and developing the specification<br>according to Service management requirement. |
| 1.4.19 | L2 | Service<br>Specification<br>Management | Service Specification Management business<br>process leverages captured service<br>requirements to develop, master, analyze, and<br>update documented standard conditions that<br>must be satisfied by service design and/or<br>delivery.<br>Service Specifications Management can result<br>in establishing, in a centralized way, technical<br>(know-how) standards.<br>Such standards provide the organization with a<br>means to control and approve the values and<br>inputs of service specification through<br>structure, review, approval and distribution<br>processes to stakeholders and suppliers. |
| 1.4.3 | L2 | Service<br>Specification<br>Development &<br>Retirement | Service Specification Development &<br>Retirement processes are project oriented in<br>that they develop and deliver new or enhanced<br>service types. These processes include process<br>and procedure implementation, systems<br>changes and customer documentation. They<br>also undertake rollout and testing of the service<br>type, capacity management and costing of the<br>service type. It ensures the ability of the<br>enterprise to deliver service types according to<br>requirements. |
| 1.4.3.4 | L3 | Develop Detailed<br>Service<br>Specifications | The Develop Detailed Service Specifications<br>processes develop and document the detailed<br>service-related technical and operational<br>specifications, and customer manuals. These<br>processes develop and document the required<br>service features, the specific underpinning<br>resource requirements and selections, the<br>specific operational, and quality requirements<br>and support activities, any service specific data<br>required for the systems and network<br>infrastructure as agreed through the Develop<br>New Service Business Proposal processes. The<br>Develop Detailed Product Specifications<br>processes provide input to these specifications.<br>The processes ensure that all detailed<br>specifications are produced and appropriately<br>documented. Additionally, the processes<br>ensure that the documentation is captured in an<br>appropriate enterprise repository. |

## 3.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Service Specification ABE |   |
| Service Performance ABE | Service Level Spec ABE |
| Service Performance ABE | Service Performance Specification ABE |
| Service Usage ABE | ServiceUsageSpec BE |
| Service Configuration ABE | ServiceConfigSpec BE |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 3.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.:

![](media/etom-sid-service-catalog-links.png)
*([PlantUML source](media/etom-sid-service-catalog-links.puml))*

## 3.4. Functional Framework Functions

Please note, these Functions were changed in GB1033, but ISA-996 - Master Data Management has repurposed catalog related functions : Has been raised to review this. Functional Framework 23.5 mapping draft:

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 897 | Building<br>Access<br>Control | Building Access Control<br>checks, stops or allow<br>physical access to facilities<br>according to access roles and<br>rules. | Identification<br>and Permission<br>Management | Permission<br>Control |
| 900 | Authorization<br>Control<br>Management | Authorization Control<br>Function controls<br>permissions according to<br>roles and related rules.<br>It consists in evaluating if a<br>requester is granted the<br>permission to act by providing<br>the required evidence. The<br>evidence corresponds to the<br>condition specified for each<br>right (for instance keying the<br>correct password to use a<br>specific mailbox). If the<br>action is protected via a right<br>which is assigned (possibly<br>via a role) to a person then<br>the person has to be<br>identified to retrieve their<br>rights and verify if the request<br>to act can be granted. | Identification<br>and Permission<br>Management | Permission<br>Control |
| 995 | Service Task<br>Item Policy<br>Control<br>Configuration | Define and configure the<br>policies which will be<br>implemented during the<br>Service task item lifecycle. | Service<br>Specification<br>Development | Service<br>Specification<br>Design |
| 1080 | Service<br>Specification<br>Change<br>Auditing | Service Specification Change<br>Auditing manages the<br>implications of Service<br>Specifications changes to<br>determine the consequences<br>of any given change.<br>Customer Facing Service<br>Specifications (CFSSpec)<br>changes may impact other<br>CFSSpec according to<br>relationships and also<br>Product Specification that<br>restrict it. Resources Facing<br>Service Specification<br>(RFSSpec) may impact other<br>RFSSpecs according to<br>relationships and / or<br>CFSSpecs it realizes.<br>The function logs Service<br>Specifications changes and<br>supports the analysis of<br>relationships between<br>Service Specifications.<br>In addition, it tracks the<br>history of changes in an easy<br>and accessible manner. | Service<br>Specification<br>Development | Service<br>Specification<br>Design |
| 1081 | Service<br>Specification<br>Repository<br>Management | Service Specification<br>Repository Management is<br>able to create, modify and<br>delete Service Specification<br>and related entities such as<br>Service Usage Specification.<br>This includes the ability to<br>manage the state of an entity<br>during its lifecycle (e.g.<br>planned, deployed, in<br>operation, replaced by,<br>locked).<br>It includes Service<br>Specifications retrieval,<br>integrity rules check and<br>versioning management.<br>It also provides Product<br>Specification and Offering<br>views adapted to the different<br>roles. | Service<br>Specification<br>Development | Service<br>Specification<br>Design |
| 1084 | Know-How<br>Specification<br>Design | Know-How Specification<br>Design provides the means to<br>describe the Customer<br>Facing Service Specifications<br>including constraints,<br>characteristics and types of<br>usages.<br>It also identifies Technical<br>Solutions usable for the<br>Know-How and rules to find<br>the Technical Solution. | Service<br>Specification<br>Development | Service<br>Specification<br>Design |
| 1085 | Technical<br>Solution<br>Design | Technical Solution Design<br>provides the means to<br>describe Resource Facing<br>Service Specifications (a.k.a.<br>RFSSpec) including<br>constraints, characteristics<br>and types of usages.<br>It also identifies Resource<br>Specifications used for each<br>Technical Solution<br>Specification (a.k.a.<br>RFSSpec). | Service<br>Specification<br>Development | Service<br>Specification<br>Design |
| 1086 | Service<br>Specification<br>to Supplier<br>Product<br>Specification<br>Relationship<br>Design | Service Specification to<br>Supplier Product<br>Specification Relationship<br>Design identifies, when know-<br>how, technical solutions or<br>part of it are not realized by<br>the CSP, the Supplier Product<br>Specification used to<br>implement and<br>corresponding rules. | Service<br>Specification<br>Development | Service<br>Specification<br>Design |
| 1135 | Technical<br>Solution<br>Policy Design | The Technical Solution Policy<br>Management Function<br>enables to define, and to<br>check consistency of,<br>potentially complex rules to<br>automate the choice of the<br>technical solution (CFS Spec)<br>for a know-how (RFS Spec) or<br>parts of the technical<br>solution.<br>Criteria can be of various<br>nature and combined:<br>• geographical<br>• depending on the chosen<br>characteristics values of<br>the know-how<br>• depending on other<br>products / know-hows of<br>the customer installed or<br>ordered<br>• depending on the current<br>state of Service Platforms,<br>Network equipment<br>(occupation rate, load<br>balancing, etc.)<br>• depending on<br>Supplier/Partner contracts<br>(volume discounts, etc.)<br>• Etc. | Service<br>Specification<br>Development | Technical<br>Solution Policy<br>Management |

# 4. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 4: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 4.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operation |
| --- | --- | --- | --- | --- | --- |
| TMF633 | Service<br>Catalog<br>Management | 4 | Mandatory | catalog | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF633 | Service<br>Catalog<br>Management | 4 | Mandatory | category | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF633 | Service<br>Catalog<br>Management | 4 | Mandatory | serviceSpecification | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF633 | Service<br>Catalog<br>Management | 4 | Mandatory | serviceCandidate | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF633 | Service<br>Catalog<br>Management | 4 | Mandatory | exportJob | GET<br>GET /ID<br>POST<br>DELETE |
| TMF633 | Service<br>Catalog<br>Management | 4 | Mandatory | importJob | GET<br>GET /ID<br>POST<br>DELETE |
| TMF657 | Service<br>Quality<br>Management | 4 | Mandatory | serviceLevelSpecification | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF657 | Service<br>Quality<br>Management | 4 | Mandatory | serviceLevelObjective | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF657 | Service<br>Quality<br>Management | 4 | Mandatory | serviceLevelSpecParamete<br>r | GET<br>GET /ID<br>POST<br>PATCH<br>DELETE |
| TMF701 | Process Flow<br>Management | 4 | Optional | processFlow | GET<br>GET /ID<br>POST<br>DELETE |
| TMF701 | Process Flow<br>Management | 4 | Optional | taskFlow | GET<br>GET /ID<br>PATCH |
| TMF688 | Event<br>Management<br>API | 4 | Optional | listener | POST |
| TMF688 | Event<br>Management<br>API | 4 | Optional | hub | POST<br>DELETE |

## 4.2. Dependent APIs

Following diagram illustrates API/Resource/Operation potentially used by the service catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operation | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| TMF634 | Resource<br>Catalog<br>Management | 4 | Optional | resourceSpecificatio<br>n | GET<br>GET /ID | n/a |
| TMF669 | Party Role<br>Management | 4 | Optional | partyRole | GET<br>GET /ID | n/a |
| TMF632 | Party | 4 | Optional | induvidual | GET<br>GET /ID | n/a |
| TMF632 | Party | 4 | Optional | organization | GET<br>GET /ID | n/a |
| TMF662 | Entity Catalog<br>Management | 4 | Optional | entitySpecification | GET<br>GET /ID | n/a |
| TMF662 | Entity Catalog<br>Management | 4 | Optional | associationSpecificat<br>ion | GET<br>GET /ID | n/a |
| TMF672 | User Role<br>Permission | 4 | Optional | permission | GET<br>GET /ID | n/a |
| TMF688 | Event<br>Management<br>API | 4 | Optional | event | GET<br>GET /ID | n/a |

## 4.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

The type of event could be: • Create : a new resource has been created (following a POST). • Delete: an existing resource has been deleted. • AttributeValueChange or Change: an attribute from the resource has changed - event structure allows to pinpoint the attribute. • InformationRequired: an attribute should be valued for the resource preventing to follow nominal lifecycle - event structure allows to pinpoint the attribute. • StateChange: resource state has changed.

# 5. Machine Readable

Component Specification Refer to the ODA Component table for the machine-readable component specification file for this component.

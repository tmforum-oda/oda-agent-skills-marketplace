---
id: TMFC009
type: component
name: Service Qualification Management
version: 1.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC009_Service_Qualification_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: 7db9795c15e893d6078f26b56e16ed5838b4b07116c41eb51277c0f7b9e3847b
  raw_path: references/components/TMFC009/TMFC009_Service_Qualification_v1.1.0.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF633
      name: service-catalog-management-api
    - id: TMF634
      name: resource-catalog-management-api
    - id: TMF638
      name: service-inventory-management-api
    - id: TMF639
      name: resource-inventory-management-api
    - id: TMF645
      name: service-qualification-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
  use_cases:
    - id: TMFS002
      name: Browse B2C Catalogue and Check Fiber Technical Eligibility
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS004
      name: Order Delivery – Fiber contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS008
      name: Service and Resource Order Management for Postpaid Mobile Subscribers
    - id: TMFS010
      name: ODA Flow with NaaS Support
    - id: TMFS014
      name: 5G Slice Management
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS028
      name: End to End Modelling of Cloud Based VPN
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.1.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Service<br>Qualification | TMFC009 | Service Qualification component is responsible<br>for checking and validating the availability of a<br>service according to specified and configured<br>business rules. It must identify at least one<br>technical solution (RFSspec) available to deliver<br>the service (CFSspec) and check the availability<br>of all the resources types involved in this<br>technical solution. No resources are allocated<br>during Service Qualification.<br>Service Qualification component has functionality<br>that include checking service feasibility status<br>and publishing or reporting service qualification<br>result, but also calculated service delivery due<br>date and identified need of an appointment at the<br>customer site.<br>Service Qualification can also be in charge of the<br>cost calculation of the technical solution<br>identified, when it cannot be determined at<br>catalog design time (complex B2B services). This<br>information will be used as an input to price<br>calculation. | Production |

![](media/service-qualification-architecture.png)
*([PlantUML source](media/service-qualification-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.4.5 | L2 | Service<br>Configuration<br>& Activation | Service Configuration & Activation processes<br>encompass allocation, implementation, configuration,<br>activation and testing of specific services to meet<br>customer requirements, or in response to requests<br>from other processes to alleviate specific service<br>capacity shortfalls, availability concerns or failure<br>conditions. Where included in the service provider<br>offering, these processes extend to cover customer<br>premises equipment.<br>Responsibilities of the Service Configuration &<br>Activation processes include, but are not limited to:<br>• Verifying whether specific service designs<br>sought by customers are feasible as part of pre-<br>order feasibility checks;<br>• Allocating the appropriate specific service<br>parameters to support service orders or requests<br>from other processes;<br>• Reserving specific service parameters (if required<br>by the business rules) for a given period of time until<br>the initiating customer order is confirmed, or until the<br>reservation period expires (if applicable);<br>• Implementing, configuring and activating specific<br>services, as appropriate;<br>• Testing the specific services to ensure the service is<br>working correctly;<br>• Recovery of specific services;<br>• Updating of the Service Inventory Database to<br>reflect that the specific service has been allocated,<br>modified or recovered;<br>• Assigning and tracking service provisioning<br>activities;<br>• Managing service provisioning jeopardy conditions<br>• Reporting progress on service orders to other<br>processes. |
| ? | ? | ? | no L3 to cover standard availability/feasibility<br>checks |

Note: refer to JIRA section and the need to identify a new Service Availability Check/Assessment activity at Service level, as part of L2 Service Configuration & Activation Note: previously identified processes at Resource level didn't exist anymore in eTOM 23.5 and no equivalent has been found. A new Jira ticket is created.

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

Note: refer to JIRA section and the need to create a Service Qualification BE.

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-service-qualification-links.png)
*([PlantUML source](media/etom-sid-service-qualification-links.puml))*

## 2.4. Functional Framework Functions

Note: refer to JIRA section for improvement in classification and new function required.

| Function<br>ID | Function<br>Name | Function Description | Aggregate Functions Level 1 | Aggregate Functions Level 2 |
| --- | --- | --- | --- | --- |
| 319 | Service<br>Feasibility<br>Checking | Service Feasibility Checking<br>provides checking based on the<br>customer service location, service<br>feasibility checks are done to<br>assure the offering can actually be<br>provided to the customer. This<br>implies that the customer location<br>is clearly established. Service<br>feasibility checks are conducted<br>via contract with the Service Order<br>Management function. | Service<br>Order<br>Management | Service<br>Availability |
| 586 | Service<br>Availability<br>Validation | Service Availability Validation<br>function validates that the service<br>or services specified on the<br>service order are available at the<br>specified customer/service<br>location and feasible from a<br>network point of view. | Service<br>Order<br>Management | Service<br>Availability |
| 571 | Service<br>Delivery<br>Due Date<br>Calculation | Service Delivery Due Date<br>Calculation functions calculates<br>the service delivery due date<br>using network capacity, access<br>provider selection and work center<br>intelligence (including workload<br>and capacity). | Service<br>Order<br>Management | Service<br>Order<br>Initialization |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF645 | TMF645 Service<br>Qualification<br>Management | 4 | Mandatory | checkServiceQualification<br>• GET<br>• GET /ID<br>• POST<br>• PATCH<br>• DELETE |
| TMF645 | TMF645 Service<br>Qualification<br>Management | 4 | Mandatory | queryServiceQualification<br>• GET<br>• GET /ID<br>• POST<br>• PATCH<br>• DELETE |

## 3.2. Dependent APIs

The following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF639 | Resource Inventory<br>Management | 4 | Optional | resource<br>• GET<br>• GET/id |
| TMF669 | Party Role Management | 4 | Optional | partyRole<br>• GET<br>• GET/id |
| TMF632 | Party | 4 | Optional | individual/organization<br>• GET<br>• GET/id |
| TMF672 | User Roles And<br>Permissions | 4 | Optional | permission<br>• GET<br>• GET/id |
| TMF673 | Geographic Address<br>Management | 4 | Optional | geographicAddress<br>• GET<br>• GET/id |
| TMF673 | Geographic Address<br>Management | 4 | Optional | geographicSubAddress<br>• GET<br>• GET/id |
| TMF674 | Geographic Site<br>Management | 4 | Optional | geographicSite<br>• GET<br>• GET/id |
| TMF675 | Geographic Location | 4 | Optional | geographicLocation<br>• GET<br>• GET/id |
| TMF633 | Service Catalog<br>Management | 4 | Mandatory | serviceSpec<br>• GET<br>• GET/id |
| TMF633 | Service Catalog<br>Management | 4 | Mandatory | serviceCategory<br>• GET<br>• GET/id |
| TMF638 | Service Inventory<br>Management | 4 | Optional | service<br>• GET<br>• GET/id |
| TMF688 | Event Management | 4 | Optional | event<br>• GET<br>• GET/id |
| TMF634 | Resource Catalog<br>management | 4 | Optional | resourceSpecification<br>• GET<br>• GET/id |

## 3.3. Events

The following diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component Map on the TM Forum website for the machine- readable component specification files for this component. TM Forum - ODA Component Directory

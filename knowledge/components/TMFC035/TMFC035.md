---
id: TMFC035
type: component
name: Permissions Management
version: 1.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC035_Permissions_Management_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: 55767e30f6d6f60123d36d3985a090c91a5d575881c4977bcf3227b961b79d1d
  raw_path: references/components/TMFC035/TMFC035_Permissions_Management_v1.1.0.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF672
      name: user-role-permission-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS001
      name: New Party – Create your accounts
    - id: TMFS005
      name: Billing - Fiber Contract
    - id: TMFS006
      name: Legal Guardian
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
    - id: TMFS026
      name: Commercializing CAMARA APIs with Operate APIs
    - id: TMFS031
      name: Problem Management
yaml_spec_version: 1.1.1
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Party Roles &<br>Permissions<br>Management | TMFC035 | Party Roles & Permissions<br>Management component aims to<br>manage and expose roles and<br>related permissions.<br>Permissions Management<br>component allows to:<br>• create, modify, and delete<br>permissions.<br>• delegate permissions<br>When a specific role is assigned, a<br>set of permissions is inherited. | Party<br>Management |

![](media/permissions-management-architecture.png)
*([PlantUML source](media/permissions-management-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for.

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Party ABE | Permission Set Specification BE |
|   | Permission Set BE |
|   | Permission BE |
|   | Party Role BE |
|   | Party Roles Specification BE |
| Customer Party ABE |   |
| Business Partner Party Role |   |
| Enterprise Party Role |   |
| Market Sales Party Roles ABE |   |
| Service Party Roles ABE |   |
| Resource Party Roles ABE |   |

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-permission-role-links.png)
*([PlantUML source](media/etom-sid-permission-role-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function<br>Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 899 | Single Sign-<br>On Access<br>Control | Single Sign-On Access Control<br>grant access in cooperation<br>with central Authentication and<br>Authorization functions to<br>secure the most updated<br>security. | Identification<br>and<br>Permission<br>Management | Identification<br>and<br>Authentication |
| 906 | PKI and<br>Digital<br>Certificates<br>Systems<br>Integration | PKI and Digital Certificates<br>Systems Integration provides<br>integration to Public Key<br>Infrastructure Systems that<br>provides digital certificates, and<br>the support to use public keys<br>and digital certificates. | Identification<br>and<br>Permission<br>Management | Identification<br>and<br>Authentication |
| 1025 | Application<br>Access | Application Access provide<br>access interfaces with<br>authentication and<br>authorization control for the<br>requests and responses related<br>to the application’s<br>functionality, including event<br>logging and usage statistics. | Identification<br>and<br>Permission<br>Management | Identification<br>and<br>Authentication |
| 897 | Building<br>Access<br>Control | Building Access Control<br>checks, stops or allow physical<br>access to facilities according to<br>access roles and rules. | Identification<br>and<br>Permission<br>Management | Permission<br>Control |
| 900 | Authorization<br>Control<br>Management | Authorization Control<br>Management sets and<br>administrates the Role and<br>Rule based access to<br>functions. | Identification<br>and<br>Permission<br>Management | Permission<br>Control |
| 898 | Application<br>Security<br>Management | Application Security<br>Management administrates the<br>roles and rules that applies to<br>getting the right to use an<br>application. | Identification<br>and<br>Permission<br>Management | Permission<br>Definition |
| 260 | Anonymous<br>User Account<br>Creation | Anonymous User Account<br>Creation provides account<br>creation for anonymous user<br>account, either through external<br>customer self empowered<br>fulfillment function or internal<br>customer support access. | Identification<br>and<br>Permission<br>Management | Digital Identity<br>Management |
| 1181 | Party Role<br>Assignment | n/a | Identification<br>and<br>Permission<br>Management | Role and<br>Permission<br>Assignment /<br>Configuration |
| 1182 | Permission<br>Perimeter<br>Configuration | n/a | Identification<br>and<br>Permission<br>Management | Role and<br>Permission<br>Assignment /<br>Configuration |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations |
| --- | --- | --- | --- | --- |
| TMF672 | User Role<br>Permission<br>Management | 4 | Mandatory | GET Permission<br>(Permission,<br>UserRole)<br>GET/id Permission<br>POST Permission<br>PATCH Permission<br>DELETE Permission<br>GET UserRole<br>GET/id UserRole<br>POST UserRole<br>PATCH UserRole<br>DELETE UserRole |
| TMF669 | Party Role<br>Management | 4 | Mandatory | GET partyRole<br>GET/id partyRole<br>POST partyRole<br>PATCH partyRole<br>DELETE partyRole |
| TMF701 | Process Flow | 4 | Optional | n/a |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation potentially used by the product catalog component:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operations | Rationales |
| --- | --- | --- | --- | --- | --- |
| TMF632 | Party<br>Management | 4 | Mandatory | GET<br>induvidual /<br>organization<br>GET/ID<br>induvidual /<br>organization | All roles and<br>identities need<br>to be accosiated<br>with a valid and<br>current Party<br>data object. |
| TMF701 | Process Flow | 4 | Optional | na |   |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

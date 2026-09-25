---
id: TMFC020
type: component
name: Digital Identity Management
version: 1.1.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC020_Digital_Identity_Management_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: d4772360a6e2dc20d8a254714ff75b1ad8049d9fa522cf5e4317bf012b123896
  raw_path: references/components/TMFC020/TMFC020_Digital_Identity_Management_v1.1.0.pdf
links:
  apis:
    - id: TMF632
      name: party-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF701
      name: process-flow-management-api
    - id: TMF720
      name: digital-identity-management-api
  use_cases:
    - id: TMFS001
      name: New Party – Create your accounts
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS020
      name: Multi Domain B2B2X Contract Management
    - id: TMFS021
      name: Orchestration of a Multi Party, Multi domain Sales Order
yaml_spec_version: 1.1.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Digital Identity<br>Management | TMFC020 | The Digital Identity Management is<br>responsible for the parties<br>(customers, employees, partners)<br>and resources authentication. | Party<br>Management |

![](media/digital-identity-management-architecture.png)
*([PlantUML source](media/digital-identity-management-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| n/a | 2 | n/a | Note: create JIRA issue to eTOM team to<br>have process for Digital Identity Management |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
| --- | --- |
| Digital Identity | n/a |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-digital-identity-links.png)
*([PlantUML source](media/etom-sid-digital-identity-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Function<br>Name | Function Description | Sub-Domain Functions Level 1 | Sub-Domain Functions Level 2 |
| --- | --- | --- | --- | --- |
| 1025 | Application<br>Access | Application Access provide<br>access interfaces with<br>authentication and<br>authorization control for the<br>requests and responses<br>related to the application’s<br>functionality, including event<br>logging and usage statistics. | Identification<br>and<br>Permission<br>Management<br>Identification<br>and<br>Authentication | Identification<br>and<br>Authentication<br>Identification<br>and<br>Permissions |
| 906 | PKI and<br>Digital<br>Certificates<br>Systems<br>Integration | PKI and Digital Certificates<br>Systems Integration<br>provides integration to<br>Public Key Infrastructure<br>Systems that provides digital<br>certificates, and the support<br>to use public keys and<br>digital certificates. | Identification<br>and<br>Permission<br>Management<br>Identification<br>and<br>Authentication | Identification<br>and<br>Authentication<br>Identification<br>and<br>Permissions |
| 899 | Single Sign-<br>On Access<br>Control | Single Sign-On Access<br>Control grant access in<br>cooperation with central<br>Authentication and<br>Authorization functions to<br>secure the most updated<br>security. | Identification<br>and<br>Permission<br>Management<br>Identification<br>and<br>Authentication | Identification<br>and<br>Authentication<br>Identification<br>and<br>Permissions |
| 897 | Building<br>Access<br>Control | Building Access Control<br>checks, stops or allow<br>physical access to facilities<br>according to access roles<br>and rules. | Identification<br>and<br>Authentication | Permission<br>Control |
| 898 | Application<br>Security<br>Management | Application Security<br>Management administrates<br>the roles and rules that<br>applies to getting the right to<br>use an application. | Identification<br>and<br>Authentication | Permission<br>Definition |
| 1240 | Identity<br>Verification | Identity Verification (aka<br>authentication) establishes<br>that an actor (i.e., a person<br>or a resource) is who they<br>purport to be using one or<br>several credentials.<br>According to the reliability of<br>the credentials used the<br>authentication has a level of<br>authentication such as a<br>biometric credential (i.e.,<br>facial recognition or<br>fingerprint) or multi-factor<br>credential with a high level<br>of authentication or a<br>network credential with a<br>low level of authentication.<br>Note: each permission<br>specifies the minimum level<br>of authentication required. | Identification<br>and<br>Permission<br>Management | Identification<br>and<br>Authentication |
| 1247 | Credentials<br>Establishment | Credentials Establishment<br>creates and/or modifies<br>credentials and associates<br>them with the Digital Identity<br>that will be using them.<br>Credentials can include<br>username/passcode<br>combinations, biometrics,<br>and physical and/or logical<br>passkeys.<br>Note: A Digital Identity aims<br>to enable identifying Party,<br>Party Roles or Resource<br>Roles. | Identification<br>and<br>Permission<br>Management | Digital Identity<br>Management |
| 1248 | Credentials<br>Query | Credentials Query provides<br>the ability to retrieve non-<br>protected information about<br>the Digital Identity of<br>credentials or about the<br>credentials themselves<br>(e.g.name, photo, badge<br>number, token ID,<br>credentials valid dates, etc.). | Identification<br>and<br>Permission<br>Management | Digital Identity<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operations |
| --- | --- | --- | --- |
| TMF720 | Digital Identity | Mandatory | • GET<br>• GET/Id<br>• POST<br>• PATCH/id<br>• DELETE/id |
| TMF688 | Event Management | Optional | event<br>• GET<br>• GET/id |
| TMF701 | Process Flow Management | Optional | processFlow<br>• GET<br>• GET/id<br>• POST<br>• DELETE/id<br>taskFlow:<br>• GET<br>• GET/id<br>• PATCH/id |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | Mandatory / Optional | Operation |
| --- | --- | --- | --- |
| TMF632 | Party Management | Conditional Mandatory (if Party<br>Role is not provided) | individual<br>• GET<br>• GET/id<br>organization<br>• GET<br>• GET/id |
| TMF669 | Party Role<br>Management | Conditional Mandatory (if Party<br>Management is not provided) | partyRole<br>• POST |
| TMF701 | Process Flow<br>Management | Optional | processFlow<br>• POST<br>• GET<br>• GET/id<br>• DELETE<br>taskFlow<br>• PATCH<br>• GET<br>• GET/id |
| TMF688 | Event<br>Management | Optional | event<br>• GET<br>• GET/id |

## 3.3. Events

The diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component table for the machine-readable component specification file for this component.

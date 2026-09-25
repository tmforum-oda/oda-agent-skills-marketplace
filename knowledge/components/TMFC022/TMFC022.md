---
id: TMFC022
type: component
name: Party Privacy Management
version: 1.1.1
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC022_Party_Privacy_Management_v1.1.1.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: be087399b1ea5d2826dc909b578f81985062a780cedf1d682f4ef46942b20d10
  raw_path: references/components/TMFC022/TMFC022_Party_Privacy_Management_v1.1.1.pdf
links:
  apis:
    - id: TMF620
      name: product-catalog-management-api
    - id: TMF632
      name: party-management-api
    - id: TMF644
      name: privacy-management-api
    - id: TMF667
      name: document-management-api
    - id: TMF669
      name: party-role-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS001
      name: New Party – Create your accounts
yaml_spec_version: 1.1.0
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Party Privacy<br>Management | TMFC022 | The Party Privacy Management component<br>aims to<br>• define the Privacy Policy rules<br>established by the CSP, according to<br>applicable regulations, such as GDPR in<br>Europe,<br>• apply these rules to each Party<br>interacting with the CSP and to all of<br>their personal information and<br>personally identifiable information (PII),<br>according to the role(s) played by the<br>Party,<br>• register explicit opt-in and opt-out given<br>by Parties regarding the usage of some<br>of their personal information for<br>dedicated purpose, such as marketing. | Party<br>Management |

![](media/party-privacy-management-architecture.png)
*([PlantUML source](media/party-privacy-management-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
| --- | --- | --- | --- |
| 1.3.21 | L2 | Customer<br>Privacy<br>Management | Customer Privacy Management processes manage<br>the privacy requirements of customers in accordance<br>with customers' information privacy requirements, and<br>regulatory mandates. These processes help to:<br>• Define the Customer Privacy Management<br>scope,<br>• Define the information that constitutes<br>Personally Identifiable Information (personal<br>identifiable information) where Privacy Policy<br>applies,<br>• Define Default Privacy requirements for each<br>type of personal identifiable information,<br>• Capture Customers explicit consent and<br>define with Customers a Privacy Policy<br>according to their wishes and the processing<br>entities default Privacy Policy possible values,<br>• Modify/update Privacy Policy according to<br>future needs or requirements,<br>• Enforce the Customer Privacy Policy and<br>ensure that Customer information is managed<br>correctly according to stated privacy policies,<br>• Communicate relevant personal identifiable<br>information processing standards to third<br>parties with whom the information is shared. |
| 1.6.22 | L2 | Business<br>Partner Privacy<br>Management | Business Partner Privacy Management processes<br>manage the privacy requirements of business<br>partners in accordance with information privacy<br>requirements, and regulatory mandates. These<br>processes help to:<br>• Define the Business Partner Privacy<br>Management scope<br>• Define the information that constitutes<br>Personally Identifiable Information (personal<br>identifiable information) where Privacy Policy<br>applies.<br>• Define Default Privacy requirements for each<br>type of personal identifiable information<br>• Capture explicit consent and define with<br>Privacy Policy according to wishes of the<br>organization<br>• Modify/update Privacy Policy according to<br>future needs or requirements<br>• Enforce the Business Partner Privacy Policy<br>and ensure that information is managed<br>correctly according to stated privacy policies.<br>• Communicate relevant personal identifiable<br>information processing standards to third<br>parties with whom the information is shared |

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified. Note: To trace the validation of the Party Privacy Profile by the Party, the Party Privacy ABE currently includes a PartyPrivacyAgreement BE, defined as a specialization of Agreement. But any of the complexity of the Agreement ABE is necessary here - no Agreement Items, no Agreement Authorization - only a global Approval is necessary.

| SID ABE<br>Level 1 | SID ABE L1 Definition | SID ABE Level 2 (or set of BEs)* | SID ABE L2<br>Definition |
| --- | --- | --- | --- |
| Party<br>Privacy | The Party Privacy Profile ABE contains<br>all entities used by the Party Privacy<br>Management process for specifying<br>• the information concerned by<br>Privacy rules,<br>• the Privacy rules themselves,<br>• and the choices made by Parties for<br>their own Privacy. |   |   |

## 2.3. eTOM L2 - SID ABEs links

![](media/etom-sid-party-privacy-links.png)
*([PlantUML source](media/etom-sid-party-privacy-links.puml))*

## 2.4. Functional Framework Functions

| Function<br>ID | Functional Framework Function | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- |
| 664 | Privacy Profile<br>Type Creation | Privacy Profile Type Creation<br>provides a privacy dashboard<br>function to define and create the<br>privacy profile types by<br>categorizing the Data Subject<br>Parties, and defining the<br>elements and of the Privacy for<br>the Privacy Profile Type, both<br>initial and additional for future<br>evolution.<br>Note: Profiles Type are defined<br>according to the Country<br>Privacy Authority such as<br>National Protective Security<br>Authority (NPSA) for UK. | Privacy<br>Development | Privacy<br>Definition<br>Management |
| 665 | Privacy Profile<br>Rules<br>Configuration | Privacy Profile Rules<br>Configuration provides a Privacy<br>Dashboard function to define<br>default and updated values for<br>the Privacy Profile including the<br>values for the Privacy Rules, and<br>the default Privacy Profile for<br>each Privacy Profile Type.<br>Note: Profiles Type are defined<br>according to the Country<br>Privacy Authority such as<br>National Protective Security<br>Authority (NPSA) for UK. | Privacy<br>Development | Privacy<br>Definition<br>Management |
| 666 | External<br>Access<br>Privacy Data<br>Browsing<br>Access | Privacy Data Browsing Access<br>provides a Privacy Dashboard<br>access to Privacy Data Browsing<br>used to provide the "Data<br>Subject Party" the ability to view<br>the current privacy profile<br>attributes, of the Privacy Profile,<br>both associated default values of<br>rules defined, and the current<br>values of rules. | Privacy<br>Management | Privacy<br>Repository<br>Management |
| 667 | External<br>Access<br>Privacy Data<br>Updating<br>Access | Privacy Data Updating Access<br>provides a Privacy Dashboard<br>function that provides an access<br>possibility for the Party to alter<br>the Privacy Profile, with<br>authorized values. | Privacy<br>Management | Privacy<br>Repository<br>Management |
| 668 | Privacy<br>Consent<br>Agreement<br>Obtaining | Privacy Consent Agreement<br>Obtaining function is used to<br>obtain consent from the "Data<br>Subject Party" at the time of a<br>change to the Privacy Profile.<br>This can be initiated by the "Data<br>Subject Party" at creation of new<br>usage, or by the Service when<br>delivering a new scenario. | Privacy<br>Management | Privacy<br>Repository<br>Management |
| 945 | Record<br>Retention<br>Management | Record Retention Management<br>of data and information monitor<br>and assures compliance with the<br>retention aspects of federal and<br>state laws, legal requirements<br>and expectations as well as the<br>enterprise policies and<br>procedures. | Privacy<br>Management | Privacy<br>Control |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. • List of Events (generated & consumed ) - The events which the component may generate are listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

The following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
| --- | --- | --- | --- | --- | --- |
| TMF644 | Privacy<br>Management | V4 | Mandatory | partyPrivacyProfile<br>Specification | GET<br>GET /id<br>POST<br>PATCH<br>DELETE |
|   |   |   |   | partyPrivacyProfile | GET<br>GET /id<br>POST<br>PATCH<br>DELETE |
|   |   |   |   | partyPrivacyAgree<br>ment | GET<br>GET /id<br>POST<br>PATCH<br>DELETE |
| TMF688https:<br>//raw.githubu<br>sercontent.co<br>m/tmforum-<br>apis/TMF688-<br>Event/master/<br>TMF688-<br>Event-<br>v4.0.0.swagg<br>er.json | Event | V4.0.0 | Optional |   |   |
| TMF701 | Process<br>Flow | V4 | Optional | processFlow | GET<br>GET /id<br>POST<br>DELETE |
|   |   |   |   | taskFlow | GET<br>GET /id<br>PATCH |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operation(s) | Rationales |
| --- | --- | --- | --- | --- | --- | --- |
| TMF620 | Product<br>Catalog<br>Management | v4 | Optional | productOfferi<br>ng | GET<br>GET /id | n/a |
| TMF632 | Party<br>Management | v4 | Mandatory | individual | GET<br>GET /id | a Party<br>Privacy<br>Profile must<br>be validated<br>by the<br>Party. |
|   |   |   |   | organization | GET<br>GET /id |   |
| TMF667 | Document | v4. | Optional | document | GET<br>GET /id<br>POST | n/a |
| TMF669 | Party Role<br>Management | v4 | Mandatory | partyRole | GET<br>GET /id | a Party<br>Privacy<br>Profile is<br>associated<br>to a Party<br>Role<br>(mandatory) |
| TMF672 | User Role<br>Permission<br>Management | v4.0.0 | Mandatory | permission | GET<br>GET /id |   |
|   |   |   |   | userRole | GET<br>GET /id |   |
| TMF688 | Event | v4.0.0 | Optional |   | Get |   |
| TMF701 | Process<br>Flow | v4 | Optional | processFlow | GET<br>GET /id<br>POST<br>DELETE | n/a |

Note: TMF669 V5 will permit to manage a resource partyRoleSpecification too (useful to be able to associate a Party Privacy Profile Type to a Party Role specification). Note: TMF651 Agreement Management is not included as dependent API. Even if it is currently part of the resource model of the TMF644 Party Privacy API, a simplification is requested at TMF644 level, as in the Party Privacy ABE.

## 3.3. Events

The diagram illustrates the Events which the component publishes and the Events that the component subscribes to and then receives. Both lists are derived from the APIs listed in the preceding sections. The type of event could be: • Create : a new resource has been created (following a POST). • Delete: an existing resource has been deleted. • AttributeValueChange: an attribute from the resource has changed - event structure allows to pinpoint the attribute. • InformationRequired: an attribute should be valued for the resource preventing to follow nominal lifecycle - event structure allows to pinpoint the attribute. • StateChange: resource state has changed.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

Note: Published events are the same for Privacy Management V4 and V5

# 4. Machine Readable Component Specification

Refer to the ODA Component Map on the TM Forum website for the machine-readable component specification files for this component.

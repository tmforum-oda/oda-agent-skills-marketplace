---
id: TMFC014
type: component
name: Location Management
version: 1.2.0
status: specified
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC014_Location_Management_v1.2.0.pdf"
  license: RAND
  retrieved: 2026-08-30
  sha256: a95de6f3fe4faf47ceeacad55bfc95269bad349c5fe194fbc5752b605ee4d320
  raw_path: references/components/TMFC014/TMFC014_Location_Management_v1.2.0.pdf
links:
  apis:
    - id: TMF669
      name: party-role-management-api
    - id: TMF673
      name: geographic-address-management-api
    - id: TMF674
      name: geographic-site-management-api
    - id: TMF675
      name: geographic-location-management-api
    - id: TMF701
      name: process-flow-management-api
  use_cases:
    - id: TMFS003
      name: Order Capture - Fiber Contract
    - id: TMFS007
      name: TMFS007
    - id: TMFS012
      name: Product Catalog - Launching a New Product Offering
    - id: TMFS016
      name: Prospect to Order for the SASE, (CPQ)
    - id: TMFS018
      name: Wholesale Broadband
    - id: TMFS030
      name: Satellite Direct-to-Device – Wholesaling Non-Terrestrial Networks capacity to Mobile Network Operators
yaml_spec_version: 1.2.1
---

# 1. Overview

| Component<br>Name | ID | Description | ODA Function Block |
| --- | --- | --- | --- |
| Location<br>Management | TMFC014 | The Location Management Component allows<br>easy reference to geographic places important<br>to other entities, where a geographic place is<br>an entity that can answer the question<br>“where?” . This component could be a facade<br>tool into GIS systems (e.g. Google Maps)<br>Also covers the operations to manage (create,<br>read, delete) geographic sites that can be<br>associated with a customer, account, service<br>delivery or other entities.<br>And finally gives the capabilities to retrieve<br>/list /validate addresses that are named as<br>structured textual ways of describing how to<br>find a Property in an urban area (country<br>properties are often defined differently). It<br>allows looking data for worldwide addresses<br>through popular GIS systems like Google<br>Maps or government master addresses<br>systems.<br>It can also be used to validate geographic<br>data, to be sure that it corresponds to a real<br>geographic address.<br>Finally, it can be used to look for an address<br>by: searching an area as a start (city, town ),<br>then zooming on the streets of this area, and<br>finally listing all the street segments (numbers)<br>in a street. | Production<br>Domain |

![](media/location-management-architecture.png)
*([PlantUML source](media/location-management-architecture.puml))*

# 2. eTOM Processes, SID Data Entities and

Functional Framework Functions

## 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:.

Note: as no eTOM business activity is currently responsible for Location Management, refer to JIRA paragraph.

## 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs)* |
| --- | --- |
| Location ABE | Geographic Place ABE |
|   | Geographic Location ABE |
|   | Geographic Address ABE |
|   | Geographic Site ABE |
|   | Local Place ABE |

*: if SID ABE Level 2 is not specified this means that all the L2 business entities must be implemented, else the L2 SID ABE Level is specified.

## 2.3. eTOM L2 - SID ABEs links

eTOM L2 vS SID ABEs links for this ODA Component.

![](media/etom-sid-location-links.png)
*([PlantUML source](media/etom-sid-location-links.puml))*

## 2.4. Functional Framework Functions

| Function | Description | ID | Domain | Aggregate Function Level 1 | Aggregate Function Level 2 |
| --- | --- | --- | --- | --- | --- |
| Location<br>Change<br>History<br>Management | Location Change History Management; Tracks all<br>changes of location data, making available attributes<br>according their historical values in certain periods. | 429 | Operations<br>Readiness &<br>Support | Resource<br>Management | Location<br>Management |
| Pre-formatted<br>Location<br>Information<br>Presentation | Pre-formatted Location Information Presentation<br>generates different views for different business cases<br>(e.g. different format of address strings) | 430 | Operations<br>Readiness &<br>Support | Resource<br>Management | Location<br>Management |
| Location<br>Information<br>Updating | Location Information Updating provides means to update<br>the repository with new/updated location information<br>from external sources. | 431 | Operations<br>Readiness &<br>Support | Resource<br>Management | Location<br>Management |
| Location<br>Information<br>Searching | Location Information Searching provide the ability to<br>search for a provided location/address, as part of the<br>Location Management, including the ability to return near<br>matches if an exact match is not found. | 432 | Operations<br>Readiness &<br>Support | Resource<br>Management | Location<br>Management |
| Location<br>Structure<br>Data<br>Configuration | Location Structure Data Configuration provides facilities<br>for creating, modifying, and deleting location structures<br>data according to business rules of Service Providers or<br>national and international location regulations. Also,<br>utilities for defining sets of location attributes, levels and<br>hierarchies should be available. | 433 | Operations<br>Readiness &<br>Support | Resource<br>Management | Location<br>Management |
| Location<br>Data Integrity<br>Management | Location Data Integrity Management provides ability to<br>maintain data integrity in the whole location repository.<br>It’s especially important if there are many external data<br>sources that deliver new addresses for the repository. | 434 | Operations<br>Readiness &<br>Support | Resource<br>Management | Location<br>Management |

# 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; This part is split in 3: • List of Exposed APIs - This is the list of APIs available from this component. At this stage we list the APIs, resource and operation we no mention to optionality (in other word no mention about mandatory VS optional resource) • List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of this set of required APIs. At this stage no optionality is defined and none of this 'required' API is listed as 'mandatory' • List of Events (generated & consumed ) - The events which the component may generate is listed in this section along with a list of the events which it may consume. Since there is a possibility of multiple sources and receivers for each defined event.

## 3.1. Exposed APIs

Following diagram illustrates API/Resource/Operation:

![](media/exposed-apis-structure.png)
*([PlantUML source](media/exposed-apis-structure.puml))*

| API ID | API Name | API Version | Mandatory / Optional | Operation |
| --- | --- | --- | --- | --- |
| TMF673 | TMF 673<br>Geographic<br>Address<br>Management<br>API | 4 | Mandatory | geographicAddressValidation<br>• GET<br>• GET /ID<br>• POST<br>• PATCH |
| TMF673 | TMF 673<br>Geographic<br>Address<br>Management<br>API | 4 | Mandatory | geographicAddress<br>• GET<br>• GET /ID |
| TMF673 | TMF 673<br>Geographic<br>Address<br>Management<br>API | 4 | Mandatory | geographicSubAddress<br>• GET<br>• GET /ID |
| TMF674 | TMF 674<br>Geographic Site<br>Management<br>API | 4 | Mandatory | geographicSite<br>• GET<br>• GET /ID<br>• POST<br>• PATCH<br>• DELETE |
| TMF675 | TMF675<br>Geographic<br>Location | 4 | Mandatory | geographicLocation<br>• GET<br>• GET /ID<br>• POST<br>• PATCH<br>• DELETE |
| TMF688 | TMF688 Event | 4 | Optional | listener<br>• POST |
| TMF688 | TMF688 Event | 4 | Optional | hub<br>• POST<br>• DELETE |
| TMF701 | TMF701<br>Process Flow<br>Management | 4 | Optional | processFlow<br>• GET<br>• GET /ID<br>• POST<br>• DELETE |
| TMF701 | TMF701<br>Process Flow<br>Management | 4 | Optional | taskFlow<br>• GET /ID<br>• PATCH |

## 3.2. Dependent APIs

Following diagram illustrates API/Resource/Operation:

![](media/dependent-apis-structure.png)
*([PlantUML source](media/dependent-apis-structure.puml))*

| API ID | API Name | API<br>Version | Mandatory / Optional | resource | Operations |
| --- | --- | --- | --- | --- | --- |
| TMF632 | TMF632 Party<br>Management | 4 | Optional |   | Individual /<br>organization<br>• GET<br>• GET/id |
| TMF674 | TMF674<br>Geographic Site | 4 | Optional |   | geographicSite<br>• GET<br>• GET/id |
| TMF688 | TMF688 Event | 4 | Optional |   | event<br>• GET<br>• GET/id |

## 3.3. Events

The following diagram illustrates the Events which the component may publish and the Events that the component may subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

![](media/events-structure.png)
*([PlantUML source](media/events-structure.puml))*

# 4. Machine Readable Component Specification

Refer to the ODA Component Map on the TM Forum website for the machine-readable component specification files for this component. TM Forum - ODA Component Directory.

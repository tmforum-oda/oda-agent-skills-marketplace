# component.yaml → diagram mapping

Paths are relative to `spec:`. Implemented in `scripts/model.mjs`.

## Title
`{componentMetadata.id}: {NAME}` upper-case. NAME = `{id}.md` frontmatter
`name:` if that file exists, else `componentMetadata.name` with CamelCase split.

## APIs
| Side | Source | Glyph |
| --- | --- | --- |
| Left | `coreFunction.dependentAPIs[]` (+ `securityFunction`/`managementFunction` with `--include`) | socket `)──` |
| Right | `coreFunction.exposedAPIs[]` (+ same) | lollipop `──○` |

- Label: `{id} {name without -api, hyphens→spaces, Title Case}` — `party-role-management-api` → `TMF669 Party Role Management`.
- Names without hyphens (implementations: `productcatalogmanagement`) → the hyphenated name for that TMF id harvested from `knowledge/components/*/component.yaml`.
- No TMF id (`metrics`, MCP) → `{Name} ({apiType})`, e.g. `Metrics (Prometheus)`.
- Drop entries whose *name* is a template placeholder (`dependentAPI_name`); a placeholder *id* (`exposedAPI_id`) just means "no TMF id".
- Group by function (core, management, security); de-dup by id within function and side (required = OR of duplicates); sort by TMF number, id-less last.
- Colour by function (stroke / fill): core `#4c9a52`/`#e8f5e9`, management `#4a7fbf`/`#e7eff9`, security `#c0504d`/`#fbeaea` — `FN_COLOR` in `layout.mjs`.
- `required: true` → bold label.
- Tooltip: label + spec version, `required`, one line per resource with its operations.

## eTOM business activities
Entry: `1.2.20|Product_Catalog_Lifecycle_Management|v24.0`.
- Level = segments − 1 (`1.2.20` = L2, `1.2.8.7` = L3, `1.2.8.7.1` = L4).
- Default: all L2, plus any L3/L4 with no listed ancestor. `--etom-levels all` shows everything.
- Label `L{n} - {Name with spaces}`; numeric dotted sort; tooltip = id, name, version.
- Empty list → one italic "No eTOM business activities assigned" row.

## SID ABEs
Entry: `Domain|ABE[|Sub_ABE or BE]|version`.
- Label = last entity segment, `_ABE`/`_BE` removed, underscores→spaces, CamelCase split (`ProductConfigSpec_BE` → `Product Config Spec`).
- YAML order, 3 columns, labels wrap to 2 lines. Tooltip = full path joined with ` › `.
- Some SID paths in the source look swapped (TMFC001: `Loyalty_ABE|Product_Usage_Spec_ABE`) — reproduce as-is.

## Known source quirks (reproduce, don't fix)
- YAML vs PDF version numbers and content differ (see `knowledge/components/AGENTS.md`).
- Management-function blocks contain template placeholders (`dependentAPI_id`) — filtered, not drawn.
- `status` may be `Pre-production` (TMFC011) rather than `specified` — shown in `<desc>` only.

## Helm charts (reference implementations)
`render.mjs --chart DIR` runs `helm template r1 DIR [--set …] [-f …]` and models the single `kind: Component` document.
- Title name borrowed from `knowledge/components/{id}/{id}.md` when the chart implements a published TMFC id; subtitle "Reference implementation".
- `--include` defaults to management + security. The note under the box shows chart name/version and the exact `helm template` arguments.
- No eTOM/SID in implementations → the box shows microservices; eTOM/SID omitted from the legend.

### Microservices and links (`buildInternals` in model.mjs)
| Drawn | Derived from |
| --- | --- |
| Rounded rect per microservice | every `Deployment`/`StatefulSet`/`DaemonSet`/`Job`/`CronJob`; label = name minus `{release}-`, subline = image basename(s), container ports. Jobs dashed/grey; images `mongo`, `postgres`, `mysql`, `redis`… marked as databases. |
| Faint dashed line → exposed API | `exposedAPIs[].implementation` = Service name → Service `selector` ⊆ pod labels → workload (or a workload with that name). |
| Faint dashed line ← dependent API | a workload env var value equal to the dependent API's `name`; otherwise (ODA runtime discovery) every workload that uses a platform API flagged `discoversDependentAPIs` in `platform-apis.json` — today the Canvas info service, TMF638. |
| Grey arrow between microservices | a workload env var whose value is (or is a URL/host:port for) another in-chart Service name. |
| Management-function dependent API (left) + faint link | env host matching an entry in `scripts/platform-apis.json` (host → TMF id / name / apiType / function). Today: `info.canvas.svc.cluster.local` → TMF638 Service Inventory Management; `observability-opentelemetry-collector.monitoring.svc.cluster.local` → OpenTelemetry (OTLP). Merged with any declared dependent API of the same id and function. |
| "Platform services used" note | env hosts containing a dot that are neither in-chart Services nor in `platform-apis.json`. |

Layout: API-linked workloads in the right column, each placed at the mean y of its APIs (pushed apart to avoid overlap); the rest in the left column, placed beside the workloads they integrate with but kept off the rows that dependent-API lines use to cross to the right column (the box grows if needed); jobs at the bottom. Dependent-API lines run level with their API row and only curve in the gap between the columns. Legend adds "Microservice" and "Internal integration", and wraps function colours onto a second row when a single row would be wider than the diagram.

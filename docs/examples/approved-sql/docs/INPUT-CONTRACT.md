# Inputs and results

This profile is `oel-approved-sql-illustration/v1`. Its only accepted `origin` is `author-created-fixture`.
Use [matching-commit.json](../fixtures/matching-commit.json) as the full shape. Every object must contain exactly its declared keys.

| Field | Meaning in this illustration |
|---|---|
| `approval.granted` | An actual JSON boolean. It is not an authenticated approval. |
| `approval.call` | The request identifier, exact SQL bytes, ordered typed parameters, target, and database principal approved in the fixture. |
| `application` | The supplied application call and outcome, or `null` for an absent record. |
| `audit.records` | Supplied database-audit projections with distinct `event_id` values. These are fixture records, not native exports. |
| `audit.scope` | The declared request, target, and a nonempty window label. It is the collector's assertion, not a checked capture boundary. |
| `audit.complete` | A boolean declaration. An empty incomplete or differently scoped collection produces insufficient evidence. |
| `later_state` | A target, resource label, bytes supplied as the at-commit state, and later bytes. Use `null` when absent. |

A call has `request_id`, `sql_utf8_b64`, `parameters`, `target`, and `executing_principal`.
SQL uses canonical base64 of exact UTF-8 bytes. Spaces and Unicode forms stay distinct. The reader does not parse or execute SQL.
Each parameter has consecutive `position` values starting at 1, an opaque `database_type`, and `value_b64`.
`value_b64: null` means SQL NULL. An empty base64 string means empty bytes. The two remain distinct.
A target has exact `instance`, `database`, and `schema` strings. The principal means the database principal in this illustration.
Do not fill that field from an application user identifier without an established native mapping.

An outcome has `statement: succeeded|failed` and `transaction: committed|rolled_back|unknown`.
The reader preserves the two claims separately. It does not infer a commit from a successful statement.

The reader joins supplied audit records by `request_id`. More than one matching record is ambiguous.
This is the illustration's comparison identifier. It is not an alias for Tadpole's turn-level `AuditEvent.requestId`.
No matching event in a declared complete, matching scope yields `no_match_in_declared_complete_scope`.
It never turns that finding into an unscoped claim that no execution occurred.
A matching record must agree with approval on SQL bytes, typed parameters, every target field, and the principal.
The application record must also agree with the audit on the request and outcome.

`recorded_commit_matches` means those supplied records agree and their supplied outcome says successful and committed.
It is not authenticity, durable database state, exactly-once execution, policy correctness, or native qualification.
The CLI returns 0 for that result, 1 for another assessment, and 2 for invalid input.
A later byte difference leaves an earlier matching commit result intact. `later_change_attribution` always remains `not_assessed`.
The comparison does not establish when the supplied values were captured or who made a change.

Native work needs one versioned Settle approval, its application resource and SQL child record, and a corresponding database-native audit event.
Keep the original bytes and the export version. Document the join, bound parameters, execution-time context, database principal, transaction outcome, and collection boundary.
Unknown fields remain unknown. Connecting a native format is a separate adapter task with its own tests and operator receipts.

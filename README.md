
Hoccleve Archive Concordance Table Data
=======================================

This repository contains various documents that we are tracking for the concordance table project.

Document Schemata
-----------------
The document schemata provided in this repository are intended to serve as *contracts* between developers and end-users of the concordance table server. The separation of server functionality from document definition allows for a re-organization of the server's structure while still providing consistent service. The reader should note permissive aspects in the policy below: These are intended to allow for the use of new capabilities or additional document meta-data without requiring migration to new schema. At the same time, such permissiveness should provide an update path between revisions of a given schema. **This usage has yet to be formalized.**

Documents submitted to the server MUST be checked against one or more of these schemata and, when the document does not match, the end-user MUST be notified of where the document is inconsistent with the schema as well as where the full schema can be read. Developers can expect that any document received meets the appropriate schema. Document features which are not explicit in the schema MAY be supported by server functionality, but the absence of such document features MUST NOT result in error.

Documents returned from the server MUST be checked against one or more of these schemata and, when the document does not match, the end-user MUST be notified of where the document is inconsistent with the schema as well as where the full schema can be read. The document MUST be returned whether or not it matches the schema; however, the server SHOULD NOT return documents that violate the agreed-upon schemata, but rather publish a new schema revision that returned documents do match.

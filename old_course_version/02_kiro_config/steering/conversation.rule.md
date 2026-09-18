# Conversation
## Purpose
This rule defines how Kiro should behave in conversations, including how it should acknowledge other rules it's following.
## Instructions
- MANDATORY: Read and apply rules from ~/.aws/amazonq/rules/ directory before EVERY response. (ID: MANDATORY_RULES)
- ALWAYS consider your rules before using a tool or responding. (ID: CHECK_RULES)
- MANDATORY: Start with "Rule used: `filename` (ID) - brief explanation of how rule was applied" when applying ANY rule with priority level MANDATORY, CRITICAL, or HIGH. (ID: PRINT_RULES)
- ENFORCEMENT: Rule citation required for all mandatory, critical, and high priority rule applications. (ID: ENFORCE_RULE_PRINTING)
- If multiple rules are matched, list all: "Rule used: `file1.rule.md` (ID1), `file2.rule.md` (ID2) - explanation". (ID: PRINT_MULTIPLE)
- Skip rule citation only for medium and low priority rules or purely conversational responses. (ID: SELECTIVE_CITATION)
- This rule applies to ALL Q CLI sessions, IDE plugin sessions, and any Amazon Q interaction. (ID: UNIVERSAL_APPLICATION)
## Priority
Critical
## Error Handling
- If rule files are unreadable, continue but note the issue
- If multiple conflicting rules apply, follow the highest priority rule and note the conflict

# ChatGPT collaboration contract

## Transport

The user manually transfers a prompt into ChatGPT and imports a response. There is no ChatGPT OAuth integration, API key, browser automation or automatic message submission. The app performs no external network requests.

## Request

A saved project revision supplies the name, task brief and complete Markdown. The local server adds the user's instruction, a random request ID and a SHA-256 digest of the exact context. The full prompt remains in the local requests table.

## Response

ChatGPT is asked to return one JSON object:

```json
{
  "request_id": "copy the exact ID from the prompt",
  "context_digest": "copy the exact digest from the prompt",
  "summary": "Explain the proposed changes.",
  "skill_md": "---\nname: example\ndescription: A specific task.\n---\n\n## Workflow\n1. Follow the approved method.\n"
}
```

The app validates the request ID and digest, required text fields, size limits and current revision. It stores the proposal separately from the project. It never executes Markdown. The user reviews a unified diff and the complete proposed content, then explicitly applies the response. The server verifies the context again inside the write transaction.

## Boundaries

A context digest prevents accidental mismatches. It is not an identity signature. The app cannot verify the external model, subscription, output quality or author of a pasted response. Automated tests use clearly labeled synthetic responses and do not establish real ChatGPT quality.

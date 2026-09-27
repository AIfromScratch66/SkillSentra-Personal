# Personal Edition validation

Executed locally on Windows on 2026-09-27.

| Check | Result | Scope |
|---|---|---|
| Python suite | 20 passed, 6.607 seconds | Storage, request binding, explicit acceptance, restoration, import limits, HTTP boundaries, deletion and ZIP contents |
| Chromium browser suite | 8 passed, 17.813 seconds | Create, save, prompt, response review, apply, checks, export, reload, stale/error handling, imports, mobile layout and deletion confirmation |
| English presentation | 10 slides; structure, geometry, font policy and import checks passed | All rendered slides inspected; native Microsoft PowerPoint rendering not verified |
| English text scan | Passed for source and user-facing documents | No CJK text in the current app or documentation |

The complete workflow uses a clearly labeled synthetic response. No real ChatGPT conversation was sent, and no model output quality was verified. The app does not send messages automatically. Original platform tests do not count toward this focused edition's results.

Browser verification found and fixed an encoding issue in check labels and mobile project-list overflow. Async actions now execute in sequence so rapid navigation waits for an in-progress action. Tests wait for completed UI operations before inspecting results.

Static Skill checks cover structure and known placeholders. They are not a complete YAML parser, execution test or security certification. Local results do not verify macOS/Linux execution or GitHub CI. The user authorized public publication. Independent security/rights review remains pending.

## Publication PDF

The user-supplied 10-page PDF replaces the distributed PPTX. Its bytes are preserved exactly. SHA-256: `59e4333f5e770bc5f6bb8d0872f12a3b241dd3ff0d529e63a5929ff04fdfc53a`. Page text was inspected for all pages and the cover was rendered for visual confirmation. The earlier deck checks above describe the prior PPTX build, not independent revalidation of PDF typography.

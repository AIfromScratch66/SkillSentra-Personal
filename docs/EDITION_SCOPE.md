# Edition scope and branch history

The private local development baseline is the reviewed 0.6.7 snapshot in branch `baseline/0.6.7`. Personal Edition was developed in `personal/chatgpt`, version 0.7.0-personal.1. The public repository starts from a clean snapshot on `main`; it does not include the private development history.

| Area | Original platform | Personal Edition |
|---|---|---|
| Audience | Platform and multiple roles | One local user |
| Skill creation | Guided platform routes | Markdown starter and editor |
| Existing Skill | Multi-stage source workflow | Single SKILL.md import |
| AI collaboration | Model API and host contracts | Manual ChatGPT request/response |
| Version evidence | Platform records | Local immutable content revisions and context digest |
| Validation | Broader platform validation | Bounded static structure checks |
| Marketplace and ranking | Present | Removed |
| Purchases, payouts and settlement | Present | Removed |
| Accounts and team administration | Present | Removed |
| Model credentials | Configurable | No credential fields |
| Runtime data | Platform schema | Projects, versions and requests only |

The web client and local HTTP service are reduced implementations for this edition. The project name and existing brand assets are retained. The baseline remains recoverable in private local Git and is not deployed over the original instance. Old platform databases are not migration inputs for this branch.

Temporary removal means the baseline code remains available in private local branch history. Disabled platform modules are not shipped in the current Personal Edition source archive.

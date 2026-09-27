# SkillSentra Personal user guide

## 1. Start the workspace

Run `python -m app.server` from the source folder, then open `http://127.0.0.1:8767`. Leave the server running while using the page. Close the terminal or press Ctrl+C to stop it. The app is intended for one person on a trusted local computer. Anyone who can use your computer's local server can access this workspace.

## 2. Create or import

Choose **New Skill**. Give the project a name and describe the task. The starter contains frontmatter, purpose, workflow, boundaries and output sections. Replace every starter placeholder with instructions specific to your task.

Alternatively, choose **Import SKILL.md** on the welcome page. Imports accept one UTF-8 Markdown file up to 160,000 bytes. References, assets and scripts in surrounding folders are not imported. The app does not execute imported text. Use only material you have permission to use.

## 3. Edit and save

The name identifies your local project. The task description adds context for ChatGPT. The Markdown editor holds the exported `SKILL.md`.

Select **Save revision** to persist changes. Each save adds a revision. Changes are not automatically saved. A second browser with an older revision cannot overwrite your newer work. Reload after a conflict and reconcile your edits.

## 4. Work with ChatGPT

Save the project before preparing a request. In **ChatGPT collaboration**, describe the improvement you want and select **Prepare ChatGPT request**. Inspect the prompt, then choose **Copy prompt**. **Open ChatGPT** opens its website with no content attached. You paste the prompt yourself.

Ask ChatGPT to return the required JSON object. Paste it into the response box or import its UTF-8 JSON file. Markdown fences around the JSON are accepted. Choose **Review response**.

Importing a response does not change the Skill. Read the summary, inspect the diff and expand **Complete proposed SKILL.md**. Confirm the review checkbox and choose **Apply reviewed response**. The result becomes a new revision, with earlier content retained.

Saved requests survive app restarts. Editing any saved project context makes older requests stale. The app rejects stale or already-applied requests. Prepare a new request after editing. Request IDs and context digests bind the exchange to a version, but do not prove that ChatGPT authored the response.

## 5. Check and export

Open **Versions & checks**. Static checks require non-empty name and description fields in frontmatter, a workflow/instructions/steps heading and removal of known starter placeholders. This is a bounded text check, not full YAML validation, security certification or proof of task quality.

Resolve findings and save before exporting. The ZIP includes only `SKILL.md`, `validation.json` and a small README. SkillSentra does not install the ZIP into ChatGPT automatically. Use its content with a host that supports your intended Skill format. Plain ChatGPT conversations can also use the Markdown as context.

## 6. Restore and delete

Select **Restore content** for a previous revision, then confirm. The app saves the old Markdown as a new revision. It does not roll back the project's name or task description.

**Delete this project** removes its current project record, version history and collaboration requests after confirmation. It does not erase exported files, external conversations, backups or storage remnants.

## 7. Backup and reset

Stop the server before backing up the entire `data` directory. Restore it only while the server is stopped. Keep backups private because prompts and responses may contain personal content.

To reset the entire Personal Edition workspace, stop the server, back up anything you need and remove its `data` directory. Restart to create an empty database. Do not delete the original platform's data folder. This edition uses its own source directory and port by default.

## 8. Troubleshooting

- **Unsaved changes:** save before preparing a request, importing a response, restoring or exporting.
- **Context mismatch:** return the exact request_id and context_digest in the prepared prompt.
- **Invalid JSON:** ask ChatGPT to return one valid object with escaped newlines in skill_md.
- **Stale request:** prepare a new request using the current saved revision.
- **Copy blocked:** the prompt is selected so you can copy with your keyboard.
- **Local operation failed:** check disk space and file permissions, then restart the app.
- **Port occupied:** use `--port 8768` and open that port.

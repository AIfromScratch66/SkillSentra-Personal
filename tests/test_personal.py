import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from app.server import Store, Problem, check_skill, create_server

SKILL="---\nname: research-brief\ndescription: Summarize approved research sources.\n---\n\n# Research Brief\n\n## Workflow\n1. Inspect the supplied sources.\n2. Summarize findings with source attribution.\n\n## Boundaries\nDo not invent citations.\n"

class PersonalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=Store(Path(self.tmp.name)/"personal.db")
        self.p=self.store.create({"name":"Research Brief","brief":"Summarize approved sources","content":SKILL})
    def request(self):return self.store.request(self.p["id"],{"instruction":"Clarify the output.","expected_revision":1})
    def response(self,r,content=None):return {"request_id":r["id"],"context_digest":r["context_digest"],"summary":"Added an output section.","skill_md":content or SKILL+"\n## Output\nA concise sourced brief.\n"}
    def test_fresh_workspace_has_no_projects_or_finance_tables(self):
        fresh=Store(Path(self.tmp.name)/"fresh.db")
        with fresh.db() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM projects").fetchone()[0],0)
            self.assertEqual({x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")},{"projects","versions","requests"})
    def test_starter_cannot_pass_export_checks(self):
        p=self.store.create({"name":"Starter"});self.assertFalse(check_skill(p["content"])["passed"])
    def test_structured_skill_passes_static_checks(self):self.assertTrue(check_skill(SKILL)["passed"])
    def test_invalid_frontmatter_is_reported(self):self.assertFalse(check_skill("# Text\n## Workflow\nDo work")["passed"])
    def test_save_rejects_stale_editor(self):
        payload=dict(name="New",brief="",content=SKILL,expected_revision=1)
        self.store.save(self.p["id"],payload)
        with self.assertRaises(Problem):self.store.save(self.p["id"],payload)
    def test_response_does_not_automatically_apply(self):
        r=self.request();self.store.response(r["id"],self.response(r))
        with self.store.db() as c:self.assertEqual(self.store.project(c,self.p["id"])["content"],SKILL)
    def test_response_bound_to_request_and_context(self):
        r=self.request();payload=self.response(r);payload["context_digest"]="wrong"
        with self.assertRaises(Problem):self.store.response(r["id"],payload)
    def test_edited_context_rejects_response(self):
        r=self.request();self.store.save(self.p["id"],dict(name="New",brief="",content=SKILL,expected_revision=1))
        with self.assertRaises(Problem):self.store.response(r["id"],self.response(r))
    def test_apply_requires_confirmation_and_preserves_history(self):
        r=self.request();self.store.response(r["id"],self.response(r))
        with self.assertRaises(Problem):self.store.apply(r["id"],{"expected_revision":1})
        p=self.store.apply(r["id"],{"expected_revision":1,"confirm":True});self.assertEqual(p["revision"],2)
        with self.store.db() as c:self.assertEqual(c.execute("SELECT count(*) FROM versions").fetchone()[0],2)
        with self.assertRaises(Problem):self.store.apply(r["id"],{"expected_revision":2,"confirm":True})
    def test_save_after_review_prevents_apply(self):
        r=self.request();self.store.response(r["id"],self.response(r));self.store.save(self.p["id"],dict(name="New",brief="",content=SKILL,expected_revision=1))
        with self.assertRaises(Problem):self.store.apply(r["id"],{"expected_revision":2,"confirm":True})
    def test_restore_retains_all_revisions(self):
        with self.store.db() as c:v=c.execute("SELECT id FROM versions").fetchone()[0]
        self.store.save(self.p["id"],dict(name="New",brief="",content=SKILL+"\nEdited",expected_revision=1))
        restored=self.store.restore(self.p["id"],{"version_id":v,"expected_revision":2})
        self.assertEqual(restored["content"],SKILL);self.assertEqual(restored["revision"],3)
    def test_imported_code_remains_text(self):
        p=self.store.create({"name":"Literal","content":SKILL+"\n<script>alert(1)</script>\n"})
        self.assertIn("<script>",p["content"])
    def test_oversized_text_is_rejected(self):
        with self.assertRaises(Problem):self.store.create({"name":"Large","content":"a"*160001})

class HttpTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.server=create_server(Path(self.tmp.name)/"web.db",0)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.close);self.base=f"http://127.0.0.1:{self.server.server_port}"
    def close(self):self.server.shutdown();self.server.server_close();self.thread.join()
    def call(self,path,method="GET",body=None,headers=None):
        headers={**({"Content-Type":"application/json"} if body is not None else {}),**(headers or {})}
        req=urllib.request.Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,method=method,headers=headers)
        try:
            with urllib.request.urlopen(req) as res:return res.status,res.read(),dict(res.headers)
        except urllib.error.HTTPError as error:return error.code,error.read(),dict(error.headers)
    def test_health_and_english_landing(self):
        self.assertEqual(self.call("/api/health")[0],200)
        status,body,headers=self.call("/");self.assertEqual(status,200);self.assertIn(b'<html lang="en">',body);self.assertIn("frame-ancestors 'none'",headers["Content-Security-Policy"])
    def test_removed_pages_and_apis_are_unavailable(self):
        for path in ["/marketplace.html","/platform.html","/api/v1/marketplace/publications","/api/v1/control/statements","/api/v1/auth/register","/api/connections","/app/server.py","/../data/personal.db"]:
            with self.subTest(path=path):self.assertEqual(self.call(path)[0],404)
    def test_host_origin_and_fetch_site_are_checked(self):
        for headers in [{"Host":"attacker.example"},{"Origin":"https://attacker.example"},{"Sec-Fetch-Site":"cross-site"}]:self.assertEqual(self.call("/api/projects",headers=headers)[0],403)
    def test_export_contains_only_reviewed_skill_and_check_report(self):
        p=json.loads(self.call("/api/projects","POST",{"name":"Research","content":SKILL})[1])["data"]
        status,body,_=self.call(f"/api/projects/{p['id']}/export");self.assertEqual(status,200)
        with zipfile.ZipFile(io.BytesIO(body)) as z:self.assertEqual(set(z.namelist()),{"SKILL.md","validation.json","README.md"});self.assertEqual(z.read("SKILL.md").decode(),SKILL)
    def test_placeholder_export_is_blocked(self):
        p=json.loads(self.call("/api/projects","POST",{"name":"Starter"})[1])["data"]
        self.assertEqual(self.call(f"/api/projects/{p['id']}/export")[0],409)
    def test_delete_cascades_versions_and_requests(self):
        p=json.loads(self.call("/api/projects","POST",{"name":"Research","content":SKILL})[1])["data"]
        self.call(f"/api/projects/{p['id']}/chatgpt","POST",{"instruction":"Review","expected_revision":1})
        self.assertEqual(self.call(f"/api/projects/{p['id']}","DELETE",{"expected_revision":1,"confirm":True})[0],200)
        with Store(Path(self.tmp.name)/"web.db").db() as c:
            for table in ["projects","versions","requests"]:self.assertEqual(c.execute("SELECT count(*) FROM "+table).fetchone()[0],0)
    def test_json_object_and_content_type_required(self):
        self.assertEqual(self.call("/api/projects","POST",[],{})[0],400)
        self.assertEqual(self.call("/api/projects","POST",{}, {"Content-Type":"text/plain"})[0],415)

if __name__=="__main__":unittest.main()

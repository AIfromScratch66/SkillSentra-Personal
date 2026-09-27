"""Build a deterministic source archive without runtime data or Git history."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ROOT_FILES={"README.md","LICENSE","CONTRIBUTING.md","SECURITY.md","SUPPORT.md","CHANGELOG.md","THIRD_PARTY_NOTICES.md","package.json","package-lock.json",".gitignore",".gitattributes","public-release.json"}
ROOT_DIRS={"app","web","docs","tests","scripts","licenses",".github"}

def build(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    files=[]
    for p in ROOT.rglob("*"):
        rel=p.relative_to(ROOT)
        if p.is_file() and not p.is_symlink() and (rel.parts[0] in ROOT_DIRS or rel.as_posix() in ROOT_FILES) and not any(x in rel.parts for x in ["__pycache__","node_modules"]):
            if p.suffix in {".db",".key",".pem",".log",".pyc"}:raise ValueError("Unexpected private/generated file: "+rel.as_posix())
            files.append(p)
    archive=output/"skillsentra-personal-0.7.0-personal.1.zip"
    entries=[]
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            name=p.relative_to(ROOT).as_posix();data=p.read_bytes()
            item=zipfile.ZipInfo(name,(2000,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(item,data)
            entries.append({"path":name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
    manifest={"version":"0.7.0-personal.1","branch":"main","archive":archive.name,"sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"files":entries}
    (output/"build-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist())=={e["path"] for e in entries}
        for entry in entries:assert hashlib.sha256(z.read(entry["path"])).hexdigest()==entry["sha256"]
    return {"archive":str(archive),"files_verified":len(entries),"sha256":manifest["sha256"]}

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=ROOT/"release");args=parser.parse_args();print(json.dumps(build(args.output)))

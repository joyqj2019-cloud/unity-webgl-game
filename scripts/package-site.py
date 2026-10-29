import argparse,hashlib,json,pathlib,shutil,tempfile,zipfile
p=argparse.ArgumentParser();p.add_argument('--build',required=True);p.add_argument('--output',required=True);p.add_argument('--tag',required=True);a=p.parse_args()
repo=pathlib.Path(__file__).resolve().parents[1];build=pathlib.Path(a.build).resolve();archive=pathlib.Path(a.output).resolve()
assert repo not in archive.parents,'Keep binary archives outside the Git repository'
assert all((build/x).is_file() for x in ['index.html','Build/Site.loader.js','Build/Site.data.unityweb','Build/Site.framework.js.unityweb','Build/Site.wasm.unityweb']),'Incomplete tested Unity output or unexpected file names'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
with tempfile.TemporaryDirectory() as temp:
 site=pathlib.Path(temp)/'site';shutil.copytree(build,site)
 for f in ['index.html','publish.css','publish.js']:shutil.copyfile(repo/'web'/f,site/f)
 (site/'.nojekyll').write_text('')
 files={str(f.relative_to(site)).replace('\\','/'):{'bytes':f.stat().st_size,'sha256':sha(f)} for f in site.rglob('*') if f.is_file() and f.name!='release-manifest.json'}
 (site/'release-manifest.json').write_text(json.dumps({'build':a.tag,'gameTitle':'Unity WebGL Game (Working Title)','compression':'Unity Gzip with Decompression Fallback','files':files},indent=2))
 total=sum(f.stat().st_size for f in site.rglob('*') if f.is_file());assert total<1_000_000_000,'Site exceeds Pages limit'
 archive.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
  for f in sorted(site.rglob('*')):
   if f.is_file():z.write(f,str(f.relative_to(site)).replace('\\','/'))
 (repo/'release.json').write_text(json.dumps({'tag':a.tag,'asset':archive.name,'sha256':sha(archive),'siteBytes':total,'build':a.tag},indent=2)+'\n')
 print('Prepared',archive.name,'with',total,'site bytes. Unity payloads were copied unchanged.')

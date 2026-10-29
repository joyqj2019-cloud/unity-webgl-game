import argparse,hashlib,json,pathlib,stat,zipfile
p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--config',required=True);p.add_argument('--extract');a=p.parse_args()
archive=pathlib.Path(a.archive);config=json.loads(pathlib.Path(a.config).read_text());h=hashlib.sha256()
with archive.open('rb') as f:
 for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
assert h.hexdigest()==config['sha256'],'Archive SHA-256 mismatch'
with zipfile.ZipFile(archive) as z:
 names=z.namelist();assert len(names)==len(set(names)),'Duplicate archive paths'
 total=0
 for item in z.infolist():
  name=pathlib.PurePosixPath(item.filename)
  assert not name.is_absolute() and '..' not in name.parts and '\\' not in item.filename and ':' not in item.filename,'Unsafe archive path'
  assert not stat.S_ISLNK(item.external_attr>>16),'Archive links are not allowed'
  total+=item.file_size
 assert total<1_000_000_000,'Published site exceeds the supported 1 GB limit'
 required=['index.html','Build/Site.loader.js','Build/Site.data.unityweb','Build/Site.framework.js.unityweb','Build/Site.wasm.unityweb','release-manifest.json']
 assert all(name in names for name in required),'Missing Unity release file'
 manifest=json.loads(z.read('release-manifest.json'))
 expected=set(manifest['files'])|{'release-manifest.json'}
 assert expected==set(names),'Archive file list does not match manifest'
 for name,item in manifest['files'].items():
  h=hashlib.sha256();size=0
  with z.open(name) as f:
   for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block);size+=len(block)
  assert h.hexdigest()==item['sha256'] and size==item['bytes'],'Site file mismatch: '+name
 if a.extract:
  target=pathlib.Path(a.extract);target.mkdir(parents=True,exist_ok=True);z.extractall(target)
 print(json.dumps({'verified':True,'files':len(names),'siteBytes':total,'archiveBytes':archive.stat().st_size,'build':manifest['build']}))

import re, json, zipfile, hashlib, collections, sys
from pathlib import Path
ZIP=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1] / 'hardware' / 'source-archives' / 'voicememory-2026-10-05_162836(2).zip'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+')
def parse(data):
    tokens=TOKEN.findall(data)
    i=0
    def item():
        nonlocal i
        s=tokens[i];i+=1
        if s!='(':
            return json.loads(s.replace('\r','\\r').replace('\n','\\n').replace('\t','\\t')) if s.startswith('"') else s
        result=[]
        while i<len(tokens) and tokens[i]!=')':result.append(item())
        i+=1
        return result
    return item()
def by(root,kind):return [x for x in root if isinstance(x,list) and x and x[0]==kind]
def first(root,kind):return next(iter(by(root,kind)),None)
def prop(root,name):return next((x[2] for x in by(root,'property') if len(x)>2 and x[1]==name),None)
def named_at(root):
    x=first(root,'at');return tuple(map(float,x[1:3])) if x else None
with zipfile.ZipFile(ZIP) as z:
    files={n: z.read(n) for n in z.namelist()}
    sch=parse(files['voicememory.kicad_sch'].decode())
    pcb=parse(files['voicememory.kicad_pcb'].decode())
    foot=parse(files['Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod'].decode())
    comps={}
    for s in by(sch,'symbol'):
        ref=prop(s,'Reference')
        if ref and not ref.startswith('#'):
            comps.setdefault(ref,{'value':prop(s,'Value'),'lib':first(s,'lib_id')[1], 'footprint':prop(s,'Footprint'), 'units':0})['units']+=1
    board={}
    footprints=by(pcb,'footprint')
    for s in footprints:
        ref=prop(s,'Reference')
        if not ref:continue
        pads=[]
        for p in by(s,'pad'):
            pads.append({'pad':p[1], 'kind':p[2], 'xy':named_at(p), 'drill':first(p,'drill')})
        board[ref]={'lib':s[1],'value':prop(s,'Value'),'pads':pads,'xy':named_at(s)}
    fp_pads=[{'pad':p[1], 'kind':p[2], 'xy':named_at(p), 'drill':first(p,'drill')} for p in by(foot,'pad')]
    report={
        'archive':ZIP.name,
        'archive_sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),
        'files':[{'path':k,'size':len(v),'sha256':hashlib.sha256(v).hexdigest()} for k,v in files.items()],
        'sch_generator':first(sch,'generator_version')[1],
        'pcb_generator':first(pcb,'generator_version')[1],
        'sch_components':len(comps),
        'pcb_footprints':len(footprints),
        'pcb_unique_ref_labels':len(board),
        'mounting_holes_with_unassigned_reference':sum(1 for fp in footprints if prop(fp,'Reference')=='REF**'),
        'pcb_tracks':len(by(pcb,'segment')),
        'pcb_vias':len(by(pcb,'via')),
        'pcb_zones':len(by(pcb,'zone')),
        'missing_on_pcb':sorted(set(comps)-set(board)),
        'missing_in_sch':sorted(set(board)-set(comps)-{'REF**'}),
        'critical':{r:{'sch':comps.get(r),'pcb': {k:v for k,v in board.get(r,{}).items() if k!='pads'}} for r in ['U1','U2','U3','U4','U5','C1','C2','C4','C11','C18','C19','R20','J1','J2']},
        'rj45_library_pad_details':fp_pads,
        'rj45_board_pad_details':{r:board[r]['pads'] for r in ['J1','J2'] if r in board},
        'resistor_footprints':dict(collections.Counter((c['footprint'] for k,c in comps.items() if re.fullmatch(r'R\d+',k)))),
        'capacitor_footprints':dict(collections.Counter((c['footprint'] for k,c in comps.items() if re.fullmatch(r'C\d+',k)))),
        'component_summary':comps,
    }
    print('Archive',report['archive_sha256']);print('Versions',report['sch_generator'],report['pcb_generator']);print('N',len(comps),len(footprints),report['pcb_tracks'],report['pcb_vias'])
    print('refs missing',report['missing_on_pcb'],report['missing_in_sch'])
    for r in report['critical']:
        c=report['critical'][r];print(r, c['sch']['value'] if c['sch'] else '?',c['sch']['footprint'] if c['sch'] else '?',c['pcb']['value'] if c['pcb'] else '?')
    print('RJ45 lib',report['rj45_library_pad_details']); print('RJ45 PCB J1', report['rj45_board_pad_details']['J1'])
    print('R footprints',report['resistor_footprints']);print('C footprints',report['capacitor_footprints'])
    output=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parents[1] / 'hardware' / 'reports' / 'inspection_2026-10-29.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2), encoding='utf-8')

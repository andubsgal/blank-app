import streamlit as st
import streamlit.components.v1 as components
import random, html, math

st.set_page_config(page_title="EXTREME — The Guide Race", page_icon="🧭", layout="wide")

SKILLS={
 "flight":("FLIGHT","🪂","#55d6be"),"board":("BOARD","🏄","#47a8ff"),
 "ride":("RIDE","🏍️","#ffb84d"),"climb":("CLIMB","🧗","#ed7b56"),
 "jump":("JUMP","🪽","#c795ff")}
COLORS=["#ff664a","#46bcec","#8bd450","#f4c542","#ed77ba","#b694ff"]
CABINS=["pacific","dune_camp","forest_lodge","alpine_hut","desert_post","island_cabin"]

NODES={
 "pacific":("Pacific Cabin",90,220,"🏡","coast","swell"),
 "reef":("Wild Reef",230,135,"🌊","coast","swell"),
 "dune_camp":("Dune Cabin",120,430,"🏡","dunes","wind"),
 "great_dune":("Great Dune",285,380,"🏜️","dunes","wind"),
 "oasis":("Oasis",350,525,"🌴","desert","heat"),
 "forest_lodge":("Forest Lodge",390,245,"🏡","forest","dry"),
 "pine_trail":("Pine Trails",520,355,"🌲","forest","dry"),
 "wind_valley":("Wind Valley",500,150,"🏞️","valley","wind"),
 "river":("Blue River",650,500,"🏞️","valley","rain"),
 "canyon":("Red Canyon",690,355,"⛰️","canyon","dry"),
 "desert_post":("Desert Post",575,610,"🏡","desert","heat"),
 "eagle_ridge":("Eagle Ridge",670,165,"🏔️","mountain","wind"),
 "alpine_hut":("Alpine Hut",810,105,"🏡","alpine","snow"),
 "needle":("The Needle",850,260,"🗻","vertical","wind"),
 "glacier":("Ice Crown",990,130,"❄️","alpine","snow"),
 "volcano":("Fire Volcano",985,330,"🌋","mountain","heat"),
 "high_pass":("High Pass",850,470,"🏔️","mountain","snow"),
 "lake":("Mirror Lake",1010,560,"🏞️","valley","rain"),
 "island_cabin":("Island Cabin",1150,435,"🏡","island","swell"),
 "storm_island":("Storm Island",1170,220,"🏝️","island","wind"),
 "base_wall":("Great Wall",770,610,"🧱","vertical","dry"),
 "snow_bowl":("Snow Bowl",1115,70,"🏂","alpine","snow")}

# a,b,skills,cost_energy,cost_gear,dice,resource,long,name
EDGES=[
 ("pacific","reef",{"board":1},1,1,6,"gear",False,"Coastal Paddle"),
 ("pacific","dune_camp",{"ride":1},1,0,8,"energy",False,"Coast Road"),
 ("pacific","forest_lodge",{"ride":1},2,1,5,"gear",False,"Jungle Traverse"),
 ("reef","wind_valley",{"board":2,"flight":1},2,1,4,"energy",True,"Ocean-to-Air Crossing"),
 ("reef","forest_lodge",{"board":1},1,1,9,"gear",False,"Reef Line"),
 ("dune_camp","great_dune",{"flight":1},1,0,6,"energy",False,"Dune Soaring"),
 ("dune_camp","oasis",{"ride":1},1,1,10,"gear",False,"Sand Track"),
 ("great_dune","oasis",{"board":1},1,1,8,"energy",False,"Sandboard Ridge"),
 ("great_dune","forest_lodge",{"ride":1},2,0,5,"gear",False,"Dust Trail"),
 ("great_dune","wind_valley",{"flight":2},2,1,3,"energy",True,"Great Wind Corridor"),
 ("oasis","desert_post",{"ride":2},2,1,4,"gear",True,"Desert Enduro"),
 ("oasis","river",{"ride":1},2,0,9,"energy",False,"Oasis Run"),
 ("forest_lodge","pine_trail",{"ride":1},1,0,6,"gear",False,"Forest Singletrack"),
 ("forest_lodge","wind_valley",{"climb":1},1,1,8,"energy",False,"Valley Approach"),
 ("pine_trail","wind_valley",{"ride":1},1,0,9,"gear",False,"North Trail"),
 ("pine_trail","river",{"ride":2},2,1,5,"energy",True,"Deep Forest Expedition"),
 ("pine_trail","canyon",{"climb":1},1,1,10,"gear",False,"Canyon Rim"),
 ("wind_valley","eagle_ridge",{"flight":2},2,0,6,"energy",False,"Thermal XC"),
 ("wind_valley","canyon",{"flight":1,"climb":1},2,1,7,"gear",True,"Valley Crossing"),
 ("river","desert_post",{"ride":1},1,0,8,"energy",False,"River Road"),
 ("river","canyon",{"ride":1},1,1,6,"gear",False,"River Gorge"),
 ("river","base_wall",{"climb":2},2,1,3,"gear",True,"Southern Big Wall"),
 ("river","lake",{"ride":2},2,0,11,"energy",True,"Great Valley Traverse"),
 ("desert_post","base_wall",{"ride":1},1,1,9,"gear",False,"Desert Wall Approach"),
 ("canyon","eagle_ridge",{"climb":2},2,1,8,"energy",False,"Eagle Scramble"),
 ("canyon","needle",{"climb":2},2,1,5,"gear",False,"Needle Approach"),
 ("canyon","high_pass",{"ride":2,"climb":1},3,1,2,"energy",True,"Canyon Grand Traverse"),
 ("eagle_ridge","alpine_hut",{"flight":2},2,0,6,"energy",False,"Ridge Soaring"),
 ("eagle_ridge","needle",{"climb":2},1,1,9,"gear",False,"North Face"),
 ("alpine_hut","needle",{"climb":1},1,1,8,"gear",False,"Alpine Route"),
 ("alpine_hut","glacier",{"board":2,"climb":1},2,1,4,"energy",True,"Glacier Expedition"),
 ("needle","glacier",{"jump":3,"climb":2},3,2,12,"gear",True,"Legendary Wingsuit Line"),
 ("needle","volcano",{"jump":2},2,1,5,"energy",True,"Needle BASE Crossing"),
 ("needle","high_pass",{"climb":2},1,1,10,"gear",False,"High Traverse"),
 ("glacier","snow_bowl",{"board":2},1,1,6,"energy",False,"Powder Line"),
 ("glacier","storm_island",{"flight":3},3,1,3,"gear",True,"Sea Thermal Crossing"),
 ("volcano","storm_island",{"jump":3},3,2,2,"energy",True,"Volcano Wingsuit"),
 ("volcano","high_pass",{"climb":2},2,1,8,"gear",False,"Lava Ridge"),
 ("volcano","island_cabin",{"flight":2},2,1,4,"energy",True,"Island XC"),
 ("high_pass","lake",{"board":2},2,0,9,"energy",False,"Snow Descent"),
 ("high_pass","base_wall",{"climb":2},2,1,5,"gear",False,"Wall Pass"),
 ("lake","island_cabin",{"board":1},1,1,6,"gear",False,"Lake Crossing"),
 ("base_wall","lake",{"ride":2},2,1,11,"energy",True,"Southern Connection"),
 ("island_cabin","storm_island",{"board":2},2,1,8,"gear",False,"Island Surf Route"),
 ("storm_island","snow_bowl",{"flight":3,"climb":2},3,2,12,"gear",True,"Storm Crown Expedition"),
 ("snow_bowl","island_cabin",{"board":3},3,1,3,"energy",True,"First Descent to Sea")]

WEATHER={
 "wind":("🌬️","Viento","FLIGHT −1 Energy"),
 "swell":("🌊","Oleaje","BOARD −1 Energy"),
 "snow":("❄️","Nieve","BOARD disponible"),
 "rain":("🌧️","Lluvia","RIDE +1 Energy"),
 "heat":("☀️","Calor","+1 Energy en rutas largas"),
 "dry":("🌤️","Seco","Sin modificador")}
VICTORY=12
CONDITION_POOL={
 "coast":["swell","wind","rain"],"dunes":["wind","heat","dry"],"desert":["heat","wind","dry"],
 "forest":["rain","dry","wind"],"valley":["wind","rain","dry"],"canyon":["dry","wind","heat"],
 "mountain":["wind","snow","dry"],"alpine":["snow","wind"],"vertical":["wind","dry","snow"],
 "island":["swell","wind","rain"]}

st.markdown("""<style>
.stApp{background:radial-gradient(circle at 45% 0,#18343b 0,#0a1820 48%,#061116 100%);color:#eef8f5}
[data-testid="stSidebar"]{background:#0a1820;border-right:1px solid #29454d}
.block-container{padding-top:.8rem;max-width:1580px}h1,h2,h3{letter-spacing:-.035em}
div[data-testid="stMetric"]{background:#10242b;border:1px solid #294851;padding:9px 13px;border-radius:14px}
.stButton>button{border-radius:11px;font-weight:750;border:1px solid #36555e}
.chip{display:inline-block;padding:4px 9px;margin:2px;border-radius:99px;background:#163039;border:1px solid #31545d}
.event{padding:7px 10px;border-left:3px solid #ffb84d;background:#10242b;margin:5px 0;border-radius:0 8px 8px 0}
</style>""",unsafe_allow_html=True)

def edge_key(a,b): return "|".join(sorted((a,b)))
def edge(a,b): return next((e for e in EDGES if {e[0],e[1]}=={a,b}),None)
def neighbors(n): return [(b if a==n else a,e) for e in EDGES for a,b in [e[:2]] if a==n or b==n]
def rarity(n): return {2:5,3:4,4:3,5:2,6:1,8:1,9:2,10:3,11:4,12:5}.get(n,0)
def route_label(e): return e[9]
def skill_text(req): return " + ".join(f"{SKILLS[k][1]} {SKILLS[k][0]} {v}" for k,v in req.items())
def person(name,color,cabin):
 return {"name":name,"color":color,"loc":cabin,"ap":3,"energy":5,"gear":4,
         "skills":{k:1 for k in SKILLS},"guides":[],"xp":0,"rolled":False,"toll":"gear"}

def start(names,cabins):
 st.session_state.game={"players":[person(n,COLORS[i],cabins[i]) for i,n in enumerate(names)],
  "turn":0,"round":1,"guides":{},"roll":None,"log":["Las expediciones salen de sus cabañas."],"winner":None,"conditions":{k:random.choice(CONDITION_POOL.get(n[4],["dry"])) for k,n in NODES.items()}}

if "game" not in st.session_state: st.session_state.game=None
if st.session_state.game is None:
 st.title("EXTREME")
 st.subheader("THE GUIDE RACE")
 st.write("Explora un mundo abierto. Documenta **12 travesías originales** antes que los demás.")
 with st.form("setup"):
  count=st.slider("Exploradores",4,6,4)
  cols=st.columns(2); names=[]; cabins=[]
  for i in range(count):
   with cols[i%2]:
    names.append(st.text_input(f"Explorador {i+1}",value=["Andubs","Lambo","Remi","Diego","Sebas","Reni"][i]))
    choices=[c for c in CABINS if c not in cabins]
    cabin=st.selectbox(f"Cabaña inicial {i+1}",choices,format_func=lambda x:NODES[x][0],key=f"cab{i}")
    cabins.append(cabin)
  if st.form_submit_button("Comenzar",use_container_width=True):
   start([x.strip() or f"Explorer {i+1}" for i,x in enumerate(names)],cabins);st.rerun()
 st.stop()

g=st.session_state.game;p=g["players"][g["turn"]]

def log(s): g["log"].insert(0,s);g["log"]=g["log"][:18]
def route_cost(e,known=False):
 energy=e[3];gear=e[4];condition=g["conditions"][e[1]]
 if g["conditions"][p["loc"]]=="wind" or condition=="wind":
  if "flight" in e[2]: energy=max(0,energy-1)
 if g["conditions"][p["loc"]]=="swell" or condition=="swell":
  if "board" in e[2]: energy=max(0,energy-1)
 if g["conditions"][p["loc"]]=="rain" or condition=="rain":
  if "ride" in e[2]: energy+=1
 if (g["conditions"][p["loc"]]=="heat" or condition=="heat") and e[8]: energy+=1
 if known: energy=math.ceil(energy/2);gear=math.floor(gear/2)
 return energy,gear
def next_turn():
 p["ap"]=3;p["rolled"]=False
 g["turn"]=(g["turn"]+1)%len(g["players"])
 if g["turn"]==0:g["round"]+=1
def produce(total):
 gains=[]
 for key,guide in g["guides"].items():
  e=next(x for x in EDGES if edge_key(x[0],x[1])==key)
  if e[5]==total:
   owner=g["players"][guide["owner"]];amount=rarity(total)
   owner[e[6]]=min(15,owner[e[6]]+amount);gains.append(f"{owner['name']} +{amount} {e[6].title()}")
 return gains

def map_svg():
 lines=[]
 for e in EDGES:
  a,b=e[:2];x1,y1=NODES[a][1:3];x2,y2=NODES[b][1:3];key=edge_key(a,b);gd=g["guides"].get(key)
  stroke=gd["color"] if gd else "#52676d";w=7 if gd else (4 if e[8] else 2.4);dash="" if gd else 'stroke-dasharray="8 9"'
  lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}" opacity=".82" {dash}/>')
  mx,my=(x1+x2)/2,(y1+y2)/2
  lines.append(f'<circle cx="{mx}" cy="{my}" r="14" fill="#0a1920" stroke="#607d83"/><text x="{mx}" y="{my+5}" text-anchor="middle" fill="white" font-size="12" font-weight="700">{e[5]}</text>')
 icons=[]
 for k,n in NODES.items():
  ico,name,x,y=n[3],n[0],n[1],n[2];cond=g["conditions"][k];wicon=WEATHER[cond][0]
  icons.append(f'<circle cx="{x}" cy="{y}" r="29" fill="#132d35" stroke="#b7d9d4" stroke-width="2"/><text x="{x}" y="{y+7}" text-anchor="middle" font-size="24">{ico}</text><text x="{x}" y="{y+44}" text-anchor="middle" fill="#edf8f5" font-size="12" font-weight="700">{html.escape(name)}</text><text x="{x+25}" y="{y-21}" font-size="15">{wicon}</text>')
 tokens=[];seen={}
 for q in g["players"]:
  i=seen.get(q["loc"],0);seen[q["loc"]]=i+1;n=NODES[q["loc"]];ox=-20+i*10
  tokens.append(f'<circle cx="{n[1]+ox}" cy="{n[2]-26}" r="8" fill="{q["color"]}" stroke="white" stroke-width="2"/>')
 return f'''<svg viewBox="0 0 1260 690" width="100%" style="background:linear-gradient(145deg,#15333b,#0b1b22);border-radius:18px;border:1px solid #31535c">
 <defs><pattern id="t" width="70" height="55" patternUnits="userSpaceOnUse"><path d="M0 36 Q18 8 38 36 T78 36" fill="none" stroke="#31545c" opacity=".3"/></pattern></defs>
 <rect width="1260" height="690" fill="url(#t)"/>{"".join(lines)}{"".join(icons)}{"".join(tokens)}</svg>'''

h1,h2,h3,h4=st.columns([2,1,1,1])
h1.title("EXTREME · GUIDE RACE");h2.metric("Ronda",g["round"]);h3.metric("Turno",p["name"]);h4.metric("Meta",f"{len(p['guides'])}/{VICTORY} Guides")

if g["winner"] is not None:
 win=g["players"][g["winner"]];st.success(f"🏆 {win['name']} gana: descubrió {len(win['guides'])} rutas y obtuvo {win['xp']} XP.")
 rank=sorted(g["players"],key=lambda q:(len(q["guides"]),q["xp"]),reverse=True)
 st.dataframe([{"Pos.":i+1,"Explorer":q["name"],"Guides":len(q["guides"]),"XP":q["xp"],"Energy":q["energy"],"Gear":q["gear"]} for i,q in enumerate(rank)],hide_index=True,use_container_width=True)
 if st.button("Nueva partida"):st.session_state.game=None;st.rerun()
 st.stop()

main,side=st.columns([2.35,1],gap="large")
with main:
 components.html(map_svg(),height=700)
 st.caption("Ruta punteada: sin explorar · Línea gruesa: travesía larga (2 XP) · Número: condiciones óptimas de producción")
with side:
 st.subheader(f"{p['name']} · {p['ap']} AP")
 a,b,c,d=st.columns(4);a.metric("Guides",len(p["guides"]));b.metric("XP",p["xp"]);c.metric("Energy",p["energy"]);d.metric("Gear",p["gear"])
 st.markdown(" ".join(f'<span class="chip">{v[1]} {p["skills"][k]}</span>' for k,v in SKILLS.items()),unsafe_allow_html=True)
 st.write(f"📍 **{NODES[p['loc']][0]}** · {WEATHER[g['conditions'][p['loc']]][0]} {WEATHER[g['conditions'][p['loc']]][1]}")
 if not p["rolled"]:
  if st.button("🎲 Tirar condiciones",use_container_width=True):
   d1=random.randint(1,6);d2=random.randint(1,6);total=d1+d2;g["roll"]=(d1,d2,total);p["rolled"]=True
   gains=produce(total);log(f"{p['name']} tiró {d1}+{d2}={total}. "+("; ".join(gains) if gains else "Ninguna Guide produjo."))
   st.rerun()
 else:
  d1,d2,total=g["roll"];st.success(f"🎲 {d1} + {d2} = **{total}**")
  move_tab,train_tab,guide_tab=st.tabs(["Explorar","Entrenar","Mis Guides"])
  with move_tab:
   opts=neighbors(p["loc"]);labels={f"{route_label(e)} → {NODES[n][0]}":(n,e) for n,e in opts}
   selected=st.selectbox("Travesía",list(labels),key=f"m{g['round']}{g['turn']}{p['loc']}")
   dest,e=labels[selected];key=edge_key(p["loc"],dest);gd=g["guides"].get(key);own=gd and gd["owner"]==g["turn"];other=gd and not own
   known=bool(gd);ec,gc=route_cost(e,known);mode="guide"
   if other:
    owner=g["players"][gd["owner"]]
    mode=st.radio("Acuerdo",["Comprar conocimiento","Pagar expedición completa"],horizontal=True)
    if mode=="Pagar expedición completa":ec,gc=route_cost(e,False)
   st.write(f"**{route_label(e)}** {'· LONG ROUTE · 2 XP' if e[8] else '· 1 XP'}")
   st.caption(f"Requiere {skill_text(e[2])} · {'1 AP' if known else '2 AP'} · {ec} Energy · {gc} Gear · produce {rarity(e[5])} {e[6].title()} con {e[5]}")
   toll_txt=""
   if other and mode=="Comprar conocimiento":toll_txt=f" + {2 if e[8] else 1} {owner['toll'].title()} para {owner['name']}"
   if toll_txt:st.caption("Tarifa:"+toll_txt)
   apc=1 if known else 2;skill_ok=all(p["skills"][k]>=v for k,v in e[2].items())
   toll=(2 if e[8] else 1) if other and mode=="Comprar conocimiento" else 0
   toll_resource=owner["toll"] if other else "gear"
   enough=p["ap"]>=apc and p["energy"]>=ec and p["gear"]>=gc and skill_ok and (not toll or p[toll_resource]>=toll)
   if st.button("Completar travesía",disabled=not enough,use_container_width=True):
    p["ap"]-=apc;p["energy"]-=ec;p["gear"]-=gc;origin=p["loc"];p["loc"]=dest
    if not gd:
     xp=2 if e[8] else 1;p["guides"].append(key);p["xp"]+=xp;g["guides"][key]={"owner":g["turn"],"color":p["color"]}
     log(f"{p['name']} abrió {route_label(e)} (+{xp} XP, Guide #{len(p['guides'])}).")
     if len(p["guides"])>=VICTORY:g["winner"]=g["turn"]
    elif other:
     if mode=="Comprar conocimiento":p[toll_resource]-=toll;owner[toll_resource]+=toll;log(f"{p['name']} compró conocimiento de {owner['name']} y cruzó {route_label(e)}.")
     else:
      owner["energy"]+=ec;owner["gear"]+=gc;log(f"{p['name']} pagó la expedición completa a {owner['name']} para cruzar {route_label(e)}.")
    else:log(f"{p['name']} regresó por su Guide {route_label(e)} sin ganar XP.")
    st.rerun()
   if not skill_ok:st.warning("Te falta nivel en uno o más Skills.")
  with train_tab:
   sk=st.selectbox("Skill",list(SKILLS),format_func=lambda k:f"{SKILLS[k][1]} {SKILLS[k][0]} · nivel {p['skills'][k]}")
   cost=p["skills"][sk]+1
   st.caption(f"2 AP + {cost} Gear")
   if st.button("Entrenar",disabled=p["ap"]<2 or p["gear"]<cost or p["skills"][sk]>=4,use_container_width=True):
    p["ap"]-=2;p["gear"]-=cost;p["skills"][sk]+=1;log(f"{p['name']} entrenó {SKILLS[sk][0]} a nivel {p['skills'][sk]}.");st.rerun()
  with guide_tab:
   p["toll"]=st.radio("Recurso preferido como tarifa",["gear","energy"],index=0 if p["toll"]=="gear" else 1,horizontal=True)
   if not p["guides"]:st.caption("Todavía no has descubierto Guides.")
   for key in p["guides"]:
    e=next(x for x in EDGES if edge_key(x[0],x[1])==key)
    st.write(f"**{route_label(e)}** · {e[5]} · +{rarity(e[5])} {e[6]}")
  x,y=st.columns(2)
  if x.button("Reabastecer",disabled=p["ap"]<1,use_container_width=True):
   p["ap"]-=1;p["energy"]=min(15,p["energy"]+2);p["gear"]=min(15,p["gear"]+1);log(f"{p['name']} se reabasteció.");st.rerun()
  if y.button("Terminar turno",use_container_width=True):
   log(f"{p['name']} terminó su turno.");next_turn();st.rerun()

st.divider();left,right=st.columns([1,2])
with left:
 st.subheader("Ranking")
 rank=sorted(g["players"],key=lambda q:(len(q["guides"]),q["xp"]),reverse=True)
 st.dataframe([{"Explorer":q["name"],"Guides":f"{len(q['guides'])}/{VICTORY}","XP":q["xp"]} for q in rank],hide_index=True,use_container_width=True)
with right:
 st.subheader("Adventure log");st.markdown("".join(f'<div class="event">{html.escape(x)}</div>' for x in g["log"]),unsafe_allow_html=True)

with st.sidebar:
 st.header("Reglas rápidas")
 st.write("1. Tira **2d6**. Todas las Guides con ese número producen, sin importar de quién sea el turno.")
 st.write("2. Tienes **3 AP** para viajar, entrenar o reabastecerte.")
 st.write("3. Una travesía nueva cuesta 2 AP y entrega su Guide: **1 XP**, o **2 XP** si es larga.")
 st.write("4. Regresar o usar una ruta ajena cuesta menos, pero nunca entrega Guide ni XP.")
 st.write("5. Para cruzar una Guide ajena, compra conocimiento en el recurso elegido por su dueño o págale el coste normal.")
 st.write("6. Gana quien descubra personalmente **12 rutas**.")
 st.divider()
 st.write("**Probabilidad y producción**")
 st.write("6/8: frecuente, 1 recurso · 5/9: 2 · 4/10: 3 · 3/11: 4 · 2/12: 5.")
 if st.button("Reiniciar partida"):st.session_state.game=None;st.rerun()

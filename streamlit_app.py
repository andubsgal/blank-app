import streamlit as st
import streamlit.components.v1 as components
import random, html

st.set_page_config(page_title="EXTREME — Expedition Game", page_icon="🧭", layout="wide")

SKILLS = {
    "flight": ("FLIGHT", "🪂", "#55d6be"),
    "board": ("BOARD", "🏄", "#4ea5ff"),
    "ride": ("RIDE", "🏍️", "#ffb84d"),
    "climb": ("CLIMB", "🧗", "#df7b56"),
    "jump": ("JUMP", "🪽", "#c69cff"),
}
COLORS = ["#ff6b4a", "#48bfe3", "#84cc65", "#f3c64f"]
NODES = {
    "base": {"name":"Base Camp","x":390,"y":330,"icon":"⛺","terrain":"valley"},
    "forest": {"name":"Pine Trail","x":220,"y":285,"icon":"🌲","terrain":"forest"},
    "dunes": {"name":"Soaring Dunes","x":90,"y":390,"icon":"🏜️","terrain":"dunes"},
    "coast": {"name":"Wild Coast","x":105,"y":155,"icon":"🌊","terrain":"coast"},
    "ridge": {"name":"Eagle Ridge","x":365,"y":130,"icon":"🏔️","terrain":"alpine"},
    "needle": {"name":"The Needle","x":590,"y":115,"icon":"🗻","terrain":"vertical"},
    "canyon": {"name":"Red Canyon","x":595,"y":305,"icon":"⛰️","terrain":"canyon"},
    "volcano": {"name":"Fire Volcano","x":745,"y":205,"icon":"🌋","terrain":"volcano"},
    "glacier": {"name":"Ice Crown","x":760,"y":410,"icon":"❄️","terrain":"snow"},
    "island": {"name":"Storm Island","x":895,"y":305,"icon":"🏝️","terrain":"island"},
}
EDGES = [
    ("base","forest","ride",1),("forest","dunes","ride",1),("forest","coast","ride",2),
    ("coast","ridge","flight",2),("base","ridge","climb",1),("ridge","needle","climb",2),
    ("base","canyon","ride",1),("canyon","needle","jump",2),("canyon","volcano","climb",2),
    ("canyon","glacier","ride",2),("volcano","glacier","board",2),("volcano","island","jump",3),
    ("glacier","island","flight",3),("needle","volcano","flight",2),("dunes","base","flight",2),
]
ACTIVITIES = {
    "forest":[("Enduro Loop","ride",1,2,False),("Forest Downhill","ride",2,3,False)],
    "dunes":[("Dune Soaring","flight",1,2,False),("Endless Dune Line","board",2,5,True)],
    "coast":[("Surf Mission","board",1,2,False),("Big Wave Session","board",3,6,True)],
    "ridge":[("XC Launch","flight",2,3,False),("Alpine Ascent","climb",2,3,False)],
    "needle":[("North Face","climb",2,3,False),("Wingsuit Line","jump",3,6,True)],
    "canyon":[("Canyon Traverse","ride",2,3,False),("Technical Wall","climb",2,3,False)],
    "volcano":[("Summit Expedition","climb",3,4,False),("Volcano Flight","flight",3,6,True)],
    "glacier":[("First Descent","board",3,6,True),("Ice Climb","climb",2,3,False)],
    "island":[("Island Jump","jump",3,5,False),("Storm Line","jump",4,8,True)],
}
WEATHER = [
    ("Cielo estable","Todas las travesías operan normalmente.","☀️"),
    ("Viento fuerte","FLIGHT cuesta 1 Energy menos; JUMP cuesta 1 más.","🌬️"),
    ("Nieve fresca","Actividades BOARD Epic otorgan +1 XP.","❄️"),
    ("Tormenta","Travesías de dificultad 3 cuestan 1 Energy adicional.","⛈️"),
    ("Condiciones perfectas","La primera Activity de cada jugador cuesta 0 Gear.","✨"),
]

st.markdown("""<style>
.stApp{background:radial-gradient(circle at 45% 0,#19333a 0,#0b1820 48%,#071116 100%);color:#eef7f5}
[data-testid="stSidebar"]{background:#0b1820;border-right:1px solid #264047}
h1,h2,h3{letter-spacing:-.03em}.block-container{padding-top:1rem;max-width:1500px}
div[data-testid="stMetric"]{background:#11242b;border:1px solid #29424a;padding:10px 14px;border-radius:14px}
.stButton>button{border-radius:12px;font-weight:700;border:1px solid #38545b}
.small{opacity:.72;font-size:.86rem}.chip{display:inline-block;padding:4px 9px;margin:2px;border-radius:999px;background:#173039;border:1px solid #31515a}
.log{padding:7px 10px;border-left:3px solid #ffb84d;background:#10232a;margin:5px 0;border-radius:0 8px 8px 0}
</style>""", unsafe_allow_html=True)

def player(name, color):
    return {"name":name,"color":color,"loc":"base","ap":3,"energy":5,"gear":3,"xp":0,
            "skills":{k:1 for k in SKILLS},"trails":[],"activities":[],"free_activity":False}

def init_game(names):
    st.session_state.game = {"players":[player(n,COLORS[i]) for i,n in enumerate(names)],
        "turn":0,"round":1,"max_rounds":10,"guides":{},"spot_xp":{n:0 for n in NODES},
        "activity_owners":{},"log":["La expedición comienza en Base Camp."],"weather":0,"over":False}

if "game" not in st.session_state:
    st.session_state.game = None

if st.session_state.game is None:
    st.title("EXTREME")
    st.subheader("Crea la expedición más extraordinaria")
    st.write("Un juego estratégico de exploración, deportes extremos y rutas compartidas.")
    with st.form("setup"):
        count=st.slider("Jugadores",2,4,3)
        names=[st.text_input(f"Nombre del explorador {i+1}", value=["Andubs","Lambo","Remi","Diego"][i]) for i in range(count)]
        submitted=st.form_submit_button("Comenzar expedición", use_container_width=True)
        if submitted:
            init_game([n.strip() or f"Explorer {i+1}" for i,n in enumerate(names)])
            st.rerun()
    st.stop()

g=st.session_state.game
p=g["players"][g["turn"]]
weather=WEATHER[g["weather"]]

def edge_key(a,b): return "|".join(sorted((a,b)))
def edge_for(a,b):
    return next((e for e in EDGES if {e[0],e[1]}=={a,b}),None)
def neighbors(node):
    return [(b if a==node else a,s,d) for a,b,s,d in EDGES if a==node or b==node]
def add_log(msg):
    g["log"].insert(0,msg); g["log"]=g["log"][:14]
def next_turn():
    p["ap"]=3
    g["turn"]+=1
    if g["turn"]>=len(g["players"]):
        g["turn"]=0; g["round"]+=1
        if g["round"]>g["max_rounds"]: g["over"]=True
        else:
            g["weather"]=(g["round"]-1)%len(WEATHER)
            for q in g["players"]: q["energy"]=min(7,q["energy"]+1)
    if not g["over"]: g["players"][g["turn"]]["ap"]=3

def map_svg():
    trails=[]
    for a,b,skill,diff in EDGES:
        x1,y1=NODES[a]["x"],NODES[a]["y"]; x2,y2=NODES[b]["x"],NODES[b]["y"]
        key=edge_key(a,b); guide=g["guides"].get(key)
        stroke=guide["color"] if guide else "#52636a"; width=7 if guide else 3
        dash="" if guide else 'stroke-dasharray="9 10"'
        trails.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" opacity=".82" {dash}/>')
        mx,my=(x1+x2)/2,(y1+y2)/2
        trails.append(f'<circle cx="{mx}" cy="{my}" r="13" fill="#0c1a20" stroke="#607980"/><text x="{mx}" y="{my+5}" text-anchor="middle" font-size="13">{SKILLS[skill][1]}</text>')
    spots=[]
    for key,n in NODES.items():
        sxp=g["spot_xp"].get(key,0)
        spots.append(f'<circle cx="{n["x"]}" cy="{n["y"]}" r="32" fill="#132b33" stroke="#b6d5d0" stroke-width="2"/>')
        spots.append(f'<text x="{n["x"]}" y="{n["y"]+7}" text-anchor="middle" font-size="25">{n["icon"]}</text>')
        spots.append(f'<text x="{n["x"]}" y="{n["y"]+49}" text-anchor="middle" fill="#e9f5f2" font-size="14" font-weight="700">{html.escape(n["name"])}</text>')
        if key!="base": spots.append(f'<text x="{n["x"]}" y="{n["y"]+65}" text-anchor="middle" fill="#9bc0ba" font-size="11">{sxp} Spot XP</text>')
    tokens=[]
    offsets={}
    for q in g["players"]:
        idx=offsets.get(q["loc"],0); offsets[q["loc"]]=idx+1
        n=NODES[q["loc"]]; ox=(-18+idx*13)
        tokens.append(f'<circle cx="{n["x"]+ox}" cy="{n["y"]-27}" r="9" fill="{q["color"]}" stroke="white" stroke-width="2"/>')
    return f'''<svg viewBox="0 0 980 500" width="100%" style="background:linear-gradient(145deg,#16313a,#0d1d24);border-radius:18px;border:1px solid #31505a">
    <defs><pattern id="topo" width="70" height="70" patternUnits="userSpaceOnUse"><path d="M0 45 Q20 15 40 45 T80 45" fill="none" stroke="#31515a" stroke-width="1" opacity=".32"/></pattern></defs>
    <rect width="980" height="500" fill="url(#topo)"/>{"".join(trails)}{"".join(spots)}{"".join(tokens)}</svg>'''

top1,top2,top3=st.columns([2,1,1])
with top1:
    st.title("EXTREME")
with top2:
    st.metric("Expedición",f"Ronda {min(g['round'],g['max_rounds'])} / {g['max_rounds']}")
with top3:
    st.metric("Turno",p["name"])

if g["over"]:
    ranking=sorted(g["players"],key=lambda x:(x["xp"],len(x["trails"])),reverse=True)
    st.success(f"🏆 {ranking[0]['name']} gana con {ranking[0]['xp']} XP")
    st.dataframe([{"Pos.":i+1,"Explorer":q["name"],"XP":q["xp"],"Guides":len(q["trails"]),"Activities":len(q["activities"])} for i,q in enumerate(ranking)],hide_index=True,use_container_width=True)
    if st.button("Nueva partida"): st.session_state.game=None; st.rerun()
    st.stop()

st.info(f"{weather[2]} **{weather[0]}** — {weather[1]}")
main,side=st.columns([2.25,1],gap="large")
with main:
    components.html(map_svg(),height=515)
    st.caption("Líneas punteadas: travesías sin explorar · Líneas de color: Guides descubiertas")

with side:
    st.subheader(f"{p['name']} · {p['ap']} AP")
    c1,c2,c3=st.columns(3)
    c1.metric("XP",p["xp"]); c2.metric("Energy",p["energy"]); c3.metric("Gear",p["gear"])
    st.markdown(" ".join(f'<span class="chip">{v[1]} {p["skills"][k]}</span>' for k,v in SKILLS.items()),unsafe_allow_html=True)
    st.write(f"📍 **{NODES[p['loc']]['name']}**")
    tab_move,tab_spot,tab_train=st.tabs(["Viajar","Spot","Entrenar"])

    with tab_move:
        opts=neighbors(p["loc"])
        if opts:
            labels={f"{NODES[n]['name']} · {SKILLS[s][1]} {SKILLS[s][0]} {d}":(n,s,d) for n,s,d in opts}
            choice=st.selectbox("Destino",list(labels),key=f"move{g['round']}{g['turn']}{p['loc']}")
            dest,skill,diff=labels[choice]; key=edge_key(p["loc"],dest); guide=g["guides"].get(key)
            ap_cost=1 if guide else 2
            energy=max(1,diff)
            if weather[0]=="Viento fuerte" and skill=="flight": energy=max(0,energy-1)
            if weather[0]=="Viento fuerte" and skill=="jump": energy+=1
            if weather[0]=="Tormenta" and diff==3: energy+=1
            owner=None
            if guide and guide["owner"]!=g["turn"]: owner=g["players"][guide["owner"]]
            st.caption(("Guide disponible" if guide else "Travesía sin explorar")+f" · {ap_cost} AP · {energy} Energy"+(f" · 1 Gear para {owner['name']}" if owner else ""))
            can=p["ap"]>=ap_cost and p["energy"]>=energy and p["skills"][skill]>=diff and (not owner or p["gear"]>=1)
            if st.button("Viajar",disabled=not can,use_container_width=True):
                old=p["loc"]; p["ap"]-=ap_cost;p["energy"]-=energy;p["loc"]=dest
                if owner: p["gear"]-=1;owner["gear"]+=1;add_log(f"{p['name']} compró la Guide de {owner['name']}.")
                if not guide:
                    g["guides"][key]={"owner":g["turn"],"color":p["color"],"skill":skill}
                    p["trails"].append(key);p["xp"]+=1
                    add_log(f"{p['name']} descubrió {NODES[old]['name']} → {NODES[dest]['name']} y ganó 1 XP.")
                else: add_log(f"{p['name']} viajó hasta {NODES[dest]['name']}.")
                st.rerun()
            if not can: st.caption(f"Necesitas {SKILLS[skill][1]} {SKILLS[skill][0]} nivel {diff}, AP y recursos suficientes.")

    with tab_spot:
        acts=ACTIVITIES.get(p["loc"],[])
        available=[]
        for name,skill,level,xp,epic in acts:
            aid=f"{p['loc']}|{name}"
            if aid not in g["activity_owners"]:
                available.append((name,skill,level,xp,epic,aid))
        if not acts: st.caption("Aquí puedes descansar, pero no hay Activities.")
        elif not available: st.caption("Todas las Activities de este Spot ya fueron abiertas.")
        else:
            labels={f"{'⭐ ' if e else ''}{n} · +{xp} XP":(n,s,l,xp,e,aid) for n,s,l,xp,e,aid in available}
            ac=st.selectbox("Activity",list(labels),key=f"act{g['round']}{g['turn']}{p['loc']}")
            name,skill,level,xp,epic,aid=labels[ac]
            unlocked=not epic or g["spot_xp"][p["loc"]]>=5
            gear_cost=0 if weather[0]=="Condiciones perfectas" and not p["free_activity"] else 1
            st.caption(f"Requiere {SKILLS[skill][1]} {SKILLS[skill][0]} {level} · 1 AP · {gear_cost} Gear"+(" · se desbloquea con 5 Spot XP" if epic else ""))
            can=p["ap"]>=1 and p["gear"]>=gear_cost and p["skills"][skill]>=level and unlocked
            if st.button("Abrir Activity",disabled=not can,use_container_width=True):
                bonus=1 if epic and skill=="board" and weather[0]=="Nieve fresca" else 0
                p["ap"]-=1;p["gear"]-=gear_cost;p["xp"]+=xp+bonus;p["activities"].append(aid);p["free_activity"]=True
                g["spot_xp"][p["loc"]]+=xp;g["activity_owners"][aid]=g["turn"]
                add_log(f"{p['name']} abrió {name} en {NODES[p['loc']]['name']} (+{xp+bonus} XP).")
                st.rerun()
    with tab_train:
        sk=st.selectbox("Skill",list(SKILLS),format_func=lambda k:f"{SKILLS[k][1]} {SKILLS[k][0]} · nivel {p['skills'][k]}")
        cost=p["skills"][sk]+1
        st.caption(f"2 AP · {cost} Gear")
        if st.button("Subir de nivel",disabled=p["ap"]<2 or p["gear"]<cost or p["skills"][sk]>=4,use_container_width=True):
            p["ap"]-=2;p["gear"]-=cost;p["skills"][sk]+=1;add_log(f"{p['name']} entrenó {SKILLS[sk][0]} a nivel {p['skills'][sk]}.");st.rerun()

    a,b=st.columns(2)
    if a.button("Descansar",disabled=p["ap"]<1,use_container_width=True):
        p["ap"]-=1;p["energy"]=min(7,p["energy"]+2);p["gear"]=min(7,p["gear"]+1);add_log(f"{p['name']} descansó y se reabasteció.");st.rerun()
    if b.button("Terminar turno",use_container_width=True):
        add_log(f"{p['name']} terminó su turno.");next_turn();st.rerun()

st.divider()
lb,history=st.columns([1,2])
with lb:
    st.subheader("Expedition ranking")
    st.dataframe(sorted([{"Explorer":q["name"],"XP":q["xp"],"Guides":len(q["trails"]),"Spot activities":len(q["activities"])} for q in g["players"]],key=lambda x:x["XP"],reverse=True),hide_index=True,use_container_width=True)
with history:
    st.subheader("Adventure log")
    st.markdown("".join(f'<div class="log">{html.escape(x)}</div>' for x in g["log"]),unsafe_allow_html=True)

with st.sidebar:
    st.header("Cómo jugar")
    st.write("Cada turno tienes **3 AP**. Explora, entrena, abre Activities y deja Guides para que otros puedan usarlas.")
    st.write("**Viajar por descubrir:** 2 AP. **Usar Guide:** 1 AP; si pertenece a otro jugador, págale 1 Gear.")
    st.write("La primera persona en cruzar una ruta gana **1 XP** y se queda con la Guide.")
    st.write("Las Activities dan XP al jugador y al Spot. Con **5 Spot XP** se desbloquean las Epic.")
    st.write("Al terminar 10 rondas gana quien tenga más XP.")
    st.divider()
    if st.button("Reiniciar partida"):
        st.session_state.game=None;st.rerun()

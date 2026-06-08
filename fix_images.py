content = open('src/app/page.tsx', encoding='utf-8').read()

old = """background:`linear-gradient(to bottom, ${p.color}44, #080d1a)`, display:'flex', alignItems:'center', justifyContent:'center'}}>
                <div style={{fontFamily:A, fontSize:'80px', color:p.color, opacity:0.6, letterSpacing:'-4px'}}>{p.nation.slice(0,3)}</div>
              </div>"""

new = """position:'absolute', inset:0}}>
              <img src={p.img} alt={p.name} referrerPolicy="no-referrer" style={{width:'100%', height:'100%', objectFit:'cover', objectPosition:'top'}} />
              <div style={{position:'absolute', inset:0, background:`linear-gradient(to bottom, ${p.color}22, #080d1a)`}} />
              </div>"""

if old in content:
    content = content.replace(old, new)
    open('src/app/page.tsx', 'w', encoding='utf-8').write(content)
    print('Fixed successfully!')
else:
    print('NOT FOUND - pattern mismatch')
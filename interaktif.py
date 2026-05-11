import re

interactive_css = """
    /* INTERACTIVE CSS */
    .ripple { position: fixed; border-radius: 50%; transform: scale(0); animation: ripple-anim 0.6s linear; background: rgba(255, 255, 255, 0.4); pointer-events: none; z-index: 9999; }
    @keyframes ripple-anim { to { transform: scale(4); opacity: 0; } }
    .floating-text { position: fixed; font-weight: bold; font-size: 18px; pointer-events: none; animation: floatUp 1s ease-out forwards; z-index: 10000; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
    @keyframes floatUp { 0% { transform: translateY(0) scale(1); opacity: 1; } 100% { transform: translateY(-50px) scale(1.3); opacity: 0; } }
    /* Cursor hints */
    .fish, .plant, .tree, .city, .factory, .sun, .cloud, .car { cursor: pointer; transition: filter 0.3s; }
    .fish:hover, .plant:hover, .tree:hover, .city:hover, .factory:hover, .sun:hover, .cloud:hover, .car:hover { filter: drop-shadow(0 0 10px rgba(255,255,255,0.8)) brightness(1.2); }
"""

interactive_js = """
// Audio Synthesizer
function playClickSound() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gainNode = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(600, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0.1, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
        osc.connect(gainNode);
        gainNode.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.1);
    } catch(e) {}
}

function createFloatingText(e, text, color) {
    let ft = document.createElement("div");
    ft.className = "floating-text";
    ft.innerText = text;
    ft.style.left = e.clientX + "px";
    ft.style.top = e.clientY + "px";
    ft.style.color = color || "white";
    document.body.appendChild(ft);
    setTimeout(() => ft.remove(), 1000);
}

document.addEventListener("click", function(e) {
    if(e.target.closest('.btn') || e.target.closest('.card') || e.target.closest('.back-btn')) {
        playClickSound();
    }
    let ripple = document.createElement("div");
    ripple.className = "ripple";
    ripple.style.left = (e.clientX - 20) + "px";
    ripple.style.top = (e.clientY - 20) + "px";
    ripple.style.width = "40px";
    ripple.style.height = "40px";
    document.body.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
});
"""

files = ['index.html', 'pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Avoid duplicate injections
    if "/* INTERACTIVE CSS */" in html:
        continue
        
    html = html.replace("</style>", interactive_css + "\n    </style>")
    
    # Add base JS
    if "</script>" in html:
        html = html.replace("</script>", interactive_js + "\n</script>")
    else:
        html = html.replace("</body>", "<script>\n" + interactive_js + "\n</script>\n</body>")

    # Add specific logic per file
    if "pencemaran air" in file:
        specific_js = """
document.querySelectorAll('.fish').forEach(el => {
    el.addEventListener('click', (e) => {
        let rv = document.getElementById('river');
        if(rv.classList.contains('foam')) createFloatingText(e, "Perih! 🫧", "#ff9999");
        else if(rv.classList.contains('plastic')) createFloatingText(e, "Tersedak! 🗑️", "#ff9999");
        else if(rv.classList.contains('green')) createFloatingText(e, "Pusing... 🤢", "#a8e6cf");
        else createFloatingText(e, "Segar! 🐟", "#99ccff");
    });
});
"""
        html = html.replace("</script>", specific_js + "\n</script>")

    elif "pencemaran tanah" in file:
        specific_js = """
document.querySelectorAll('.plant, .tree, .worm').forEach(el => {
    el.addEventListener('click', (e) => {
        let ld = document.querySelector('.land');
        if(ld.classList.contains('polluted')) createFloatingText(e, "Layu... 🥀", "#ffb347");
        else createFloatingText(e, "Subur! 🌱", "#77dd77");
    });
});
"""
        html = html.replace("</script>", specific_js + "\n</script>")

    elif "pencemaran udara" in file:
        specific_js = """
document.querySelectorAll('.city, .car, .factory, .sun, .cloud, .tree').forEach(el => {
    el.addEventListener('click', (e) => {
        let sim = document.getElementById('simulation');
        if(sim.classList.contains('polluted')) createFloatingText(e, "Uhuk uhuk! 😷", "#ff9999");
        else if(sim.classList.contains('firebg')) createFloatingText(e, "Panas! 🔥", "#ffb347");
        else createFloatingText(e, "Udara sejuk! 🌬️", "#84b6f4");
    });
});
"""
        html = html.replace("</script>", specific_js + "\n</script>")
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Interactive features added successfully!")

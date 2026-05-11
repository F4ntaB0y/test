import re

with open('pencemaran udara.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS
css_udara = """
        /* NEW POLLUTION UDARA CSS */
        .smoke { position: absolute; border-radius: 50%; background: rgba(30,41,59,0.6); filter: blur(15px); pointer-events: none; transition: 0.5s; }
        .factory-smoke { width: 100px; height: 100px; }
        .fs1 { left: 100px; bottom: 230px; animation: smoke-rise 4s infinite ease-out; }
        .fs2 { left: 150px; bottom: 300px; animation: smoke-rise 4s infinite 1.2s ease-out; }
        .fs3 { left: 200px; bottom: 360px; animation: smoke-rise 4s infinite 2.4s ease-out; }
        @keyframes smoke-rise { 0% { transform: translateY(0) scale(0.5); opacity: 0.8; } 100% { transform: translateY(-150px) scale(2); opacity: 0; } }

        .car-smoke-container { position: absolute; left: -20px; bottom: 10px; width: 40px; height: 40px; opacity: 0; transition: 0.5s; pointer-events: none; }
        .cs { position: absolute; background: rgba(30,41,59,0.8); border-radius: 50%; width: 20px; height: 20px; filter: blur(5px); animation: car-smoke-puff 1.5s infinite; }
        .cs1 { left: 0; animation-delay: 0s; }
        .cs2 { left: -10px; bottom: 5px; animation-delay: 0.5s; }
        .cs3 { left: -5px; bottom: -5px; animation-delay: 1s; }
        @keyframes car-smoke-puff { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(3) translateX(-20px) translateY(-10px); opacity: 0; } }

        .active-pollution { opacity: 1 !important; }
    </style>
"""

# Replace existing .smoke css
html = re.sub(r'\.smoke \{ position: absolute;.*?@keyframes smoke \{.*?\}', '', html, flags=re.DOTALL)
html = html.replace('    </style>', css_udara)

# 2. Update HTML
html = html.replace("""        <!-- ASAP -->
        <div class="smoke s1"></div>
        <div class="smoke s2"></div>
        <div class="smoke s3"></div>""", """        <!-- ASAP PABRIK -->
        <div id="factory-smoke-group" style="opacity: 0; transition: 1s;">
            <div class="smoke factory-smoke fs1"></div>
            <div class="smoke factory-smoke fs2"></div>
            <div class="smoke factory-smoke fs3"></div>
        </div>""")

html = html.replace("""            <!-- MOBIL -->
            <div class="car">

                <div class="wheel w1"></div>
                <div class="wheel w2"></div>

            </div>""", """            <!-- MOBIL -->
            <div class="car">
                <div class="car-smoke-container" id="car-smoke-group">
                    <div class="cs cs1"></div><div class="cs cs2"></div><div class="cs cs3"></div>
                </div>
                <div class="wheel w1"></div>
                <div class="wheel w2"></div>
            </div>""")

# 3. Update JS
js_udara = """
function clearAirPollution() {
    document.getElementById("factory-smoke-group").classList.remove("active-pollution");
    document.getElementById("car-smoke-group").classList.remove("active-pollution");
}
"""

html = html.replace("function kendaraan(){", js_udara + "\nfunction kendaraan(){\n    clearAirPollution();\n    document.getElementById('car-smoke-group').classList.add('active-pollution');")
html = html.replace("function pabrik(){", "function pabrik(){\n    clearAirPollution();\n    document.getElementById('factory-smoke-group').classList.add('active-pollution');")
html = html.replace("function kebakaran(){", "function kebakaran(){\n    clearAirPollution();")
html = html.replace("function penghijauan(){", "function penghijauan(){\n    clearAirPollution();")

with open('pencemaran udara.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Udara animations added!")

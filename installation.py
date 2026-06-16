"""Section 3 — Installation & activation."""

content = r"""
<div id="installation" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-screwdriver-wrench" style="color: var(--gold); margin-right: 10px;"></i>15-minute plug-and-play installation</h2>
        <p>One installer can equip <strong style="color:#F4C95D;">3–4 vehicles per hour</strong>. A 200-truck fleet deploys in a week; a 1,000-truck fleet in a month.</p>
    </div>

    <h3 class="section-header fade-up">The 5-step universal install</h3>
    <div class="card fade-up">
        <div class="pipeline-container">
            <div class="pipeline-line"></div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-plug"></i></div>
                <div class="pipeline-title">Step 1 — 2 min</div>
                <div class="pipeline-desc">Plug into OBD-II / J1939 / FMS port. Power + vehicle data from one connection.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-wind"></i></div>
                <div class="pipeline-title">Step 2 — 5 min</div>
                <div class="pipeline-desc">Windshield mount with standard bracket. Centre the camera below the rearview.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-crosshairs"></i></div>
                <div class="pipeline-title">Step 3 — 3 min</div>
                <div class="pipeline-desc">AI auto-calibrates to the windshield angle. No manual ADAS tuning needed.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-tower-cell"></i></div>
                <div class="pipeline-title">Step 4 — 2 min</div>
                <div class="pipeline-desc">Embedded cellular auto-connects (or insert your SIM if using own connectivity).</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-circle-check"></i></div>
                <div class="pipeline-title">Step 5 — 3 min</div>
                <div class="pipeline-desc">Open the CMS, confirm livestream, GPS, and first AI event. Vehicle is operational.</div>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Vehicle-type install playbooks</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-truck" style="color: var(--gold);"></i> Long-haul tractor</h4>
            <ul class="checklist">
                <li><strong>Front-facing</strong> — windshield, centred</li>
                <li><strong>Driver DMS</strong> — C29N on A-pillar at eye level for sunglasses + low-light coverage</li>
                <li><strong>Side cameras</strong> — wing mirror housings</li>
                <li><strong>Rear</strong> — top of cab, facing trailer connection</li>
                <li><strong>Recommended config</strong> — AD Plus 3.0 (5CH) or MDVR + 5 cameras</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-bus" style="color: var(--purple);"></i> City bus / transit</h4>
            <ul class="checklist">
                <li><strong>Forward</strong> — above driver, behind windshield</li>
                <li><strong>Driver DMS</strong> — dashboard or A-pillar mount</li>
                <li><strong>Door cameras</strong> — at each entry/exit, IR for low-light</li>
                <li><strong>Interior</strong> — front, mid, rear ceiling coverage</li>
                <li><strong>Recommended config</strong> — MDVR (12CH) + driver console</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-taxi" style="color: var(--gold);"></i> Taxi / rideshare</h4>
            <ul class="checklist">
                <li><strong>Forward + interior dual</strong> — combined unit, dash-mounted</li>
                <li><strong>Passenger panic button</strong> — accessible in rear seat</li>
                <li><strong>Recommended config</strong> — C6 Lite 3.0 (3CH)</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-mountain" style="color: var(--purple);"></i> Mining haul truck</h4>
            <ul class="checklist">
                <li><strong>Mining MDVR (M10)</strong> — hardened for vibration, dust, -40 to +85 °C, 4TB storage</li>
                <li><strong>AVM 360°</strong> — 6 HD cameras, surround view</li>
                <li><strong>Bucket-area</strong> — tooth-loss detection, large-block detection</li>
                <li><strong>DMS for PPE</strong> — algorithm tuned for helmets, masks, reflective vests, safety glasses</li>
            </ul>
        </div>
    </div>

    <h3 class="section-header fade-up">First-boot verification checklist</h3>
    <div class="card fade-up">
        <p>Before you mark a vehicle "deployed," walk through these checks in your CMS:</p>
        <div class="grid-2">
            <ul class="checklist">
                <li><strong>Device online</strong> — green status indicator in <em>CMS → Fleet → [vehicle]</em></li>
                <li><strong>Livestream loads</strong> — every camera channel returns video within 10 seconds</li>
                <li><strong>GPS lock</strong> — vehicle pin on the map, current location within 10m</li>
                <li><strong>Time sync</strong> — timestamp on video matches your timezone</li>
            </ul>
            <ul class="checklist">
                <li><strong>Fire a test event</strong> — wave your hand near the DMS lens, confirm a "distraction" event appears within 60 seconds</li>
                <li><strong>Audio test</strong> — send a TTS message from the CMS to the camera speaker</li>
                <li><strong>Storage health</strong> — eMMC card recognised, &gt; 80% available</li>
                <li><strong>Firmware version</strong> — confirm latest in <em>CMS → Devices → Firmware</em></li>
            </ul>
        </div>
    </div>

    <h3 class="section-header fade-up">Sensor gateway — what you can connect</h3>
    <div class="card fade-up">
        <p>The camera/MDVR is the central data hub. Connect via Bluetooth, RS-232, or I/O — all sensor data flows through <strong>one cellular connection</strong>:</p>
        <table class="stmx-table">
            <thead><tr><th>Sensor</th><th>Use case</th></tr></thead>
            <tbody>
                <tr><td><strong>TPMS</strong> (tire pressure)</td><td>Blowout prevention, fuel efficiency, compliance</td></tr>
                <tr><td><strong>Fuel monitoring</strong></td><td>Theft detection, efficiency, cost management</td></tr>
                <tr><td><strong>Temperature &amp; humidity</strong></td><td>Cold-chain, perishables, pharmaceutical</td></tr>
                <tr><td><strong>Door sensors</strong></td><td>Unauthorised access, delivery verification</td></tr>
                <tr><td><strong>RFID / iButton</strong></td><td>Driver authentication, cargo tags, chain of custody</td></tr>
                <tr><td><strong>Alcohol breathalyser</strong></td><td>Pre-trip testing, zero-tolerance enforcement</td></tr>
                <tr><td><strong>PTO (Power Take-Off)</strong></td><td>Equipment usage, idle time, job costing</td></tr>
            </tbody>
        </table>
    </div>

    <h3 class="section-header fade-up">Common installation pitfalls</h3>
    <div class="card fade-up" style="border-left: 4px solid #fbbf24;">
        <div class="grid-2">
            <div>
                <h4 style="color: #fbbf24;"><i class="fa-solid fa-triangle-exclamation"></i> Mounting too high</h4>
                <p style="font-size: 0.9rem;">If the windshield-DMS lens sits above brow height, drowsy-driver detection fails when the head dips. Mount centred and low, or use C29N on the A-pillar.</p>
            </div>
            <div>
                <h4 style="color: #fbbf24;"><i class="fa-solid fa-triangle-exclamation"></i> Skipping the auto-calibration</h4>
                <p style="font-size: 0.9rem;">Drivers shouldn't move the vehicle for the first 3 minutes after power-on. Movement during calibration produces lane-departure false positives.</p>
            </div>
            <div>
                <h4 style="color: #fbbf24;"><i class="fa-solid fa-triangle-exclamation"></i> SIM not activated</h4>
                <p style="font-size: 0.9rem;">Cameras boot and record locally even without cellular. They just don't reach the cloud. Always verify "online" status in CMS before signing off the install.</p>
            </div>
            <div>
                <h4 style="color: #fbbf24;"><i class="fa-solid fa-triangle-exclamation"></i> Loose OBD-II connection</h4>
                <p style="font-size: 0.9rem;">Engine vibration can work an OBD-II plug loose over time. Use the supplied locking clip or a hard-wire harness for trucks operating in heavy vibration.</p>
            </div>
        </div>
    </div>

</div>
"""

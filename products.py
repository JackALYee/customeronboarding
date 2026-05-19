"""Section 2 — My Products: the Streamax portfolio."""

content = r"""
<div id="products" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-box" style="color: var(--primary-green); margin-right: 10px;"></i>Your Streamax product portfolio</h2>
        <p>Streamax is the only company in the world offering <strong style="color:#2AF598;">three commercial-vehicle product lines from a single source</strong>: video telematics, visibility assistance, and asset protection. Find your device below — every spec, channel count, and platform compatibility note is here.</p>
    </div>

    <h3 class="section-header fade-up">Line 1 — Video Telematics (AI dashcams + MDVRs)</h3>
    <div class="card fade-up">
        <p>The core safety platform. AI dashcams ship in four tiers; MDVRs cover 5–24 channel configurations.</p>
        <h4 style="margin-top: 20px;">2026 Dashcam lineup</h4>
        <table class="stmx-table">
            <thead><tr><th>Model</th><th>Channels</th><th>SafeGPT</th><th>CAN bus</th><th>NPU</th><th>Best fit</th></tr></thead>
            <tbody>
                <tr><td><strong>DS100</strong></td><td>2CH</td><td>—</td><td>—</td><td>Entry</td><td>Cost-sensitive light commercial vehicles</td></tr>
                <tr><td><strong>C6 Lite 3.0</strong></td><td>3CH</td><td><span class="badge badge-green">Yes</span></td><td>Optional</td><td>Mid</td><td>LCVs, urban delivery vans, taxi fleets</td></tr>
                <tr><td><strong>AD Plus 3.0</strong></td><td>5CH</td><td><span class="badge badge-green">Yes</span></td><td>Optional</td><td>3.5 TOPS</td><td>Long-haul tractors, structured safety programmes</td></tr>
                <tr><td><strong>AD Max</strong></td><td>6CH</td><td><span class="badge badge-green">Yes</span></td><td>Optional</td><td>Flagship</td><td>Premium fleets, multi-camera enterprise deployments</td></tr>
            </tbody>
        </table>
        <p style="font-size: 0.85rem; color: var(--text-grey); margin-top: 12px;">CAN decode software license activates OBD-II / J1939 / FMS / Split Wire protocols. Same hardware ships globally; regional decode is software-activated. Need 7+ channels? Use an MDVR instead.</p>
    </div>

    <div class="card fade-up">
        <h4>MDVR range — 5 to 24 channels</h4>
        <p>The industry's most comprehensive MDVR range. Typical configurations:</p>
        <div class="grid-4">
            <div class="glass-panel" style="padding: 16px;"><h4 style="font-size: 0.95rem;">Long-haul tractor</h4><p style="font-size: 0.82rem; margin: 0;">5 cameras — front, cab DMS, both sides, rear</p></div>
            <div class="glass-panel" style="padding: 16px;"><h4 style="font-size: 0.95rem;">City bus</h4><p style="font-size: 0.82rem; margin: 0;">12 cameras — forward, driver, interior multi-zone, doors</p></div>
            <div class="glass-panel" style="padding: 16px;"><h4 style="font-size: 0.95rem;">Mining haul truck</h4><p style="font-size: 0.82rem; margin: 0;">8 cameras — surround-view + bucket + cab</p></div>
            <div class="glass-panel" style="padding: 16px;"><h4 style="font-size: 0.95rem;">Cash-in-transit</h4><p style="font-size: 0.82rem; margin: 0;">24-channel — every cargo, vault, and approach angle</p></div>
        </div>
        <p style="margin-top: 14px; font-size: 0.85rem; color: var(--text-grey);">All MDVRs include built-in eMMC storage, Bluetooth IoT gateway, and <strong>Sentry Mode</strong> — quick cold boot on G-sensor impact for hit-and-run evidence capture when parked.</p>
    </div>

    <div class="card fade-up">
        <h4>C29N dedicated DMS camera <span class="badge badge-blue">Recommended add-on</span></h4>
        <p>Most dashcam DMS sits in the windshield lens. When a drowsy driver's head dips forward, the brow ridge covers their eyes from that angle — and sunglasses make it worse.</p>
        <p>The <strong>C29N</strong> mounts on the A-pillar at eye level. <strong>940nm infrared</strong> penetrates sunglasses. <strong>Operates at 0 Lux</strong> in total darkness. Pairs with two-layer fatigue AI: rule-based + deep-learning trained on millions of real fatigue events.</p>
        <p style="font-size: 0.85rem; color: var(--text-grey); margin-top: 10px;"><em>Test from your camera provider: ask them to demonstrate fatigue detection at night with the driver wearing sunglasses. If their camera is windshield-mounted above the driver, you'll have your answer.</em></p>
    </div>

    <h3 class="section-header fade-up">Line 2 — Visibility Assistance (regulatory compliance)</h3>
    <div class="card fade-up">
        <p>Camera-based visibility for the strictest international regulations. All visibility products deploy independently (offline) <strong>or</strong> connect to the Streamax platform — start with offline compliance, add SafeGPT to the same vehicles later.</p>
        <table class="stmx-table">
            <thead><tr><th>Product</th><th>Architecture</th><th>Best-fit</th></tr></thead>
            <tbody>
                <tr><td><strong>C53 BSIS</strong></td><td>AI BSIS dual-lens (side + rear/top-side)</td><td>EU BSIS/MOIS programmes, urban logistics, regulated HGVs</td></tr>
                <tr><td><strong>C46 IPC</strong></td><td>Connected (LAN / MDVR-linked); AI pedestrian/vehicle BSD; remote config</td><td>On-road fleets, premium projects, platform-enabled customers</td></tr>
                <tr><td><strong>C46A AHD</strong></td><td>Lightweight local; USB config; local alarm</td><td>Construction, forklift, agriculture, retrofit — fastest path</td></tr>
                <tr><td><strong>AI-AVM / 360</strong></td><td>4 stitched HD cameras + AI overlay</td><td>Large trucks, construction equipment, premium safety packages</td></tr>
                <tr><td><strong>CM31 / CMS</strong></td><td>Digital mirror (UN R46) + AI VRU detection</td><td>OEM programmes, premium truck safety, 1–3% fuel savings</td></tr>
            </tbody>
        </table>
        <h4 style="margin-top: 24px;">Regulatory compliance covered</h4>
        <div class="grid-3">
            <div class="glass-panel">
                <h4 style="font-size: 0.95rem;">London DVS / PSS</h4>
                <p style="font-size: 0.82rem;">Front, side, rear VRU detection cameras fully certified.</p>
            </div>
            <div class="glass-panel">
                <h4 style="font-size: 0.95rem;">EU GSR2 (R151/R155/R158)</h4>
                <p style="font-size: 0.82rem;">ADAS &amp; visibility meeting EU type-approval for new vehicles.</p>
            </div>
            <div class="glass-panel">
                <h4 style="font-size: 0.95rem;">UN R46 — CMS</h4>
                <p style="font-size: 0.82rem;">Legal mirror-replacement Camera Monitor System with simultaneous AI VRU detection.</p>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Line 3 — Asset Protection (cargo &amp; vehicle security)</h3>
    <div class="grid-2 fade-up">
        <div class="card">
            <h4><i class="fa-solid fa-trailer" style="color: var(--primary-green);"></i> Z5 Trailer Camera</h4>
            <p>Standalone trailer-mounted device with its own cellular + GPS. The trailer becomes an independently trackable, monitorable asset — even when disconnected from the tractor.</p>
            <ul class="checklist">
                <li><strong>Trailer GPS tracking</strong> — real-time location of unpowered trailer</li>
                <li><strong>Security camera</strong> — activates on suspicious door opening</li>
                <li><strong>Load capacity sensing</strong> — remaining volume, dwell time, cargo fixture status</li>
            </ul>
            <p style="font-size: 0.82rem; color: var(--text-grey); margin-top: 10px;"><em>Limitation: no refrigerated trailer support yet.</em></p>
        </div>
        <div class="card">
            <h4><i class="fa-solid fa-shield-halved" style="color: var(--secondary-blue);"></i> Sentinel Camera <span class="badge badge-amber">NEW — June 2026</span></h4>
            <p>First-of-its-kind standalone exterior camera for fuel tank, cargo hold, and toolbox monitoring. Built-in cellular, storage, GPS, AI suspicious-movement detection.</p>
            <ul class="checklist">
                <li><strong>Blacklight Ultra (0.02 LUX)</strong> — clear colour video in near pitch-black</li>
                <li><strong>No cable to cab</strong> — connect to nearest power supply</li>
                <li><strong>Multi-unit</strong> — multiple Sentinels per vehicle, all merging on FT Cloud</li>
            </ul>
        </div>
    </div>

    <div class="card fade-up">
        <h4><i class="fa-solid fa-user-shield" style="color: var(--primary-green);"></i> Driver identity &amp; vehicle immobilisation</h4>
        <p><strong>Continuous facial recognition</strong> — AI compares the driver against their authorised profile in real time. Instant unauthorised-driver detection. <em>No other video telematics vendor offers this.</em></p>
        <p><strong>Vehicle immobilisation relay</strong> — detected unauthorised driver → relay activates → vehicle immobilised remotely. Moves from "detect and report" to "detect and PREVENT."</p>
        <p><strong>Driver distress response</strong> — panic button, two-way covert audio, real-time GPS + video during the incident.</p>
        <p style="font-size: 0.82rem; color: var(--text-grey); margin-top: 10px;"><em>Honest limitation: during a hijacking, criminal groups use cellular jammers — real-time alerts, panic, immobilisation, and GPS are all blocked. The MDVR records locally so evidence is preserved for post-event recovery. This affects every cellular-dependent security system, not just Streamax.</em></p>
    </div>

    <h3 class="section-header fade-up">The "one-device revolution" — why Streamax replaces your tracker</h3>
    <div class="card fade-up">
        <p>Traditionally, video telematics + GPS tracking required <strong>two devices</strong>: a separate tracker plus a separate camera. Two installations, two cellular plans, two points of failure.</p>
        <p>Streamax cameras now read native vehicle data via <strong>CAN bus / OBD-II / J1939 / FMS</strong>. One camera does everything:</p>
        <table class="stmx-table">
            <thead><tr><th>Capability</th><th>Traditional (2 devices)</th><th>Streamax (1 camera)</th></tr></thead>
            <tbody>
                <tr><td>Video AI (ADAS + DMS)</td><td>Camera</td><td>Built in</td></tr>
                <tr><td>GPS tracking &amp; trip recording</td><td>Tracker</td><td>Built in</td></tr>
                <tr><td>Vehicle ECU data (speed, RPM, fuel, fault codes)</td><td>Tracker via J1939</td><td>Built in — native CAN</td></tr>
                <tr><td>Sensor gateway (TPMS, fuel, temp, door, RFID)</td><td>Separate hub</td><td>Built in</td></tr>
                <tr><td>Cellular plans</td><td>2–3</td><td>1</td></tr>
                <tr><td>Installation</td><td>2 mounts, 2 wiring jobs</td><td>1 cable, 15 min</td></tr>
            </tbody>
        </table>
    </div>

</div>
"""

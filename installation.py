"""Section 3 — Installation.

Per-product installation hub: grouped by the same product lines as My
Products. Each product is an accordion with (1) an installation video
placeholder, (2) an interactive step-through install guide, and (3) an
interactive verification checklist.

Guides are grounded in the products' own spec sheets where available (the
dashcam flow is taken from the AD Plus 2.0 spec — OBD/ACC power box,
windshield bracket, dual Micro-SD + industrial Nano SIM, Wi-Fi AP via the
function button, video-output cable for IPC/AHD/display, ADAS auto-cal).
Where model-specific install detail isn't available, the guide is left as a
placeholder for that product.
"""

# ── guide library: key -> {steps:[(title, detail)], check:[...]} ──────────
_GENERIC_CHECK = [
    "Device powered — status LED normal",
    "Mounted securely at the correct position and angle",
    "All channels / data visible in the CMS",
    "GPS lock confirmed (if equipped)",
    "A test event / detection was verified",
    "Firmware on the latest version",
]

GUIDES = {
    "adplus": {
        "steps": [
            ("Insert storage & SIM",
             "Open the side cover. Insert up to two Micro SD cards (Class 10+, up to 1 TB each) and one <strong>industrial Nano SIM (MP2)</strong> — do not use a consumer MP1 SIM."),
            ("Choose a power method",
             "Connect the Power Box, then pick one: <strong>OBD plug-and-play</strong> (16-PIN or 9-PIN OBD power cable) for the fastest install, or the <strong>open-wire ACC cable</strong> (POWER, GND, ACC, CAN-H, CAN-L + sensor I/O) to hard-wire. 12 V / 24 V self-adaptive."),
            ("Mount on the windshield",
             "Wipe the glass with the alcohol pad, fit the camera to the bracket, and press it centred just below the rear-view mirror. Tighten with the hex wrench so the road-facing lens sits level."),
            ("Connect optional cameras / devices",
             "Use the video-output cable for an extra AHD camera, an IPC camera, or a display. R-Watch and iButton connect at the Power Box. Note: the AHD channel carries no audio and an external display can't preview the IPC channel."),
            ("Power on & set Wi-Fi",
             "Start the vehicle — the Power LED turns green. To put Wi-Fi into AP mode for local setup, press the <strong>Function button twice within 2 seconds</strong>."),
            ("Calibrate & verify",
             "Keep the vehicle stationary for ~3 minutes while ADAS auto-calibrates to the windshield angle. Then confirm livestream, GPS lock, and a test AI event in the CMS."),
        ],
        "check": [
            "Two Micro SD cards seated; SIM is industrial (MP2)",
            "Power LED green; 12/24 V detected",
            "Camera centred and level below the mirror",
            "Every connected channel shows video in the CMS",
            "GPS pin within ~10 m of actual location",
            "Test distraction/ADAS event appears within 60 s",
            "Firmware on latest (CMS → Devices → Firmware)",
        ],
    },
    "dashcam": {
        "steps": [
            ("Insert storage & SIM", "Insert the Micro SD card(s) (Class 10+) and an industrial Nano SIM."),
            ("Connect the Power Box", "Use OBD plug-and-play (16/9-PIN) for speed, or hard-wire the ACC cable (POWER / GND / ACC). 12/24 V self-adaptive."),
            ("Mount on the windshield", "Clean the glass, fit the bracket, and press the camera centred below the mirror. Level the road-facing lens."),
            ("Connect extra channels", "Attach any optional AHD/IPC camera or display via the video cable, if your configuration uses them."),
            ("Power on & set Wi-Fi", "Start the vehicle; the Power LED turns green. Double-press the function button to enter Wi-Fi AP mode for local setup."),
            ("Calibrate & verify", "Hold stationary ~3 min for ADAS auto-calibration, then verify livestream, GPS, and a test event in the CMS."),
        ],
        "check": _GENERIC_CHECK,
    },
    "dcmax": {
        "steps": [
            ("Install the GT1 Pro first", "DC Max deploys only as a pair with the GT1 Pro gateway — power and data route through it. Install the gateway before the camera."),
            ("Insert storage & connect", "Insert the Micro SD card(s) and connect DC Max to the GT1 Pro per the supplied harness."),
            ("Mount on the windshield", "Clean the glass and press the camera centred below the mirror; level the lens."),
            ("Power on", "Start the vehicle and confirm the GT1 Pro gateway comes online on the platform."),
            ("Calibrate & verify", "Keep stationary ~3 min for ADAS calibration; verify all channels, GPS, and events in the CMS."),
        ],
        "check": _GENERIC_CHECK,
    },
    "gateway": {
        "steps": [
            ("Connect to the diagnostic port", "Locate the OBD-II / J1939 port and connect the GT1 Pro power+data harness."),
            ("Mount the gateway", "Fix it in a dry, vibration-stable spot under the dash with the supplied bracket."),
            ("Insert SIM & pair camera", "Insert the industrial SIM and connect the paired DC Max camera."),
            ("Power on & register", "Start the vehicle; confirm the gateway registers on the platform (currently USA market only)."),
            ("Verify vehicle data", "Confirm speed, RPM, fuel, and fault-code data is flowing into the CMS."),
        ],
        "check": _GENERIC_CHECK,
    },
    "powerbox": {
        "steps": [
            ("Power down the dashcam", "Disconnect the AD Plus 2.0 from its standard power box."),
            ("Swap in the expansion box", "Replace the standard power box with the PBM (adds 2 channels + CAN) or PBP (adds CAN only)."),
            ("Wire CAN", "Connect CAN-H / CAN-L to the vehicle bus (OBD-II / J1939) per the harness. For PBM, also connect the two extra cameras."),
            ("Reconnect & power on", "Reconnect to the AD Plus 2.0 and start the vehicle."),
            ("Verify", "Confirm CAN data (and the extra channels for PBM) appear in the CMS."),
        ],
        "check": [
            "Expansion box replaces the standard box",
            "CAN-H / CAN-L wired to the vehicle bus",
            "PBM: both extra cameras show video",
            "Vehicle CAN data visible in the CMS",
        ],
    },
    "mdvr": {
        "steps": [
            ("Mount the recorder", "Fix the MDVR in a secure, ventilated spot (under-seat / cabinet). Insert storage (SD/HDD per model)."),
            ("Connect the cameras", "Wire each camera to its labelled channel (AHD/IPC), plus the DMS camera (C29N) and any aux cams (CA20S, C40W)."),
            ("Wire power", "Connect ACC, +B (battery), and GND; add CAN / OBD if used."),
            ("Antennas & SIM", "Insert the SIM and connect the GPS and 4G antennas with a clear sky view."),
            ("Power on & verify", "Start the vehicle; confirm every channel shows video, GPS lock, and online status in the CMS."),
        ],
        "check": _GENERIC_CHECK,
    },
    "bsd_connected": {
        "steps": [
            ("Mount the camera", "Fix the camera at the blind-spot position (side / rear) at the height given in the spec sheet."),
            ("Wire or link to host", "C53 (standalone): wire power + alarm output. C46 (IPC): connect to the MDVR via LAN/AHD."),
            ("Aim the lens", "Angle the lens to cover the target blind zone and lock the bracket."),
            ("Power on & configure", "Power on; for connected models, set the detection zone remotely (OTA)."),
            ("Test detection", "Walk a person through the zone and confirm a BSD alert fires."),
        ],
        "check": _GENERIC_CHECK,
    },
    "bsd_standalone": {
        "steps": [
            ("Mount the camera", "Fix the camera at the specified blind-spot position and angle."),
            ("Connect power, display & alarm", "Wire to vehicle power, the in-cab display, and the audible alarm (AHD)."),
            ("Aim & secure", "Angle to cover the blind zone and tighten the bracket."),
            ("Power on", "Confirm a live image on the display."),
            ("Test detection", "Walk through the zone to confirm the alert."),
        ],
        "check": _GENERIC_CHECK,
    },
    "bsd_kit": {
        "steps": [
            ("Mount the kit cameras", "Fix each camera at its designated position."),
            ("Connect the harness", "Connect the kit harness to the host channels (AD Plus 2.0 / MDVR)."),
            ("Route & power", "Route and secure the cabling, then power on."),
            ("Configure & verify", "Set detection and confirm all kit channels in the CMS."),
            ("Test zones", "Walk through each detection zone to confirm alerts."),
        ],
        "check": _GENERIC_CHECK,
    },
    "dms": {
        "steps": [
            ("Mount on the A-pillar", "Mount the C29N on the A-pillar at the driver's eye level so the lens isn't blocked when the head dips forward."),
            ("Connect to the host", "Wire the C29N to the host's DMS/AHD input per the harness."),
            ("Aim at the driver", "Point at the driver's face; the 940 nm IR sees through sunglasses and works at 0 Lux, so a clear line of sight is all that's needed."),
            ("Power on", "Confirm the DMS channel appears in the CMS."),
            ("Test", "Cover the lens or simulate a look-away / yawn to trigger a DMS event."),
        ],
        "check": [
            "Mounted on the A-pillar at eye level",
            "DMS channel shows the driver in the CMS",
            "Clear line of sight to the face",
            "Test DMS event (distraction/fatigue) fires",
        ],
    },
    "aux_cam": {
        "steps": [
            ("Mount the camera", "Fix the auxiliary camera at the target view (cabin / side / rear)."),
            ("Connect to a channel", "Wire it to a free AHD channel on the MDVR or AD Plus 2.0."),
            ("Route & secure", "Route and secure the cabling."),
            ("Power on & verify", "Confirm the channel shows video in the CMS."),
        ],
        "check": _GENERIC_CHECK,
    },
    "ibutton": {
        "steps": [
            ("Mount the reader", "Fix the iButton reader within the driver's reach."),
            ("Connect to the host", "Wire the reader to the host's iButton lead (on the Power Box)."),
            ("Register keys", "Power on and register driver iButton keys in the CMS."),
            ("Test", "Tap a key and confirm the driver is identified in the log."),
        ],
        "check": [
            "Reader mounted within reach",
            "Wired to the host iButton port",
            "Driver keys registered in the CMS",
            "Tap logs the correct driver",
        ],
    },
    "asset_trailer": {
        "steps": [
            ("Mount on the trailer", "Fix the Z5 with a view of the cargo door. It's standalone — its own cellular + GPS, independent of the tractor."),
            ("Connect power", "Connect to trailer power (or use its internal supply per model)."),
            ("SIM & sky view", "Insert the SIM and ensure a clear sky view for GPS."),
            ("Power on", "Confirm the trailer appears on the map with a GPS fix."),
            ("Test door event", "Open the cargo door to confirm a door-open event and clip."),
        ],
        "check": [
            "Mounted with a clear cargo-door view",
            "Powered (trailer or internal supply)",
            "Trailer shows on the map with GPS",
            "Door-open event/clip captured",
        ],
    },
    # placeholder — interactive guide not yet available for this product
    "placeholder": None,
}

GROUPS = [
    {"group": "AI Dashcams", "icon": "fa-solid fa-video", "items": [
        ("AD Plus 2.0", "adplus"), ("AD Max", "dashcam"), ("C6 Lite 2.0", "dashcam"), ("DC Max", "dcmax")]},
    {"group": "Telematics Gateway", "icon": "fa-solid fa-tower-cell", "items": [
        ("GT1 Pro", "gateway")]},
    {"group": "AD Plus 2.0 Accessories", "icon": "fa-solid fa-puzzle-piece", "items": [
        ("PBM (Power Box Max)", "powerbox"), ("PBP (Power Box Plus)", "powerbox")]},
    {"group": "MDVRs", "icon": "fa-solid fa-hard-drive", "items": [
        ("M1N 2.0", "mdvr"), ("F6N", "mdvr"), ("M3N", "mdvr")]},
    {"group": "Visibility / BSD Cameras", "icon": "fa-solid fa-eye", "items": [
        ("C53", "bsd_connected"), ("C46", "bsd_connected"), ("DP7Q", "bsd_standalone"),
        ("DP7Q-T", "bsd_standalone"), ("DP7Q-RT", "bsd_standalone"), ("DP7S", "bsd_standalone"),
        ("DP7S-T", "bsd_standalone"), ("DP12S", "bsd_standalone"), ("C41W", "bsd_standalone"),
        ("CA42 Kit 2.0", "bsd_kit")]},
    {"group": "Accessories", "icon": "fa-solid fa-screwdriver-wrench", "items": [
        ("C29N", "dms"), ("B2", "placeholder"), ("B3", "placeholder"),
        ("C40W", "aux_cam"), ("CA20S", "aux_cam"), ("iButton", "ibutton"), ("R-Watch", "placeholder")]},
    {"group": "Asset Security", "icon": "fa-solid fa-shield-halved", "items": [
        ("Z5", "asset_trailer"), ("Sentinel", "placeholder")]},
]


def _video(name):
    return ('<div class="inst-video"><div class="inst-video-ph">'
            '<i class="fa-brands fa-youtube"></i>'
            f'<span class="inst-video-t">{name} — installation video</span>'
            '<span class="inst-video-s">Coming soon</span></div></div>')


def _stepper(steps):
    if not steps:
        return ('<div class="inst-ph"><i class="fa-solid fa-screwdriver-wrench"></i>'
                'Interactive guide coming soon for this product. Meanwhile, see its user manual under '
                '<a href="javascript:void(0)" onclick="switchTab(\'products\')">My Products</a>.</div>')
    rows = ""
    for i, (t, d) in enumerate(steps, 1):
        rows += (f'<div class="inst-step"><div class="inst-step-top">'
                 f'<span class="inst-step-chk" title="Mark done"></span>'
                 f'<span class="inst-step-no">{i}</span>'
                 f'<span class="inst-step-t">{t}</span>'
                 f'<i class="fa-solid fa-chevron-down inst-step-cv"></i></div>'
                 f'<div class="inst-step-d">{d}</div></div>')
    total = len(steps)
    return ('<div class="inst-guide">'
            f'<div class="inst-prog"><span class="inst-prog-bar"><i></i></span><span class="inst-prog-n">0 / {total} steps</span></div>'
            f'<div class="inst-steps">{rows}</div></div>')


def _checklist(items):
    lis = "".join(f'<label class="inst-check"><span class="inst-cbox"></span><span>{it}</span></label>' for it in items)
    return f'<div class="inst-checklist">{lis}</div>'


def _product(name, guide_key):
    g = GUIDES.get(guide_key)
    steps = g["steps"] if g else None
    check = g["check"] if g else _GENERIC_CHECK
    tag = "Guide + checklist" if steps else "Guide coming soon"
    return (
        '<div class="inst-prod">'
        f'<div class="inst-prod-head"><span class="inst-prod-name">{name}</span>'
        f'<span class="inst-prod-tag">{tag}</span><i class="fa-solid fa-chevron-down inst-prod-cv"></i></div>'
        '<div class="inst-prod-body">'
        '<div class="inst-grid">'
        f'<div class="inst-col"><div class="inst-lbl"><i class="fa-solid fa-play"></i> Installation video</div>{_video(name)}</div>'
        f'<div class="inst-col"><div class="inst-lbl"><i class="fa-solid fa-list-ol"></i> Interactive installation guide</div>{_stepper(steps)}</div>'
        '</div>'
        f'<div class="inst-lbl" style="margin-top:16px;"><i class="fa-solid fa-clipboard-check"></i> Verification checklist</div>{_checklist(check)}'
        '</div></div>'
    )


def _group(g):
    prods = "".join(_product(n, k) for n, k in g["items"])
    return (f'<h3 class="section-header fade-up"><i class="{g["icon"]}" style="color: var(--gold); margin-right: 10px;"></i>{g["group"]}</h3>'
            f'<div class="fade-up">{prods}</div>')


_GROUPS_HTML = "\n".join(_group(g) for g in GROUPS)

content = r"""
<div id="installation" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-screwdriver-wrench" style="color: var(--gold); margin-right: 10px;"></i>Installation</h2>
        <p>Pick your product below. Each one has an <strong>installation video</strong>, a click-through <strong>interactive guide</strong> (tick off each step as you go), and a <strong>verification checklist</strong>. Most devices are 15-minute plug-and-play — one installer can equip 3–4 vehicles an hour.</p>
    </div>

    __GROUPS__

    <style>
        .inst-prod { background: var(--glass-bg); border: var(--glass-border); border-radius: 12px; margin-bottom: 12px; overflow: hidden; }
        .inst-prod-head { display: flex; align-items: center; gap: 12px; padding: 16px 20px; cursor: pointer; transition: var(--transition); }
        .inst-prod-head:hover { background: rgba(255,255,255,0.03); }
        .inst-prod-name { font-weight: 700; color: var(--text-white); font-size: 1.05rem; }
        .inst-prod-tag { font-size: 0.7rem; font-weight: 600; color: var(--gold); background: rgba(244,201,93,0.12); border: 1px solid rgba(244,201,93,0.28); padding: 2px 9px; border-radius: 20px; }
        .inst-prod-cv { margin-left: auto; color: var(--text-grey); font-size: 0.8rem; transition: transform 0.25s ease; }
        .inst-prod.open .inst-prod-cv { transform: rotate(180deg); }
        .inst-prod-body { display: none; padding: 0 20px 20px; }
        .inst-prod.open .inst-prod-body { display: block; }

        .inst-grid { display: grid; grid-template-columns: 1fr 1.3fr; gap: 20px; }
        @media (max-width: 900px) { .inst-grid { grid-template-columns: 1fr; } }
        .inst-lbl { font-size: 0.78rem; font-weight: 700; color: var(--text-grey); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
        .inst-lbl i { color: var(--gold); margin-right: 6px; }

        .inst-video { position: relative; width: 100%; padding-bottom: 56.25%; background: #000; border-radius: 12px; overflow: hidden; }
        .inst-video-ph { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;
            background: radial-gradient(circle at 50% 40%, rgba(160,107,255,0.12), rgba(0,0,0,0.85) 70%); color: #fff; text-align: center; padding: 16px; }
        .inst-video-ph .fa-youtube { font-size: 2.6rem; color: #ff0000; filter: drop-shadow(0 4px 12px rgba(255,0,0,0.4)); }
        .inst-video-t { font-weight: 600; font-size: 0.92rem; }
        .inst-video-s { font-size: 0.74rem; color: #94a3b8; }

        .inst-guide { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; }
        .inst-prog { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
        .inst-prog-bar { flex: 1; height: 6px; border-radius: 4px; background: rgba(255,255,255,0.08); overflow: hidden; }
        .inst-prog-bar i { display: block; height: 100%; width: 0%; background: linear-gradient(90deg, var(--gold), var(--purple)); transition: width 0.3s ease; }
        .inst-prog-n { font-size: 0.74rem; color: var(--text-grey); font-weight: 600; white-space: nowrap; }
        .inst-steps { display: flex; flex-direction: column; gap: 6px; }
        .inst-step { border: 1px solid rgba(255,255,255,0.06); border-radius: 9px; overflow: hidden; }
        .inst-step-top { display: flex; align-items: center; gap: 11px; padding: 10px 12px; cursor: pointer; }
        .inst-step-top:hover { background: rgba(255,255,255,0.03); }
        .inst-step-chk { width: 19px; height: 19px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.22); flex-shrink: 0; cursor: pointer; transition: var(--transition); position: relative; }
        .inst-step.done .inst-step-chk { background: linear-gradient(135deg, var(--gold), var(--purple)); border-color: transparent; }
        .inst-step.done .inst-step-chk::after { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; font-size: 0.6rem; color: #0c0a14; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
        .inst-step-no { font-size: 0.72rem; font-weight: 700; color: var(--gold); }
        .inst-step-t { font-size: 0.9rem; font-weight: 600; color: var(--text-white); flex: 1; }
        .inst-step.done .inst-step-t { color: var(--text-grey); text-decoration: line-through; }
        .inst-step-cv { color: var(--text-grey); font-size: 0.72rem; transition: transform 0.25s ease; }
        .inst-step.open .inst-step-cv { transform: rotate(180deg); }
        .inst-step-d { display: none; padding: 0 12px 12px 42px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; }
        .inst-step.open .inst-step-d { display: block; }
        .inst-step-d strong { color: var(--gold); font-weight: 600; }

        .inst-checklist { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 18px; }
        @media (max-width: 700px) { .inst-checklist { grid-template-columns: 1fr; } }
        .inst-check { display: flex; align-items: flex-start; gap: 10px; font-size: 0.86rem; color: var(--text-grey); cursor: pointer; padding: 5px 0; }
        .inst-cbox { width: 18px; height: 18px; border-radius: 5px; border: 2px solid rgba(255,255,255,0.22); flex-shrink: 0; margin-top: 1px; position: relative; transition: var(--transition); }
        .inst-check.done .inst-cbox { background: linear-gradient(135deg, var(--gold), var(--purple)); border-color: transparent; }
        .inst-check.done .inst-cbox::after { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; font-size: 0.6rem; color: #0c0a14; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
        .inst-check.done span:last-child { color: var(--text-white); text-decoration: line-through; }

        .inst-ph { border: 1px dashed rgba(255,255,255,0.18); border-radius: 12px; padding: 24px; text-align: center; color: var(--text-grey); font-size: 0.88rem; }
        .inst-ph i { display: block; font-size: 1.6rem; color: var(--purple); margin-bottom: 10px; }
        .inst-ph a { color: var(--gold); }
    </style>

    <script>
    (function () {
        var root = document.getElementById('installation');
        if (!root || root.dataset.instInit) return;
        root.dataset.instInit = '1';

        // product accordions
        root.querySelectorAll('.inst-prod-head').forEach(function (h) {
            h.addEventListener('click', function () { h.closest('.inst-prod').classList.toggle('open'); });
        });

        function updateProgress(guide) {
            var steps = guide.querySelectorAll('.inst-step');
            var done = guide.querySelectorAll('.inst-step.done').length;
            var bar = guide.querySelector('.inst-prog-bar i');
            var num = guide.querySelector('.inst-prog-n');
            if (bar) bar.style.width = steps.length ? (done / steps.length * 100) + '%' : '0%';
            if (num) num.textContent = done + ' / ' + steps.length + ' steps';
        }

        // step expand + check
        root.querySelectorAll('.inst-step').forEach(function (step) {
            var top = step.querySelector('.inst-step-top');
            var chk = step.querySelector('.inst-step-chk');
            top.addEventListener('click', function (e) {
                if (e.target === chk) return;
                step.classList.toggle('open');
            });
            chk.addEventListener('click', function (e) {
                e.stopPropagation();
                step.classList.toggle('done');
                updateProgress(step.closest('.inst-guide'));
            });
        });

        // checklist
        root.querySelectorAll('.inst-check').forEach(function (c) {
            c.addEventListener('click', function () { c.classList.toggle('done'); });
        });
    })();
    </script>

</div>
""".replace("__GROUPS__", _GROUPS_HTML)

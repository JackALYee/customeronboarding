"""Section 5 — AI Features (SafeGPT + per-detection guide).

Keeps the SafeGPT overview, then breaks down each AI detection (ADAS + DMS)
as an accordion: short description, a sample-clip video placeholder, and a
real parameter-configuration table.

Detections are grounded in the products' spec sheets + the streamax-knowledge
base (ADAS: FCW/LDW/HMW/PCW/TSR/AEB; DMS: fatigue, distraction, phone,
smoking, seatbelt, yawning, no-driver, lens-covering). Parameter *meanings*
are standard ADAS/DMS config; exact default values aren't in the knowledge
base, so they're noted as set per-model in the CMS (a placeholder for the
specifics). AEB config is a full placeholder — it's safety-critical and set
by Streamax/installer, not user-tunable.
"""

# Each feature: (icon, name, category, description, params)
# params = list of (parameter, what it controls, how to adjust) — or None for placeholder.
_ADAS = [
    ("fa-solid fa-car-burst", "Forward Collision Warning (FCW)", "ADAS",
     "Warns when you're closing on the vehicle ahead too fast for the gap — a likely rear-end. The forward camera estimates time-to-collision and alerts the driver to brake.",
     [("Sensitivity (Low / Med / High)", "How early the warning fires (a longer time-to-collision trips it sooner).", "Raise for cautious fleets; lower to cut nuisance alerts in dense, slow traffic."),
      ("Minimum activation speed", "FCW only runs above this speed.", "Raise it to silence stop-and-go false alarms in city driving."),
      ("Alert modality", "Audio, on-screen, and/or seat vibration.", "Use audio+visual as default; reserve vibration for critical fleets.")]),
    ("fa-solid fa-road-lock", "Lane Departure Warning (LDW)", "ADAS",
     "Detects unintended drift across lane markings without a turn signal — a classic fatigue / distraction tell.",
     [("Minimum activation speed", "LDW is typically off below highway speeds (city lane discipline differs).", "Raise it for highway fleets to avoid urban nuisance alerts."),
      ("Turn-signal suppression", "Don't alert when the driver signals a deliberate lane change.", "Keep ON — it removes most false positives."),
      ("Sensitivity", "How far across the line before it fires.", "Lower to alert only on clear departures.")]),
    ("fa-solid fa-arrows-left-right-to-line", "Headway Monitoring (HMW)", "ADAS",
     "Measures the time gap to the vehicle ahead and warns when following too closely (tailgating).",
     [("Following-time threshold (sec)", "The minimum safe time gap before it warns.", "Raise to enforce a larger buffer; lower if alerts are too frequent in traffic."),
      ("Minimum activation speed", "Tailgating logic only applies above this speed.", "Set to highway speeds for long-haul."),
      ("Sensitivity", "How strictly the gap is judged.", "Tune to your traffic density.")]),
    ("fa-solid fa-person-walking", "Pedestrian Collision Warning (PCW)", "ADAS",
     "Detects pedestrians and cyclists (vulnerable road users) in the vehicle's path — critical in urban and turning scenarios.",
     [("Detection zone / range", "How far ahead and which area is monitored for VRUs.", "Widen for urban delivery; narrow for highway."),
      ("Speed gating", "Active in the low/medium-speed band where VRU strikes happen.", "Keep enabled for city fleets."),
      ("Sensitivity", "Confidence needed to fire.", "Raise in dense pedestrian areas.")]),
    ("fa-solid fa-sign-hanging", "Traffic Sign Recognition (TSR)", "ADAS",
     "Reads speed-limit and key road signs to give context — e.g. flagging overspeed against the posted limit.",
     [("Overspeed margin", "How far above the posted limit before it flags.", "Lower for strict speed policies."),
      ("Sign types enabled", "Which signs are recognised / acted on.", "Enable the set relevant to your routes.")]),
    ("fa-solid fa-hand", "Autonomous Emergency Braking (AEB / CMCS)", "ADAS",
     "Goes beyond warning — automatically brakes to mitigate or avoid a collision at low speed (AEB up to ~30 km/h) using radar-vision fusion. Available only on equipped configurations.",
     None),
]

_DMS = [
    ("fa-solid fa-bed", "Fatigue / Drowsiness", "DMS",
     "Detects eye closure, microsleep and prolonged blinks. Streamax runs two-layer fatigue AI — rule-based plus a deep-learning model trained on millions of real fatigue events — to catch edge cases (small eyes, long lashes). With the C29N DMS at A-pillar eye level (940 nm IR) it works at night and through sunglasses. SafeGPT can flag fatigue 5–15 minutes before the eyes close.",
     [("Sensitivity", "Eye-closure duration / blink pattern that triggers an alert.", "Raise for night / long-haul shifts where fatigue risk is highest."),
      ("Minimum speed", "Only evaluates while the vehicle is moving.", "Keeps it from alerting when parked."),
      ("Alert modality", "Audio, visual, and seat vibration.", "Enable seat vibration for critical drowsiness events.")]),
    ("fa-solid fa-eye-slash", "Distraction", "DMS",
     "Flags eyes or head turned off-road beyond a safe window.",
     [("Gaze-off duration (sec)", "How long the driver may look away before it fires.", "Lower for high-risk routes; raise to reduce nuisance alerts."),
      ("Minimum speed", "Active only above this speed.", "Set so it ignores stops."),
      ("Sensitivity", "How far off-axis counts as distracted.", "Tune to cab geometry.")]),
    ("fa-solid fa-mobile-screen-button", "Phone use", "DMS",
     "Detects handheld phone use and calls while driving.",
     [("Sensitivity / confidence", "Detection confidence needed to log an event.", "Raise to reduce false positives from hand-near-face gestures."),
      ("Minimum speed", "Only while driving.", "Keep enabled above ~5 km/h.")]),
    ("fa-solid fa-smoking", "Smoking", "DMS",
     "Detects smoking in the cab — for company policy and hazardous-cargo safety.",
     [("Sensitivity / confidence", "Confidence needed to flag.", "Raise where false positives are a concern."),
      ("Action", "Alert the driver and/or log silently for review.", "Log-only suits coaching; alert suits zero-tolerance.")]),
    ("fa-solid fa-user-shield", "Seatbelt", "DMS",
     "Detects an unfastened seatbelt while the vehicle is in motion.",
     [("Enable / disable", "Turn the check on per fleet.", "Enable for all on-road fleets."),
      ("Minimum speed", "Only checks once moving.", "Avoids alerts while stationary."),
      ("Alert delay (grace)", "Grace period after moving off before alerting.", "Raise slightly to allow buckling at departure.")]),
    ("fa-solid fa-face-tired", "Yawning", "DMS",
     "Yawning is an early fatigue indicator; counted toward a fatigue escalation rather than alerting on every yawn.",
     [("Count threshold", "How many yawns in a window before escalation.", "Lower for long-haul to catch fatigue earlier."),
      ("Sensitivity", "How clearly a yawn must register.", "Tune to reduce false counts.")]),
    ("fa-solid fa-user-slash", "No driver / Driver absent", "DMS",
     "Detects an empty seat or no face while the vehicle is in gear or moving — unauthorised movement or a removed/blocked camera.",
     [("Trigger condition", "In-gear vs moving.", "Use 'moving' to avoid alerts during loading."),
      ("Minimum speed", "Speed above which absence is an alert.", "Set low for security-sensitive fleets.")]),
    ("fa-solid fa-ban", "Lens covering / obstruction", "DMS",
     "Detects the DMS lens being blocked, taped, or tampered with — protects against drivers defeating the camera.",
     [("Duration threshold (sec)", "How long the lens must be obstructed before flagging.", "Lower to catch tampering quickly; raise to ignore brief glare.")]),
]


def _video(name):
    return ('<div class="aif-video"><div class="aif-video-ph">'
            '<i class="fa-solid fa-circle-play"></i>'
            f'<span class="aif-video-t">{name} — sample clip</span>'
            '<span class="aif-video-s">Coming soon</span></div></div>')


def _params(params):
    if not params:
        return ('<div class="aif-ph"><i class="fa-solid fa-lock"></i>'
                'Parameters for this feature are safety-critical and set by Streamax / your installer per vehicle — they are not user-tunable in the standard CMS.</div>')
    rows = "".join(
        f'<tr><td><strong>{p}</strong></td><td>{c}</td><td>{a}</td></tr>' for p, c, a in params)
    return ('<table class="stmx-table"><thead><tr><th>Parameter</th><th>What it controls</th><th>How to adjust</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>'
            '<p class="aif-note"><i class="fa-solid fa-circle-info"></i> Set these in <em>CMS → AI Settings</em>. Exact default values and ranges vary by camera model — check the device config; this guide explains what each parameter means.</p>')


def _feature(icon, name, cat, desc, params):
    badge = ('<span class="aif-cat aif-adas">ADAS</span>' if cat == "ADAS"
             else '<span class="aif-cat aif-dms">DMS</span>')
    return (
        '<div class="aif-feat">'
        f'<div class="aif-feat-head"><i class="{icon} aif-feat-icon"></i>'
        f'<span class="aif-feat-name">{name}</span>{badge}'
        '<i class="fa-solid fa-chevron-down aif-feat-cv"></i></div>'
        '<div class="aif-feat-body">'
        f'<p class="aif-desc">{desc}</p>'
        '<div class="aif-grid">'
        f'<div><div class="aif-lbl"><i class="fa-solid fa-play"></i> Sample clip</div>{_video(name)}</div>'
        f'<div><div class="aif-lbl"><i class="fa-solid fa-sliders"></i> Configure parameters</div>{_params(params)}</div>'
        '</div></div></div>'
    )


_FEATURES_HTML = (
    '<h3 class="section-header fade-up"><i class="fa-solid fa-road" style="color: var(--gold); margin-right: 10px;"></i>ADAS — forward-facing detections</h3>'
    '<div class="fade-up">' + "".join(_feature(*f) for f in _ADAS) + '</div>'
    '<h3 class="section-header fade-up"><i class="fa-solid fa-user" style="color: var(--gold); margin-right: 10px;"></i>DMS — driver-facing detections</h3>'
    '<div class="fade-up">' + "".join(_feature(*f) for f in _DMS) + '</div>'
)

content = r"""
<div id="ai-features" class="content-section hidden">

    <div class="card fade-up" style="background: linear-gradient(135deg, rgba(244,201,93,0.06), rgba(160,107,255,0.04));">
        <h2><i class="fa-solid fa-robot" style="color: var(--gold); margin-right: 10px;"></i>SafeGPT — cloud behavioral intelligence</h2>
        <p style="font-size: 1.05rem; color: #e2e8f0;">
            Most cameras <em>detect events</em>. SafeGPT <em>understands behavior</em>. The difference is whether the fatigued driver gets pulled over before the crash, or whether the crash gets recorded for the insurance claim.
        </p>
    </div>

    <h3 class="section-header fade-up">The problem SafeGPT solves</h3>
    <div class="card fade-up">
        <p>A 200-truck fleet running traditional cameras generates <strong>500–1,000 alerts per day</strong>. Most are false positives — a pothole, a mirror glance, a shadow.</p>
        <p>The safety manager reviews everything on Monday, skims on Wednesday, ignores by Friday. The fleet paid for cameras but didn't get safety. <strong>SafeGPT changes the architecture.</strong></p>
        <p>Instead of firing an alert for every individual event on-device, the camera streams rich behavioral metadata every second — speed, G-sensor, lane position, following distance, gaze direction, blink rate, vehicle CAN data — to the cloud. SafeGPT analyses all these streams together, identifying behavioral patterns no single sensor can detect alone.</p>
    </div>

    <h3 class="section-header fade-up">Six core SafeGPT capabilities</h3>
    <div class="card fade-up">
        <table class="stmx-table">
            <thead><tr><th>Capability</th><th>How it works</th><th>What your fleet gets</th></tr></thead>
            <tbody>
                <tr><td><strong>90% event reduction</strong></td><td>Only alerts when combined behavioral patterns indicate genuine risk — not individual sensor triggers</td><td>10–20 critical events/day, not 500 noise alerts. Reviews take 20 min, not 3 hours.</td></tr>
                <tr><td><strong>Early fatigue detection</strong></td><td>Correlates lane-position degradation + speed oscillation + blink-rate changes + steering input variance</td><td>Detects fatigue <strong>5–15 minutes before</strong> the driver's eyes close. Intervention while still safe.</td></tr>
                <tr><td><strong>Risk type classification</strong></td><td>Tags every event by category: fatigue, distraction, aggressive driving, potential impairment, environmental hazard</td><td>Right events to the right stakeholders. Monitoring centres only get events matching their mandate.</td></tr>
                <tr><td><strong>Multi-sensor accident detection</strong></td><td>Confirms collisions by correlating G-sensor + speed change + lane departure + driver reaction + CAN data</td><td>Eliminates pothole false positives. Catches low-speed parking collisions G-sensor alone misses.</td></tr>
                <tr><td><strong>Behavioral tagging</strong></td><td>Builds persistent driver profiles with specific tags: <em>chronic tailgater, night-fatigue prone, excellent cornering, smooth braking</em></td><td>Targeted coaching on specific patterns. Positive tags enable gamification and recognition.</td></tr>
                <tr><td><strong>Coaching prioritisation</strong></td><td>Auto-ranks video clips by coaching impact based on each driver's behavioral profile</td><td>Safety manager finds the right clip for the right driver instantly. No more searching footage.</td></tr>
            </tbody>
        </table>
    </div>

    <h3 class="section-header fade-up">Evidence Cards — solving the AI black-box problem</h3>
    <div class="card fade-up">
        <p>The most common objection to AI safety systems: <em>"the system says this is an event, but the fleet manager doesn't understand why."</em></p>
        <p><strong>Evidence Cards</strong> show the visual explanation for every event — which signals contributed, how they deviated from the driver's baseline, and what pattern triggered the alert.</p>
        <p>Coaching conversations shift from <em>"the camera says you did something wrong"</em> to <em>"here's what the data shows — your lane position was degrading and your blink rate had changed, indicating early-stage fatigue. Let's talk about your sleep schedule."</em></p>
    </div>

    <div class="card fade-up">
        <h3 style="margin-top:0;"><i class="fa-solid fa-circle-info" style="color: var(--gold); margin-right:8px;"></i>How to read the detections below</h3>
        <p>Each AI detection has a <strong>short explanation</strong>, a <strong>sample clip</strong> (placeholder for now), and a <strong>parameter guide</strong> — what each setting controls and which way to adjust it. Tap a detection to expand it. Three settings recur across most features:</p>
        <ul class="checklist">
            <li><strong>Sensitivity</strong> — how readily the feature fires. Higher = earlier/more alerts but more false positives.</li>
            <li><strong>Minimum speed / speed gating</strong> — the speed band a feature is active in, so it doesn't alert when parked or crawling.</li>
            <li><strong>Duration / threshold</strong> — how long or how far the behaviour must persist before it counts (e.g. seconds of gaze-off-road).</li>
        </ul>
    </div>

    __FEATURES__

    <h3 class="section-header fade-up">Recommended starting profiles by fleet type</h3>
    <div class="card fade-up">
        <p>Start here, then re-tune after week 2 once you've seen your baseline event rate. Your CSM can review the data with you on a 30-min call.</p>
        <table class="stmx-table">
            <thead><tr><th>Fleet type</th><th>Recommended starting profile</th><th>Why</th></tr></thead>
            <tbody>
                <tr><td>Long-haul trucking</td><td>Standard ADAS + High DMS</td><td>Fatigue is the #1 risk; following-distance varies with traffic.</td></tr>
                <tr><td>Urban delivery</td><td>High ADAS + Standard DMS</td><td>Frequent pedestrians, cyclists, sudden stops.</td></tr>
                <tr><td>Transit bus</td><td>Standard ADAS + High DMS</td><td>Public-safety scrutiny is highest in this segment.</td></tr>
                <tr><td>Mining / haul truck</td><td>Custom mining profile</td><td>Standard ADAS triggers constantly off-road; mining profile filters dust/glare.</td></tr>
                <tr><td>Taxi / rideshare</td><td>Standard ADAS + High distraction</td><td>Phone use is the dominant risk.</td></tr>
            </tbody>
        </table>
    </div>

    <h3 class="section-header fade-up">Five-layer sensor fusion — where this is heading</h3>
    <div class="card fade-up">
        <p>SafeGPT today fuses video + driver-state + behavioral data. By H1 2027, every Streamax camera will integrate <strong>five intelligence layers</strong> in one device:</p>
        <table class="stmx-table">
            <thead><tr><th>Layer</th><th>Intelligence</th><th>Provides</th></tr></thead>
            <tbody>
                <tr><td><strong>L1: Eyes</strong></td><td>Video AI (ADAS + DMS)</td><td>FCW, LDW, pedestrian detection, fatigue, phone use, seatbelt</td></tr>
                <tr><td><strong>L2: Feel</strong></td><td>Advanced maneuver recognition</td><td>150+ risky-driving types — cornering, lane handling, braking — calibrated across billions of miles</td></tr>
                <tr><td><strong>L3: Know</strong></td><td>Native vehicle CAN/J1939/OBD-II</td><td>RPM, fuel, brake application, transmission, fault codes</td></tr>
                <tr><td><strong>L4: Locate</strong></td><td>GPS positioning &amp; trip recording</td><td>Real-time location, route deviation, geofencing</td></tr>
                <tr><td><strong>L5: Think</strong></td><td>SafeGPT cloud behavioral fusion</td><td>Continuous analysis of L1–L4. Predicts risk before events occur.</td></tr>
            </tbody>
        </table>
    </div>

    <style>
        .aif-feat { background: var(--glass-bg); border: var(--glass-border); border-radius: 12px; margin-bottom: 10px; overflow: hidden; }
        .aif-feat-head { display: flex; align-items: center; gap: 12px; padding: 15px 18px; cursor: pointer; transition: var(--transition); }
        .aif-feat-head:hover { background: rgba(255,255,255,0.03); }
        .aif-feat-icon { color: var(--gold); width: 20px; text-align: center; font-size: 1rem; }
        .aif-feat-name { font-weight: 700; color: var(--text-white); font-size: 1rem; }
        .aif-cat { font-size: 0.62rem; font-weight: 700; padding: 2px 8px; border-radius: 5px; letter-spacing: 0.5px; }
        .aif-adas { color: var(--purple); background: rgba(160,107,255,0.14); border: 1px solid rgba(160,107,255,0.3); }
        .aif-dms { color: var(--gold); background: rgba(244,201,93,0.12); border: 1px solid rgba(244,201,93,0.28); }
        .aif-feat-cv { margin-left: auto; color: var(--text-grey); font-size: 0.8rem; transition: transform 0.25s ease; }
        .aif-feat.open .aif-feat-cv { transform: rotate(180deg); }
        .aif-feat-body { display: none; padding: 0 18px 18px; }
        .aif-feat.open .aif-feat-body { display: block; }
        .aif-desc { color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0 0 14px; }
        .aif-grid { display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px; align-items: start; }
        @media (max-width: 900px) { .aif-grid { grid-template-columns: 1fr; } }
        .aif-lbl { font-size: 0.76rem; font-weight: 700; color: var(--text-grey); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
        .aif-lbl i { color: var(--gold); margin-right: 6px; }
        .aif-video { position: relative; width: 100%; padding-bottom: 56.25%; background: #000; border-radius: 12px; overflow: hidden; }
        .aif-video-ph { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px;
            background: radial-gradient(circle at 50% 40%, rgba(160,107,255,0.12), rgba(0,0,0,0.85) 70%); color: #fff; text-align: center; padding: 14px; }
        .aif-video-ph .fa-circle-play { font-size: 2.2rem; color: var(--gold); }
        .aif-video-t { font-weight: 600; font-size: 0.86rem; }
        .aif-video-s { font-size: 0.72rem; color: #94a3b8; }
        .aif-feat-body .stmx-table { margin: 0; font-size: 0.86rem; }
        .aif-note { font-size: 0.8rem; color: var(--text-grey); margin: 10px 0 0; }
        .aif-note i { color: var(--purple); margin-right: 5px; }
        .aif-ph { border: 1px dashed rgba(255,255,255,0.18); border-radius: 12px; padding: 18px; color: var(--text-grey); font-size: 0.86rem; }
        .aif-ph i { color: var(--purple); margin-right: 7px; }
    </style>

    <script>
    (function () {
        var root = document.getElementById('ai-features');
        if (!root || root.dataset.aifInit) return;
        root.dataset.aifInit = '1';
        root.querySelectorAll('.aif-feat-head').forEach(function (h) {
            h.addEventListener('click', function () { h.closest('.aif-feat').classList.toggle('open'); });
        });
    })();
    </script>

</div>
""".replace("__FEATURES__", _FEATURES_HTML)

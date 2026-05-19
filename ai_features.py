"""Section 5 — AI Features (SafeGPT deep-dive)."""

content = r"""
<div id="ai-features" class="content-section hidden">

    <div class="card fade-up" style="background: linear-gradient(135deg, rgba(42,245,152,0.06), rgba(0,158,253,0.04));">
        <h2><i class="fa-solid fa-robot" style="color: var(--primary-green); margin-right: 10px;"></i>SafeGPT — cloud behavioral intelligence</h2>
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
                <tr>
                    <td><strong>90% event reduction</strong></td>
                    <td>Only alerts when combined behavioral patterns indicate genuine risk — not individual sensor triggers</td>
                    <td>10–20 critical events/day, not 500 noise alerts. Reviews take 20 min, not 3 hours.</td>
                </tr>
                <tr>
                    <td><strong>Early fatigue detection</strong></td>
                    <td>Correlates lane-position degradation + speed oscillation + blink-rate changes + steering input variance</td>
                    <td>Detects fatigue <strong>5–15 minutes before</strong> the driver's eyes close. Intervention while still safe.</td>
                </tr>
                <tr>
                    <td><strong>Risk type classification</strong></td>
                    <td>Tags every event by category: fatigue, distraction, aggressive driving, potential impairment, environmental hazard</td>
                    <td>Right events to the right stakeholders. Monitoring centres only get events matching their mandate.</td>
                </tr>
                <tr>
                    <td><strong>Multi-sensor accident detection</strong></td>
                    <td>Confirms collisions by correlating G-sensor + speed change + lane departure + driver reaction + CAN data</td>
                    <td>Eliminates pothole false positives. Catches low-speed parking collisions G-sensor alone misses.</td>
                </tr>
                <tr>
                    <td><strong>Behavioral tagging</strong></td>
                    <td>Builds persistent driver profiles with specific tags: <em>chronic tailgater, night-fatigue prone, excellent cornering, smooth braking</em></td>
                    <td>Targeted coaching on specific patterns. Positive tags enable gamification and recognition.</td>
                </tr>
                <tr>
                    <td><strong>Coaching prioritisation</strong></td>
                    <td>Auto-ranks video clips by coaching impact based on each driver's behavioral profile</td>
                    <td>Safety manager finds the right clip for the right driver instantly. No more searching footage.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <h3 class="section-header fade-up">Evidence Cards — solving the AI black-box problem</h3>
    <div class="card fade-up">
        <p>The most common objection to AI safety systems: <em>"the system says this is an event, but the fleet manager doesn't understand why."</em></p>
        <p><strong>Evidence Cards</strong> show the visual explanation for every event — which signals contributed, how they deviated from the driver's baseline, and what pattern triggered the alert.</p>
        <p>Coaching conversations shift from <em>"the camera says you did something wrong"</em> to <em>"here's what the data shows — your lane position was degrading and your blink rate had changed, indicating early-stage fatigue. Let's talk about your sleep schedule."</em></p>
        <p style="font-size: 0.9rem; color: var(--text-grey); margin-top: 12px;">The driver sees the data behind the decision. The coaching is specific, not generic. The system is fair because it shows its reasoning.</p>
    </div>

    <h3 class="section-header fade-up">ADAS &amp; DMS event types — what your cameras detect</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-road" style="color: var(--secondary-blue);"></i> ADAS — forward-facing</h4>
            <ul class="checklist">
                <li><strong>FCW</strong> — Forward Collision Warning</li>
                <li><strong>LDW</strong> — Lane Departure Warning</li>
                <li><strong>HMW</strong> — Headway Monitoring (tailgating)</li>
                <li><strong>PCW</strong> — Pedestrian Collision Warning</li>
                <li><strong>Traffic-sign recognition</strong> — speed limits, stop signs</li>
                <li><strong>Lane change / overtake</strong> — unsafe maneuver detection</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-user" style="color: var(--primary-green);"></i> DMS — driver-facing</h4>
            <ul class="checklist">
                <li><strong>Drowsiness</strong> — eyes-closed, microsleep, yawn</li>
                <li><strong>Distraction</strong> — gaze off-road, head turn</li>
                <li><strong>Phone use</strong> — handheld, ear-cradle, dashboard glance</li>
                <li><strong>Smoking</strong> / <strong>Seatbelt off</strong></li>
                <li><strong>Driver absent</strong> — when the vehicle is in gear</li>
                <li><strong>Unauthorised driver</strong> — face-ID mismatch</li>
            </ul>
        </div>
    </div>

    <h3 class="section-header fade-up">Tuning alert sensitivity for your fleet</h3>
    <div class="card fade-up">
        <p>One-size-fits-all alerting is the #1 cause of "we have cameras but didn't get safety." Tune for your operating profile in <em>CMS → AI Settings → Alert Sensitivity</em>:</p>
        <table class="stmx-table">
            <thead><tr><th>Fleet type</th><th>Recommended starting profile</th><th>Why</th></tr></thead>
            <tbody>
                <tr><td>Long-haul trucking</td><td>Standard ADAS + High DMS</td><td>Fatigue is the #1 risk; following-distance varies with traffic.</td></tr>
                <tr><td>Urban delivery</td><td>High ADAS + Standard DMS</td><td>Frequent pedestrians, cyclists, sudden stops.</td></tr>
                <tr><td>Transit bus</td><td>Standard ADAS + High DMS + Aggressive event review</td><td>Public-safety scrutiny is highest in this segment.</td></tr>
                <tr><td>Mining / haul truck</td><td>Custom mining profile</td><td>Standard ADAS triggers constantly off-road; mining profile filters dust/glare/unmarked roads.</td></tr>
                <tr><td>Taxi / rideshare</td><td>Standard ADAS + Standard DMS + High distraction</td><td>Phone use is the dominant risk.</td></tr>
            </tbody>
        </table>
        <p style="margin-top: 14px; font-size: 0.88rem; color: var(--text-grey);">Re-tune after week 2 once you've seen your baseline event rate. Your CSM can review the data with you on a 30-min call.</p>
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

</div>
"""

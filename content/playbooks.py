"""Section 7 — Best Practices & Playbooks."""

content = r"""
<div id="playbooks" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-book-open" style="color: var(--gold); margin-right: 10px;"></i>Best practices &amp; playbooks</h2>
        <p>The repeatable workflows that turn a camera deployment into a measurable safety programme. Each playbook is field-tested by Streamax customers running tens of thousands of vehicles.</p>
    </div>

    <h3 class="section-header fade-up">The first-90-days success plan</h3>
    <div class="card fade-up">
        <table class="stmx-table">
            <thead><tr><th>Phase</th><th>Goal</th><th>Activities</th></tr></thead>
            <tbody>
                <tr>
                    <td><strong>Days 1–14<br>Pilot</strong></td>
                    <td>Prove the system works in your operation</td>
                    <td>Install on 3–5 vehicles. Verify all data flowing to CMS. Have your safety team review one week of events. Calibrate alert thresholds.</td>
                </tr>
                <tr>
                    <td><strong>Days 15–30<br>Baseline</strong></td>
                    <td>Capture your "before" numbers</td>
                    <td>Roll out to a representative sub-fleet (~20%). Run for 2 weeks without coaching to establish baseline event rates per driver per 100 miles. <strong>Don't coach yet</strong> — you need a clean baseline.</td>
                </tr>
                <tr>
                    <td><strong>Days 31–60<br>Coach</strong></td>
                    <td>Reduce events with targeted coaching</td>
                    <td>Begin weekly 1-on-1 coaching for top 3 highest-risk drivers, using Evidence Cards. Use behavioral tags to make conversations specific. Track event reduction per driver per week.</td>
                </tr>
                <tr>
                    <td><strong>Days 61–90<br>Scale</strong></td>
                    <td>Full-fleet roll-out</td>
                    <td>Roll the system out to the remainder of the fleet. Publish driver leaderboard. Launch your gamification or recognition programme. Schedule monthly safety reviews with the C-suite.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <h3 class="section-header fade-up">Driver coaching cadence</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-clock" style="color: var(--gold);"></i> Recommended rhythm</h4>
            <ul class="checklist">
                <li><strong>Daily</strong> — Safety officer reviews high-severity events (15 min)</li>
                <li><strong>Weekly</strong> — 1-on-1 coaching with top 3 risk drivers (15 min each)</li>
                <li><strong>Monthly</strong> — Fleet-wide trend review with operations team (30 min)</li>
                <li><strong>Quarterly</strong> — Board-level safety scorecard + ROI</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-comments" style="color: var(--purple);"></i> Coaching conversation script</h4>
            <ol style="padding-left: 20px; color: var(--text-grey); font-size: 0.9rem;">
                <li>Open with the data, not the verdict. <em>"Walk me through what was happening here..."</em></li>
                <li>Show the Evidence Card. Let the driver see the signals.</li>
                <li>Ask, don't tell. <em>"What do you think we could do differently?"</em></li>
                <li>Agree on one specific behavior to focus on next week.</li>
                <li>Schedule the follow-up review on the calendar before they leave.</li>
            </ol>
        </div>
    </div>

    <h3 class="section-header fade-up">Driver buy-in playbook</h3>
    <div class="card fade-up">
        <p>The biggest obstacle to a successful camera deployment isn't technology — it's <strong>driver resistance</strong>. Get this right or your scores will be artificially low (drivers gaming the system), your turnover will spike, and in unionised environments cameras become a labour relations crisis.</p>
        <h4 style="margin-top: 14px;">Five things to do in the first month</h4>
        <ul class="checklist">
            <li><strong>Hold the conversation BEFORE you install.</strong> Town hall, written FAQ, 1-on-1 with stewards. Surprise installation kills trust.</li>
            <li><strong>Show drivers the Evidence Cards.</strong> Drivers accept cameras when the AI is transparent. They reject "the camera says you did something wrong."</li>
            <li><strong>Lead with the exoneration story.</strong> A real example: "Last month a driver was rear-ended at a light. The video closed the insurance claim in 48 hours — without the camera, it would have dragged on for months and gone on his record." Drivers care most about this.</li>
            <li><strong>Two-way audio + TTS makes the camera <em>their</em> tool.</strong> They can report road hazards or vehicle issues hands-free. Frame it as a comms tool, not surveillance.</li>
            <li><strong>Recognise positive behavior publicly.</strong> Use the leaderboard. Behavioral tags like <em>"smooth braking, excellent cornering"</em> are coaching gold — share them.</li>
        </ul>
    </div>

    <h3 class="section-header fade-up">Accident investigation workflow</h3>
    <div class="card fade-up">
        <p>When an accident happens, the first 24 hours determine whether evidence helps you or hurts you. The workflow:</p>
        <table class="stmx-table">
            <thead><tr><th>Time</th><th>Action</th><th>Where in CMS</th></tr></thead>
            <tbody>
                <tr><td><strong>0–5 min</strong></td><td>Multi-sensor accident detection auto-fires. CMS pushes notification + 30s pre/post video clip to safety officer's phone.</td><td>Mobile app → Events → New</td></tr>
                <tr><td><strong>5–30 min</strong></td><td>Open full incident in CMS. Pull all cameras for the 5 minutes before + 5 minutes after. Confirm driver is OK, log first-response details.</td><td>CMS → Events → [event] → 360° View</td></tr>
                <tr><td><strong>30 min – 4 hrs</strong></td><td>Generate "Insurance Evidence Pack" — bundles video, GPS track, CAN data, driver baseline, and a one-page summary into a single PDF + ZIP. Send to insurer.</td><td>CMS → Reports → New → Insurance Evidence</td></tr>
                <tr><td><strong>4 – 48 hrs</strong></td><td>If at-fault is disputed: pull behavioral tags for the 30 days prior. Did SafeGPT flag fatigue, distraction, or aggressive patterns? Evidence-grade context.</td><td>CMS → Drivers → [driver] → Behavioral History</td></tr>
                <tr><td><strong>1 week+</strong></td><td>Post-incident review with the driver. Use the video for coaching, not punishment (unless gross negligence is proven).</td><td>CMS → Coaching → New session</td></tr>
            </tbody>
        </table>
    </div>

    <h3 class="section-header fade-up">Insurance partnership pack</h3>
    <div class="card fade-up">
        <p>If your insurer offers usage-based premiums, the data your fleet generates is worth real discount dollars. The pack to share with your carrier:</p>
        <ul class="checklist">
            <li><strong>Hardware spec sheet</strong> — confirms approved telematics device</li>
            <li><strong>Driver behavior data feed</strong> — aggregated scorecards, exportable monthly</li>
            <li><strong>Accident-frequency trend</strong> — pre- vs post-deployment comparison</li>
            <li><strong>Exonerating-evidence case studies</strong> — claims you've defended successfully</li>
            <li><strong>SafeGPT methodology paper</strong> — explains the behavioral risk model (request from your CSM)</li>
        </ul>
        <p style="margin-top: 14px; font-size: 0.88rem; color: var(--text-grey);">Streamax has insurance partnerships with major carriers across multiple regions globally. Ask your CSM to introduce you to the right regional contact.</p>
    </div>

    <h3 class="section-header fade-up">Industry-specific playbooks</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-truck" style="color: var(--gold);"></i> Trucking</h4>
            <p style="font-size: 0.85rem;">Lead with fatigue detection + R151/R155/R158 blind-spot compliance. Pair with Z5 for trailer security on high-value cargo runs.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-school-flag" style="color: var(--purple);"></i> School bus</h4>
            <p style="font-size: 0.85rem;">Interior coverage, stop-arm camera, stop-arm violation detection, exterior PSS / DVS compliance, child-left-behind detection.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-bus-simple" style="color: var(--gold);"></i> Transit bus</h4>
            <p style="font-size: 0.85rem;">Multi-zone interior recording for fare disputes + assault claims, AVM 360° for tight urban turns, driver wellness monitoring.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-mountain" style="color: var(--purple);"></i> Mining</h4>
            <p style="font-size: 0.85rem;">M10 hardened MDVR, bucket-tooth-loss AI ($500K–$2M per crusher incident), DMS tuned for PPE, V2X 200m over-the-horizon detection.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-taxi" style="color: var(--gold);"></i> Taxi / ride-hail</h4>
            <p style="font-size: 0.85rem;">Driver-passenger dual cam, panic button + covert audio for distress, route deviation alerts, exonerating dispute resolution.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-truck-pickup" style="color: var(--purple);"></i> Last-mile delivery</h4>
            <p style="font-size: 0.85rem;">Cargo verification, door-open events, Sentinel for fuel/tool theft, delivery proof + signature capture, dwell-time optimisation.</p>
        </div>
    </div>

</div>
"""

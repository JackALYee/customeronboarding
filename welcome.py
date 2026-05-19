"""Section 1 — Welcome & onboarding roadmap."""

content = r"""
<div id="welcome" class="content-section">

    <div class="card fade-up" style="text-align: center; padding: 40px 30px; background: linear-gradient(135deg, rgba(42,245,152,0.06), rgba(0,158,253,0.04));">
        <h2 style="font-size: 2.2rem; margin-bottom: 14px;">You're now part of the <span class="gradient-text">world's #1 video telematics</span> family</h2>
        <p style="font-size: 1.05rem; max-width: 760px; margin: 0 auto 24px; color: #cbd5e1;">
            Streamax has been ranked <strong style="color:#2AF598;">#1 by Berg Insight for 6 consecutive years</strong> — 5 million+ vehicles, 100+ countries, 500+ partners. This portal walks you from your very first power-on to running a structured AI-powered safety programme across your whole fleet.
        </p>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <a href="javascript:void(0)" onclick="switchTab('products', document.querySelectorAll('.nav-btn')[1])" class="cta-btn"><i class="fa-solid fa-rocket"></i> Start with My Products</a>
            <a href="javascript:void(0)" onclick="switchTab('training', document.querySelectorAll('.nav-btn')[3])" class="cta-btn secondary"><i class="fa-solid fa-graduation-cap"></i> Jump to Training</a>
        </div>
    </div>

    <h3 class="section-header fade-up">Your 30-day onboarding roadmap</h3>
    <div class="card fade-up">
        <div class="pipeline-container">
            <div class="pipeline-line"></div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-box-open"></i></div>
                <div class="pipeline-title">Week 1</div>
                <div class="pipeline-desc">Unbox &amp; identify devices. Activate cloud accounts. Watch the 5-min welcome video.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-screwdriver-wrench"></i></div>
                <div class="pipeline-title">Week 2</div>
                <div class="pipeline-desc">Install on 3–5 pilot vehicles. Verify livestream + GPS + AI alerts in CMS.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-chalkboard-user"></i></div>
                <div class="pipeline-title">Week 3</div>
                <div class="pipeline-desc">Train your team: Fleet Manager, Safety Officer, Dispatcher. Tune SafeGPT thresholds.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-chart-line"></i></div>
                <div class="pipeline-title">Week 4</div>
                <div class="pipeline-desc">Roll out to full fleet. Launch your first coaching cycle. Review your baseline scorecard.</div>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Your Day-1 checklist</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-circle-check" style="color: var(--primary-green); margin-right: 6px;"></i> Account setup</h4>
            <ul class="checklist">
                <li><strong>CMS login</strong> — your Customer Success Manager (CSM) sent your platform URL + admin credentials separately.</li>
                <li><strong>Mobile app</strong> — install <em>FT Cloud</em> (iOS / Google Play). Sign in with the same credentials.</li>
                <li><strong>SIM / data plan</strong> — confirm each camera's cellular plan is active. If your cameras shipped with embedded connectivity (Webbing), no action needed.</li>
                <li><strong>Add fleet managers</strong> — invite your team in <em>CMS → Users</em>. Assign role: Admin, Manager, Safety, or Viewer.</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-headset" style="color: var(--secondary-blue); margin-right: 6px;"></i> Key contacts</h4>
            <table class="stmx-table">
                <tr><td><strong>Customer Success</strong></td><td>csm@streamax.com</td></tr>
                <tr><td><strong>Technical Support</strong></td><td>support@streamax.com</td></tr>
                <tr><td><strong>Hardware RMA</strong></td><td>rma@streamax.com</td></tr>
                <tr><td><strong>Billing</strong></td><td>billing@streamax.com</td></tr>
                <tr><td><strong>Emergency hotline</strong></td><td>Available 24/7 via your CSM</td></tr>
            </table>
            <p style="font-size: 0.82rem; margin-top: 12px; color: var(--text-grey);">Response SLA: 4 business hours for Essential, 2 hours for Pro, 30 min for Enterprise.</p>
        </div>
    </div>

    <h3 class="section-header fade-up">What "onboarding success" looks like</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <div style="color: var(--primary-green); font-size: 2rem; font-weight: 800;">90%</div>
            <h4>Fewer false alerts</h4>
            <p style="font-size: 0.88rem;">With SafeGPT tuned, your safety manager sees 10–20 critical events/day instead of 500 noise alerts.</p>
        </div>
        <div class="glass-panel">
            <div style="color: var(--secondary-blue); font-size: 2rem; font-weight: 800;">15 min</div>
            <h4>Per-vehicle install</h4>
            <p style="font-size: 0.88rem;">One cable. One camera. One cellular plan. 3–4 vehicles per hour per installer.</p>
        </div>
        <div class="glass-panel">
            <div style="color: var(--primary-green); font-size: 2rem; font-weight: 800;">5–15 min</div>
            <h4>Fatigue lead-time</h4>
            <p style="font-size: 0.88rem;">SafeGPT detects fatigue 5–15 minutes <em>before</em> the driver's eyes close — intervention while still safe.</p>
        </div>
    </div>

    <h3 class="section-header fade-up">Why this matters</h3>
    <div class="card fade-up" style="border-left: 4px solid var(--primary-green);">
        <p style="font-size: 1.05rem; color: #e2e8f0; margin: 0;">
            "A camera-only system <em>sees</em> a driver's eyes close. A five-layer system <em>knew</em> the driver was fatigued 10 minutes earlier — because lane position was degrading, speed was oscillating, blink rate was changing, and steering input variance had increased. The difference is whether the fatigued driver gets pulled over before the crash, or whether the crash gets recorded for the insurance claim."
        </p>
        <p style="margin-top: 16px; color: var(--primary-green); font-size: 0.85rem; font-weight: 600;">— Streamax SafeGPT design principle</p>
    </div>

</div>
"""

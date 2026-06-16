"""Section 1 — Welcome & onboarding roadmap."""

content = r"""
<div id="welcome" class="content-section">

    <div class="card fade-up" style="text-align: center; padding: 40px 30px; background: linear-gradient(135deg, rgba(244,201,93,0.06), rgba(160,107,255,0.04));">
        <h2 style="font-size: 2.2rem; margin-bottom: 14px;">You're now part of the <span class="gradient-text">world's #1 video telematics</span> family</h2>
        <p style="font-size: 1.05rem; max-width: 760px; margin: 0 auto 24px; color: #cbd5e1;">
            Streamax has been ranked <strong style="color:#F4C95D;">#1 by Berg Insight for 6 consecutive years</strong> — 5 million+ vehicles, 100+ countries, 500+ partners. This portal walks you from your very first power-on to running a structured AI-powered safety programme across your whole fleet.
        </p>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <a href="javascript:void(0)" onclick="switchTab('products')" class="cta-btn"><i class="fa-solid fa-rocket"></i> Start with My Products</a>
            <a href="javascript:void(0)" onclick="switchTab('training')" class="cta-btn secondary"><i class="fa-solid fa-graduation-cap"></i> Jump to Training</a>
        </div>
    </div>

    <h3 class="section-header fade-up">Watch your welcome video</h3>
    <div class="card fade-up" style="padding: 0; overflow: hidden;">
        <div class="welcome-video-wrap">
            <iframe class="welcome-video-frame"
                src="https://www.youtube.com/embed/sp60sNpDXPo?list=PLygpi767M5jr25RDxtO-y_IsChoAC1Mvd&amp;rel=0"
                title="Welcome to Streamax"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen></iframe>
        </div>
    </div>
    <style>
        .welcome-video-wrap { position: relative; width: 100%; padding-bottom: 56.25%; background: #000; border-radius: 14px; overflow: hidden; }
        .welcome-video-frame { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
    </style>

    <h3 class="section-header fade-up">Your 30-day onboarding roadmap</h3>
    <div class="card fade-up">
        <div class="pipeline-container">
            <div class="pipeline-line"></div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-box-open"></i></div>
                <div class="pipeline-title">Week 1</div>
                <div class="pipeline-desc">Unbox &amp; identify devices, activate cloud accounts, and install your first 3–5 pilot vehicles. Confirm data is flowing in the CMS.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-screwdriver-wrench"></i></div>
                <div class="pipeline-title">Week 2</div>
                <div class="pipeline-desc">Roll installation out across your whole fleet. Verify livestream + GPS + AI alerts on every vehicle.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-chalkboard-user"></i></div>
                <div class="pipeline-title">Week 3</div>
                <div class="pipeline-desc">Train your team: Fleet Manager, Safety Officer, Dispatcher. Tune SafeGPT thresholds to your operation.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-icon"><i class="fa-solid fa-chart-line"></i></div>
                <div class="pipeline-title">Week 4</div>
                <div class="pipeline-desc">Launch your first driver-coaching cycle and review your baseline safety scorecard. Your programme is live.</div>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Your Day-1 checklist</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-circle-check" style="color: var(--gold); margin-right: 6px;"></i> Account setup</h4>
            <ul class="checklist">
                <li><strong>CMS login</strong> — your Customer Success Manager (CSM) sent your platform URL + admin credentials separately.</li>
                <li><strong>Mobile app</strong> — install <em>FT Cloud</em> (iOS / Google Play). Sign in with the same credentials.</li>
                <li><strong>SIM / data plan</strong> — confirm each camera's cellular plan is active. If your cameras shipped with embedded connectivity, no action needed.</li>
                <li><strong>Add fleet managers</strong> — invite your team in <em>CMS → Users</em>. Assign role: Admin, Manager, Safety, or Viewer.</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-headset" style="color: var(--purple); margin-right: 6px;"></i> Key contacts</h4>
            <table class="stmx-table">
                __KEY_CONTACTS__
            </table>
            <p style="font-size: 0.82rem; margin-top: 12px; color: var(--text-grey);">Response SLA: 4 business hours for Essential, 2 hours for Pro, 30 min for Enterprise.</p>
        </div>
    </div>

    <h3 class="section-header fade-up">What "onboarding success" looks like</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <div style="color: var(--gold); font-size: 2rem; font-weight: 800;">Day 1</div>
            <h4>Up &amp; running</h4>
            <p style="font-size: 0.88rem;">Your first vehicles are installed, online, and streaming data and AI insight into your CMS the same day the hardware arrives.</p>
        </div>
        <div class="glass-panel">
            <div style="color: var(--purple); font-size: 2rem; font-weight: 800;">Week 1</div>
            <h4>Team fluent</h4>
            <p style="font-size: 0.88rem;">Your fleet managers, safety officers, and dispatchers understand the platform's mechanics and key features &mdash; and use it smoothly in their daily routine.</p>
        </div>
        <div class="glass-panel">
            <div style="color: var(--gold); font-size: 2rem; font-weight: 800;">Month 1</div>
            <h4>Fully operational at scale</h4>
            <p style="font-size: 0.88rem;">The full fleet is deployed, your first coaching cycle is live, and your baseline safety scorecard is in hand &mdash; the programme is running.</p>
        </div>
    </div>

    <h3 class="section-header fade-up">Why this matters</h3>
    <div class="card fade-up" style="border-left: 4px solid var(--gold);">
        <p style="font-size: 1.05rem; color: #e2e8f0; margin: 0;">
            The age of AI promises a great deal &mdash; sharper efficiency, better accuracy, fewer incidents. But new technology only pays off if it actually gets used. If a powerful platform leaves you and your team buried in unfamiliar tools and information, it isn't doing you any good.
        </p>
        <p style="font-size: 1.05rem; color: #e2e8f0; margin: 18px 0 0;">
            That's exactly why this portal exists &mdash; and why you have a <strong style="color: var(--gold);">dedicated Streamax team behind it, both virtual and in person</strong>. We're here to help you adopt these technologies seamlessly and turn them into real results for your fleet, whether your priority is safety or efficiency. You focus on running your business; we'll make sure you get the full value of your technology &mdash; without ever wondering whether you're using it to its potential.
        </p>
        <p style="margin-top: 18px; color: var(--gold); font-size: 0.85rem; font-weight: 600;">— Your Streamax Customer Success team</p>
    </div>

</div>
"""

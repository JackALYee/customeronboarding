"""Section 8 — Support & Resources."""

content = r"""
<div id="support" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-life-ring" style="color: var(--primary-green); margin-right: 10px;"></i>Support &amp; resources</h2>
        <p>Everything you need to get help, stay current, and self-serve. Response SLAs by tier: <strong>Essential</strong> 4 business hours · <strong>Pro</strong> 2 hours · <strong>Enterprise</strong> 30 min.</p>
    </div>

    <h3 class="section-header fade-up">Get help</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-envelope" style="color: var(--primary-green);"></i> Email a ticket</h4>
            <p style="font-size: 0.9rem;">Quickest written record. Include vehicle ID, device serial, and a screenshot if applicable.</p>
            <a href="mailto:support@streamax.com" class="cta-btn secondary" style="margin-top: 8px;">support@streamax.com</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-comments" style="color: var(--secondary-blue);"></i> Live chat</h4>
            <p style="font-size: 0.9rem;">Bottom-right corner of the CMS. Agents online during your regional business hours.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;">Open in CMS</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-phone" style="color: #fbbf24;"></i> Emergency hotline</h4>
            <p style="font-size: 0.9rem;">24/7 critical issues (fleet-down, security incident). Hotline number provided by your CSM.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><em>Enterprise tier only.</em></p>
        </div>
    </div>

    <h3 class="section-header fade-up">FAQ — top questions from new customers</h3>
    <div class="card fade-up">
        <details style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">Why am I getting so many false alerts in week 1?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;">Default thresholds are tuned conservatively. After 7–14 days of baseline data, retune in <em>CMS → AI Settings → Alert Sensitivity</em> using the recommended profile for your fleet type. Most customers see a 60–80% reduction in alert volume after this single change. If you're on Enterprise, SafeGPT does much of this automatically after week 2.</p>
        </details>
        <details style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">Can drivers turn off the camera?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;">No. Cameras are hard-wired and tamper-resistant. Any attempt to disconnect generates an immediate "device offline" alert to dispatch. Power-cycling the vehicle doesn't disable recording — the camera resumes within 10 seconds.</p>
        </details>
        <details style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">What happens to video if cellular drops?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;">Video continues to record locally to onboard eMMC storage. When connectivity returns, AI events and requested clips upload automatically. Continuous video stays on the device and can be retrieved on demand.</p>
        </details>
        <details style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">How do I export video for an insurance claim?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;"><em>CMS → Events → [event] → Generate Insurance Pack</em>. Bundles video clips from all cameras, GPS track, CAN data, and driver baseline into a single PDF + ZIP. The pack is timestamped and hash-signed so insurers can verify integrity.</p>
        </details>
        <details style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">How long is video retained?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;">Standard retention: 30 days for continuous footage on the device (rolling), 90 days for AI events in the cloud (Pro), 180 days (Enterprise). Custom retention available — contact your CSM. Cloud storage is included in your subscription up to standard limits.</p>
        </details>
        <details style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">Is my data secure?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;">TLS 1.3 in transit, AES-256 at rest. SSO via SAML for enterprise. Cloud-hosted by default; on-premise deployment available for partners with data sovereignty requirements. SOC 2 Type II + ISO 27001 certified. Streamax never sells or shares customer footage.</p>
        </details>
        <details style="padding: 14px 0; cursor: pointer;">
            <summary style="color: var(--text-white); font-weight: 600;">When does Sentinel ship?</summary>
            <p style="margin-top: 10px; color: var(--text-grey); font-size: 0.92rem;">June 2026. Pre-orders open now via your CSM. Sentinel can deploy independently or merge into your existing FT Cloud account at no additional subscription cost if you're already on Pro or Enterprise.</p>
        </details>
    </div>

    <h3 class="section-header fade-up">Downloads</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-brands fa-apple" style="color: var(--text-white);"></i> / <i class="fa-brands fa-android" style="color: var(--primary-green);"></i> FT Cloud mobile app</h4>
            <p style="font-size: 0.88rem;">Live video, alerts, two-way audio on the go.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;">App Store</a>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px; margin-left: 8px;">Google Play</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-microchip" style="color: var(--secondary-blue);"></i> Firmware</h4>
            <p style="font-size: 0.88rem;">Latest firmware bundles for all device models. OTA pushed automatically; manual download available for offline updates.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;">Browse firmware</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-file-pdf" style="color: #ef4444;"></i> Documentation</h4>
            <p style="font-size: 0.88rem;">Spec sheets, wiring diagrams, API reference, regulatory certificates.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;">Browse docs</a>
        </div>
    </div>

    <h3 class="section-header fade-up">What's new</h3>
    <div class="card fade-up">
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-sparkles"></i></div>
            <div class="video-meta">
                <div class="video-title">SafeGPT 2.4 — Evidence Cards general availability</div>
                <div class="video-sub">Released May 2026 · Visual explanations on every event. Available to all Enterprise customers.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-sparkles"></i></div>
            <div class="video-meta">
                <div class="video-title">Sentinel pre-orders open</div>
                <div class="video-sub">April 2026 · First-of-its-kind standalone exterior camera. Shipping June 2026. Contact your CSM.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-sparkles"></i></div>
            <div class="video-meta">
                <div class="video-title">CAN decode now supports 2,500+ EU vehicle models</div>
                <div class="video-sub">March 2026 · Inventure partnership live. Non-intrusive CAN/FMS inductive reading — no diagnostic port required.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-sparkles"></i></div>
            <div class="video-meta">
                <div class="video-title">DS100 entry-level dashcam shipping</div>
                <div class="video-sub">Q1 2026 · 2CH cost-optimised dashcam for LCV fleets. AI included, no SafeGPT.</div>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Community &amp; feedback</h3>
    <div class="card fade-up" style="background: linear-gradient(135deg, rgba(0,158,253,0.06), rgba(42,245,152,0.03));">
        <div style="display: flex; gap: 24px; align-items: center; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px;">
                <h4>Help shape what we build next</h4>
                <p>You're a new Streamax customer — your feedback in the first 90 days carries extra weight in our product roadmap. Drop ideas in the customer community, vote on features, or book a 30-min product feedback call with the team.</p>
            </div>
            <div>
                <a href="#" class="cta-btn"><i class="fa-solid fa-users"></i> Join community</a>
            </div>
        </div>
    </div>

</div>
"""

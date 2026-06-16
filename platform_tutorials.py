"""Section 6 — Platform Tutorials (CMS + mobile app + APIs)."""

content = r"""
<div id="platform" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-chart-line" style="color: var(--gold); margin-right: 10px;"></i>Platform tutorials</h2>
        <p>FT Cloud is your CMS — every camera, every driver, every event, every report lives here. Same login works in the mobile app. TSP partners: see the dedicated integration section at the bottom.</p>
    </div>

    <h3 class="section-header fade-up">Three platform tiers — pick the one that matches your maturity</h3>
    <div class="card fade-up">
        <table class="stmx-table">
            <thead><tr><th>Tier</th><th>What you get</th><th>Best for</th></tr></thead>
            <tbody>
                <tr>
                    <td><strong>Essential</strong></td>
                    <td>Livestream video, GPS location, historical video playback</td>
                    <td>Fleets adopting cameras for the first time. <em>"I need to see what's happening on my trucks."</em></td>
                </tr>
                <tr>
                    <td><strong>Pro</strong></td>
                    <td>Essential + AI event upload, driver scorecards, coaching workflows</td>
                    <td>Fleets running a structured safety programme. <em>"I need to coach my drivers and reduce incidents."</em></td>
                </tr>
                <tr>
                    <td><strong>Enterprise</strong></td>
                    <td>Pro + SafeGPT behavioral intelligence, risk classification, behavioral tagging, coaching prioritisation, insurance analytics — and all future AI agent capabilities included</td>
                    <td>Fleets demanding maximum intelligence. <em>"I need to predict and prevent incidents before they happen."</em></td>
                </tr>
            </tbody>
        </table>
        <p style="margin-top: 14px; font-size: 0.88rem;">Upgrading between tiers is a <strong>software activation</strong> — no new hardware, no reinstallation, no data migration. Talk to your Streamax CSM for commercial details on each tier and upgrade options.</p>
    </div>

    <h3 class="section-header fade-up">CMS walkthrough — the 6 screens you'll live in</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-house" style="color: var(--gold);"></i> 1. Dashboard</h4>
            <p style="font-size: 0.88rem;">Daily fleet status — vehicles online, today's events by severity, top 5 drivers needing coaching, system health.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-map" style="color: var(--purple);"></i> 2. Live Map</h4>
            <p style="font-size: 0.88rem;">Real-time vehicle positions. Click any pin → instant livestream from all cameras, vehicle CAN data, recent events.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-triangle-exclamation" style="color: #fbbf24;"></i> 3. Events</h4>
            <p style="font-size: 0.88rem;">All AI events with filters: type, driver, vehicle, severity, date. Evidence Cards on every event. One-click coaching tag.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-user-group" style="color: var(--gold);"></i> 4. Drivers</h4>
            <p style="font-size: 0.88rem;">Driver scorecards, behavioral tags, coaching history, trend lines, leaderboards.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-truck-fast" style="color: var(--purple);"></i> 5. Fleet</h4>
            <p style="font-size: 0.88rem;">Per-vehicle inventory, install date, firmware version, online status, storage health, RMA history.</p>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-file-export" style="color: #fbbf24;"></i> 6. Reports</h4>
            <p style="font-size: 0.88rem;">Safety scorecards, harsh-event trends, fuel reports, IFTA mileage, insurance evidence exports. PDF, CSV, or scheduled email.</p>
        </div>
    </div>

    <h3 class="section-header fade-up">Building your first report</h3>
    <div class="card fade-up">
        <ol style="padding-left: 22px; color: var(--text-grey);">
            <li style="margin-bottom: 8px;">Open <strong>CMS → Reports → New Report</strong></li>
            <li style="margin-bottom: 8px;">Pick a template: <em>Fleet Safety Scorecard</em>, <em>Driver Coaching Pack</em>, <em>Incident Investigation</em>, <em>Insurance Evidence</em>, or <em>Custom</em></li>
            <li style="margin-bottom: 8px;">Set the date range and select drivers / vehicles to include</li>
            <li style="margin-bottom: 8px;">Choose delivery: download now, email me weekly, or push to a shared folder</li>
            <li style="margin-bottom: 8px;">Save the configuration — the report regenerates automatically on the schedule you set</li>
        </ol>
    </div>

    <h3 class="section-header fade-up">Mobile app — FT Cloud</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-brands fa-apple" style="color: var(--text-white);"></i> / <i class="fa-brands fa-android" style="color: var(--gold);"></i> What you can do from your phone</h4>
            <ul class="checklist">
                <li><strong>Live video</strong> from any vehicle, any camera</li>
                <li><strong>Push notifications</strong> for critical events (panic button, accident, unauthorised driver)</li>
                <li><strong>Two-way audio</strong> with the driver</li>
                <li><strong>Send text-to-speech</strong> messages (route changes, safety reminders)</li>
                <li><strong>Approve / dismiss</strong> events on the go</li>
                <li><strong>Driver mode</strong> — separate app view for drivers to see their own scorecard</li>
            </ul>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-mobile-screen" style="color: var(--purple);"></i> Setup</h4>
            <p style="font-size: 0.9rem;">Download <strong>FT Cloud</strong> from the App Store or Google Play. Sign in with the same email + password as the CMS. Enable push notifications for the alert types you want to be paged for.</p>
            <p style="font-size: 0.85rem; color: var(--text-grey); margin-top: 10px;">If you're an Enterprise customer, ask your CSM to enable the SafeGPT mobile widget — daily AI digest pushed at 8am local.</p>
        </div>
    </div>

    <h3 class="section-header fade-up">Integration &amp; white-label — for TSP partners</h3>
    <div class="card fade-up" style="border-top: 3px solid var(--purple);">
        <p>Two integration paths for TSP / channel partners:</p>
        <div class="grid-2">
            <div class="glass-panel">
                <h4><i class="fa-solid fa-code" style="color: var(--purple);"></i> Path 1 — API integration</h4>
                <p style="font-size: 0.9rem;">Streamax cameras connect to your existing platform. Event data, video clips, GPS, vehicle metadata flow into your software.</p>
                <ul class="checklist">
                    <li><strong>REST API</strong> — events, vehicles, drivers, video URLs</li>
                    <li><strong>Webhook callbacks</strong> — push events to your endpoint in real time</li>
                    <li><strong>OAuth 2.0</strong> — secure auth</li>
                    <li><strong>Sandbox environment</strong> — develop and test before production cutover</li>
                </ul>
                <a href="#" class="cta-btn secondary" style="margin-top: 10px;"><i class="fa-solid fa-book"></i> API Reference</a>
            </div>
            <div class="glass-panel">
                <h4><i class="fa-solid fa-palette" style="color: var(--gold);"></i> Path 2 — White-label platform</h4>
                <p style="font-size: 0.9rem;">Streamax provides a complete ready-to-deploy platform under <em>your</em> brand. Your fleet customers see your logo, colours, and domain — not Streamax.</p>
                <ul class="checklist">
                    <li><strong>Zero engineering required</strong></li>
                    <li><strong>SSO supported</strong> — Okta, Azure AD, custom SAML</li>
                    <li><strong>Cloud or on-premise</strong> — for data sovereignty requirements</li>
                    <li><strong>Every Streamax platform update</strong> arrives automatically — new SafeGPT capabilities, new AI agents, new workflows</li>
                </ul>
                <a href="#" class="cta-btn secondary" style="margin-top: 10px;"><i class="fa-solid fa-handshake"></i> Become a partner</a>
            </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-grey); margin-top: 14px;">Streamax partners with TSPs globally rather than competing for their fleet customers. Our role is to make your platform the place fleets buy video telematics from — extending what you already offer your customers, on infrastructure you already control. Talk to your CSM about which integration path fits your roadmap best.</p>
    </div>

</div>
"""

"""Section 4 — Training Academy."""

content = r"""
<div id="training" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-graduation-cap" style="color: var(--primary-green); margin-right: 10px;"></i>Streamax Training Academy</h2>
        <p>Role-based learning paths. Pick the track that matches your job — each video module is 3–8 minutes, with a quiz and a downloadable completion certificate at the end of each track.</p>
    </div>

    <h3 class="section-header fade-up">Choose your learning path</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel" style="border-top: 3px solid var(--primary-green);">
            <h4><i class="fa-solid fa-user-tie" style="color: var(--primary-green);"></i> Fleet Manager</h4>
            <p style="font-size: 0.88rem;">Strategic view of your safety programme. KPIs, reports, ROI tracking.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><strong>~45 min</strong> · 7 lessons</p>
        </div>
        <div class="glass-panel" style="border-top: 3px solid var(--secondary-blue);">
            <h4><i class="fa-solid fa-helmet-safety" style="color: var(--secondary-blue);"></i> Safety Officer</h4>
            <p style="font-size: 0.88rem;">Daily event review, coaching workflows, incident investigation.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><strong>~60 min</strong> · 9 lessons</p>
        </div>
        <div class="glass-panel" style="border-top: 3px solid #fbbf24;">
            <h4><i class="fa-solid fa-headset" style="color: #fbbf24;"></i> Dispatcher</h4>
            <p style="font-size: 0.88rem;">Live tracking, two-way comms, route changes, driver messaging.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><strong>~30 min</strong> · 5 lessons</p>
        </div>
        <div class="glass-panel" style="border-top: 3px solid #a78bfa;">
            <h4><i class="fa-solid fa-screwdriver-wrench" style="color: #a78bfa;"></i> Installer</h4>
            <p style="font-size: 0.88rem;">Mounting, wiring, calibration, first-boot verification, RMA.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><strong>~40 min</strong> · 6 lessons</p>
        </div>
        <div class="glass-panel" style="border-top: 3px solid #ef4444;">
            <h4><i class="fa-solid fa-truck" style="color: #ef4444;"></i> Driver</h4>
            <p style="font-size: 0.88rem;">What the camera does, what it doesn't do, how the alerts work, how it protects you.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><strong>~15 min</strong> · 4 lessons</p>
        </div>
        <div class="glass-panel" style="border-top: 3px solid #2AF598;">
            <h4><i class="fa-solid fa-code" style="color: #2AF598;"></i> Integration / TSP</h4>
            <p style="font-size: 0.88rem;">API, white-label platform, SSO, data partnership addendum, OEM patterns.</p>
            <p style="font-size: 0.8rem; color: var(--text-grey); margin-top: 8px;"><strong>~75 min</strong> · 10 lessons</p>
        </div>
    </div>

    <h3 class="section-header fade-up">Fleet Manager — sample lessons</h3>
    <div class="card fade-up">
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">1. Reading your fleet safety scorecard</div>
                <div class="video-sub">6 min · How driver scores combine speed, distraction, fatigue, and following-distance into one number — and what the number actually means.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">2. The three platform tiers — Essential, Pro, Enterprise</div>
                <div class="video-sub">4 min · Which tier fits which fleet maturity. When to upgrade (and when not to).</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">3. Building your monthly safety report</div>
                <div class="video-sub">8 min · CMS report builder — fleet-wide trends, driver leaderboard, incident drill-downs.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">4. ROI tracking — fuel, accidents, insurance</div>
                <div class="video-sub">7 min · Pulling the numbers that justify the programme to your board.</div>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Safety Officer — sample lessons</h3>
    <div class="card fade-up">
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">1. Your daily event review — 20 minutes, not 3 hours</div>
                <div class="video-sub">5 min · The SafeGPT-tuned workflow. Why 10 events/day beats 500 alerts/day.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">2. The driver coaching conversation — using Evidence Cards</div>
                <div class="video-sub">8 min · How to coach from data, not opinion. Sample scripts. Handling driver pushback.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">3. Incident investigation — pulling the full video record</div>
                <div class="video-sub">7 min · 360° rebuild of an accident from camera + CAN + GPS. Insurance-ready exports.</div>
            </div>
        </div>
        <div class="video-card">
            <div class="video-thumb"><i class="fa-solid fa-play"></i></div>
            <div class="video-meta">
                <div class="video-title">4. Behavioral tagging — chronic tailgater, night-fatigue prone</div>
                <div class="video-sub">6 min · How SafeGPT tags driver patterns over weeks. Targeted coaching using tags.</div>
            </div>
        </div>
    </div>

    <h3 class="section-header fade-up">Live webinars + community</h3>
    <div class="grid-2 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-calendar" style="color: var(--secondary-blue);"></i> Upcoming webinars</h4>
            <ul class="checklist">
                <li><strong>SafeGPT deep-dive</strong> — 1st Tuesday of each month, 10am ET / 4pm CET</li>
                <li><strong>"What's new" release briefing</strong> — quarterly, with the product team</li>
                <li><strong>Insurance partner workshop</strong> — by invitation, with regional carriers</li>
                <li><strong>TSP integration office hours</strong> — every other Thursday, 9am SGT</li>
            </ul>
            <a href="#" class="cta-btn secondary" style="margin-top: 10px;"><i class="fa-solid fa-calendar-plus"></i> Register</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-certificate" style="color: var(--primary-green);"></i> Certifications</h4>
            <p style="font-size: 0.9rem;">Complete a learning track and pass the end-of-track quiz (80% to pass) to earn a downloadable Streamax-issued certificate. Re-certification every 12 months.</p>
            <ul class="checklist">
                <li><strong>Streamax Certified Fleet Manager</strong></li>
                <li><strong>Streamax Certified Safety Officer</strong></li>
                <li><strong>Streamax Certified Installer</strong></li>
                <li><strong>Streamax Certified Integration Partner</strong> (TSP only)</li>
            </ul>
        </div>
    </div>

</div>
"""

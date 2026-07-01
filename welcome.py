"""Section 1 - Welcome and scroll-driven truck-to-logo story."""

content = r"""
<div id="welcome" class="content-section">

    <section class="stmx-brand-morph" id="stmx-brand-morph" data-morph-init="0" aria-label="Streamax truck-to-logo animation">
        <div class="stmx-morph-pin">
            <iframe id="stmx-morph-frame" class="stmx-morph-frame"
                src="__TRUCK_TO_LOGO_SRC__"
                title="Peterbilt particle truck morphing into the Streamax logo"
                loading="eager"
                referrerpolicy="no-referrer"></iframe>
            <div class="stmx-morph-field" aria-hidden="true"></div>
            <div class="stmx-morph-vignette" aria-hidden="true"></div>

            <div class="stmx-morph-copy stmx-morph-copy-primary">
                <span>Streamax road intelligence</span>
                <h1>Guardian of road safety</h1>
            </div>
            <div class="stmx-morph-copy stmx-morph-copy-secondary">
                <span>AI video telematics</span>
                <h2>best AI solutions provider for road safety</h2>
            </div>
            <div class="stmx-morph-progress" aria-hidden="true"><i></i></div>

            <div class="stmx-scroll-hint" id="stmx-scroll-hint" aria-hidden="true">
                <div class="stmx-scroll-hint-inner">
                    <span>scroll down slowly</span>
                    <i class="fa-solid fa-chevron-down"></i>
                </div>
            </div>

            <button type="button" class="stmx-skip-btn" id="stmx-skip-btn"
                onclick="if(window.StreamaxMorphStory&&window.StreamaxMorphStory.skip)window.StreamaxMorphStory.skip()">
                Skip intro <i class="fa-solid fa-forward-step"></i>
            </button>
        </div>
    </section>

    <section class="stmx-onboarding-hero fade-up" id="stmx-onboarding-start">
        <div class="stmx-onboarding-copy">
            <div class="stmx-kicker">Streamax customer onboarding</div>
            <h1>From first install to fleet-wide safety.</h1>
            <p>
                Your portal is a deployment workspace: identify the hardware, install with confidence,
                train the team, tune AI events, and move into a repeatable safety operating rhythm.
            </p>
            <div class="stmx-hero-actions">
                <a href="javascript:void(0)" onclick="switchTab('products')" class="cta-btn">
                    <i class="fa-solid fa-box-open"></i> View products
                </a>
                <a href="javascript:void(0)" onclick="switchTab('installation')" class="cta-btn secondary">
                    <i class="fa-solid fa-screwdriver-wrench"></i> Start installation
                </a>
            </div>
        </div>

        <div class="stmx-command-panel" aria-label="Portal focus areas">
            <div class="stmx-command-head">
                <span>Portal focus</span>
                <strong>Onboarding control room</strong>
            </div>
            <div class="stmx-command-grid">
                <button onclick="switchTab('products')">
                    <i class="fa-solid fa-box-open"></i>
                    <strong>Products</strong>
                    <span>Confirm hardware, manuals, and files.</span>
                </button>
                <button onclick="switchTab('installation')">
                    <i class="fa-solid fa-screwdriver-wrench"></i>
                    <strong>Install</strong>
                    <span>Bring vehicles online with guided checks.</span>
                </button>
                <button onclick="switchTab('platform')">
                    <i class="fa-solid fa-display"></i>
                    <strong>Operate</strong>
                    <span>Practice the CMS views your team will use.</span>
                </button>
                <button onclick="switchTab('ai-features')">
                    <i class="fa-solid fa-brain"></i>
                    <strong>Safety AI</strong>
                    <span>Review event logic and coaching signals.</span>
                </button>
            </div>
        </div>
    </section>

    <section class="stmx-overview-grid fade-up" aria-label="Onboarding overview">
        <div class="stmx-overview-lead">
            <div class="stmx-kicker">30-day operating path</div>
            <h2>Every tab answers one deployment question.</h2>
            <p>
                The portal follows the sequence your team actually uses: know what was purchased,
                install it, learn the platform, activate AI, train people, then run repeatable playbooks.
            </p>
        </div>
        <div class="stmx-route-board">
            <button onclick="switchTab('products')" class="stmx-route-card">
                <span>01</span><strong>My Products</strong><em>Specs, manuals, and product groups</em>
            </button>
            <button onclick="switchTab('installation')" class="stmx-route-card">
                <span>02</span><strong>Installation</strong><em>Guided install flows and checklists</em>
            </button>
            <button onclick="switchTab('platform')" class="stmx-route-card">
                <span>03</span><strong>Platform Tutorials</strong><em>FleetMind CMS walkthroughs</em>
            </button>
            <button onclick="switchTab('ai-features')" class="stmx-route-card">
                <span>04</span><strong>AI Features</strong><em>ADAS, DMS, and event settings</em>
            </button>
        </div>
    </section>

    <section class="stmx-roadmap-panel fade-up">
        <div class="stmx-roadmap-head">
            <div>
                <div class="stmx-kicker">Launch rhythm</div>
                <h2>Your first month, reduced to four operating decisions.</h2>
            </div>
            <a href="javascript:void(0)" onclick="switchTab('training')" class="cta-btn secondary">
                <i class="fa-solid fa-graduation-cap"></i> Open training
            </a>
        </div>
        <div class="stmx-roadmap">
            <article>
                <span>Week 1</span>
                <h3>Pilot vehicles online</h3>
                <p>Unbox, identify devices, activate accounts, and verify the first 3-5 vehicles in the CMS.</p>
            </article>
            <article>
                <span>Week 2</span>
                <h3>Installation scaled</h3>
                <p>Roll out across the fleet and check livestream, GPS, storage, and AI events on every vehicle.</p>
            </article>
            <article>
                <span>Week 3</span>
                <h3>Team roles trained</h3>
                <p>Give fleet managers, safety officers, and dispatchers the views they need for daily work.</p>
            </article>
            <article>
                <span>Week 4</span>
                <h3>Programme live</h3>
                <p>Review the baseline scorecard, start coaching, and agree the operating cadence with your CSM.</p>
            </article>
        </div>
    </section>

    <section class="stmx-day-one fade-up">
        <div class="stmx-video-panel">
            <div class="stmx-kicker">Welcome video</div>
            <div class="welcome-video-wrap">
                <iframe class="welcome-video-frame"
                    src="https://www.youtube.com/embed/sp60sNpDXPo?list=PLygpi767M5jr25RDxtO-y_IsChoAC1Mvd&amp;rel=0"
                    title="Welcome to Streamax"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen></iframe>
            </div>
        </div>
        <div class="stmx-contact-panel">
            <div class="stmx-kicker">Your Streamax team</div>
            <h2>Day-1 contacts and account checks.</h2>
            <ul class="checklist">
                <li><strong>CMS login</strong> - your CSM sends your platform URL and admin credentials separately.</li>
                <li><strong>Mobile app</strong> - install FT Cloud on iOS or Android and use the same account.</li>
                <li><strong>Connectivity</strong> - confirm every camera cellular plan or approved data path is active.</li>
                <li><strong>User roles</strong> - invite operators in CMS - Users and assign the right permissions.</li>
            </ul>
            <table class="stmx-table">
                __KEY_CONTACTS__
            </table>
        </div>
    </section>

    <style>
        #welcome {
            --morph-progress: 0;
            --morph-visual-opacity: 1;
            --guardian-opacity: 0;
            --solution-opacity: 0;
            --stmx-nav-offset: 0px;
            --morph-shell-opacity: 1;
            --hero-reveal-opacity: 0;
            --hero-reveal-y: 48px;
        }
        .stmx-kicker {
            color: var(--gold);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }
        .stmx-brand-morph {
            width: calc(100vw - 8px);
            margin-left: calc(50% - 50vw + 4px);
            min-height: 1620vh;
            position: relative;
            background:
                radial-gradient(circle at 52% 45%, rgba(231,189,98,0.16), transparent 31%),
                radial-gradient(circle at 73% 58%, rgba(146,114,242,0.18), transparent 34%),
                linear-gradient(180deg, #050505 0%, #0c0909 54%, #070707 100%);
            overflow: visible;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .stmx-morph-pin {
            position: fixed;
            top: var(--stmx-nav-offset);
            left: 0;
            right: 0;
            min-height: 620px;
            height: calc(100dvh - var(--stmx-nav-offset));
            overflow: hidden;
            isolation: isolate;
            opacity: var(--morph-shell-opacity);
            pointer-events: none;
            z-index: 4;
        }
        .stmx-brand-morph.morph-released .stmx-morph-pin {
            display: none;
        }
        .nav-tabs {
            transition: opacity 0.28s ease, transform 0.28s ease;
            will-change: opacity, transform;
        }
        body.stmx-morph-nav-hidden .nav-tabs,
        .nav-tabs.stmx-nav-hidden-during-morph {
            opacity: 0;
            pointer-events: none;
            transform: translate3d(0, -100%, 0);
        }
        body.stmx-morph-nav-returned .nav-tabs,
        .nav-tabs.stmx-nav-returned-after-morph {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            opacity: 1 !important;
            pointer-events: auto !important;
            transform: translate3d(0, 0, 0) !important;
        }
        body.stmx-morph-nav-returned .container {
            padding-top: 68px;
        }
        .stmx-morph-frame {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            display: block;
            border: 0;
            background: transparent;
            opacity: var(--morph-visual-opacity);
            transform-origin: center center;
            will-change: transform, opacity;
            pointer-events: none;
            z-index: 1;
        }
        .stmx-morph-field {
            position: absolute;
            inset: 0;
            z-index: 0;
            opacity: 0.28;
            background:
                linear-gradient(90deg, rgba(255,255,255,0.055) 1px, transparent 1px),
                linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px);
            background-size: 92px 92px;
            mask-image: radial-gradient(circle at 50% 48%, black 0%, rgba(0,0,0,0.85) 34%, transparent 76%);
            transform: perspective(900px) rotateX(64deg) translateY(25%);
            transform-origin: center bottom;
            pointer-events: none;
        }
        .stmx-morph-vignette {
            position: absolute;
            inset: 0;
            z-index: 2;
            pointer-events: none;
            background:
                radial-gradient(circle at 50% 46%, transparent 0%, transparent 34%, rgba(0,0,0,0.44) 76%, rgba(0,0,0,0.78) 100%),
                linear-gradient(180deg, rgba(0,0,0,0.36) 0%, transparent 22%, transparent 62%, rgba(0,0,0,0.58) 100%);
        }
        .stmx-morph-copy {
            position: absolute;
            display: none;
            z-index: 7;
            width: min(560px, calc(100vw - 48px));
            pointer-events: none;
            will-change: opacity, transform;
            text-shadow: 0 18px 54px rgba(0,0,0,0.78);
            transform: translate3d(0, 0, 0);
        }
        .stmx-morph-copy span {
            display: block;
            color: var(--gold);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        .stmx-morph-copy h1,
        .stmx-morph-copy h2 {
            margin: 0;
            font-size: clamp(3rem, 7vw, 7.2rem);
            line-height: 0.9;
            letter-spacing: 0;
            color: rgba(255,255,255,0.96);
            text-wrap: balance;
        }
        .stmx-morph-copy-primary {
            left: clamp(24px, 6vw, 96px);
            bottom: clamp(78px, 16vh, 170px);
            opacity: var(--guardian-opacity);
            transform: translate3d(0, calc((1 - var(--guardian-opacity)) * 28px), 0);
        }
        .stmx-morph-copy-secondary {
            right: clamp(24px, 6vw, 96px);
            top: clamp(108px, 18vh, 190px);
            text-align: right;
            opacity: var(--solution-opacity);
            transform: translate3d(0, calc((1 - var(--solution-opacity)) * 28px), 0);
        }
        .stmx-morph-copy-secondary h2 {
            font-size: clamp(2.4rem, 5.4vw, 5.8rem);
        }
        .stmx-morph-progress {
            position: absolute;
            z-index: 8;
            left: clamp(24px, 6vw, 96px);
            right: clamp(24px, 6vw, 96px);
            bottom: 34px;
            height: 2px;
            background: rgba(255,255,255,0.12);
            transform: translateY(0);
            overflow: hidden;
        }
        .stmx-morph-progress i {
            display: block;
            width: 100%;
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, var(--gold), #f6e5b8, var(--purple));
            transform: scaleX(var(--morph-progress));
            transform-origin: left center;
            box-shadow: 0 0 24px rgba(231,189,98,0.35);
        }
        .stmx-onboarding-hero {
            display: grid;
            grid-template-columns: minmax(280px, 0.95fr) minmax(320px, 1.05fr);
            gap: clamp(26px, 5vw, 72px);
            align-items: center;
            padding: clamp(72px, 10vw, 128px) 0 clamp(36px, 6vw, 72px);
            opacity: var(--hero-reveal-opacity);
            transform: translate3d(0, var(--hero-reveal-y), 0);
            transition: opacity 0.16s linear, transform 0.16s linear;
            will-change: opacity, transform;
        }
        .stmx-onboarding-copy h1 {
            font-size: clamp(3.4rem, 7.4vw, 8rem);
            line-height: 0.88;
            max-width: 920px;
            margin: 0 0 26px;
        }
        .stmx-onboarding-copy p {
            max-width: 670px;
            color: rgba(255,255,255,0.72);
            font-size: clamp(1.02rem, 1.45vw, 1.28rem);
            line-height: 1.74;
            margin: 0 0 30px;
        }
        .stmx-hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        .stmx-command-panel {
            min-height: 500px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.09);
            background:
                radial-gradient(circle at 14% 12%, rgba(231,189,98,0.14), transparent 28%),
                radial-gradient(circle at 86% 86%, rgba(146,114,242,0.14), transparent 32%),
                linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.018));
            box-shadow: var(--shadow-soft), var(--edge-highlight);
            padding: clamp(20px, 3vw, 34px);
        }
        .stmx-command-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 18px;
            margin-bottom: 26px;
        }
        .stmx-command-head span {
            color: var(--gold);
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .stmx-command-head strong {
            max-width: 16ch;
            text-align: right;
            font-family: var(--font-display);
            font-size: clamp(1.5rem, 2.8vw, 2.6rem);
            line-height: 0.96;
            font-weight: 700;
        }
        .stmx-command-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1px;
            border-radius: 8px;
            overflow: hidden;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .stmx-command-grid button {
            min-height: 190px;
            border: 0;
            background: rgba(8,8,8,0.86);
            color: var(--text-white);
            text-align: left;
            padding: 24px;
            cursor: pointer;
            font-family: var(--font-main);
            transition: background 0.22s ease, transform 0.22s ease;
        }
        .stmx-command-grid button:hover {
            background: rgba(26,23,18,0.96);
            transform: translateY(-2px);
        }
        .stmx-command-grid i {
            display: inline-flex;
            width: 34px;
            height: 34px;
            align-items: center;
            justify-content: center;
            color: var(--gold);
            border: 1px solid rgba(231,189,98,0.28);
            border-radius: 50%;
            margin-bottom: 26px;
        }
        .stmx-command-grid strong {
            display: block;
            font-size: 1.02rem;
            line-height: 1.18;
            margin-bottom: 8px;
        }
        .stmx-command-grid span {
            display: block;
            color: rgba(255,255,255,0.6);
            font-size: 0.88rem;
            line-height: 1.55;
        }
        .stmx-overview-grid {
            display: grid;
            grid-template-columns: minmax(280px, 0.85fr) minmax(320px, 1.15fr);
            gap: 24px;
            margin-top: 12px;
            align-items: stretch;
        }
        .stmx-overview-lead,
        .stmx-route-board,
        .stmx-roadmap-panel,
        .stmx-video-panel,
        .stmx-contact-panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.018));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 8px;
            box-shadow: var(--shadow-soft), var(--edge-highlight);
        }
        .stmx-overview-lead {
            padding: clamp(26px, 4vw, 44px);
        }
        .stmx-overview-lead h2,
        .stmx-roadmap-head h2,
        .stmx-contact-panel h2 {
            font-size: clamp(2rem, 4vw, 4.4rem);
            line-height: 0.95;
            margin-bottom: 18px;
        }
        .stmx-overview-lead p {
            max-width: 620px;
            color: rgba(255,255,255,0.66);
            font-size: 1.02rem;
        }
        .stmx-route-board {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1px;
            overflow: hidden;
            padding: 1px;
            background: rgba(255,255,255,0.08);
        }
        .stmx-route-card {
            min-height: 190px;
            border: 0;
            background: #12110f;
            color: var(--text-white);
            text-align: left;
            padding: 26px;
            cursor: pointer;
            font-family: var(--font-main);
            transition: transform 0.22s ease, background 0.22s ease;
        }
        .stmx-route-card:hover {
            background: #1a1712;
            transform: translateY(-2px);
        }
        .stmx-route-card span {
            display: block;
            color: var(--gold);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            margin-bottom: 22px;
        }
        .stmx-route-card strong {
            display: block;
            font-family: var(--font-main);
            font-size: 1.08rem;
            font-weight: 700;
            line-height: 1.18;
            margin-bottom: 8px;
        }
        .stmx-route-card em {
            display: block;
            color: rgba(255,255,255,0.58);
            font-size: 0.88rem;
            font-style: normal;
            line-height: 1.5;
        }
        .stmx-roadmap-panel {
            padding: clamp(26px, 4vw, 44px);
            margin-top: 24px;
        }
        .stmx-roadmap-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
            margin-bottom: 28px;
        }
        .stmx-roadmap {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }
        .stmx-roadmap article {
            min-height: 230px;
            padding: 22px;
            border-radius: 8px;
            background: rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.07);
        }
        .stmx-roadmap span {
            color: var(--gold);
            font-weight: 800;
            font-size: 0.74rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .stmx-roadmap h3 {
            margin: 42px 0 8px;
            font-size: 1.2rem;
            font-family: var(--font-main);
            font-weight: 700;
            line-height: 1.2;
        }
        .stmx-roadmap p {
            color: rgba(255,255,255,0.62);
            font-size: 0.9rem;
            margin: 0;
        }
        .stmx-day-one {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-top: 24px;
            margin-bottom: 20px;
        }
        .stmx-video-panel,
        .stmx-contact-panel {
            padding: clamp(22px, 3vw, 34px);
        }
        .welcome-video-wrap {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .welcome-video-frame {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }
        .stmx-contact-panel .stmx-table {
            margin-top: 18px;
        }
        @media (max-width: 1100px) {
            .stmx-brand-morph {
                min-height: 1476vh;
            }
            .stmx-onboarding-hero {
                grid-template-columns: 1fr;
                padding-top: 72px;
            }
            .stmx-command-panel {
                min-height: auto;
            }
        }
        @media (max-width: 820px) {
            #welcome {
                --stmx-nav-offset: 0px;
            }
            body.stmx-morph-nav-returned .container {
                padding-top: 58px;
            }
            .stmx-brand-morph {
                width: calc(100vw - 4px);
                margin-left: calc(50% - 50vw + 2px);
                min-height: 1368vh;
            }
            .stmx-morph-pin {
                min-height: 560px;
            }
            .stmx-morph-copy {
                left: 24px;
                right: 24px;
                width: auto;
                text-align: left;
            }
            .stmx-morph-copy-primary {
                bottom: 86px;
            }
            .stmx-morph-copy-secondary {
                top: 108px;
            }
            .stmx-morph-copy h1,
            .stmx-morph-copy h2,
            .stmx-onboarding-copy h1 {
                font-size: clamp(2.7rem, 13vw, 4.6rem);
            }
            .stmx-overview-grid,
            .stmx-day-one,
            .stmx-roadmap {
                grid-template-columns: 1fr;
            }
            .stmx-command-grid,
            .stmx-route-board {
                grid-template-columns: 1fr;
            }
            .stmx-roadmap-head {
                display: block;
            }
            .stmx-roadmap-head .cta-btn {
                margin-top: 12px;
            }
        }
        @media (prefers-reduced-motion: reduce) {
            .stmx-brand-morph {
                min-height: 100vh;
            }
            .stmx-onboarding-hero {
                opacity: 1;
                transform: none;
            }
            .stmx-morph-frame {
                opacity: 1;
            }
            .stmx-morph-copy {
                opacity: 1 !important;
                transform: none !important;
            }
        }

        /* Scroll hint — slow-flashing arrow + label, fades out once scrolling starts */
        .stmx-scroll-hint {
            position: absolute; left: 75%; top: 50%;
            transform: translate(-50%, -50%); display: flex; justify-content: center;
            z-index: 8; pointer-events: none; transition: opacity 0.5s ease;
        }
        .stmx-scroll-hint.is-gone { opacity: 0; }
        .stmx-scroll-hint-inner {
            display: flex; flex-direction: column; align-items: center; gap: 12px;
            color: rgba(255,255,255,0.85); font-family: var(--font-display);
            font-size: 1.05rem; font-weight: 400; letter-spacing: 0.06em;
            text-shadow: 0 4px 20px rgba(0,0,0,0.85);
            animation: stmxHintFlash 2.2s ease-in-out infinite;
        }
        .stmx-scroll-hint-inner i { font-size: 1.5rem; color: var(--gold); animation: stmxHintBob 1.5s ease-in-out infinite; }
        @keyframes stmxHintFlash { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
        @keyframes stmxHintBob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(8px); } }

        /* Skip button — bottom-left, jumps past the scroll story to the hero */
        .stmx-skip-btn {
            position: absolute; left: clamp(16px, 3vw, 36px); bottom: clamp(56px, 9vh, 84px);
            z-index: 9; pointer-events: auto; cursor: pointer;
            display: inline-flex; align-items: center; gap: 8px;
            background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.72);
            border: 1px solid rgba(255,255,255,0.16); border-radius: 30px;
            padding: 9px 18px; font-family: var(--font-ui); font-size: 0.76rem;
            font-weight: 600; letter-spacing: 0.04em;
            backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
            transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        }
        .stmx-skip-btn:hover { color: #fff; border-color: var(--gold); background: rgba(244,201,93,0.12); }
        .stmx-skip-btn i { font-size: 0.7rem; }
        @media (prefers-reduced-motion: reduce) {
            .stmx-scroll-hint-inner, .stmx-scroll-hint-inner i { animation: none; }
        }
    </style>

    <script>
        (function () {
            function onReady(fn) {
                if (document.readyState !== 'loading') fn();
                else document.addEventListener('DOMContentLoaded', fn);
            }

            onReady(function () {
                var root = document.getElementById('stmx-brand-morph');
                var frame = document.getElementById('stmx-morph-frame');
                var nav = document.querySelector('.nav-tabs');
                if (!root || !frame || root.dataset.morphInit === '1') return;
                root.dataset.morphInit = '1';

                var currentProgress = 0;
                var ticking = false;
                var morphCompleteAt = 0.82;
                var logoFadeStart = 0.975;
                var heroRevealStart = 0.985;
                var heroRevealEnd = 0.998;

                function clamp01(value) {
                    return Math.max(0, Math.min(1, value || 0));
                }

                function smoothstep(start, end, value) {
                    var t = clamp01((value - start) / Math.max(0.0001, end - start));
                    return t * t * (3 - 2 * t);
                }

                function postMorphProgress(progress) {
                    try {
                        if (frame.contentWindow) {
                            frame.contentWindow.postMessage({
                                type: 'streamaxMorphProgress',
                                progress: progress
                            }, '*');
                        }
                    } catch (error) {
                        // Decorative iframe only; the rest of the portal should stay usable.
                    }
                }

                function getMorphTravel() {
                    var viewport = window.innerHeight || document.documentElement.clientHeight || 1;
                    return Math.max(1, root.offsetHeight - viewport);
                }

                function setProgress(progress) {
                    currentProgress = clamp01(progress);
                    var guardian = smoothstep(0.06, 0.22, currentProgress) * (1 - smoothstep(0.34, 0.46, currentProgress));
                    var solution = smoothstep(0.32, 0.46, currentProgress) * (1 - smoothstep(0.68, 0.84, currentProgress));
                    var released = currentProgress >= heroRevealEnd;
                    var navHidden = currentProgress > 0.01 && !released;
                    var heroReveal = smoothstep(heroRevealStart, heroRevealEnd, currentProgress);
                    var logoFade = smoothstep(logoFadeStart, heroRevealEnd, currentProgress);
                    var visualOpacity = 1 - logoFade;
                    var shellOpacity = 1 - logoFade;
                    var sceneProgress = clamp01(currentProgress / morphCompleteAt);
                    var displayedProgress = Math.max(currentProgress, sceneProgress);

                    root.style.setProperty('--morph-progress', displayedProgress.toFixed(4));
                    root.style.setProperty('--guardian-opacity', guardian.toFixed(4));
                    root.style.setProperty('--solution-opacity', solution.toFixed(4));
                    root.style.setProperty('--morph-visual-opacity', visualOpacity.toFixed(4));
                    root.style.setProperty('--morph-shell-opacity', shellOpacity.toFixed(4));
                    root.style.setProperty('--hero-reveal-opacity', heroReveal.toFixed(4));
                    root.style.setProperty('--hero-reveal-y', ((1 - heroReveal) * 48).toFixed(2) + 'px');
                    root.classList.toggle('morph-released', released);
                    document.body.classList.toggle('stmx-morph-nav-hidden', navHidden);
                    document.body.classList.toggle('stmx-morph-nav-returned', released);
                    if (nav) nav.classList.toggle('stmx-nav-hidden-during-morph', navHidden);
                    if (nav) nav.classList.toggle('stmx-nav-returned-after-morph', released);
                    var hero = document.getElementById('stmx-onboarding-start');
                    if (hero) hero.style.pointerEvents = heroReveal > 0.96 ? 'auto' : 'none';
                    var hint = document.getElementById('stmx-scroll-hint');
                    if (hint) hint.classList.toggle('is-gone', currentProgress > 0.006);
                    frame.style.transform = 'scale(' + (1.01 + currentProgress * 0.045).toFixed(4) + ')';

                    postMorphProgress(sceneProgress);
                }

                function handleScrollProgress() {
                    var rect = root.getBoundingClientRect();
                    var travel = getMorphTravel();
                    if (rect.bottom <= 0) {
                        setProgress(1);
                        document.body.classList.remove('stmx-morph-nav-hidden');
                        document.body.classList.add('stmx-morph-nav-returned');
                        if (nav) nav.classList.remove('stmx-nav-hidden-during-morph');
                        if (nav) nav.classList.add('stmx-nav-returned-after-morph');
                        return;
                    }
                    var progress = clamp01((0 - rect.top) / travel);
                    setProgress(progress);
                }

                function scheduleRefresh() {
                    if (ticking) return;
                    ticking = true;
                    window.requestAnimationFrame(function () {
                        ticking = false;
                        handleScrollProgress();
                    });
                }

                frame.addEventListener('load', function () {
                    setProgress(currentProgress);
                });

                window.addEventListener('scroll', scheduleRefresh, { passive: true });
                window.addEventListener('resize', scheduleRefresh, { passive: true });
                handleScrollProgress();
                window.setTimeout(handleScrollProgress, 250);
                window.setTimeout(function () { setProgress(currentProgress); }, 1200);

                function postMorphReset() {
                    try {
                        if (frame.contentWindow) {
                            frame.contentWindow.postMessage({ type: 'streamaxMorphReset' }, '*');
                        }
                    } catch (error) {
                        // Decorative iframe only.
                    }
                }

                // Snap the story back to the truck-forward start with no backward
                // animation, so returning to Welcome always begins fresh.
                function resetStory() {
                    currentProgress = 0;
                    try { window.scrollTo(0, 0); } catch (e) {}
                    setProgress(0);
                    postMorphReset();
                }

                // Jump past the scroll story straight to the onboarding hero.
                function skipStory() {
                    var hero = document.getElementById('stmx-onboarding-start');
                    if (!hero) return;
                    // Apply the completed/released state first (this adds the fixed-nav
                    // offset + reflows), THEN measure on the next frame so the hero
                    // lands flush under the nav instead of clipped above the viewport.
                    setProgress(1);
                    window.requestAnimationFrame(function () {
                        var navEl = document.querySelector('.nav-tabs');
                        var navH = navEl ? navEl.getBoundingClientRect().height : 0;
                        var y = hero.getBoundingClientRect().top + window.pageYOffset - navH;
                        window.scrollTo(0, Math.max(0, y));
                        handleScrollProgress();
                    });
                }

                window.StreamaxMorphStory = {
                    refresh: handleScrollProgress,
                    reset: resetStory,
                    skip: skipStory
                };
                window.StreamaxTruckStory = window.StreamaxMorphStory;
            });
        })();
    </script>
</div>
"""

"""Section — Documentations.

A documentation hub: a library of downloadable docs (spec sheets, manuals,
API reference, firmware, release notes) plus the installation & setup guides
(folded in from the former standalone Installation tab so none of that content
is lost after the nav reorg).
"""

content = r"""
<div id="documentations" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-folder-open" style="color: var(--gold); margin-right: 10px;"></i>Documentations</h2>
        <p>Everything you need in writing — product spec sheets and manuals, platform &amp; API references, firmware, and release notes. Browse by category below.</p>
    </div>

    <h3 class="section-header fade-up">Documentation library</h3>
    <div class="grid-3 fade-up">
        <div class="glass-panel">
            <h4><i class="fa-solid fa-file-lines" style="color: var(--gold);"></i> Quick-start guides</h4>
            <p style="font-size: 0.88rem;">One-page setup for each device — unbox, mount, activate, verify.</p>
            <a href="javascript:void(0)" onclick="switchTab('products')" class="cta-btn secondary" style="margin-top: 8px;"><i class="fa-solid fa-arrow-right"></i> See per-device docs</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-file-pdf" style="color: var(--purple);"></i> Spec sheets &amp; manuals</h4>
            <p style="font-size: 0.88rem;">Full technical specifications and user manuals for every product you own.</p>
            <a href="javascript:void(0)" onclick="switchTab('products')" class="cta-btn secondary" style="margin-top: 8px;"><i class="fa-solid fa-box"></i> Open My Products</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-code" style="color: #fbbf24;"></i> API &amp; integration</h4>
            <p style="font-size: 0.88rem;">REST API, webhooks, OAuth, and white-label / SSO setup for TSP partners.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;"><i class="fa-solid fa-book"></i> API reference</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-microchip" style="color: var(--gold);"></i> Firmware</h4>
            <p style="font-size: 0.88rem;">Latest firmware bundles per model. OTA-pushed automatically; manual download for offline updates.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;"><i class="fa-solid fa-download"></i> Browse firmware</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-sliders" style="color: var(--purple);"></i> Platform guide</h4>
            <p style="font-size: 0.88rem;">How-to for the CMS — dashboards, events, reports, coaching, and settings.</p>
            <a href="javascript:void(0)" onclick="switchTab('platform')" class="cta-btn secondary" style="margin-top: 8px;"><i class="fa-solid fa-chart-line"></i> Open Platform Tutorials</a>
        </div>
        <div class="glass-panel">
            <h4><i class="fa-solid fa-bullhorn" style="color: #fbbf24;"></i> Release notes</h4>
            <p style="font-size: 0.88rem;">What's new in each platform and firmware release.</p>
            <a href="#" class="cta-btn secondary" style="margin-top: 8px;"><i class="fa-solid fa-clock-rotate-left"></i> View changelog</a>
        </div>
    </div>

</div>
"""

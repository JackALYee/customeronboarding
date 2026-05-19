"""Section 2 — My Products.

Product list and download URLs are sourced from the salestoolkit's
terminology_db.py (TERMINOLOGY_DB). Only products that are actually
in the Streamax database are listed — planning / roadmap items
(C6 Lite 3.0, AD Plus 3.0, DS100, etc.) are intentionally excluded.

The "Upload your proforma invoice" panel at the top is a UI
placeholder. The auto-parser is not implemented yet — when the
invoice template is finalised we can wire it up to extract the
product list and surface the matching spec/manual links from this
same registry.
"""

# Each entry mirrors a terminology_db.py row, trimmed to what this
# section needs: name, short blurb, and the spec/manual Drive links.
PRODUCTS_BY_GROUP = [
    {
        "group": "AI Dashcams",
        "icon": "fa-solid fa-video",
        "blurb": "On-vehicle AI cameras — ADAS + DMS + cloud connectivity in a single windshield-mounted device.",
        "items": [
            {
                "name": "AD Plus 2.0",
                "desc": "Bread-and-butter 4-channel AI dashcam. ADAS + DSC built in. Expandable via the PBM accessory.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=15UTpGJD4U4hPTktn3UjW-7xFUcD6X3PN"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1nGmQytGKRr288kGiqI4ci651liqmxKdx"),
                ],
            },
            {
                "name": "AD Max",
                "desc": "Flagship 6-channel AI dashcam. Black Light low-light, eSIM, eMMC storage, full ADAS + DMS.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1nciNxEXenYg0qSWyGUdI0nnYVAZP7TPr"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1yGJIAe0S25mELDQfNx3dtBLNZ4ONXMkt"),
                ],
            },
            {
                "name": "C6 Lite 2.0",
                "desc": "Economic 2-channel AI dashcam with ADAS + DSC. The right choice for cost-sensitive LCV and taxi deployments.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1PC1fbWuVgPgWSEt3asOIKQA1JOtdE0fa"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1uYe7JIQffiepX3oIWi3sEImrlUYi3Sdd"),
                ],
            },
            {
                "name": "DC Max",
                "desc": "6-channel AI dashcam paired with the GT1 Pro telematics gateway. Deploys only as a DC Max + GT1 Pro pair.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=181wM9Jg9omsyzttMrHHNInshYjqAEqY-"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1eucgSJmlEsBC0tNPQ90aR_5s3dYJksk0"),
                ],
            },
        ],
    },
    {
        "group": "Telematics Gateway",
        "icon": "fa-solid fa-tower-cell",
        "blurb": "FMS / CAN gateway for fleets that want vehicle data alongside video.",
        "items": [
            {
                "name": "GT1 Pro",
                "desc": "Telematics FMS gateway. Pairs with DC Max for a video + vehicle-data deployment. Currently restricted to the USA market.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1SPIEBvK1mvP3mMsJp36lRTZY-Ys88SBI"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1j6Bc6omBKMFRqb2IMGdJv-b6wIsYRumo"),
                ],
            },
        ],
    },
    {
        "group": "AD Plus 2.0 Accessories",
        "icon": "fa-solid fa-puzzle-piece",
        "blurb": "Channel + CAN-bus expansion modules for AD Plus 2.0 deployments.",
        "items": [
            {
                "name": "PBM (Power Box Max)",
                "desc": "Enables AD Plus 2.0 to add 2 extra channels AND read CAN bus / OBD-II / J1939. Pick this if you need channel count or CAN.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1dVh-YNKubqhr5mJMpaBhCfLoWVMrlKRy"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=12zNPRXFRAFqDuGEQLpw9rTBfbP4OraIo"),
                    ("PBM vs PBP comparison", "https://drive.google.com/uc?export=download&id=1da0R5LaYIKJ4kX2EujskfY_JNVT_3-oW"),
                ],
            },
            {
                "name": "PBP (Power Box Plus)",
                "desc": "Enables AD Plus 2.0 to read CAN bus / OBD-II without the extra channels. Pick this if you only need vehicle-data integration.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1_mPVTAcyUx_0_ZjgJ11Zp5b2NVuHsSQc"),
                    ("PBM vs PBP comparison", "https://drive.google.com/uc?export=download&id=1da0R5LaYIKJ4kX2EujskfY_JNVT_3-oW"),
                ],
            },
        ],
    },
    {
        "group": "MDVRs",
        "icon": "fa-solid fa-hard-drive",
        "blurb": "Mobile Digital Video Recorders — multi-channel ruggedised recorders for buses, trucks, mining and high-channel deployments.",
        "items": [
            {
                "name": "M1N 2.0",
                "desc": "Bread-and-butter MDVR. Pairs natively with CA20S, C29N, C53, CA51 and the standard AHD / IPC camera range.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1hlQ-5vNlxoZ7dH7I0L2uOY4bj3CX9ie5"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1Q7xYb6jG8E0ZHgWDDVuuWMI9w5vecmvA"),
                ],
            },
            {
                "name": "F6N",
                "desc": "5-channel 1080P MDVR — a focused mid-channel option without HDD.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=160vMHwSffxZWIu1D-iqfKWs3TlmPOy1h"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1jFIymbi1M39JC8vpPu-s5EYUgjuymEBG"),
                ],
            },
            {
                "name": "M3N",
                "desc": "Higher-channel MDVR for 8+ camera deployments. Compatible with ADKIT, CA20S, C40W, C29N, C46, CA46.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=14-vI6TLJrhNSys4qgnbhHOewU0iEWHOa"),
                ],
            },
        ],
    },
    {
        "group": "Visibility / BSD Cameras",
        "icon": "fa-solid fa-eye",
        "blurb": "Blind-spot, mirror-replacement and surround visibility cameras. Many deploy standalone (no MDVR) for fastest install on construction / forklift / municipal fleets.",
        "items": [
            {
                "name": "C53",
                "desc": "AI BSIS dual-lens camera (side + rear/top-side). Designed for EU BSIS/MOIS programmes and urban-logistics HGVs.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1KeDlNr-IheWJyPcI5tncvSkWn8o7u-SX"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1kNo2s_pcRHyE3U3TFX7lccmQpEAgvqc3"),
                ],
            },
            {
                "name": "C46",
                "desc": "AI BSD IPC camera. Connects via LAN or to an MDVR. Remote-configurable; best for on-road fleets on the Streamax platform.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=15HUOyruXT96bTI_SFVYPAwTKVd0Dddw1"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1PaCk1L9Mg5KXwRndPlRpJxgZ5W6jHDr8"),
                ],
            },
            {
                "name": "DP7Q",
                "desc": "Visibility camera, Q series. Standalone-capable AHD blind-spot camera.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=T96bTI_SFVYPAwTKVd0Dddw1"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1PaCk1L9Mg5KXwRndPlRpJxgZ5W6jHDr8"),
                ],
            },
            {
                "name": "DP7Q-T",
                "desc": "DP7Q variant tuned for tail / rear-mount deployments.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1DqoHoy7iEjxkXYGEGvBOUq3uQut2G6LT"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=14G4hocFebDV14ltGeulSAFv8AzoVyJBC"),
                ],
            },
            {
                "name": "DP7Q-RT",
                "desc": "DP7Q-RT — rear/top combined variant of the Q series.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1tjEZOUmVAJHkl7uPvwtwv68ZEPeng_cj"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1Wiz44D3G8VkarQU3b-6ivcoABimu_k4u"),
                ],
            },
            {
                "name": "DP7S",
                "desc": "Visibility camera, S series. Side-mount blind-spot detection.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1rn0NpghwO0ls_diXBITzDLoRUh-YacSu"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1m9f5KCf4L8BGPIsE6VbzxEoBYdcJ8N59"),
                ],
            },
            {
                "name": "DP7S-T",
                "desc": "DP7S variant for tail / rear-mount.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/file/d/1AUd-_h-6YUheKkQy8IF"),
                ],
            },
            {
                "name": "DP12S",
                "desc": "Visibility camera, 12-series. Higher-spec option for premium projects.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1lWW4CsnNZzA-FZR7UuGPgziKgn4aqvl0"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1DvymTFtzA0PEz78WvaOLwYKh-tDJIcR6"),
                ],
            },
            {
                "name": "C41W",
                "desc": "Visibility camera — wide-angle variant.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=12KT8NuTSLZGq0HccrEtHV7EcsJenkKGc"),
                ],
            },
            {
                "name": "CA42 Kit 2.0",
                "desc": "Visibility kit combining cameras and connectors for a turnkey blind-spot install.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1zVkFbVM8_XhF3UxmsHzJfqN7xICBj2-t"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1LnTRKOsy2tbIWNZFfbFf4cjdqM6IzLlG"),
                ],
            },
        ],
    },
    {
        "group": "Accessories",
        "icon": "fa-solid fa-screwdriver-wrench",
        "blurb": "DMS cameras, exterior alarms, supplementary cameras, driver-identity tags.",
        "items": [
            {
                "name": "C29N",
                "desc": "Dedicated DMS camera. Mount on the A-pillar at eye level — 940nm IR sees through sunglasses, works at 0 Lux. Recommended whenever in-cab DMS matters.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1nzOhRlXB0C0e-LuOOoXvuBozJEhq2i6H"),
                ],
            },
            {
                "name": "B2",
                "desc": "Exterior alarm module.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1UzGW4DsjBVkYf2VfAWHfX8ci-HInzAxI"),
                ],
            },
            {
                "name": "B3",
                "desc": "Exterior alarm module — second generation.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1cjRMppN_iA5yXs7MchiqqEfGlmkfbkKV"),
                ],
            },
            {
                "name": "C40W",
                "desc": "Wide-angle accessory camera. Pairs with M-series MDVRs and AD Plus 2.0 deployments.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1SCZ2osT57ZnpA4U-Z2-UF2Meomqkb136"),
                ],
            },
            {
                "name": "CA20S",
                "desc": "Cabin / supplementary AHD camera used across MDVR builds.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1ihECy7LRDVwv3643UbkLasnqCUlFzpmz"),
                ],
            },
            {
                "name": "iButton",
                "desc": "Driver authentication tag — contact-reader ID for driver login, chain-of-custody, and unauthorised-driver detection.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1RhPKqMjg8y6-LeKnoU5E5uBarvFoMn38"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1IQIMxFOuGNhIoiO9adyZh-9kDCpdEA9F"),
                ],
            },
            {
                "name": "R-Watch",
                "desc": "Driver wearable — companion device for personal alerts and driver-state telemetry.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1cgcKy_NCwThDLncHRjGy8Zu_fq9DH6ry"),
                ],
            },
        ],
    },
    {
        "group": "Asset Security",
        "icon": "fa-solid fa-shield-halved",
        "blurb": "Cargo and vehicle-security devices that deploy independently of the cab dashcam.",
        "items": [
            {
                "name": "Z5",
                "desc": "Standalone trailer-mounted device with its own cellular + GPS. Tracks unpowered trailers, captures door-open events, senses cargo load.",
                "files": [
                    ("Spec sheet", "https://drive.google.com/uc?export=download&id=1OLy4_RLLiggAWwbCD26qBcrObf2BHvjA"),
                    ("User manual", "https://drive.google.com/uc?export=download&id=1z2Dt-VTohjhRWh4QEfBkK_NlwKQ4SGJ-"),
                ],
            },
            {
                "name": "Sentinel",
                "desc": "Standalone exterior security camera for fuel tank, cargo hold and toolbox monitoring. Blacklight Ultra (0.02 LUX), built-in cellular + GPS + AI.",
                "files": [],
                "note": "Documentation in preparation — talk to your CSM for the latest spec.",
            },
        ],
    },
]


def _render_product_card(item: dict) -> str:
    files_html = ""
    if item.get("files"):
        chips = []
        for label, url in item["files"]:
            chips.append(
                f'<a href="{url}" target="_blank" rel="noopener" class="dl-btn">'
                f'<i class="fa-solid fa-file-pdf"></i> {label}'
                f"</a>"
            )
        files_html = '<div class="dl-row">' + "".join(chips) + "</div>"
    elif item.get("note"):
        files_html = f'<div class="dl-note"><i class="fa-solid fa-circle-info"></i> {item["note"]}</div>'

    return (
        f'<div class="product-card">'
        f'<div class="product-name">{item["name"]}</div>'
        f'<div class="product-desc">{item["desc"]}</div>'
        f'{files_html}'
        f"</div>"
    )


def _render_group(g: dict) -> str:
    cards = "".join(_render_product_card(it) for it in g["items"])
    return (
        f'<h3 class="section-header fade-up"><i class="{g["icon"]}" style="color: var(--primary-green); margin-right: 10px;"></i>{g["group"]}</h3>'
        f'<div class="card fade-up">'
        f'<p style="margin-top: 0;">{g["blurb"]}</p>'
        f'<div class="product-grid">{cards}</div>'
        f"</div>"
    )


_PRODUCT_SECTION_STYLE = r"""
<style>
    .product-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 20px; }
    @media (max-width: 900px) { .product-grid { grid-template-columns: 1fr; } }
    .product-card { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 18px 20px; transition: var(--transition); }
    .product-card:hover { border-color: rgba(42,245,152,0.3); background: rgba(255,255,255,0.04); transform: translateY(-2px); }
    .product-name { color: var(--primary-green); font-weight: 700; font-size: 1.1rem; margin-bottom: 6px; letter-spacing: 0.3px; }
    .product-desc { color: #cbd5e1; font-size: 0.88rem; margin-bottom: 12px; line-height: 1.55; }
    .dl-row { display: flex; flex-wrap: wrap; gap: 8px; }
    .dl-btn { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 20px; background: rgba(42,245,152,0.08); border: 1px solid rgba(42,245,152,0.3); color: var(--primary-green) !important; font-size: 0.78rem; font-weight: 600; text-decoration: none; transition: var(--transition); }
    .dl-btn:hover { background: rgba(42,245,152,0.18); color: #ffffff !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(42,245,152,0.2); }
    .dl-btn .fa-file-pdf { color: #ef4444; }
    .dl-btn:hover .fa-file-pdf { color: #ff6b6b; }
    .dl-note { color: #94a3b8; font-size: 0.82rem; font-style: italic; padding-top: 4px; }
    .dl-note i { color: var(--secondary-blue); margin-right: 4px; }

    /* Upload placeholder */
    .invoice-uploader {
        position: relative;
        border: 2px dashed rgba(42,245,152,0.35);
        border-radius: 14px;
        padding: 32px 24px;
        text-align: center;
        background: linear-gradient(135deg, rgba(42,245,152,0.04), rgba(0,158,253,0.03));
        transition: var(--transition);
        cursor: pointer;
    }
    .invoice-uploader:hover { border-color: var(--primary-green); background: linear-gradient(135deg, rgba(42,245,152,0.08), rgba(0,158,253,0.05)); }
    .invoice-uploader.is-dragover { border-color: var(--primary-green); background: rgba(42,245,152,0.10); }
    .invoice-uploader .uploader-icon { font-size: 2.6rem; color: var(--primary-green); margin-bottom: 12px; }
    .invoice-uploader .uploader-title { font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px; }
    .invoice-uploader .uploader-sub { color: #94a3b8; font-size: 0.88rem; max-width: 540px; margin: 0 auto 14px; }
    .invoice-uploader .uploader-btn {
        display: inline-flex; align-items: center; gap: 8px;
        background: linear-gradient(135deg, #2AF598, #009EFD);
        color: #050810; font-weight: 700; font-size: 0.88rem;
        padding: 9px 22px; border-radius: 30px; border: none;
        cursor: pointer; transition: var(--transition);
    }
    .invoice-uploader .uploader-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(42,245,152,0.25); }
    .invoice-uploader input[type=file] { display: none; }
    .invoice-uploader .coming-soon-badge {
        position: absolute; top: 12px; right: 14px;
        font-size: 0.65rem; font-weight: 700; letter-spacing: 1px;
        text-transform: uppercase; padding: 4px 10px; border-radius: 12px;
        background: rgba(251,191,36,0.15); color: #fbbf24;
        border: 1px solid rgba(251,191,36,0.4);
    }
    .invoice-result {
        margin-top: 14px; padding: 12px 18px; border-radius: 10px;
        background: rgba(0,158,253,0.08); border: 1px solid rgba(0,158,253,0.3);
        color: #cbd5e1; font-size: 0.88rem; text-align: left; display: none;
    }
    .invoice-result.show { display: block; }
    .invoice-result strong { color: var(--secondary-blue); }
</style>
"""


_INVOICE_PLACEHOLDER = r"""
    <h3 class="section-header fade-up"><i class="fa-solid fa-wand-magic-sparkles" style="color: var(--primary-green); margin-right: 10px;"></i>Upload your proforma invoice (auto-recognise products)</h3>
    <div class="card fade-up" style="padding: 24px;">
        <p style="margin-top: 0;">Drop your Streamax proforma invoice here. The portal will automatically detect the products on your order and surface the matching spec sheets and user manuals below — no scrolling needed.</p>
        <div class="invoice-uploader" id="invoice-uploader-zone" onclick="document.getElementById('invoice-file-input').click()">
            <div class="coming-soon-badge"><i class="fa-solid fa-flask"></i> Coming soon</div>
            <div class="uploader-icon"><i class="fa-solid fa-file-arrow-up"></i></div>
            <div class="uploader-title">Drop your proforma invoice here</div>
            <div class="uploader-sub">PDF or image. Auto-recognition is in development — the picker below will receive your file, but for now please reach out to your CSM to walk through the line items manually.</div>
            <button type="button" class="uploader-btn" onclick="event.stopPropagation(); document.getElementById('invoice-file-input').click();">
                <i class="fa-solid fa-folder-open"></i> Select file
            </button>
            <input type="file" id="invoice-file-input" accept=".pdf,.png,.jpg,.jpeg" onchange="window.handleInvoiceUpload && window.handleInvoiceUpload(this)">
            <div class="invoice-result" id="invoice-upload-result"></div>
        </div>
    </div>

    <script>
        (function () {
            // Drag/drop styling on the upload zone — purely visual, the
            // file isn't sent anywhere yet (auto-parser TBD).
            var zone = document.getElementById('invoice-uploader-zone');
            if (!zone) return;
            ['dragenter','dragover'].forEach(function (ev) {
                zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('is-dragover'); });
            });
            ['dragleave','drop'].forEach(function (ev) {
                zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('is-dragover'); });
            });
            zone.addEventListener('drop', function (e) {
                var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
                if (f) { window.handleInvoiceUpload && window.handleInvoiceUpload({ files: [f] }); }
            });

            window.handleInvoiceUpload = function (input) {
                var f = input && input.files && input.files[0];
                if (!f) return;
                var box = document.getElementById('invoice-upload-result');
                if (!box) return;
                var sizeKb = Math.round(f.size / 1024);
                box.innerHTML = '<strong>Received:</strong> ' + f.name + ' &middot; ' + sizeKb + ' KB' +
                    '<br><span style="color:#fbbf24;">Auto-parsing isn’t live yet</span> &mdash; ' +
                    'please email this invoice to your Streamax CSM and they will map the line items to spec sheets for you.';
                box.classList.add('show');
            };
        })();
    </script>
"""


# Build the section. The intro card + invoice uploader + product groups +
# educational "one-device" closing card.
_intro = r"""
<div id="products" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-box" style="color: var(--primary-green); margin-right: 10px;"></i>Your Streamax product catalogue</h2>
        <p>Browse every product currently in the Streamax catalogue, with the spec sheet and user manual for each one a single click away. Products still in planning or pre-release are not listed here &mdash; ask your CSM for the roadmap.</p>
    </div>
"""

_outro = r"""
    <h3 class="section-header fade-up"><i class="fa-solid fa-bolt" style="color: var(--primary-green); margin-right: 10px;"></i>The "one-device" architecture &mdash; why one Streamax camera replaces your tracker</h3>
    <div class="card fade-up">
        <p>Traditionally video telematics + GPS tracking required two devices &mdash; a separate tracker plus a separate camera, with two installations, two cellular plans, and two points of failure.</p>
        <p>Streamax cameras read native vehicle data via <strong>CAN bus / OBD-II / J1939 / FMS</strong>. One camera does everything:</p>
        <table class="stmx-table">
            <thead><tr><th>Capability</th><th>Traditional (2 devices)</th><th>Streamax (1 camera)</th></tr></thead>
            <tbody>
                <tr><td>Video AI (ADAS + DMS)</td><td>Camera</td><td>Built in</td></tr>
                <tr><td>GPS tracking &amp; trip recording</td><td>Tracker</td><td>Built in</td></tr>
                <tr><td>Vehicle ECU data (speed, RPM, fuel, fault codes)</td><td>Tracker via J1939</td><td>Built in &mdash; native CAN</td></tr>
                <tr><td>Sensor gateway (TPMS, fuel, temp, door, RFID)</td><td>Separate hub</td><td>Built in</td></tr>
                <tr><td>Cellular plans</td><td>2&ndash;3</td><td>1</td></tr>
                <tr><td>Installation</td><td>2 mounts, 2 wiring jobs</td><td>1 cable, ~15 min</td></tr>
            </tbody>
        </table>
    </div>

</div>
"""


_groups_html = "\n".join(_render_group(g) for g in PRODUCTS_BY_GROUP)
content = _PRODUCT_SECTION_STYLE + _intro + _INVOICE_PLACEHOLDER + _groups_html + _outro

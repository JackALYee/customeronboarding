"""Section 6 — Platform Tutorials.

A detailed interactive CLONE of the FleetMind platform (the customer's
white-label Streamax platform), embedded as a light-themed "app window"
inside the dark portal. Reconstructed from the live platform — three
top-bar contexts (Vision / Subscription / Settings), each with its own
left sidebar (incl. accordion submenus for Safety, Fuel, Basic Data), and
a faithful layout for every page. Representative sample data only — no live
backend. Hover any function for a pop-up explanation.

Everything is scoped under `.fm-sim` so the platform's light theme doesn't
clash with the portal's gold/purple glass theme. This string is injected
into the portal's components.html iframe (JS executes there).
"""


def _tip(t):
    return f' data-tip="{t}"' if t else ""


def _kpi(label, val, unit="", sub="", accent="", tip=""):
    u = f'<span>{unit}</span>' if unit else ""
    s = f'<div class="fm-kpi-trend">{sub}</div>' if sub else ""
    acc = f' style="border-left:3px solid {accent};"' if accent else ""
    return (f'<div class="fm-kpi"{acc}{_tip(tip)}>'
            f'<div class="fm-kpi-label">{label}</div>'
            f'<div class="fm-kpi-val">{val}{u}</div>{s}</div>')


def _row(cells):
    return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


def _table(headers, rows, tip=""):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(rows)
    return (f'<table class="fm-table"{_tip(tip)}><thead><tr>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table>")


def _pagehead(title, controls="", badge=""):
    b = f' <span class="fm-head-badge">{badge}</span>' if badge else ""
    return (f'<div class="fm-page-head"><h3>{title}{b}</h3>'
            f'<div class="fm-pills">{controls}</div></div>')


def _pill(label, tip=""):
    return f'<span class="fm-pill"{_tip(tip)}>{label} <i class="fa-solid fa-chevron-down"></i></span>'


def _btn(label, primary=False, icon="", tip=""):
    cls = "fm-btn fm-btn-primary" if primary else "fm-btn"
    ic = f'<i class="fa-solid {icon}"></i> ' if icon else ""
    return f'<span class="{cls}"{_tip(tip)}>{ic}{label}</span>'


def _badge(text, kind):
    return f'<span class="fm-bdg fm-bdg-{kind}">{text}</span>'


# ───────────────────────── VISION views ─────────────────────────

def _v_dashboard():
    insight = (
        '<div class="fm-insight" data-tip="Smart Insights|AI-written summary of what changed this week and what to act on — generated from your own data.">'
        '<i class="fa-solid fa-wand-magic-sparkles"></i>'
        '<div><strong>Smart Insights</strong> — Safety score up 4 pts this week; distraction events down 18%. Driver <em>Frank</em> needs attention (3 high-severity events).</div>'
        '<span class="fm-insight-link">View all →</span></div>'
    )
    kpis = (
        '<div class="fm-kpis">'
        + _kpi("Fleet Utilisation", "76", "%", '<span class="up">▲ 5% vs last week</span>', tip="Fleet Utilisation|Share of available vehicle-hours actually driven. Low utilisation = idle assets.")
        + _kpi("Fuel Efficiency", "27.2", "km/l", '<span class="up">▲ 2%</span>', tip="Fuel Efficiency|Average distance per unit of fuel across the fleet. Rises as coaching reduces harsh driving.")
        + _kpi("Total Events", "142", "", '<span class="up">▼ 18% (good)</span>', tip="Total Events|All AI safety events this period. The goal is a steady downward trend as drivers improve.")
        + '<div class="fm-kpi fm-kpi-score" data-tip="Safety Score|A 0–100 score blending speed, distraction, fatigue and following distance across the fleet.">'
          '<div class="fm-kpi-label">Safety Score</div>'
          '<div class="fm-donut" style="--pct:83;"><span>83<small>/100</small></span></div></div>'
        + '</div>'
    )
    chart = (
        '<div class="fm-panel fm-panel-wide" data-tip="Weekly Trend|Distance and event volume over the last 7 days. Hover the line in the real app for daily values.">'
        '<div class="fm-panel-head">Weekly trend <span>Last 7 days</span></div>'
        '<div class="fm-chart"><svg viewBox="0 0 320 90" preserveAspectRatio="none">'
        '<defs><linearGradient id="fmg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7c5cff" stop-opacity="0.35"/><stop offset="100%" stop-color="#7c5cff" stop-opacity="0"/></linearGradient></defs>'
        '<path d="M0,60 C40,50 60,40 90,44 C130,49 150,30 190,34 C230,38 260,28 320,32 L320,90 L0,90 Z" fill="url(#fmg)"/>'
        '<path d="M0,60 C40,50 60,40 90,44 C130,49 150,30 190,34 C230,38 260,28 320,32" fill="none" stroke="#7c5cff" stroke-width="2.5"/></svg>'
        '<div class="fm-axis"><span>Mon</span><span>Wed</span><span>Fri</span><span>Sun</span></div></div></div>'
    )
    drivers = (
        '<div class="fm-panel" data-tip="Top Drivers|Your highest-scoring drivers this week. Use it to recognise good behaviour, not only flag bad.">'
        '<div class="fm-panel-head">Top drivers <span>Score</span></div><ul class="fm-rank">'
        '<li><span class="fm-rk">1</span> David <b>94</b></li><li><span class="fm-rk">2</span> Zoe <b>88</b></li>'
        '<li><span class="fm-rk">3</span> Maria <b>81</b></li><li><span class="fm-rk">4</span> Sam <b>74</b></li>'
        '<li><span class="fm-rk">5</span> Frank <b>62</b></li></ul></div>'
    )
    types = (
        '<div class="fm-panel" data-tip="Events by Type|Which risk categories dominate — so you know what to coach on first.">'
        '<div class="fm-panel-head">Events by type <span>7 days</span></div><ul class="fm-bars">'
        '<li><span>Distraction</span><i style="width:90%"></i><b>58</b></li>'
        '<li><span>Fatigue</span><i style="width:62%"></i><b>34</b></li>'
        '<li><span>Phone use</span><i style="width:48%"></i><b>27</b></li>'
        '<li><span>Tailgating</span><i style="width:30%"></i><b>15</b></li>'
        '<li><span>No driver</span><i style="width:16%"></i><b>8</b></li></ul></div>'
    )
    return ('<section class="fm-view" data-view="dashboard" hidden>'
            + _pagehead("Dashboard", _pill("Last 7 days", "Date range|Switch the whole dashboard between Today, Last 7 days, or a custom range.") + _pill("All Fleets", "Fleet filter|Slice every chart by a specific fleet or depot."))
            + insight + kpis + '<div class="fm-row2">' + chart + drivers + types + '</div></section>')


def _v_map():
    vehs = [("TRK-4471", "Downtown depot", "58 km/h", "moving"), ("TRK-2210", "Route 9", "44 km/h", "moving"),
            ("VAN-0087", "Logistics yard", "0 km/h", "idle"), ("TRK-3390", "Hwy 401", "71 km/h", "moving"),
            ("BUS-1102", "Terminal B", "0 km/h", "idle"), ("TRK-5566", "Industrial Ave", "33 km/h", "moving"),
            ("VAN-0143", "— offline", "—", "offline")]
    rows = "".join(
        f'<div class="fm-veh"><span class="fm-veh-dot {st}"></span><div><b>{p}</b><small>{loc}</small></div><span class="fm-veh-spd">{spd}</span></div>'
        for p, loc, spd, st in vehs)
    pins = (
        '<span class="fm-pin moving" style="left:30%;top:34%;"><i class="fa-solid fa-truck"></i></span>'
        '<span class="fm-pin moving" style="left:54%;top:48%;"><i class="fa-solid fa-truck"></i></span>'
        '<span class="fm-pin idle" style="left:42%;top:62%;"><i class="fa-solid fa-van-shuttle"></i></span>'
        '<span class="fm-pin moving" style="left:68%;top:30%;"><i class="fa-solid fa-truck"></i></span>'
        '<span class="fm-pin idle" style="left:74%;top:64%;"><i class="fa-solid fa-bus"></i></span>'
        '<span class="fm-pin moving" style="left:48%;top:24%;"><i class="fa-solid fa-truck"></i></span>')
    return ('<section class="fm-view" data-view="safety-map" hidden><div class="fm-map-wrap">'
            '<div class="fm-vehlist"><div class="fm-panel-head" style="padding:14px 14px 10px;">Vehicles <span>7 / 1000 · <span style="color:#16a34a;">Live</span></span></div>'
            '<div class="fm-veh-search"><i class="fa-solid fa-magnifying-glass"></i> Search vehicle…</div>' + rows + '</div>'
            '<div class="fm-map" data-tip="Live Map|Each pin is a real vehicle. Green = moving, amber = parked, grey = offline. Click a pin to livestream its cameras.">'
            '<div class="fm-map-grid"></div>' + pins +
            '<div class="fm-map-scale">500 m</div><div class="fm-map-zoom"><span>+</span><span>−</span></div></div></div></section>')


def _v_risk():
    kpis = (
        '<div class="fm-kpis">'
        + _kpi("Fleet Risk Index", "72", "/100", '<span class="up">▲ 3 pts vs last month · Moderate risk</span>', "#d97706", "Fleet Risk Index|A predictive 0–100 risk score for the whole fleet, forecast from behaviour trends.")
        + _kpi("Predicted Incidents", "3", "", 'next 30 days · High confidence', "#dc2626", "Predicted Incidents|SafeGPT's forecast of likely incidents in the next 30 days if nothing changes.")
        + _kpi("High Risk", "12", "drivers", '▼ 2 vs last month · Need intervention', "#dc2626", "High Risk Drivers|Drivers whose risk trend crossed the intervention threshold — coach these first.")
        + _kpi("Safety Improvement", "+8", "pts", 'Fleet average improved · Coaching effective', "#16a34a", "Safety Improvement|How much fleet safety has improved — proof your coaching programme works.")
        + '</div>')
    forecast = (
        '<div class="fm-panel fm-panel-wide" data-tip="Risk Score Trend & Forecast|Historical risk vs the AI forecast band. The dashed line projects where risk is heading.">'
        '<div class="fm-panel-head">Risk score trend &amp; forecast <span>AI Forecast</span></div>'
        '<div class="fm-chart"><svg viewBox="0 0 320 90" preserveAspectRatio="none">'
        '<path d="M0,70 C40,64 70,40 110,38 C150,36 170,58 210,50 C240,44 250,30 320,24" fill="none" stroke="#7c5cff" stroke-width="2.5"/>'
        '<path d="M210,50 C250,46 270,40 320,30" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3"/>'
        '<line x1="210" y1="0" x2="210" y2="90" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3 3"/></svg>'
        '<div class="fm-axis"><span>Jan</span><span>Apr</span><span>Jul</span><span>Forecast</span></div></div></div>')
    dist = (
        '<div class="fm-panel" data-tip="Risk Distribution|How drivers split across Critical / High / Medium / Low risk bands.">'
        '<div class="fm-panel-head">Risk distribution <span>72 drivers</span></div>'
        '<ul class="fm-bars">'
        '<li><span>Critical</span><i style="width:8%;background:#dc2626"></i><b>2</b></li>'
        '<li><span>High</span><i style="width:24%;background:#d97706"></i><b>10</b></li>'
        '<li><span>Medium</span><i style="width:42%;background:#eab308"></i><b>18</b></li>'
        '<li><span>Low</span><i style="width:90%;background:#16a34a"></i><b>42</b></li></ul></div>')
    return ('<section class="fm-view" data-view="safety-risk" hidden>'
            + _pagehead("Risk Prediction", _pill("Last 30 days") + _pill("All Fleets") + _btn("Export", icon="fa-download", tip="Export|Download the risk report as PDF / CSV."), badge="AI-Powered")
            + kpis + '<div class="fm-row2b">' + forecast + dist + '</div></section>')


def _v_events():
    rows = [
        ("58", "Distraction", "high", "16 Jun · 13:42", "TRK-4471", "David"),
        ("44", "Fatigue", "high", "16 Jun · 13:27", "TRK-2210", "Frank"),
        ("0", "No driver", "mid", "16 Jun · 12:38", "VAN-0087", "—"),
        ("71", "Phone use", "high", "16 Jun · 12:10", "TRK-3390", "Maria"),
        ("33", "Tailgating", "mid", "16 Jun · 10:01", "TRK-5566", "Sam"),
    ]
    trs = "".join(_row([
        f'<span class="fm-clip"><i class="fa-solid fa-play"></i><em>{spd}</em></span>',
        f'<b>{ev}</b><span class="fm-sev {sev}">{"High" if sev=="high" else "Med"}</span>',
        t, veh, drv, '<span class="fm-media">Video</span>',
        '<span class="fm-status">Needs review</span> <i class="fa-regular fa-star fm-star"></i>',
    ]) for spd, ev, sev, t, veh, drv in rows)
    tabs = ('<div class="fm-tabs">'
            '<span class="fm-tab active" data-tip="Needs review|AI-flagged events a human hasn\'t actioned yet. Your daily work queue.">Needs review <b>142</b></span>'
            '<span class="fm-tab" data-tip="All events|Every event, reviewed or not.">All events</span>'
            '<span class="fm-tab" data-tip="Reviewed|Events you\'ve already actioned or dismissed.">Reviewed</span>'
            '<span class="fm-tab" data-tip="Starred|Events you flagged for coaching or evidence.">Starred <b>4</b></span></div>')
    table = _table(["Clip", "Event", "Time", "Vehicle", "Driver", "Media", "Status"], [trs],
                   "Event row|Hover the clip to preview; click to open the full video + Evidence Card explaining why the AI flagged it.")
    return ('<section class="fm-view" data-view="safety-events" hidden>'
            + _pagehead("Events", _btn("Export", icon="fa-download", tip="Export|Download the filtered list as CSV, or bundle clips into an insurance-ready pack."))
            + tabs + table + '<div class="fm-tablefoot">Showing 5 of 142 · <span>1 2 3 … 29 ›</span></div></section>')


def _v_fuel_realtime():
    return ('<section class="fm-view" data-view="fuel-realtime" hidden>'
            + _pagehead("Real-time Fuel")
            + '<div class="fm-filterbar" data-tip="Vehicle filter|Pick a vehicle to see its live fuel level, consumption rate, and tank events.">'
              '<label>Vehicle</label><span class="fm-select">Select vehicle… <i class="fa-solid fa-chevron-down"></i></span>'
              + _btn("Reset", icon="fa-rotate-left") + _btn("Search…", primary=True, icon="fa-magnifying-glass") + '</div>'
            + '<div class="fm-empty"><i class="fa-solid fa-gas-pump"></i><p>Select a vehicle to view its real-time fuel telemetry.</p></div></section>')


def _v_fuel_usage():
    kpis = ('<div class="fm-kpis">'
            + _kpi("This Month", "84,320", "L", '<span class="up">▲ 6.4% vs last month</span>', tip="This Month|Total fuel consumed across the fleet this month.")
            + _kpi("Monthly Cost", "$90,644", "", '<span class="up">▲ 5.8%</span>', tip="Monthly Cost|Your fuel spend this month (operational cost, your own figures).")
            + _kpi("Fleet Avg Efficiency", "33.8", "km/L", '<span class="up">▲ 1.2%</span>', tip="Fleet Avg Efficiency|Average distance per litre across all vehicles.")
            + _kpi("CO₂ Emissions", "223", "t", '<span class="up">▲ 6.4%</span>', tip="CO₂ Emissions|Estimated carbon output — for sustainability reporting.")
            + '</div>')
    rows = [("YUA2345", "Fleet A", "Marcus Rivera", "4,820 km", "4,950 L", "32.4 km/L", "$5,321", "212 L", "13,068"),
            ("YUA2346", "Fleet A", "James Chen", "4,210 km", "4,420 L", "29.8 km/L", "$4,751", "318 L", "11,669"),
            ("YUA2347", "Fleet B", "David Lee", "5,640 km", "3,820 L", "38.1 km/L", "$4,107", "98 L", "10,085"),
            ("YUA2348", "Fleet B", "Sarah Kim", "3,180 km", "5,810 L", "27.2 km/L", "$6,246", "540 L", "15,338"),
            ("YUA2349", "Fleet C", "Frank Muller", "5,020 km", "4,110 L", "35.6 km/L", "$4,418", "164 L", "10,850")]
    trs = "".join(_row([f'<b>{a}</b>', f'<span class="fm-link">{b}</span>', c, d, e, f'<span class="fm-eff">{f}</span>', g, f'<span class="fm-idle">{h}</span>', i]) for a, b, c, d, e, f, g, h, i in rows)
    return ('<section class="fm-view" data-view="fuel-usage" hidden>'
            + _pagehead("Fuel Usage", _pill("This Month") + _pill("All Fleets") + _btn("Export", icon="fa-download"))
            + kpis + _table(["Vehicle", "Fleet", "Driver", "Total Distance", "Fuel Used", "Avg Efficiency", "Fuel Cost", "Idle Fuel", "CO₂"], [trs],
                            "Usage row|Per-vehicle fuel breakdown. Red idle-fuel flags engines burning fuel while parked.")
            + '</section>')


def _v_compliance():
    kpis = ('<div class="fm-kpis">'
            + _kpi("Fleet Compliance Rate", "74", "%", 'Fully compliant drivers', "#16a34a", "Fleet Compliance Rate|Share of drivers fully compliant on hours, licence and inspections.")
            + _kpi("Hours Violations", "3", "", 'Drivers exceeding limit', "#7c5cff", "Hours Violations|Drivers over their daily/weekly driving-hour limits (HOS / tachograph).")
            + _kpi("Active Violations", "8", "", 'Speeding &amp; red light', "#d97706", "Active Violations|Open traffic violations awaiting action.")
            + _kpi("Docs Expiring", "4", "", 'Licences &amp; inspections', "#dc2626", "Docs Expiring|Licences / inspections expiring soon — renew before they lapse.")
            + '</div>')
    alerts = ('<div class="fm-alerts">'
              '<div class="fm-alert crit" data-tip="Critical alert|Auto-detected by AI. Requires immediate action."><div class="fm-alert-tag">Critical</div><h4>Driver License Expired</h4><p>Driver licence is expired. Immediate action required.</p>' + _btn("Notify HR", primary=True) + '</div>'
              '<div class="fm-alert warn"><div class="fm-alert-tag">Warning</div><h4>Hours Limit Approaching</h4><p>Driver is approaching daily/weekly hour limits.</p>' + _btn("Send Alert") + '</div>'
              '<div class="fm-alert warn"><div class="fm-alert-tag">Warning</div><h4>Traffic Violations</h4><p>Driver has recent traffic violations.</p>' + _btn("View Violations") + '</div>'
              '<div class="fm-alert info"><div class="fm-alert-tag">Info</div><h4>Vehicle Inspection Due</h4><p>Vehicle inspection is overdue.</p>' + _btn("Book Service") + '</div>'
              '</div>')
    rows = [("Marcus Rivera", "88", "6h 20m", "41h", "0", _badge("Valid", "ok"), _badge("Compliant", "ok")),
            ("James Chen", "71", "9h 05m", "52h", "1", _badge("Valid", "ok"), _badge("Hours warning", "warn")),
            ("David Lee", "64", "7h 40m", "44h", "2", _badge("Expiring", "warn"), _badge("Review", "warn")),
            ("Sarah Kim", "52", "10h 15m", "58h", "3", _badge("Expired", "bad"), _badge("Violation", "bad"))]
    trs = "".join(_row([f'<b>{a}</b>', b, c, d, e, f, g]) for a, b, c, d, e, f, g in rows)
    return ('<section class="fm-view" data-view="compliance" hidden>'
            + _pagehead("Compliance", _btn("Export", icon="fa-download"))
            + '<p class="fm-subtle">Monitor driver compliance and licence status</p>'
            + kpis
            + '<div class="fm-insight" data-tip="AI Compliance Alerts|Auto-detected compliance risks, ranked by severity, each with a one-click action."><i class="fa-solid fa-shield-halved"></i><div><strong>AI Compliance Alerts</strong> — auto-detected</div></div>'
            + alerts
            + _table(["Driver", "Score", "Hours Today", "Hours This Week", "Violations", "License", "Status"], [trs])
            + '</section>')


def _v_reports():
    tabs = ('<div class="fm-tabs"><span class="fm-tab active">My Reports</span><span class="fm-tab">All Reports</span></div>')
    rows = [("Fleet Safety Scorecard — June", "Jun 2026", "PDF", "Safety", "Scheduled"),
            ("Weekly Incident Summary", "Wk 24", "PDF", "Safety", "Ready"),
            ("Fuel Efficiency Report", "Jun 2026", "CSV", "Fuel", "Ready"),
            ("Driver Coaching Log", "Q2 2026", "PDF", "Coaching", "Ready")]
    trs = "".join(_row([f'<b>{a}</b>', b, f'<span class="fm-media">{c}</span>', d, _badge(e, "ok" if e == "Ready" else "warn")]) for a, b, c, d, e in rows)
    return ('<section class="fm-view" data-view="reports" hidden>'
            + _pagehead("Reports", _btn("Create Report", primary=True, icon="fa-plus", tip="Create Report|Build a custom report — pick metrics, date range, fleets — then schedule or export it."))
            + tabs + _table(["Name", "Period", "File Type", "Type", "Category"], [trs],
                            "Report row|Click to open or download. Scheduled reports regenerate and email automatically.")
            + '</section>')


def _v_coaching():
    tabs = ('<div class="fm-tabs"><span class="fm-tab active" data-tip="Upcoming|Coaching sessions queued for drivers who need attention.">Upcoming</span>'
            '<span class="fm-tab" data-tip="Completed|Sessions already delivered, with outcomes.">Completed</span>'
            '<span class="fm-tab" data-tip="Group Coaching|Run a session for several drivers sharing the same risky pattern.">Group Coaching</span></div>')
    rows = [("Frank Muller", "62", "Fatigue, Distraction", "—", "—", _badge("Needs scheduling", "warn")),
            ("Sam Patel", "74", "Tailgating", "8 Jun", "You", _badge("Scheduled", "ok")),
            ("Maria Gomez", "81", "Phone use", "2 Jun", "You", _badge("Scheduled", "ok"))]
    trs = "".join(_row([f'<b>{a}</b>', b, c, d, e, f]) for a, b, c, d, e, f in rows)
    return ('<section class="fm-view" data-view="coaching" hidden>'
            + _pagehead("Driver Coaching", _btn("Export", icon="fa-download"))
            + tabs + _table(["Driver", "Safety", "Behaviors to Coach", "Last Coached", "Assigned Coach", "Status"], [trs],
                            "Coaching row|Assign clips, schedule a 1-on-1, and track whether the driver's score improves after.")
            + '</section>')


def _v_bd_vehicle():
    rows = [("B06HY5", "00F90004CB", "LIGHT_TRUCK", "Fleet A", "Marcus Rivera", _badge("Online", "ok"), "16 Jun, 14:08"),
            ("B5Q2M2", "00F90004DB", "LIGHT_TRUCK", "Fleet A", "James Chen", _badge("Offline", "muted"), "15 Jun, 22:08"),
            ("BD359C", "00F90004E5", "LIGHT_TRUCK", "Fleet B", "David Lee", _badge("Online", "ok"), "16 Jun, 14:17"),
            ("BZ1H13", "00F90004C8", "LIGHT_TRUCK", "Fleet B", "Sarah Kim", _badge("Online", "ok"), "16 Jun, 14:13"),
            ("CX7700", "00F700042C", "ORDINARY_TRUCK", "Fleet C", "Frank Muller", _badge("Offline", "muted"), "9 Jun, 13:45")]
    trs = "".join(_row([f'<span class="fm-link">{a}</span>', b, c, f'<span class="fm-link">{d}</span>', e, f, g]) for a, b, c, d, e, f, g in rows)
    return ('<section class="fm-view" data-view="bd-vehicle" hidden>'
            + _pagehead("Vehicle Management", _btn("Export", icon="fa-download") + _btn("Import", icon="fa-upload") + _btn("Add Vehicle", primary=True, icon="fa-plus", tip="Add Vehicle|Register a device — plate, model, fleet — to start streaming data."), badge="Live · 7 devices")
            + _table(["Plate", "UniqueID", "Model", "Fleet", "Driver", "Status", "Last Active"], [trs],
                     "Vehicle row|Each row is a registered device. Online = streaming now. Click the plate to manage it.")
            + '</section>')


def _v_bd_driver():
    rows = [("DRV-001", "Marcus Rivera", "+1 555 0142", "DL-88421", "Fleet A", "88", _badge("Active", "ok"), "12 Jan 2026"),
            ("DRV-002", "James Chen", "+1 555 0177", "DL-77310", "Fleet A", "71", _badge("Active", "ok"), "3 Feb 2026"),
            ("DRV-003", "David Lee", "+1 555 0199", "DL-66204", "Fleet B", "64", _badge("Active", "ok"), "20 Feb 2026"),
            ("DRV-004", "Sarah Kim", "+1 555 0233", "DL-55190", "Fleet B", "52", _badge("Suspended", "bad"), "1 Mar 2026")]
    trs = "".join(_row([f'<span class="fm-link">{a}</span>', f'<b>{b}</b>', c, d, f'<span class="fm-link">{e}</span>', f, g, h]) for a, b, c, d, e, f, g, h in rows)
    return ('<section class="fm-view" data-view="bd-driver" hidden>'
            + _pagehead("Driver Management", _btn("Export", icon="fa-download") + _btn("Import", icon="fa-upload") + _btn("Add Driver", primary=True, icon="fa-plus"))
            + _table(["Driver ID", "Full Name", "Phone", "License", "Fleet", "Safety Score", "Status", "Joined Date"], [trs],
                     "Driver row|Driver profiles tie events, scores and coaching to a person — even across vehicles.")
            + '</section>')


def _v_bd_fleet():
    rows = [("fleet-a", "Fleet A — Long Haul", "North", "M. Rivera", "12", "10", "88", _badge("Active", "ok"), "9 Apr 2026"),
            ("fleet-b", "Fleet B — Urban", "Central", "D. Lee", "9", "8", "76", _badge("Active", "ok"), "9 Apr 2026"),
            ("fleet-c", "Fleet C — Regional", "South", "F. Muller", "7", "6", "71", _badge("Active", "ok"), "9 Apr 2026"),
            ("fleet-test", "Test Fleet", "—", "—", "0", "0", "0", _badge("Active", "ok"), "8 Apr 2026")]
    trs = "".join(_row([f'<span class="fm-link">{a}</span>', f'<b>{b}</b>', c, d, e, f, g, h, i]) for a, b, c, d, e, f, g, h, i in rows)
    return ('<section class="fm-view" data-view="bd-fleet" hidden>'
            + _pagehead("Fleet Management", _pill("All dates") + _btn("Export", icon="fa-download") + _btn("Add Fleet", primary=True, icon="fa-plus"))
            + _table(["Fleet ID", "Fleet Name", "Region", "Manager", "Vehicles", "Driver", "Avg Safety Score", "Status", "Created Date"], [trs],
                     "Fleet row|Group vehicles and drivers into fleets/depots so every report can be sliced by group.")
            + '</section>')


# ───────────────────────── SUBSCRIPTION views ─────────────────────────

def _v_invoices():
    tabs = '<div class="fm-tabs"><span class="fm-tab active">Invoices</span><span class="fm-tab">Payment Due</span></div>'
    return ('<section class="fm-view" data-view="sub-invoices" hidden>'
            + _pagehead("Invoices", _btn("Export", icon="fa-download"))
            + tabs + _table(["Invoice", "Date", "Invoice Period", "Net", "VAT", "Total", "Status"], [
                '<tr class="fm-empty-row"><td colspan="7">No invoices found.</td></tr>'],
                "Invoices|Every billing statement, downloadable. Switch to Payment Due for anything outstanding.")
            + '</section>')


def _v_sub_details():
    return ('<section class="fm-view" data-view="sub-details" hidden>'
            + _pagehead("Subscription Details")
            + '<div class="fm-row2b">'
            + '<div class="fm-panel" data-tip="Current plan|Your active tier, seat count and renewal date."><div class="fm-panel-head">Current plan</div>'
              '<div class="fm-plan-big">Pro <span class="fm-bdg fm-bdg-ok">Active</span></div>'
              '<ul class="fm-deflist"><li>Devices <b>7 / 50</b></li><li>Seats <b>4 / 10</b></li><li>Renews <b>1 Jul 2026</b></li><li>Billing <b>Monthly</b></li></ul>'
              + _btn("Manage plan", primary=True) + '</div>'
            + '<div class="fm-panel" data-tip="Plan tiers|Upgrade is a software activation — no new hardware."><div class="fm-panel-head">Available tiers</div>'
              '<ul class="fm-tiers"><li><b>Essential</b><span>Live video, GPS, playback</span></li>'
              '<li class="cur"><b>Pro</b><span>+ AI events, scorecards, coaching</span> <em>Current</em></li>'
              '<li><b>Enterprise</b><span>+ SafeGPT, risk prediction, analytics</span></li></ul></div>'
            + '</div></section>')


def _v_sub_features():
    feats = [("SafeGPT behavioral intelligence", "Enterprise", False),
             ("Risk prediction", "Enterprise", False),
             ("AI event upload", "Pro", True),
             ("Driver scorecards", "Pro", True),
             ("Extra cloud storage (180 days)", "Add-on", False),
             ("API & white-label access", "Add-on", True)]
    cards = "".join(
        f'<div class="fm-feat{" on" if on else ""}"><div><b>{n}</b><span>{tier}</span></div>'
        f'<span class="fm-toggle{" on" if on else ""}"></span></div>' for n, tier, on in feats)
    return ('<section class="fm-view" data-view="sub-features" hidden>'
            + _pagehead("Additional Features")
            + '<p class="fm-subtle">Toggle optional capabilities and add-ons for your plan.</p>'
            + f'<div class="fm-feat-grid" data-tip="Add-ons|Switch optional modules on or off; changes apply at the next billing cycle.">{cards}</div></section>')


def _v_sub_contacts():
    rows = [("Billing contact", "Anna Doyle", "billing@acme-logistics.com", _badge("Primary", "ok")),
            ("Technical contact", "Raj Patel", "it@acme-logistics.com", _badge("—", "muted")),
            ("Account owner", "M. Rivera", "owner@acme-logistics.com", _badge("Admin", "ok"))]
    trs = "".join(_row([a, f'<b>{b}</b>', f'<span class="fm-link">{c}</span>', d]) for a, b, c, d in rows)
    return ('<section class="fm-view" data-view="sub-contacts" hidden>'
            + _pagehead("Contacts", _btn("Add Contact", primary=True, icon="fa-plus"))
            + _table(["Role", "Name", "Email", "Status"], [trs],
                     "Contacts|Who receives invoices, renewal notices and technical updates.")
            + '</section>')


def _v_sub_delivery():
    return ('<section class="fm-view" data-view="sub-delivery" hidden>'
            + _pagehead("Invoice Delivery")
            + '<div class="fm-panel" style="max-width:620px;" data-tip="Invoice Delivery|How and where your invoices are sent."><div class="fm-panel-head">Delivery preferences</div>'
            + '<div class="fm-form-grid">'
              '<div class="fm-field"><label>Delivery method</label><span class="fm-select">Email + Portal <i class="fa-solid fa-chevron-down"></i></span></div>'
              '<div class="fm-field"><label>Send to</label><span class="fm-input">billing@acme-logistics.com</span></div>'
              '<div class="fm-field"><label>Format</label><span class="fm-select">PDF <i class="fa-solid fa-chevron-down"></i></span></div>'
              '<div class="fm-field"><label>Frequency</label><span class="fm-select">Monthly <i class="fa-solid fa-chevron-down"></i></span></div>'
            + '</div>' + _btn("Save preferences", primary=True) + '</div></section>')


def _v_sub_orgs():
    rows = [("Acme Logistics GmbH", "DE", "Owner", "7 devices", _badge("Active", "ok")),
            ("Acme Freight UK Ltd", "UK", "Member", "0 devices", _badge("Invited", "warn"))]
    trs = "".join(_row([f'<b>{a}</b>', b, c, d, e]) for a, b, c, d, e in rows)
    return ('<section class="fm-view" data-view="sub-orgs" hidden>'
            + _pagehead("Your Organizations", _btn("New Organization", primary=True, icon="fa-plus"))
            + _table(["Organization", "Country", "Your role", "Devices", "Status"], [trs],
                     "Organizations|Manage multiple companies/entities under one login — switch between them anytime.")
            + '</section>')


# ───────────────────────── SETTINGS views ─────────────────────────

def _v_set_general():
    subtabs = ('<div class="fm-subtabs">'
               '<span class="fm-subtab active">Company</span><span class="fm-subtab">Branding</span>'
               '<span class="fm-subtab">Units</span><span class="fm-subtab">Preferences</span></div>')
    form = ('<div class="fm-panel" data-tip="Company Information|Your account basics — used across reports, invoices and the platform UI.">'
            '<div class="fm-panel-head" style="border-left:3px solid #7c5cff;padding-left:10px;">Company Information</div>'
            '<div class="fm-form-grid">'
            '<div class="fm-field"><label>Company Name</label><span class="fm-input">Acme Logistics GmbH</span></div>'
            '<div class="fm-field"><label>Industry</label><span class="fm-select">Transport &amp; Logistics <i class="fa-solid fa-chevron-down"></i></span></div>'
            '<div class="fm-field"><label>Timezone</label><span class="fm-select">Europe/Berlin <i class="fa-solid fa-chevron-down"></i></span></div>'
            '<div class="fm-field"><label>Date Format</label><span class="fm-select">DD/MM/YYYY <i class="fa-solid fa-chevron-down"></i></span></div>'
            '</div></div>')
    return ('<section class="fm-view" data-view="set-general" hidden>'
            + _pagehead("General Settings", _btn("Save Changes", primary=True, icon="fa-floppy-disk"))
            + '<p class="fm-subtle">Manage your account and preferences</p>'
            + '<div class="fm-settings-wrap"><div class="fm-settings-aside">' + subtabs + '</div><div class="fm-settings-main">' + form + '</div></div></section>')


def _v_set_users():
    rows = [("Marcus Rivera", "owner@acme-logistics.com", "Owner", "Full access", _badge("Active", "ok")),
            ("Anna Doyle", "anna@acme-logistics.com", "Admin", "Manage fleet & users", _badge("Active", "ok")),
            ("Raj Patel", "raj@acme-logistics.com", "Manager", "View + coach", _badge("Active", "ok")),
            ("Sara Lin", "sara@acme-logistics.com", "Viewer", "Read only", _badge("Invited", "warn"))]
    trs = "".join(_row([f'<b>{a}</b>', f'<span class="fm-link">{b}</span>', _badge(c, "ok" if c in ("Owner", "Admin") else "muted"), d, e]) for a, b, c, d, e in rows)
    return ('<section class="fm-view" data-view="set-users" hidden>'
            + _pagehead("Users & Roles", _btn("Invite User", primary=True, icon="fa-plus", tip="Invite User|Send an email invite and assign a role (Owner / Admin / Manager / Viewer)."))
            + _table(["Name", "Email", "Role", "Permissions", "Status"], [trs],
                     "User row|Roles control what each person can see and do. Owner has full access; Viewer is read-only.")
            + '</section>')


def _v_set_privacy():
    items = [("Two-factor authentication (2FA)", "Require a second factor at sign-in.", True),
             ("Data retention — video", "Keep continuous footage for 30 days.", True),
             ("Driver data anonymisation", "Hide driver identity in shared reports.", False),
             ("Audit log", "Record every admin action.", True)]
    cards = "".join(f'<div class="fm-feat{" on" if on else ""}"><div><b>{n}</b><span>{d}</span></div><span class="fm-toggle{" on" if on else ""}"></span></div>' for n, d, on in items)
    return ('<section class="fm-view" data-view="set-privacy" hidden>'
            + _pagehead("Privacy &amp; Security")
            + '<p class="fm-subtle">Control authentication, data retention and audit.</p>'
            + f'<div class="fm-feat-grid" data-tip="Privacy controls|Security and data-handling switches for your whole account.">{cards}</div></section>')


def _v_set_notifications():
    rows = [("Accident detected", "Push + Email", "Immediate"),
            ("Panic button", "Push + SMS", "Immediate"),
            ("Daily safety digest", "Email", "08:00 daily"),
            ("Compliance docs expiring", "Email", "7 days before"),
            ("Weekly report ready", "Email", "Monday 09:00")]
    trs = "".join(_row([f'<b>{a}</b>', b, c]) for a, b, c in rows)
    return ('<section class="fm-view" data-view="set-notifications" hidden>'
            + _pagehead("Notifications", _btn("Save Changes", primary=True, icon="fa-floppy-disk"))
            + '<p class="fm-subtle">Choose what you\'re alerted about, how, and when.</p>'
            + _table(["Event", "Channel", "Timing"], [trs],
                     "Notification rule|Pick the channel (push / email / SMS) and timing for each alert type.")
            + '</section>')


# ───────────────────────── Sidebars ─────────────────────────

def _nav(view, icon, label, tip=""):
    return f'<div class="fm-nav" data-view="{view}"{_tip(tip)}><i class="fa-solid {icon}"></i> {label}</div>'


def _group(gid, icon, label, children, tip=""):
    subs = "".join(f'<div class="fm-nav fm-subnav" data-view="{v}"{_tip(t)}>{lbl}</div>' for v, lbl, t in children)
    return (f'<div class="fm-group" data-group="{gid}">'
            f'<div class="fm-group-head"{_tip(tip)}><i class="fa-solid {icon}"></i> {label}<i class="fa-solid fa-chevron-right fm-caret"></i></div>'
            f'<div class="fm-sub">{subs}</div></div>')


def _rail_vision():
    return ('<aside class="fm-rail active" data-rail="vision">'
            + _nav("dashboard", "fa-grip", "Dashboard", "Dashboard|Your fleet's daily overview — utilisation, fuel efficiency, safety score and trends.")
            + _group("safety", "fa-shield-halved", "Safety", [
                ("safety-map", "Map", "Live Map|Real-time location and status of every vehicle. Click a vehicle to livestream."),
                ("safety-risk", "Risk Prediction", "Risk Prediction|SafeGPT forecasts which drivers are trending toward risk before incidents happen."),
                ("safety-events", "Events", "Events|Every AI-detected safety event with video — ready to review and coach."),
            ], "Safety|AI safety tools — live map, predictive risk, and event review.")
            + _group("fuel", "fa-gas-pump", "Fuel", [
                ("fuel-realtime", "Real-time Information", "Real-time Fuel|Live fuel level and consumption per vehicle."),
                ("fuel-usage", "Usage", "Fuel Usage|Fleet fuel spend, efficiency and CO₂ — spot theft and waste."),
            ], "Fuel|Monitor consumption, cost and efficiency.")
            + _nav("compliance", "fa-clipboard-check", "Compliance", "Compliance|DVS / GSR / ELD status and audit-ready records, kept current automatically.")
            + _nav("reports", "fa-file-lines", "Reports", "Reports|Safety scorecards, trip and incident reports. Schedule or export.")
            + _nav("coaching", "fa-chalkboard-user", "Driver Coaching", "Driver Coaching|Assign clips, run sessions, and watch scores improve.")
            + _group("bd", "fa-database", "Basic Data", [
                ("bd-vehicle", "Vehicle", "Vehicles|Register and manage your devices."),
                ("bd-driver", "Driver", "Drivers|Manage driver profiles tied to events and scores."),
                ("bd-fleet", "Fleet", "Fleets|Group vehicles and drivers into fleets/depots."),
            ], "Basic Data|Manage vehicles, drivers and fleets.")
            + '<div class="fm-side-foot"><div class="fm-plan"><span class="fm-plan-dot"></span> Demo plan</div></div></aside>')


def _rail_subscription():
    return ('<aside class="fm-rail" data-rail="subscription">'
            + _nav("sub-invoices", "fa-file-invoice", "Invoices", "Invoices|Your billing statements and anything due.")
            + _nav("sub-details", "fa-id-card", "Subscription Details", "Subscription Details|Your current plan, seats, devices and renewal.")
            + _nav("sub-features", "fa-puzzle-piece", "Additional Features", "Additional Features|Optional modules and add-ons.")
            + _nav("sub-contacts", "fa-address-book", "Contacts", "Contacts|Who receives billing and technical notices.")
            + _nav("sub-delivery", "fa-paper-plane", "Invoice Delivery", "Invoice Delivery|How and where invoices are sent.")
            + _nav("sub-orgs", "fa-building", "Your Organizations", "Organizations|Manage multiple entities under one login.")
            + '<div class="fm-side-foot"><div class="fm-plan"><span class="fm-plan-dot"></span> Demo plan</div></div></aside>')


def _rail_settings():
    return ('<aside class="fm-rail" data-rail="settings">'
            + _nav("set-general", "fa-building", "General", "General|Company info, branding, units and preferences.")
            + _nav("set-users", "fa-users", "Users & Roles", "Users & Roles|Invite people and control their access.")
            + _nav("set-privacy", "fa-lock", "Privacy", "Privacy & Security|2FA, data retention and audit log.")
            + _nav("set-notifications", "fa-bell", "Notifications", "Notifications|Choose what you're alerted about, how and when.")
            + '<div class="fm-side-foot"><div class="fm-plan"><span class="fm-plan-dot"></span> Demo plan</div></div></aside>')


# ───────────────────────── Assembly ─────────────────────────

_TOPBAR = (
    '<div class="fm-topbar"><div class="fm-brand"><i class="fa-solid fa-shield-halved"></i> FleetMind</div>'
    '<div class="fm-topnav">'
    '<span class="fm-topnav-item active" data-top="vision">Vision</span>'
    '<span class="fm-topnav-item" data-top="subscription">Subscription</span>'
    '<span class="fm-topnav-item" data-top="settings">Settings</span></div>'
    '<div class="fm-topicons">'
    '<i class="fa-solid fa-bell" data-tip="Notifications|Real-time pushes for critical events — accidents, panic button, unauthorised driver."></i>'
    '<i class="fa-solid fa-circle-question" data-tip="Help|In-app guides and support."></i>'
    '<span class="fm-avatar">AD</span></div></div>'
)

_VIEWS = (
    _v_dashboard() + _v_map() + _v_risk() + _v_events() + _v_fuel_realtime() + _v_fuel_usage()
    + _v_compliance() + _v_reports() + _v_coaching() + _v_bd_vehicle() + _v_bd_driver() + _v_bd_fleet()
    + _v_invoices() + _v_sub_details() + _v_sub_features() + _v_sub_contacts() + _v_sub_delivery() + _v_sub_orgs()
    + _v_set_general() + _v_set_users() + _v_set_privacy() + _v_set_notifications()
)

content = r"""
<div id="platform" class="content-section hidden">

    <div class="card fade-up">
        <h2><i class="fa-solid fa-chart-line" style="color: var(--gold); margin-right: 10px;"></i>Try your platform — full live demo</h2>
        <p>This is a hands-on clone of your FleetMind platform. Use the <strong>top tabs</strong> (Vision · Subscription · Settings) and the <strong>left menu</strong> (with its submenus) to move through every screen — and <strong style="color: var(--gold);">hover any function</strong> for a pop-up explanation. It's a sandbox with sample data; explore freely.</p>
    </div>

    <div class="card fade-up" style="padding: 14px; overflow: hidden;">
      <div class="fm-window">
        <div class="fm-chrome">
            <span class="fm-dot" style="background:#ff5f57;"></span>
            <span class="fm-dot" style="background:#febc2e;"></span>
            <span class="fm-dot" style="background:#28c840;"></span>
            <span class="fm-url"><i class="fa-solid fa-lock" style="font-size:0.62rem; margin-right:6px; opacity:0.6;"></i>app.fleetmind.com<span id="fm-crumb">/dashboard</span></span>
            <span class="fm-live"><span class="fm-live-dot"></span> Demo</span>
        </div>
        <div class="fm-sim">
            __TOPBAR__
            <div class="fm-body">
                __RAILS__
                <main class="fm-main">
                    __VIEWS__
                </main>
            </div>
        </div>
      </div>
    </div>

    <div id="fm-tip" class="fm-tip"></div>

    <style>
        .fm-window { border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.10); box-shadow: 0 24px 60px rgba(0,0,0,0.45); }
        .fm-chrome { display:flex; align-items:center; gap:7px; padding:10px 14px; background:#1b1726; border-bottom:1px solid rgba(255,255,255,0.06); }
        .fm-dot { width:11px; height:11px; border-radius:50%; display:inline-block; }
        .fm-url { margin-left:14px; background:rgba(255,255,255,0.06); color:#b9b2cc; font-size:0.74rem; padding:5px 14px; border-radius:20px; font-family:'Inter',sans-serif; }
        .fm-url #fm-crumb { color:#8b84a0; }
        .fm-live { margin-left:auto; color:#cdb6ff; font-size:0.7rem; font-weight:600; display:inline-flex; align-items:center; gap:6px; }
        .fm-live-dot { width:7px; height:7px; border-radius:50%; background:#9b6bff; box-shadow:0 0 0 3px rgba(155,107,255,0.25); }

        .fm-sim { background:#f8f9fc; color:#0f1624; font-family:'DM Sans','Inter',sans-serif; }
        .fm-sim *, .fm-tip * { box-sizing:border-box; }
        .fm-topbar { display:flex; align-items:center; gap:22px; height:54px; padding:0 18px; background:#edeef3; border-bottom:1px solid #e2e3ea; }
        .fm-brand { font-weight:800; font-size:1.05rem; color:#2c1d52; display:inline-flex; align-items:center; gap:8px; }
        .fm-brand i { color:#7c5cff; }
        .fm-topnav { display:flex; gap:18px; }
        .fm-topnav-item { font-size:0.85rem; color:#6b7280; font-weight:600; cursor:pointer; padding-bottom:2px; border-bottom:2px solid transparent; }
        .fm-topnav-item.active { color:#0f1624; border-bottom-color:#7c5cff; }
        .fm-topicons { margin-left:auto; display:flex; align-items:center; gap:16px; color:#8089a0; }
        .fm-topicons i { cursor:pointer; }
        .fm-avatar { width:30px; height:30px; border-radius:50%; background:#7c5cff; color:#fff; font-size:0.72rem; font-weight:700; display:flex; align-items:center; justify-content:center; }

        .fm-body { display:flex; min-height:560px; }
        .fm-rail { width:212px; flex-shrink:0; background:#fff; border-right:1px solid #e9eaf0; padding:14px 12px; position:relative; display:none; }
        .fm-rail.active { display:block; }
        .fm-nav { display:flex; align-items:center; gap:11px; padding:10px 12px; border-radius:9px; font-size:0.85rem; font-weight:600; color:#3f4658; cursor:pointer; margin-bottom:2px; }
        .fm-nav i { width:16px; text-align:center; color:#8089a0; font-size:0.9rem; }
        .fm-nav:hover { background:#f3f1fd; color:#0f1624; } .fm-nav:hover i { color:#7c5cff; }
        .fm-nav.active { background:#f0ecff; color:#5b3cc4; } .fm-nav.active i { color:#7c5cff; }
        .fm-subnav { padding-left:38px; font-size:0.82rem; font-weight:500; }
        .fm-group-head { display:flex; align-items:center; gap:11px; padding:10px 12px; border-radius:9px; font-size:0.85rem; font-weight:600; color:#3f4658; cursor:pointer; }
        .fm-group-head i:first-child { width:16px; text-align:center; color:#8089a0; font-size:0.9rem; }
        .fm-group-head:hover { background:#f3f1fd; }
        .fm-caret { margin-left:auto; font-size:0.7rem !important; transition:transform .2s; color:#a3a9b8 !important; }
        .fm-group.open .fm-caret { transform:rotate(90deg); }
        .fm-sub { display:none; } .fm-group.open .fm-sub { display:block; }
        .fm-side-foot { position:absolute; left:12px; right:12px; bottom:14px; }
        .fm-plan { font-size:0.72rem; color:#8089a0; display:flex; align-items:center; gap:7px; }
        .fm-plan-dot { width:7px; height:7px; border-radius:50%; background:#16a34a; }

        .fm-main { flex:1; padding:20px 22px; overflow:hidden; min-width:0; }
        .fm-page-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; gap:12px; flex-wrap:wrap; }
        .fm-page-head h3 { margin:0; font-size:1.35rem; font-weight:800; color:#0f1624; display:flex; align-items:center; gap:10px; }
        .fm-head-badge { font-size:0.64rem; font-weight:700; color:#7c5cff; background:#f0ecff; padding:3px 9px; border-radius:6px; }
        .fm-subtle { color:#8089a0; font-size:0.85rem; margin:-8px 0 16px; }
        .fm-pills { display:flex; gap:8px; flex-wrap:wrap; }
        .fm-pill { background:#fff; border:1px solid #e2e3ea; border-radius:8px; padding:7px 12px; font-size:0.78rem; color:#3f4658; font-weight:600; cursor:pointer; display:inline-flex; align-items:center; gap:7px; }
        .fm-pill i { font-size:0.62rem; color:#8089a0; } .fm-pill:hover { border-color:#c9bdf6; }
        .fm-btn { background:#fff; border:1px solid #e2e3ea; border-radius:8px; padding:7px 14px; font-size:0.78rem; color:#3f4658; font-weight:600; cursor:pointer; display:inline-flex; align-items:center; gap:7px; }
        .fm-btn:hover { border-color:#c9bdf6; }
        .fm-btn-primary { background:#2c3344; border-color:#2c3344; color:#fff; }
        .fm-btn-primary:hover { background:#3a4358; border-color:#3a4358; }

        .fm-insight { display:flex; align-items:center; gap:12px; background:linear-gradient(135deg,#f3efff,#fbfaff); border:1px solid #e6def9; border-radius:12px; padding:13px 16px; font-size:0.84rem; color:#3f4658; margin-bottom:16px; }
        .fm-insight i { color:#7c5cff; font-size:1rem; } .fm-insight em { color:#0f1624; font-style:normal; font-weight:700; }
        .fm-insight-link { margin-left:auto; color:#7c5cff; font-weight:700; font-size:0.78rem; white-space:nowrap; }

        .fm-kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:16px; }
        .fm-kpi { background:#fff; border:1px solid #e9eaf0; border-radius:12px; padding:16px; transition:box-shadow .15s, transform .15s; }
        .fm-kpi:hover { box-shadow:0 8px 24px rgba(124,92,255,0.10); transform:translateY(-2px); }
        .fm-kpi-label { font-size:0.72rem; color:#8089a0; text-transform:uppercase; letter-spacing:0.6px; font-weight:600; }
        .fm-kpi-val { font-size:1.7rem; font-weight:800; color:#0f1624; margin-top:6px; }
        .fm-kpi-val span { font-size:0.78rem; color:#8089a0; font-weight:600; margin-left:3px; }
        .fm-kpi-trend { font-size:0.72rem; font-weight:600; margin-top:4px; color:#8089a0; }
        .fm-kpi-trend .up { color:#16a34a; font-weight:700; }
        .fm-kpi-score { display:flex; flex-direction:column; align-items:flex-start; }
        .fm-donut { width:78px; height:78px; border-radius:50%; margin:8px auto 0; display:flex; align-items:center; justify-content:center; background:conic-gradient(#7c5cff calc(var(--pct)*1%), #ece9f6 0); position:relative; }
        .fm-donut::before { content:''; position:absolute; inset:9px; background:#fff; border-radius:50%; }
        .fm-donut span { position:relative; font-weight:800; font-size:1.1rem; color:#0f1624; }
        .fm-donut small { font-size:0.6rem; color:#8089a0; font-weight:600; }

        .fm-row2 { display:grid; grid-template-columns:1.6fr 1fr 1fr; gap:14px; }
        .fm-row2b { display:grid; grid-template-columns:1.7fr 1fr; gap:14px; }
        .fm-panel { background:#fff; border:1px solid #e9eaf0; border-radius:12px; padding:14px 16px; }
        .fm-panel-head { font-size:0.9rem; font-weight:700; color:#0f1624; display:flex; justify-content:space-between; align-items:baseline; margin-bottom:10px; }
        .fm-panel-head span { font-size:0.7rem; color:#a3a9b8; font-weight:600; }
        .fm-chart svg { width:100%; height:90px; display:block; }
        .fm-axis { display:flex; justify-content:space-between; font-size:0.66rem; color:#a3a9b8; margin-top:4px; }
        .fm-rank { list-style:none; margin:0; padding:0; }
        .fm-rank li { display:flex; align-items:center; gap:10px; padding:7px 0; font-size:0.84rem; color:#3f4658; border-bottom:1px solid #f1f2f6; }
        .fm-rank li:last-child { border-bottom:none; }
        .fm-rank .fm-rk { width:18px; height:18px; border-radius:50%; background:#f0ecff; color:#7c5cff; font-size:0.66rem; font-weight:700; display:flex; align-items:center; justify-content:center; }
        .fm-rank b { margin-left:auto; color:#0f1624; }
        .fm-bars { list-style:none; margin:0; padding:0; }
        .fm-bars li { display:flex; align-items:center; gap:8px; font-size:0.76rem; color:#6b7280; padding:5px 0; }
        .fm-bars li span { width:74px; flex-shrink:0; }
        .fm-bars li i { height:7px; border-radius:4px; background:linear-gradient(90deg,#7c5cff,#a78bfa); display:block; }
        .fm-bars li b { margin-left:auto; color:#0f1624; }

        /* Map */
        .fm-map-wrap { display:flex; border:1px solid #e9eaf0; border-radius:12px; overflow:hidden; height:540px; }
        .fm-vehlist { width:280px; flex-shrink:0; background:#fff; border-right:1px solid #e9eaf0; overflow:auto; }
        .fm-veh-search { margin:0 14px 8px; background:#f3f4f8; border-radius:8px; padding:8px 12px; font-size:0.78rem; color:#a3a9b8; }
        .fm-veh-search i { margin-right:6px; }
        .fm-veh { display:flex; align-items:center; gap:10px; padding:11px 14px; border-top:1px solid #f1f2f6; cursor:pointer; }
        .fm-veh:hover { background:#f8f7ff; }
        .fm-veh b { font-size:0.83rem; color:#0f1624; } .fm-veh small { display:block; font-size:0.7rem; color:#a3a9b8; }
        .fm-veh-spd { margin-left:auto; font-size:0.74rem; font-weight:700; color:#3f4658; }
        .fm-veh-dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
        .fm-veh-dot.moving { background:#16a34a; } .fm-veh-dot.idle { background:#f59e0b; } .fm-veh-dot.offline { background:#b8bdc9; }
        .fm-map { flex:1; position:relative; background:radial-gradient(circle at 40% 30%, #eef1f7, #e4e8f1); overflow:hidden; }
        .fm-map-grid { position:absolute; inset:0; background-image:linear-gradient(#d7dce8 1px,transparent 1px),linear-gradient(90deg,#d7dce8 1px,transparent 1px); background-size:46px 46px; opacity:0.5; }
        .fm-pin { position:absolute; width:30px; height:30px; border-radius:50% 50% 50% 0; transform:rotate(-45deg); display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(0,0,0,0.2); cursor:pointer; }
        .fm-pin i { transform:rotate(45deg); color:#fff; font-size:0.72rem; }
        .fm-pin.moving { background:#16a34a; } .fm-pin.idle { background:#f59e0b; }
        .fm-pin:hover { z-index:5; filter:brightness(1.08); }
        .fm-map-scale { position:absolute; left:14px; bottom:12px; font-size:0.66rem; color:#6b7280; background:rgba(255,255,255,0.7); padding:2px 8px; border-radius:4px; }
        .fm-map-zoom { position:absolute; right:14px; bottom:12px; display:flex; flex-direction:column; background:#fff; border:1px solid #e2e3ea; border-radius:8px; overflow:hidden; }
        .fm-map-zoom span { width:28px; height:28px; display:flex; align-items:center; justify-content:center; cursor:pointer; color:#3f4658; }
        .fm-map-zoom span:first-child { border-bottom:1px solid #eef0f4; }

        /* Tabs / subtabs */
        .fm-tabs { display:flex; gap:18px; border-bottom:1px solid #e9eaf0; margin-bottom:8px; }
        .fm-tab { font-size:0.83rem; font-weight:600; color:#8089a0; padding:8px 2px; cursor:pointer; border-bottom:2px solid transparent; }
        .fm-tab b { color:#7c5cff; margin-left:4px; }
        .fm-tab.active { color:#0f1624; border-bottom-color:#7c5cff; }
        .fm-subtabs { display:flex; flex-direction:column; gap:2px; }
        .fm-subtab { font-size:0.84rem; font-weight:600; color:#6b7280; padding:9px 12px; border-radius:8px; cursor:pointer; }
        .fm-subtab.active { background:#f0ecff; color:#5b3cc4; }
        .fm-subtab:hover { background:#f3f1fd; }

        /* Table */
        .fm-table { width:100%; border-collapse:collapse; font-size:0.8rem; }
        .fm-table th { text-align:left; color:#a3a9b8; font-weight:600; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.4px; padding:10px 10px; border-bottom:1px solid #e9eaf0; }
        .fm-table td { padding:11px 10px; border-bottom:1px solid #f1f2f6; color:#3f4658; vertical-align:middle; }
        .fm-table tbody tr { cursor:pointer; } .fm-table tbody tr:hover { background:#f8f7ff; }
        .fm-table td b { color:#0f1624; }
        .fm-empty-row td { text-align:center; color:#a3a9b8; padding:40px; }
        .fm-link { color:#7c5cff; font-weight:600; }
        .fm-eff { color:#16a34a; font-weight:700; } .fm-idle { color:#dc2626; font-weight:700; }
        .fm-clip { position:relative; width:54px; height:34px; border-radius:6px; background:linear-gradient(135deg,#2c2540,#4b4063); display:flex; align-items:center; justify-content:center; color:#fff; }
        .fm-clip i { font-size:0.7rem; opacity:0.9; }
        .fm-clip em { position:absolute; left:3px; bottom:2px; font-style:normal; font-size:0.58rem; background:rgba(0,0,0,0.5); padding:0 4px; border-radius:3px; }
        .fm-sev { display:inline-block; margin-left:8px; font-size:0.62rem; font-weight:700; padding:1px 7px; border-radius:5px; }
        .fm-sev.high { background:#fde8e8; color:#dc2626; } .fm-sev.mid { background:#fef3e2; color:#d97706; }
        .fm-media { font-size:0.66rem; font-weight:700; color:#2563eb; background:#e8f0fe; padding:2px 8px; border-radius:5px; }
        .fm-status { font-size:0.66rem; font-weight:700; color:#d97706; background:#fef3e2; padding:2px 8px; border-radius:5px; }
        .fm-star { color:#c9cdd8; margin-left:6px; }
        .fm-tablefoot { font-size:0.74rem; color:#a3a9b8; margin-top:12px; } .fm-tablefoot span { color:#3f4658; cursor:pointer; }
        .fm-bdg { font-size:0.64rem; font-weight:700; padding:2px 9px; border-radius:6px; }
        .fm-bdg-ok { background:#e6f6ec; color:#16a34a; } .fm-bdg-warn { background:#fef3e2; color:#d97706; }
        .fm-bdg-bad { background:#fde8e8; color:#dc2626; } .fm-bdg-muted { background:#eef0f4; color:#8089a0; }

        /* Filter bar / empty */
        .fm-filterbar { display:flex; align-items:center; gap:12px; background:#fff; border:1px solid #e9eaf0; border-radius:12px; padding:14px 16px; margin-bottom:16px; }
        .fm-filterbar label { font-size:0.8rem; color:#6b7280; font-weight:600; }
        .fm-select, .fm-input { background:#fff; border:1px solid #e2e3ea; border-radius:8px; padding:8px 12px; font-size:0.8rem; color:#3f4658; min-width:200px; display:inline-flex; align-items:center; justify-content:space-between; gap:10px; }
        .fm-empty { display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; min-height:300px; color:#a3a9b8; background:#fff; border:1px solid #e9eaf0; border-radius:12px; }
        .fm-empty i { font-size:2.2rem; color:#d7d2ec; margin-bottom:12px; }

        /* Compliance alerts */
        .fm-alerts { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:16px; }
        .fm-alert { background:#fff; border:1px solid #e9eaf0; border-radius:12px; padding:16px; }
        .fm-alert.crit { border-color:#f6caca; background:#fef5f5; } .fm-alert.warn { border-color:#f6e2bf; background:#fffaf0; } .fm-alert.info { border-color:#cdd9f6; background:#f5f8ff; }
        .fm-alert-tag { font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px; }
        .fm-alert.crit .fm-alert-tag { color:#dc2626; } .fm-alert.warn .fm-alert-tag { color:#d97706; } .fm-alert.info .fm-alert-tag { color:#2563eb; }
        .fm-alert h4 { margin:0 0 5px; font-size:0.9rem; color:#0f1624; } .fm-alert p { margin:0 0 12px; font-size:0.76rem; color:#6b7280; }

        /* Subscription / settings extras */
        .fm-plan-big { font-size:1.5rem; font-weight:800; color:#0f1624; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
        .fm-deflist { list-style:none; margin:0 0 14px; padding:0; } .fm-deflist li { display:flex; justify-content:space-between; padding:7px 0; font-size:0.82rem; color:#6b7280; border-bottom:1px solid #f1f2f6; } .fm-deflist b { color:#0f1624; }
        .fm-tiers { list-style:none; margin:0; padding:0; } .fm-tiers li { padding:11px 12px; border:1px solid #eef0f4; border-radius:9px; margin-bottom:8px; font-size:0.82rem; color:#6b7280; }
        .fm-tiers li b { color:#0f1624; display:block; } .fm-tiers li.cur { border-color:#c9bdf6; background:#faf8ff; position:relative; } .fm-tiers li.cur em { position:absolute; right:12px; top:12px; font-style:normal; font-size:0.64rem; font-weight:700; color:#7c5cff; }
        .fm-feat-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:12px; }
        .fm-feat { display:flex; align-items:center; justify-content:space-between; background:#fff; border:1px solid #e9eaf0; border-radius:10px; padding:14px 16px; }
        .fm-feat b { color:#0f1624; font-size:0.86rem; display:block; } .fm-feat span { color:#8089a0; font-size:0.72rem; }
        .fm-toggle { width:38px; height:21px; border-radius:20px; background:#d7dce8; position:relative; flex-shrink:0; transition:background .2s; }
        .fm-toggle::after { content:''; position:absolute; top:2px; left:2px; width:17px; height:17px; border-radius:50%; background:#fff; transition:left .2s; box-shadow:0 1px 3px rgba(0,0,0,0.2); }
        .fm-toggle.on { background:#7c5cff; } .fm-toggle.on::after { left:19px; }
        .fm-form-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px 18px; margin-bottom:16px; }
        .fm-field { display:flex; flex-direction:column; gap:6px; } .fm-field label { font-size:0.74rem; color:#8089a0; font-weight:600; }
        .fm-field .fm-input, .fm-field .fm-select { min-width:0; }
        .fm-settings-wrap { display:flex; gap:18px; } .fm-settings-aside { width:180px; flex-shrink:0; } .fm-settings-main { flex:1; min-width:0; }

        .fm-tip { position:fixed; z-index:99999; max-width:280px; background:#15101f; color:#ECE7F5; border:1px solid rgba(244,201,93,0.45); border-radius:10px; padding:11px 13px; font-size:0.8rem; line-height:1.5; box-shadow:0 16px 40px rgba(0,0,0,0.5); opacity:0; visibility:hidden; transform:translateY(6px); transition:opacity .15s ease, transform .15s ease; pointer-events:none; font-family:'Inter',sans-serif; }
        .fm-tip.show { opacity:1; visibility:visible; transform:translateY(0); }
        .fm-tip .fm-tip-title { color:var(--gold); font-weight:700; display:block; margin-bottom:3px; font-size:0.78rem; }

        @media (max-width: 920px) {
            .fm-kpis, .fm-alerts { grid-template-columns:repeat(2,1fr); }
            .fm-row2, .fm-row2b, .fm-feat-grid, .fm-form-grid { grid-template-columns:1fr; }
            .fm-rail { width:62px; } .fm-nav, .fm-group-head { font-size:0; gap:0; justify-content:center; } .fm-nav i, .fm-group-head i:first-child { font-size:1rem; } .fm-caret, .fm-subnav { display:none; }
            .fm-vehlist { width:170px; } .fm-settings-wrap { flex-direction:column; } .fm-settings-aside { width:100%; } .fm-subtabs { flex-direction:row; flex-wrap:wrap; }
        }
    </style>

    <script>
    (function () {
        var root = document.getElementById('platform');
        if (!root || root.dataset.fmInit) return;
        root.dataset.fmInit = '1';

        var rails = root.querySelectorAll('.fm-rail');
        var views = root.querySelectorAll('.fm-view');
        var tops = root.querySelectorAll('.fm-topnav-item');
        var crumb = root.querySelector('#fm-crumb');

        var defaultView = { vision:'dashboard', subscription:'sub-invoices', settings:'set-general' };
        var crumbMap = {
            dashboard:'/dashboard', 'safety-map':'/safety/map', 'safety-risk':'/safety/risk-prediction',
            'safety-events':'/safety/events', 'fuel-realtime':'/fuel/realtime', 'fuel-usage':'/fuel/usage',
            compliance:'/compliance', reports:'/reports', coaching:'/coaching',
            'bd-vehicle':'/basic-data/vehicle', 'bd-driver':'/basic-data/driver', 'bd-fleet':'/basic-data/fleet',
            'sub-invoices':'/invoices', 'sub-details':'/subscription', 'sub-features':'/features',
            'sub-contacts':'/contacts', 'sub-delivery':'/invoice-delivery', 'sub-orgs':'/organizations',
            'set-general':'/settings/general', 'set-users':'/settings/users-roles', 'set-privacy':'/settings/privacy', 'set-notifications':'/settings/notifications'
        };

        function showView(view) {
            views.forEach(function (v) { v.hidden = (v.getAttribute('data-view') !== view); });
            root.querySelectorAll('.fm-nav, .fm-subnav').forEach(function (n) {
                n.classList.toggle('active', n.getAttribute('data-view') === view);
            });
            if (crumb && crumbMap[view]) crumb.textContent = crumbMap[view];
            // open the accordion group that contains this view
            root.querySelectorAll('.fm-group').forEach(function (g) {
                var has = g.querySelector('.fm-subnav[data-view="' + view + '"]');
                if (has) g.classList.add('open');
            });
        }
        function showRail(top) {
            rails.forEach(function (r) { r.classList.toggle('active', r.getAttribute('data-rail') === top); });
            tops.forEach(function (t) { t.classList.toggle('active', t.getAttribute('data-top') === top); });
            showView(defaultView[top]);
        }

        tops.forEach(function (t) { t.addEventListener('click', function () { showRail(t.getAttribute('data-top')); }); });

        // sidebar simple navs
        root.querySelectorAll('.fm-nav[data-view], .fm-subnav[data-view]').forEach(function (n) {
            n.addEventListener('click', function (e) { e.stopPropagation(); showView(n.getAttribute('data-view')); });
        });
        // accordion group headers
        root.querySelectorAll('.fm-group-head').forEach(function (h) {
            h.addEventListener('click', function () {
                var g = h.closest('.fm-group');
                var willOpen = !g.classList.contains('open');
                root.querySelectorAll('.fm-group').forEach(function (o) { o.classList.remove('open'); });
                if (willOpen) g.classList.add('open');
            });
        });
        // inner tabs / subtabs (visual only)
        function bindTabs(sel) {
            root.querySelectorAll(sel).forEach(function (group) {
                group.addEventListener('click', function (e) {
                    var t = e.target.closest(sel.indexOf('subtab') > -1 ? '.fm-subtab' : '.fm-tab');
                    if (!t) return;
                    group.querySelectorAll(sel.indexOf('subtab') > -1 ? '.fm-subtab' : '.fm-tab').forEach(function (x) { x.classList.remove('active'); });
                    t.classList.add('active');
                });
            });
        }
        bindTabs('.fm-tabs'); bindTabs('.fm-subtabs');
        // toggles
        root.querySelectorAll('.fm-toggle').forEach(function (tg) {
            tg.addEventListener('click', function (e) { e.stopPropagation(); tg.classList.toggle('on'); });
        });

        // hover explanation popup
        var tip = root.querySelector('#fm-tip');
        function place(el) {
            var r = el.getBoundingClientRect();
            tip.style.left = Math.max(8, Math.min(r.left, window.innerWidth - 300)) + 'px';
            var top = r.bottom + 10;
            if (top + tip.offsetHeight > window.innerHeight) top = r.top - tip.offsetHeight - 10;
            tip.style.top = Math.max(8, top) + 'px';
        }
        root.querySelectorAll('[data-tip]').forEach(function (el) {
            el.addEventListener('mouseenter', function () {
                var parts = (el.getAttribute('data-tip') || '').split('|');
                tip.innerHTML = parts.length > 1 ? '<span class="fm-tip-title">' + parts[0] + '</span>' + parts.slice(1).join('|') : parts[0];
                tip.classList.add('show'); place(el);
            });
            el.addEventListener('mouseleave', function () { tip.classList.remove('show'); });
        });

        showRail('vision');
    })();
    </script>

</div>
""".replace("__TOPBAR__", _TOPBAR).replace("__RAILS__", _rail_vision() + _rail_subscription() + _rail_settings()).replace("__VIEWS__", _VIEWS)

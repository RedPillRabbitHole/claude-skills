---
name: sonicwall-skill
description: Provides step-by-step SonicWall configuration instructions using official SonicWall documentation as the primary source. Covers SonicWall firewalls (TZ, NSa, NSsp series), Cloud Secure Edge (CSE) ZTNA/SASE platform, and Network Security Manager (NSM) centralized management. Always searches official docs first (sonicwall.com, cse-docs.sonicwall.com, MySonicWall). Prioritizes GUI over CLI. Provides accurate, beginner-friendly instructions verified against official sources before responding.
---

# SonicWall Skill

## Purpose

This skill provides accurate, step-by-step SonicWall configuration and troubleshooting instructions based on **official SonicWall documentation only**. It covers three product areas:

1. **SonicWall Firewalls** — TZ, NSa, NSsp, NSv series (SonicOS)
2. **Cloud Secure Edge (CSE)** — Zero Trust / SASE remote access platform (formerly Banyan Security)
3. **Network Security Manager (NSM)** — Centralized multi-device firewall management

---

## CRITICAL RULES — Read Before Responding

### Rule 1: Official Sources First — Always

**Before writing any instructions, search official SonicWall documentation.**

Do NOT rely on training data for procedural steps. SonicWall's UI, menu paths, and feature names change between firmware versions. Training data may be wrong or outdated.

**Search order:**
1. `site:sonicwall.com [topic]` — KB articles, tech docs, admin guides
2. `site:cse-docs.sonicwall.com [topic]` — CSE-specific docs
3. `site:docs.banyansecurity.io [topic]` — CSE legacy docs (still valid)
4. SonicWall community forums (`community.sonicwall.com`) — if official docs incomplete
5. Reddit (`r/sonicwall`), other forums — last resort only, flag as unofficial

**If no official source found:** State this clearly and flag any community/unofficial information with:
```
⚠️ WARNING: No official SonicWall documentation found for this topic.
The following is from community/unofficial sources and may be inaccurate or outdated.
Source: [URL]
```

### Rule 2: GUI First

Always provide web management interface (SonicOS GUI) instructions as the primary method. Only provide CLI if:
- No GUI method exists
- User explicitly asks for CLI
- The task is only possible via CLI

### Rule 3: No Made-Up Steps

If you cannot find a specific menu path, field name, or procedure in official documentation, say so. Do not guess. Do not invent steps. State what you found and what you could not verify.

### Rule 4: Version Awareness

SonicOS 7.x (Gen 7 hardware) and SonicOS 6.x (Gen 6 hardware) have different UIs. CSE integration requires **SonicOS 7.1.2 or higher**. NSM behavior varies by version. Always clarify firmware version where relevant.

---

## Skill Indicator

Begin all responses with:
```
🔷 Using SonicWall Skill
```

---

## Product Coverage

### Firewalls — SonicOS

**TZ Series (Small/Branch Office):**
- TZ270, TZ370, TZ470, TZ570, TZ670
- TZ270W, TZ370W, TZ470W, TZ570W (wireless variants)

**NSa Series (Mid-size Enterprise):**
- NSa 2700, NSa 3700, NSa 4700, NSa 5700, NSa 6700

**NSsp Series (High Performance):**
- NSsp 12400, NSsp 12800, NSsp 15700

**NSv Series (Virtual):**
- NSv 270, NSv 470, NSv 870 (VMware, Hyper-V, AWS, Azure, KVM)

**Generation Reference:**
- Gen 7 = TZ270-TZ670, NSa 2700+, NSsp 12400+ → SonicOS 7.x
- Gen 6 = TZ300-TZ600, NSA 2650-6650 → SonicOS 6.5.x

---

### Cloud Secure Edge (CSE)

CSE (formerly Banyan Security, acquired by SonicWall) is a **Zero Trust Network Access (ZTNA) / Security Service Edge (SSE)** platform. It replaces traditional SSL VPN with a cloud-brokered, clientless or client-based access model.

**CSE is NOT the same as the firewall.** It is a separate cloud platform managed at:
- `console.banyanops.com` (legacy)
- Or through MySonicWall / Capture Security Center

**CSE Components:**
- **Connector** — Installed on Gen 7 firewall (SonicOS 7.1.2+) or standalone Linux VM. Dial-out only, no inbound ports needed. Creates WireGuard tunnel to CSE Global Edge Network.
- **CSE App (Endpoint Client)** — Installed on user devices (Windows, macOS, iOS, Android). Replaces VPN client.
- **Access Tier** — SonicWall-managed cloud proxy (Global Edge) or self-hosted (Private Edge)
- **Command Center / Console** — Web portal for policy, users, services configuration
- **MySonicWall** — License activation and registration

**CSE Use Cases:**
- Zero Trust remote access (replacing SSL VPN)
- ZTNA for internal apps (web, RDP, SSH, infrastructure)
- VPN-as-a-Service (VPNaaS)
- Secure Web Gateway (SWG)
- Cloud Access Security Broker (CASB)
- Device Trust enforcement

**CSE Documentation URLs:**
- Primary: `https://cse-docs.sonicwall.com/`
- Legacy (still valid): `https://docs.banyansecurity.io/`
- SonicOS integration guide: `https://www.sonicwall.com/support/technical-documentation/`

**Key CSE Technical Facts:**
- Connector uses WireGuard tunnels (outbound only from firewall to CSE POPs)
- CSE infrastructure enforces access control — NOT the SonicWall firewall
- SonicOS creates a Group Address Object automatically per Connector
- Internal domain resolution: Wildcard DNS entries (`*.domain.local`) must be added in Connector settings to route internal domain queries through the tunnel
- Requires SonicOS 7.1.2 or higher for firewall-integrated Connector
- CSE trial activated via MySonicWall (`mysonicwall.com`)

---

### Network Security Manager (NSM)

NSM is SonicWall's **centralised multi-device firewall management platform**. It replaces the older Global Management System (GMS) and Capture Security Center Management (CSC MA).

**NSM is NOT a firewall.** It is a management layer on top of your firewalls.

**Deployment Options:**
- **NSM SaaS (Cloud)** — Hosted by SonicWall, accessed at `cloud.sonicwall.com`. No on-prem install needed.
- **NSM On-Premises** — Self-hosted on ESXi or Hyper-V. Requires separate SonicWall Analytics install for reporting/analytics.

**NSM Key Features:**
- Centralised policy management across all SonicWall firewalls
- Multi-tenant (MSP-ready)
- Auditable change workflows
- Firmware management (push updates to devices)
- Zero Touch Provisioning (ZTP) — devices phone home to NSM automatically via MySonicWall
- Reporting (Essentials: 7 days; Advanced: 365 days)
- SD-WAN and VPN orchestration

**NSM Licensing Tiers:**
- NSM Essentials — 7-day reporting
- NSM Advanced — 365-day reporting + 30-day log analytics

**NSM Technical Facts:**
- Cloud NSM accessed at: `cloud.sonicwall.com`
- ZTP communication uses TCP/UDP port **21021** (must be open inbound/outbound on ISP side)
- With Zero Touch enabled, firewall phones home through MySonicWall — WAN management access not required to be open
- With Zero Touch disabled, firewall communicates to NSM via `cloud.sonicwall.com` configured under `Appliance | Base Settings | Advanced Management`
- Local modifications on firewall after NSM acquisition are not recommended (NSM owns config)
- NSM is the replacement for GMS (Global Management System)

**NSM Documentation URLs:**
- `https://www.sonicwall.com/support/technical-documentation/` (search for NSM)
- `https://www.sonicwall.com/support/knowledge-base/sonicwall-network-security-manager-nsm-faq/`

---

## Source Priority & Search Strategy

### Step 1 — Search Official SonicWall Docs First

For **firewall/SonicOS** topics:
```
web_search: site:sonicwall.com [feature] [model if known] SonicOS
web_search: site:sonicwall.com [feature] configuration guide
```

For **CSE** topics:
```
web_search: site:cse-docs.sonicwall.com [topic]
web_search: site:docs.banyansecurity.io [topic]
web_search: site:sonicwall.com cloud secure edge [topic]
```

For **NSM** topics:
```
web_search: site:sonicwall.com NSM [topic]
web_search: site:sonicwall.com "network security manager" [topic]
```

### Step 2 — Fetch Full Documentation

Use `web_fetch` on any SonicWall KB, tech doc, or CSE doc URL returned in search results. Snippets are often truncated — fetch the full page before writing instructions.

Useful base URLs to fetch from:
- `https://www.sonicwall.com/support/knowledge-base/`
- `https://www.sonicwall.com/support/technical-documentation/`
- `https://cse-docs.sonicwall.com/docs/`
- `https://docs.banyansecurity.io/docs/`

### Step 3 — If Official Docs Insufficient

Try:
```
web_search: site:community.sonicwall.com [topic]
web_search: sonicwall [topic] reddit
web_search: sonicwall [topic] forum
```

Always flag community/unofficial content with the warning block.

### Step 4 — Check Firmware Version Compatibility

When relevant, verify whether the instruction applies to SonicOS 6.x or 7.x. Many KB articles specify a version. If unknown, note the ambiguity.

---

## Firewall Default Access Reference

| Item | Value |
|---|---|
| LAN IP (default) | 192.168.168.168 |
| Web interface | https://192.168.168.168 |
| Default username | admin |
| Default password | password (or check label) |
| SSH | ssh admin@192.168.168.168 |
| Serial console | 115200 baud, 8-N-1 |
| Browser | Chrome or Firefox recommended |

**First login:** Setup Wizard will appear. Can be skipped.

**Certificate warning on first login:** Expected. Click Advanced > Proceed (Chrome) or Accept Risk (Firefox).

---

## SonicOS Navigation Reference (Gen 7 / SonicOS 7.x)

**Top menu bar tabs:**
- **Dashboard** — Status, widgets, threat overview
- **Network** — Interfaces, zones, DHCP, DNS, routing
- **Object** — Address objects, service objects, groups
- **Policy** — Firewall rules, NAT, app control, routing policies
- **Security Services** — IPS, GAV, anti-spyware, content filter, Capture ATP, DPI-SSL
- **VPN** — IPsec VPN, SSL VPN, CSE Connector
- **Device** — System settings, certificates, backups, firmware, diagnostics, logs
- **Users** — Local users/groups, RADIUS, SSO, guest services

**Saving configuration:**
- Changes are pending until you click the **Accept** button in the yellow banner at the top
- Some dialogs use **Add** to append an item, then **Accept** to commit
- **Backup before major changes:** Device > Settings > Firmware Management > Export Configuration

---

## CSE Navigation Reference

**CSE Console (cloud portal):**
- Login: `console.banyanops.com` or via MySonicWall
- **Directory** — Users, groups, device registrations
- **Networks** — Registered Networks (private resources exposed to CSE users)
- **Services** — Published apps/services (web, SSH, RDP, infrastructure)
- **Policies** — Access control rules (who can access what)
- **Connectors** — Manage installed connectors, view status
- **Settings** — IDP integration, Trust Levels, device policy, event logs

**SonicOS CSE Integration (on the firewall):**
- Navigate to: **VPN > Cloud Secure Edge** (SonicOS 7.1.2+)
- CSE status, Connector configuration, and published networks are managed here

---

## NSM Navigation Reference

**NSM Cloud Portal:**
- Login: `cloud.sonicwall.com`
- Sign in with MySonicWall credentials
- **Firewall Manager** — Device inventory, policy management, firmware
- **Analytics** — Traffic reports, threat logs (Advanced license only)
- **Tenants** — Multi-tenant management (MSP use)
- **Zero Touch** — Provision new devices without being on-site

**Adding a firewall to NSM:**
- Zero Touch (recommended): Enable in MySonicWall device settings. Firewall phones home automatically.
- Manual: On firewall, go to **Device > Settings > Base Settings > Advanced Management**, set NSM cloud address to `cloud.sonicwall.com`

---

## Response Format Templates

### Standard Firewall Task

```
🔷 Using SonicWall Skill

[Task Title] — SonicOS Web Interface

Source: [Official KB/doc URL]

Prerequisites:
- [Any required licences, objects, or prior config]

Steps:

1. Access the SonicWall web interface
   - Connect to a LAN port, open browser, go to https://192.168.168.168
   - Log in: admin / password (or check device label)

2. Navigate to [Menu Path]
   - Click [Tab] in the top menu
   - Click [Section] in the left sidebar

3. [Action]
   - Field: [Name] → Enter: [Value]
   - Field: [Name] → Select: [Option]

4. Save
   - Click Add / OK to close the dialog
   - Click Accept in the yellow pending changes banner

5. Verify
   - [How to confirm it worked]
   - [Log path to check if needed]
```

### CSE Task

```
🔷 Using SonicWall Skill

[Task Title] — Cloud Secure Edge

Source: [cse-docs.sonicwall.com or docs.banyansecurity.io URL]

Note: CSE has TWO management areas:
- CSE Console (cloud portal) — for policies, services, connectors
- SonicOS GUI (firewall) — for Connector activation and private resource publishing

CSE Console Steps:
1. Log in to [console URL]
2. Navigate to [section]
   ...

SonicOS Steps (if applicable):
1. Log in to firewall at https://[firewall-ip]
2. Navigate to VPN > Cloud Secure Edge
   ...

Verification:
- [How to confirm]
```

### NSM Task

```
🔷 Using SonicWall Skill

[Task Title] — Network Security Manager

Source: [sonicwall.com NSM doc URL]

Note: NSM manages firewalls centrally. Changes made in NSM override local firewall config when deployed.

Steps:
1. Log in to NSM at https://cloud.sonicwall.com
   - Use MySonicWall credentials

2. Navigate to [section]

3. [Action]

4. Deploy/Push changes
   - [How to commit and push to devices]

5. Verify on firewall
   - [Check that change appears on managed device]
```

---

## Detailed Examples

### Example 1 — Port Forwarding (NAT Policy) on TZ370

```
🔷 Using SonicWall Skill

Port Forwarding (Inbound NAT Policy) — SonicWall TZ370, SonicOS 7.x

Source: https://www.sonicwall.com/support/knowledge-base/ (search: NAT policy port forwarding)

Prerequisites:
- You know the internal server's IP address
- You know which port/service to forward (e.g., TCP 443 for HTTPS)
- You have a static or dynamic WAN IP on the firewall

1. Log in to the SonicWall web interface
   - Browser → https://192.168.168.168
   - Username: admin | Password: password (or device label)
   - If first login, skip the wizard

2. Create an Address Object for the internal server
   - Top menu: Object > Address Objects
   - Click Add
     - Name: Internal-Web-Server
     - Zone: LAN
     - Type: Host
     - IP Address: 192.168.1.50 (your server IP)
   - Click Add to save

3. Navigate to NAT Policies
   - Top menu: Policy > NAT Policies
   - Click Add

4. Configure the NAT Policy
   - Original Source: Any
   - Translated Source: Original
   - Original Destination: [Select your WAN interface object, e.g. "WAN Interface IP"]
   - Translated Destination: Internal-Web-Server (object created in step 2)
   - Original Service: HTTPS (port 443) — or create a custom service object under Object > Service Objects
   - Translated Service: Original
   - Inbound Interface: WAN (X1)
   - Outbound Interface: LAN
   - Enable NAT Policy: Checked
   - Create a reflexive policy: Optionally check (creates reverse NAT)
   - Click Add

5. Create a Firewall Access Rule (may auto-create, verify manually)
   - Top menu: Policy > Rules and Policies
   - Look for a WAN→LAN rule allowing HTTPS to Internal-Web-Server
   - If not auto-created, click Add:
     - Action: Allow
     - From Zone: WAN | To Zone: LAN
     - Source: Any
     - Destination: Internal-Web-Server
     - Service: HTTPS
   - Click Add

6. Accept changes
   - Click Accept in the yellow pending changes banner

7. Verify
   - From an external connection, browse to https://[your-WAN-IP]
   - Check Device > Log > View for connection events
   - Logs will show NAT translations and allow/deny decisions
```

---

### Example 2 — CSE Connector Setup on Gen 7 Firewall (SonicOS 7.1.2+)

```
🔷 Using SonicWall Skill

Cloud Secure Edge (CSE) Connector — Setup on SonicWall Gen 7 Firewall

Source: https://cse-docs.sonicwall.com/docs/quickstart/
        https://www.sonicwall.com/support/technical-documentation/ (CSE Feature Guide)

Prerequisites:
- SonicOS 7.1.2 or higher
- Active CSE licence registered in MySonicWall
- MySonicWall account with CSE activated (trial or paid)

PART A — Activate CSE in MySonicWall

1. Go to https://www.mysonicwall.com
   - Log in with your SonicWall partner/admin credentials
   - Go to My Products → find your firewall serial number
   - Confirm CSE licence is registered and active

PART B — Create a Connector in CSE Console

2. Log in to the CSE Console
   - URL: https://console.banyanops.com (or via MySonicWall / Capture Security Center)
   - Navigate to: Connectors (left sidebar)
   - Click: Add Connector
     - Connector Name: [descriptive name, e.g. "Naas-Office-TZ570"]
     - Deployment: Select "SonicWall Firewall" (for Gen 7 integration)
   - Save the Connector — a Connector token/ID will be generated
   - Note the Connector details (you will need these in SonicOS)

PART C — Enable CSE Connector on the Firewall (SonicOS)

3. Log in to SonicOS
   - Browser → https://[firewall-management-IP]
   - Username: admin | Password: [your password]

4. Navigate to CSE settings
   - Top menu: VPN > Cloud Secure Edge
   - Click: Enable Cloud Secure Edge
   - Enter the Connector token/details from the CSE Console
   - Click Apply

5. Configure Private Access (what internal resources CSE users can reach)
   - In the CSE tab on SonicOS, configure:
     - Allowed private IPv4 networks (the internal subnets CSE users should access)
       Example: 192.168.1.0/24
     - Private Domains (optional): Internal domain names CSE users need to resolve
       Example: *.company.local
       ⚠️ IMPORTANT: Use wildcard format (*.domain.local) — this is required for
       internal DNS queries to route correctly through the WireGuard tunnel.

6. Enable the Connector
   - Click Enable on the Connector in the CSE tab
   - SonicOS will automatically create a Group Address Object for this Connector
   - The Connector will establish an outbound WireGuard tunnel to CSE POPs
   - No inbound firewall ports need to be opened

PART D — Publish a Service in CSE Console

7. Back in CSE Console:
   - Navigate to: Services
   - Click: Add Service
     - Service Type: Web, Infrastructure (SSH/RDP), or Service Tunnel
     - Name: [descriptive name]
     - Backend: Internal address of the resource (e.g. 192.168.1.10:443)
     - Connector: Select the connector you set up
   - Save

8. Configure an Access Policy
   - Navigate to: Policies
   - Create a policy that allows your users/groups to access the published service
   - Assign device trust level requirements as needed

PART E — Test

9. Install CSE App on a user device
   - Download from CSE Console > Settings > App Downloads
   - User logs in with their IdP credentials (or local CSE user)
   - Verify they can access the published internal resource

10. Check Connector status
    - SonicOS: VPN > Cloud Secure Edge → CSE Status tab
    - CSE Console: Connectors → confirm status shows Connected
    - Firewall logs: Device > Log > View → filter by "Cloud Secure Edge" category
```

---

### Example 3 — Adding a Firewall to NSM (Cloud) with Zero Touch

```
🔷 Using SonicWall Skill

Adding a SonicWall Firewall to NSM Cloud (Zero Touch Provisioning)

Source: https://www.sonicwall.com/support/knowledge-base/sonicwall-network-security-manager-nsm-faq/
        https://www.sonicwall.com/support/technical-documentation/ (NSM Administration Guide)

Prerequisites:
- NSM licence registered in MySonicWall against the firewall serial number
- MySonicWall admin access
- Firewall has internet access (outbound TCP/UDP 21021 must not be blocked upstream)

PART A — Register NSM licence and set device to NSM management in MySonicWall

1. Go to https://www.mysonicwall.com
   - Log in
   - Go to My Products → locate the firewall by serial number
   - Verify NSM licence is registered (Essentials or Advanced)
   - Click on the device → click Manage
   - Set "Managed By" to: NSM Cloud (or "Cloud Management")
   - Enable Zero Touch if available

PART B — NSM Cloud Portal — Add the Tenant/Device

2. Log in to NSM
   - Go to https://cloud.sonicwall.com
   - Log in with MySonicWall credentials

3. Add Tenant (if MSP multi-tenant setup)
   - Navigate to: Tenants (left panel)
   - Add or select the appropriate tenant

4. Acquire the firewall
   - Navigate to: Firewall Manager > Inventory
   - The firewall should appear automatically if Zero Touch is configured in MySonicWall
   - If not appearing: Click Add Device, enter the firewall serial number and authentication key
   - Click Acquire

PART C — Zero Touch Communication Notes

- The firewall phones home to NSM via MySonicWall — WAN management does NOT need to be open
- Communication uses TCP/UDP port 21021 — confirm this is allowed outbound on the upstream ISP circuit
- If Zero Touch is disabled, configure manually on firewall:
  - SonicOS: Device > Settings > Base Settings > Advanced Management
  - Set NSM Cloud Address to: cloud.sonicwall.com
  - Save and click Accept

PART D — Verify

5. In NSM Cloud Portal
   - Firewall Manager > Inventory → device should show status: Connected or Managed
   - Click on device → confirm firmware version, interface status visible

6. Important note:
   - Once NSM acquires a device, manage config changes through NSM
   - Local modifications on the firewall are not recommended and may cause sync conflicts
   - Always push changes from NSM to the device rather than editing locally
```

---

## Common SonicWall Terminology

| Term | Meaning |
|---|---|
| SonicOS | Firewall operating system/firmware |
| Gen 7 | Current generation hardware (TZ270+, NSa 2700+) running SonicOS 7.x |
| Gen 6 | Previous generation (TZ300-TZ600, NSA series) running SonicOS 6.5.x |
| CSE | Cloud Secure Edge — ZTNA/SSE platform (formerly Banyan Security) |
| NSM | Network Security Manager — centralised multi-device management |
| MySonicWall | SonicWall licensing and registration portal (mysonicwall.com) |
| Zone | Security boundary (WAN, LAN, DMZ, WLAN, VPN, Custom) |
| DPI-SSL | Deep Packet Inspection of SSL/TLS traffic |
| GAV | Gateway Anti-Virus |
| IPS | Intrusion Prevention Service |
| AppControl | Application-based firewall rules |
| CFS | Content Filtering Service |
| Capture ATP | Advanced Threat Protection (cloud sandbox) |
| HA | High Availability (Active/Passive or Active/Active) |
| ZTP | Zero Touch Provisioning (NSM) |
| GMS | Global Management System (legacy, replaced by NSM) |
| CSC MA | Capture Security Center Management (legacy, replaced by NSM) |
| WireGuard | VPN protocol used by CSE Connector tunnels |
| ZTNA | Zero Trust Network Access (CSE capability) |
| SSE | Security Service Edge (CSE product category) |
| POPs | Points of Presence (CSE Global Edge Network nodes) |
| Access Tier | CSE identity-aware proxy/gateway (Global Edge or self-hosted) |
| Connector | CSE dial-out tunnel component (on firewall or standalone) |
| Accept button | Commits pending SonicOS configuration changes (yellow banner) |

---

## Best Practices Summary

- **Always search official docs before answering** — never rely on training data for steps
- **Fetch the full KB article** with `web_fetch` — search snippets are truncated
- **Check firmware generation** — SonicOS 7.x and 6.x UIs differ significantly
- **GUI first** — provide web interface steps as primary method
- **State version requirements** — especially for CSE (requires SonicOS 7.1.2+)
- **Never invent menu paths** — if you can't verify it, say so
- **Always include the Accept step** — changes are not committed until Accept is clicked
- **Recommend config backup** before major changes: Device > Settings > Firmware Management > Export Configuration
- **CSE access control is managed in the CSE Console**, not on the SonicWall firewall
- **NSM config changes** should be pushed from NSM — avoid local edits after acquisition
- **Flag all unofficial sources** with the warning block

---

## Source Citation Format

**Official SonicWall source:**
```
Source: [KB Article / Doc Title](https://www.sonicwall.com/support/...)
```

**Official CSE source:**
```
Source: [Doc Title](https://cse-docs.sonicwall.com/docs/...)
```

**Unofficial / community source:**
```
⚠️ WARNING: Not from official SonicWall documentation. May be inaccurate or outdated.
Source: [URL]
```

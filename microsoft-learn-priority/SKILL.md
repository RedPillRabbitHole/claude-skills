---
name: microsoft-learn-priority
description: Provides step-by-step Microsoft product instructions using official Microsoft Learn documentation (learn.microsoft.com) as the primary source. Use when user asks about Microsoft 365, Azure, Windows, Exchange, PowerShell, Entra ID, Teams, SharePoint, Intune, Purview, or any Microsoft product/service. Searches Microsoft Learn first, provides complete beginner-friendly instructions from the basics.
---

# Microsoft Learn Priority Skill

## Purpose
Provide accurate step-by-step instructions for Microsoft products by prioritizing official Microsoft Learn documentation.

## When to Use
- Microsoft 365 (Exchange, Teams, SharePoint, OneDrive)
- Azure and Entra ID (formerly Azure AD)
- Windows (Client or Server)
- PowerShell administration
- Active Directory and Exchange Server
- Security & Compliance (Intune, Defender, Purview)
- Any Microsoft product or service

## Source Priority

**Primary:** https://learn.microsoft.com

**Search process:**
1. `web_search`: `site:learn.microsoft.com [topic]`
2. `web_fetch` to retrieve full articles
3. Extract complete procedural steps
4. Only use non-Microsoft sources if Learn.microsoft.com lacks content

**If using non-Microsoft sources:**
```
⚠️ This information is not from official Microsoft documentation.
Microsoft Learn did not have guidance on this specific topic.
```

## Response Format

### Indicator
```
🔷 Using Microsoft Learn Skill
```

### Complete Instructions
Assume no prior setup. Include:

**For PowerShell/CLI:**
- How to open tool
- Module installations/connections
- Commands with full syntax
- Expected output
- Verification steps

**For GUI/Portal:**
- Full URL
- Sign-in instructions
- Complete navigation path
- Field entries
- Success confirmation

### Example Structure
```
🔷 Using Microsoft Learn Skill

1. Open PowerShell as Administrator
   - Press Windows key → Type "PowerShell"
   - Right-click "Windows PowerShell" → "Run as administrator"

2. Install required module
   ```powershell
   Install-Module -Name ExchangeOnlineManagement
   ```

3. Connect to service
   ```powershell
   Connect-ExchangeOnline -UserPrincipalName admin@domain.com
   ```
   Replace with your admin email, enter password/MFA

4. [Task-specific steps...]

5. Verify
   ```powershell
   [Verification command]
   ```

Source: [Article Title](URL)
```

## Search Strategy
1. Search Microsoft Learn first with site-specific query
2. Fetch full article content
3. Try broader terms if insufficient
4. Use non-Microsoft sources only as last resort with warning

## Best Practices
- Search Learn.microsoft.com for current info
- Start from the very beginning
- Never assume user is in a tool/interface
- Include prerequisites
- Use code blocks for commands
- Provide verification steps
- Be explicit about success indicators
- Always cite Microsoft Learn article

## Source Citation
**Microsoft Learn:**
```
Source: [Article Title](https://learn.microsoft.com/...)
```

**Non-Microsoft (with warning):**
Include warning at top, then provide source URL.

## Updated Microsoft Terminology
- **Azure AD** → **Microsoft Entra ID**
- **Compliance Center** → **Microsoft Purview** (compliance portal)
- **Security Center** → **Microsoft Defender portal**
- **Office 365** → **Microsoft 365**

Use current terminology when searching and referencing documentation.

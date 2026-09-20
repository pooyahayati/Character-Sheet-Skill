# Install and Use on ChatGPT for Windows

This guide describes the supported ChatGPT Skill installation flow as of the v1.1.0 release.

## Requirements

- ChatGPT desktop app for Windows.
- A workspace/account where Skills are available.
- Permission to upload/install Skills in that workspace.

OpenAI currently documents Skills for eligible ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability.

Official references:

- Skills in ChatGPT: https://help.openai.com/en/articles/20001066
- ChatGPT Windows app: https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app
- ChatGPT desktop / Work: https://help.openai.com/en/articles/20001275

If you do not see the Skills tab, your plan/workspace may not have Skills enabled or your workspace administrator may have disabled skill creation/uploading.

## Get the install package

### Option A — Official GitHub Release

Recommended.

Release page:

https://github.com/pooyahayati/Character-Sheet-Skill/releases/tag/v1.1.0

Direct ZIP:

https://github.com/pooyahayati/Character-Sheet-Skill/releases/download/v1.1.0/character-sheet-skill-v1.1.0.zip

Checksum:

https://github.com/pooyahayati/Character-Sheet-Skill/releases/download/v1.1.0/SHA256SUMS.txt

### Option B — GitHub Actions artifact

Every successful validation run also builds an installable ZIP artifact.

1. Open **Actions**.
2. Open the latest successful **Validate Skill** run.
3. Download the `character-sheet-skill-v1.1.0` artifact.
4. Extract the outer GitHub artifact ZIP once if needed.
5. Install the inner `character-sheet-skill-v1.1.0.zip`.

### Option C — Build locally on Windows

Requirements: Python 3.11+.

From the repository root:

```powershell
python scripts/package_skill.py
```

The package is created at:

```text
dist/character-sheet-skill-v1.1.0.zip
```

You can verify it with:

```powershell
python scripts/package_skill.py --check dist/character-sheet-skill-v1.1.0.zip
```

## Install the Skill in ChatGPT Windows

1. Install/open the ChatGPT Windows desktop app and sign in.
2. In the left sidebar, open **Plugins**.
3. Open the **Skills** tab in the Plugin Directory.
4. Select **Create**.
5. Select **Upload from your computer**.
6. Choose:
   `character-sheet-skill-v1.1.0.zip`
7. Wait for ChatGPT's skill scan to complete.
8. Review the skill if the UI marks it **Needs Review**.
9. Install/enable the skill.

If a workspace administrator has shared the skill instead, open **Skills → Shared with me** (or **Shared by your workspace**), open the **•••** menu, and select **Install**.

## Recommended clean-room setup

For a real test, do not test in the development conversation that was used to design the Skill.

1. Create a new ChatGPT Project, for example:
   `Character Sheet Test`
2. Start a completely new **Chat** inside that project.
3. Do not paste the architecture or expected internal behavior into the test chat.
4. Explicitly select the installed skill by typing `@` and choosing **Character Sheet Skill**, or let ChatGPT trigger it automatically when relevant.
5. Upload the subject photographs directly into the new test chat.
6. Use a normal end-user request.

Recommended Persian starting prompt:

```text
می‌خواهم از این عکس‌ها یک Character Sheet دقیق، فوتورئال و قابل استفاده برای تولید همین شخص در پوزیشن‌ها و زاویه‌های مختلف بسازی. ابتدا عکس‌ها را بررسی کن، بهترین رفرنس‌ها را انتخاب کن و فقط اگر اطلاعات مهمی واقعاً کم است از من عکس یا اطلاعات تکمیلی بخواه.
```

Recommended English starting prompt:

```text
Build a precise, photorealistic, pose-ready Character Sheet from these photos so I can reproduce the same person consistently across different poses and camera angles. Analyze and select the best references first, and only ask me for additional references when a material gap truly blocks the target quality.
```

## What to upload

For a strong first test, 10–20 varied photographs are useful when available:

- neutral front face;
- left and right 3/4;
- at least one useful profile;
- neutral and smiling expressions;
- full-body front/side where possible;
- a few natural candid images;
- hands visible in at least one useful image if hand identity matters.

Do not optimize for photo count. Diversity and reliability matter more.

## How to use after the Character Sheet is approved

Use the approved character as the canonical identity. Then request new production panels or images while specifying pose/camera intent.

Examples:

```text
Using the approved character identity, create a full-body walking pose with a normal camera perspective. Preserve face identity, body proportions, hair identity and skin texture.
```

```text
Generate a seated three-quarter pose. Keep the canonical body proportions unchanged, allow realistic clothing folds, and validate the face and hands before approval.
```

```text
Create a P4 self-occluding pose with crossed arms. Use the strongest available pose/geometry control and reject the output if hand anatomy, occlusion ordering or identity consistency fails.
```

## Suggested pose-readiness test sequence

After the base sheet is approved, test progressively:

1. P0 — neutral full body.
2. P1 — simple 3/4 standing.
3. P2 — walking / weight shift.
4. P3 — seated / leaning.
5. P4 — crossed arms.
6. P4 — hand near face.
7. P5 — crouching / deep bend.
8. P5 — arms overhead.
9. over-shoulder turn.
10. low-angle full-body view.

Do not call the character **Production pose-ready** unless the required visual benchmark passes Identity Fidelity, Pose Accuracy, Anatomical Plausibility, and Photorealism without hidden blocking failures.

## Updating the Skill

When a newer release is available:

1. Download/build the new version ZIP.
2. Review `CHANGELOG.md`.
3. In ChatGPT **Plugins → Skills**, replace/update the installed skill using the controls available in your workspace.
4. Run a clean-room regression test before using the new version for production.

Keep approved character outputs separately from the Skill package. Updating the Skill must not overwrite a character's canonical identity/version history.

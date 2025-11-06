# 🔧 COMPREHENSIVE FIX: EnumMeta Issue Across All Models

## 🚨 Problem Overview

Your database has `"EnumMeta.VALUE"` stored instead of just `"VALUE"` for **multiple enum fields** across different models, causing GraphQL enum errors.

## 📋 Affected Models & Fields

### 1. **User** Model

- **Field**: `role`
- **Example**: `"EnumMeta.COMPANY"` → should be `"COMPANY"`
- **Impact**: Cannot create company profiles

### 2. **Influencer** Model

- **Field**: `disponibilite_collaboration`
- **Example**: `"EnumMeta.DISPONIBLE"` → should be `"disponible"`
- **Impact**: GraphQL query errors for influencer profiles

### 3. **ReseauSocial** Model

- **Fields**: `plateforme`, `frequence_publication`
- **Examples**:
  - `"EnumMeta.INSTAGRAM"` → should be `"Instagram"`
  - `"EnumMeta.HEBDOMADAIRE"` → should be `"hebdomadaire"`
- **Impact**: Cannot display social network data

### 4. **OffreCollaboration** Model

- **Field**: `type_collaboration`
- **Example**: `"EnumMeta.POST"` → should be `"post"`
- **Impact**: Cannot display collaboration offers

## 🔴 Your Specific Errors

```json
{
  "errors": [
    {
      "message": "Enum 'DisponibiliteEnum' cannot represent value: 'EnumMeta.DISPONIBLE'",
      "path": ["myInfluencerProfile", "disponibiliteCollaboration"]
    },
    {
      "message": "Enum 'TypeCollaborationEnum' cannot represent value: 'EnumMeta.POST'",
      "path": [
        "myInfluencerProfile",
        "offresCollaboration",
        0,
        "typeCollaboration"
      ]
    },
    {
      "message": "Enum 'FrequencePublicationEnum' cannot represent value: 'EnumMeta.HEBDOMADAIRE'",
      "path": [
        "myInfluencerProfile",
        "reseauxSociaux",
        0,
        "frequencePublication"
      ]
    },
    {
      "message": "Enum 'PlateformeEnum' cannot represent value: 'EnumMeta.INSTAGRAM'",
      "path": ["myInfluencerProfile", "reseauxSociaux", 0, "plateforme"]
    }
  ]
}
```

## ✅ SOLUTION: One Command to Fix Everything

I've created a comprehensive management command that fixes **ALL** enum fields in your database.

### Step 1: Preview What Will Be Fixed (Dry Run)

```bash
python manage.py fix_user_roles --dry-run
```

**Expected Output:**

```
🔍 DRY RUN MODE - No changes will be made

📌 Checking Users...
  Would fix User gigid35285@keevle.com: EnumMeta.COMPANY → COMPANY
✅ Users: 1 would be fixed

📌 Checking Influencers...
  Would fix Influencer dalel@example.com: EnumMeta.DISPONIBLE → disponible
✅ Influencers: 1 would be fixed

📌 Checking Réseaux Sociaux...
  Would fix ReseauSocial 2: plateforme: EnumMeta.INSTAGRAM → Instagram, frequence: EnumMeta.HEBDOMADAIRE → hebdomadaire
✅ Réseaux Sociaux: 1 would be fixed

📌 Checking Offres Collaboration...
  Would fix OffreCollaboration 1: EnumMeta.POST → post
✅ Offres Collaboration: 1 would be fixed

============================================================
🔍 DRY RUN COMPLETE: Would fix 4 total records
💡 Run without --dry-run to apply these changes:
   python manage.py fix_user_roles
============================================================
```

### Step 2: Apply The Fix

```bash
python manage.py fix_user_roles
```

This will fix ALL enum values across your entire database!

### Step 3: Restart Your Server

```bash
# Stop server with Ctrl+C
python manage.py runserver
```

## 🧪 Test After Fixing

Try your GraphQL query again:

```graphql
query {
  myInfluencerProfile {
    id
    pseudo
    disponibiliteCollaboration
    reseauxSociaux {
      plateforme
      frequencePublication
      nombreAbonnes
    }
    offresCollaboration {
      typeCollaboration
      tarifMinimum
      tarifMaximum
    }
  }
}
```

**Expected Result**: ✅ No more enum errors! All data displays correctly.

## 📊 What Gets Fixed

| Model              | Field                       | Before                  | After          |
| ------------------ | --------------------------- | ----------------------- | -------------- |
| User               | role                        | `EnumMeta.COMPANY`      | `COMPANY`      |
| User               | role                        | `EnumMeta.INFLUENCER`   | `INFLUENCER`   |
| Influencer         | disponibilite_collaboration | `EnumMeta.DISPONIBLE`   | `disponible`   |
| Influencer         | disponibilite_collaboration | `EnumMeta.OCCUPE`       | `occupe`       |
| ReseauSocial       | plateforme                  | `EnumMeta.INSTAGRAM`    | `Instagram`    |
| ReseauSocial       | plateforme                  | `EnumMeta.TIKTOK`       | `TikTok`       |
| ReseauSocial       | frequence_publication       | `EnumMeta.HEBDOMADAIRE` | `hebdomadaire` |
| ReseauSocial       | frequence_publication       | `EnumMeta.QUOTIDIENNE`  | `quotidienne`  |
| OffreCollaboration | type_collaboration          | `EnumMeta.POST`         | `post`         |
| OffreCollaboration | type_collaboration          | `EnumMeta.STORY`        | `story`        |

## 🛡️ Prevention Tips

To prevent this issue in the future:

### ✅ DO: Use string values

```python
user.role = "COMPANY"
influencer.disponibilite_collaboration = "disponible"
reseau.plateforme = "Instagram"
reseau.frequence_publication = "hebdomadaire"
offre.type_collaboration = "post"
```

### ❌ DON'T: Use enum objects directly

```python
# This can cause EnumMeta issues:
user.role = UserRole.COMPANY
```

## 📁 Files Created/Modified

1. ✅ **`users/management/commands/fix_user_roles.py`**

   - Comprehensive command to fix all enum values
   - Supports dry-run mode
   - Fixes 4 different models

2. ✅ **`users/mutations/company_mutations.py`**

   - Added `is_company_role()` helper function
   - Company mutations now work with EnumMeta roles

3. ✅ **`FIX_ALL_ENUMS.md`** (this file)
   - Complete documentation and guide

## 🎯 Quick Summary

**Problem**: Database has `EnumMeta.VALUE` instead of `VALUE`  
**Solution**: Run `python manage.py fix_user_roles`  
**Result**: All enum fields cleaned, GraphQL queries work perfectly!

## ⚡ TL;DR - Quick Fix

```bash
# 1. Preview changes
python manage.py fix_user_roles --dry-run

# 2. Apply fixes
python manage.py fix_user_roles

# 3. Restart server
# (Ctrl+C then: python manage.py runserver)

# 4. Test your GraphQL queries - they should work now!
```

---

**Status**: ✅ Fix ready to apply  
**Action Required**: Run the command above  
**Impact**: Fixes all enum-related GraphQL errors

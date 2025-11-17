# How to Push ForgeEd to GitHub

Follow these steps to push your ForgeEd project to GitHub:

## Step 1: Create a New GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `forgeed` (or your preferred name)
   - **Description**: "AI-Enhanced Learning Management System for SLU"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Push Your Code to GitHub

GitHub will show you instructions, but here's what to do in the Replit Shell:

### Option A: If this is a fresh repository

```bash
git add .
git commit -m "Initial commit: ForgeEd AI-Enhanced LMS"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/forgeed.git
git push -u origin main
```

### Option B: If you've already committed before

```bash
git add .
git commit -m "Update: Complete ForgeEd implementation"
git remote add origin https://github.com/YOUR_USERNAME/forgeed.git
git push -u origin main
```

**Important**: Replace `YOUR_USERNAME` with your actual GitHub username!

## Step 3: Enter GitHub Credentials

When prompted:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your GitHub password)

### How to Create a Personal Access Token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a note like "ForgeEd Replit"
4. Select scopes: Check **"repo"** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing

## Step 4: Verify Your Repository

1. Go to `https://github.com/YOUR_USERNAME/forgeed`
2. You should see all your files except:
   - `forgeed.db` (excluded by .gitignore)
   - `.env` files (excluded by .gitignore)
   - `__pycache__/` folders (excluded by .gitignore)
   - Other temporary files

## What Gets Pushed to GitHub

✅ **Included:**
- All Python source files (`app.py`, `database.py`, etc.)
- HTML templates
- CSS stylesheets
- `README.md`, `DEPLOYMENT_GUIDE.md`, `replit.md`
- `requirements.txt`
- `.gitignore`
- Sample data scripts

❌ **Excluded (Protected):**
- `forgeed.db` (database file with student data)
- `.env` (contains API keys and secrets)
- `__pycache__/` (Python cache files)
- `.replit`, `uv.lock`, `pyproject.toml` (Replit-specific)
- Log files and temporary files

## Important Security Notes

🔒 **Never commit these files to GitHub:**
- Database files (`.db`, `.sqlite`)
- Environment files (`.env`)
- API keys or secrets

These are already protected by `.gitignore`!

## After Pushing

### Add a Repository Description

1. Go to your repository on GitHub
2. Click the ⚙️ gear icon next to "About"
3. Add description: "AI-Enhanced Learning Management System with GPT integration, dual quiz system, wellbeing tracking, and admin dashboard"
4. Add topics/tags: `python`, `flask`, `openai`, `lms`, `education`, `ai`, `chatgpt`

### Add a License (Optional)

1. On GitHub, click "Add file" → "Create new file"
2. Name it `LICENSE`
3. Click "Choose a license template"
4. Select MIT License (or your preference)
5. Commit the file

## Troubleshooting

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/forgeed.git
```

### Error: "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: Authentication failed

- Make sure you're using a **Personal Access Token**, not your password
- Token must have "repo" scope enabled
- Copy/paste carefully (tokens are long!)

### Want to push updates later?

```bash
git add .
git commit -m "Description of your changes"
git push
```

## Next Steps

After pushing to GitHub, you can:
1. Share the repository link with others
2. Enable GitHub Pages for documentation
3. Add collaborators
4. Set up GitHub Actions for CI/CD
5. Clone the repo on other machines

## Need Help?

- Check GitHub's [Quick Start Guide](https://docs.github.com/en/get-started/quickstart)
- Read about [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- See the [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics) documentation

---

**Your ForgeEd project is now ready to be shared with the world! 🚀**

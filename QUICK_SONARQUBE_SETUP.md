# 🚀 Quick SonarQube Setup - 5 Minutes

## Why SonarQube?

SonarQube provides:
- ✅ Code quality metrics
- ✅ Security vulnerability detection
- ✅ Code coverage tracking
- ✅ Code smell detection
- ✅ Duplication analysis

**And it's FREE with SonarCloud!**

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Sign Up (1 minute)

1. Go to **https://sonarcloud.io/signup**
2. Click **"Log in with GitHub"**
3. Authorize SonarCloud to access your GitHub account

### Step 2: Create Project (2 minutes)

1. After logging in, click **"+"** → **"Analyze new project"**
2. Select **"From GitHub"**
3. Choose your organization/user: **vamsigorle29**
4. Select repository: **aceest-fitness-devops**
5. Click **"Set up"**
6. Choose **"Free"** plan
7. Click **"Create project"**

### Step 3: Get Your Token (1 minute)

1. Click your profile icon (top right)
2. Go to **"My Account"** → **"Security"**
3. Under **"Generate Tokens"**, enter name: **`GitHub Actions`**
4. Click **"Generate"**
5. **COPY THE TOKEN** (you won't see it again!)

### Step 4: Add Secret to GitHub (1 minute)

1. Go to: **https://github.com/vamsigorle29/aceest-fitness-devops/settings/secrets/actions**
2. Click **"New repository secret"**
3. **Name**: `SONAR_TOKEN`
4. **Value**: Paste your token from Step 3
5. Click **"Add secret"**

### ✅ Done!

Push any code change and SonarQube will run automatically!

---

## 🎯 What Happens Next?

After adding the `SONAR_TOKEN` secret:

1. **Next Push**: SonarQube analysis runs automatically
2. **Results**: View in SonarCloud dashboard
3. **Metrics**: Code quality, coverage, security issues
4. **Reports**: Available in GitHub Actions artifacts

---

## 🔍 Verify Setup

After your next push, check:

1. **GitHub Actions**: 
   - Go to **Actions** tab
   - Latest workflow run
   - **SonarQube Analysis** job should show ✅

2. **SonarCloud Dashboard**:
   - Go to **https://sonarcloud.io**
   - Your project should appear
   - See code quality metrics

---

## ❓ Troubleshooting

### "SONAR_TOKEN not configured"
- Make sure you added the secret in GitHub
- Check the secret name is exactly `SONAR_TOKEN`
- Verify the token is valid (not expired)

### "Failed to connect to SonarQube"
- For SonarCloud, you don't need `SONAR_HOST_URL`
- If using custom server, ensure `SONAR_HOST_URL` is correct

### "Project key not found"
- Check project key in SonarCloud matches repository
- Or update project key in workflow if needed

---

## 📊 What You'll See

After setup, you'll get:

- **Code Quality**: A-F rating
- **Coverage**: Test coverage percentage
- **Bugs**: Potential bugs found
- **Vulnerabilities**: Security issues
- **Code Smells**: Code quality issues
- **Duplications**: Duplicated code

---

## 🆓 Free Tier Limits

- ✅ **Up to 100,000 lines of code** per project
- ✅ **Unlimited projects**
- ✅ **Public repositories**: Completely free
- ✅ **Private repositories**: Limited free tier

**For this project, free tier is more than enough!**

---

## 📚 Need More Help?

- **Full Guide**: See `SONARQUBE_SETUP_GUIDE.md`
- **SonarCloud Docs**: https://docs.sonarcloud.io
- **GitHub Actions**: Check workflow logs for errors

---

## ✅ Checklist

- [ ] Signed up for SonarCloud
- [ ] Created project in SonarCloud
- [ ] Generated authentication token
- [ ] Added `SONAR_TOKEN` secret in GitHub
- [ ] Pushed code to trigger workflow
- [ ] Verified SonarQube runs in GitHub Actions
- [ ] Checked results in SonarCloud dashboard

---

**That's it! SonarQube is now integrated with your CI/CD pipeline.** 🎉


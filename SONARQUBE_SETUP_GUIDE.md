# SonarQube Setup Guide - Quick & Free

## 🎯 Quick Setup with SonarCloud (FREE)

SonarCloud is the free cloud version of SonarQube. No server setup required!

### Step 1: Sign Up for SonarCloud

1. Go to **https://sonarcloud.io**
2. Click **"Log in"** or **"Sign up"**
3. Choose **"Log in with GitHub"** (recommended)
4. Authorize SonarCloud to access your GitHub account

### Step 2: Create a Project

1. After logging in, click **"+"** → **"Analyze new project"**
2. Select **"From GitHub"**
3. Choose your organization/user
4. Select repository: **`aceest-fitness-devops`**
5. Click **"Set up"**
6. Choose **"Free"** plan
7. Click **"Create project"**

### Step 3: Get Your Token

1. Go to **Account** → **My Account** → **Security**
2. Under **"Generate Tokens"**, enter a name: `GitHub Actions`
3. Click **"Generate"**
4. **Copy the token** (you won't see it again!)

### Step 4: Add Secret to GitHub

1. Go to your GitHub repository: **https://github.com/vamsigorle29/aceest-fitness-devops**
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. **Name**: `SONAR_TOKEN`
5. **Value**: Paste your SonarCloud token
6. Click **"Add secret"**

### Step 5: Get Project Key (Optional)

1. In SonarCloud, go to your project
2. Click **"Project Information"**
3. Copy the **"Project Key"** (e.g., `vamsigorle29_aceest-fitness-devops`)
4. If needed, update it in `.github/workflows/main.yml` (currently set to `aceest-fitness`)

### ✅ Done!

On your next push, SonarQube will automatically run and analyze your code!

---

## 🔍 Verify Setup

After pushing code, check:

1. **GitHub Actions**: Go to **Actions** tab → Latest workflow run
2. **SonarQube Analysis** job should show:
   - ✅ Configuration validated
   - ✅ SonarQube scan completed
3. **SonarCloud Dashboard**: Go to https://sonarcloud.io → Your project
   - See code quality metrics
   - View code coverage
   - Check for bugs, vulnerabilities, code smells

---

## 📊 What You'll Get

- **Code Quality Metrics**: Maintainability rating
- **Code Coverage**: Test coverage percentage
- **Security**: Vulnerabilities and security hotspots
- **Bugs**: Potential bugs in your code
- **Code Smells**: Code quality issues
- **Duplications**: Duplicated code detection

---

## 🆓 SonarCloud Limits (Free Tier)

- **Up to 100,000 lines of code** per project
- **Unlimited projects**
- **Public repositories**: Free
- **Private repositories**: Limited free tier

For this project, the free tier is more than sufficient!

---

## 🔧 Alternative: Self-Hosted SonarQube

If you prefer to host your own SonarQube server:

### Option 1: Docker (Easiest)

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:latest
```

Then:
1. Access: http://localhost:9000
2. Default login: `admin` / `admin`
3. Create a project and get token
4. Add secrets:
   - `SONAR_TOKEN`: Your token
   - `SONAR_HOST_URL`: `http://your-server:9000`

### Option 2: Cloud Provider

Deploy SonarQube on:
- AWS (EC2, ECS)
- Azure (VM, Container Instances)
- GCP (Compute Engine, Cloud Run)
- DigitalOcean
- Heroku

---

## 🐛 Troubleshooting

### Issue: "SONAR_TOKEN not configured"

**Solution**: Add the `SONAR_TOKEN` secret in GitHub repository settings.

### Issue: "Failed to connect to SonarQube server"

**Solution**: 
- Check `SONAR_HOST_URL` is correct
- Ensure SonarQube server is accessible
- For SonarCloud, don't set `SONAR_HOST_URL` (it's automatic)

### Issue: "Project key not found"

**Solution**: 
- Check project key in SonarCloud matches workflow
- Or update workflow to use correct project key

### Issue: "Authentication failed"

**Solution**:
- Regenerate token in SonarCloud
- Update `SONAR_TOKEN` secret in GitHub

---

## 📝 Current Configuration

The workflow is configured to:
- Use SonarCloud if only `SONAR_TOKEN` is set
- Use custom server if both `SONAR_TOKEN` and `SONAR_HOST_URL` are set
- Skip gracefully if neither is set (with instructions)

---

## ✅ Quick Checklist

- [ ] Signed up for SonarCloud
- [ ] Created project in SonarCloud
- [ ] Generated authentication token
- [ ] Added `SONAR_TOKEN` secret in GitHub
- [ ] Pushed code to trigger workflow
- [ ] Verified SonarQube analysis runs
- [ ] Checked results in SonarCloud dashboard

---

## 🎉 Next Steps

Once SonarQube is set up:

1. **Review Code Quality**: Check SonarCloud dashboard regularly
2. **Fix Issues**: Address bugs, vulnerabilities, and code smells
3. **Improve Coverage**: Aim for >85% test coverage
4. **Set Quality Gates**: Configure quality gates in SonarCloud
5. **Integrate with PRs**: Add SonarCloud checks to pull requests

---

## 📚 Resources

- **SonarCloud Docs**: https://docs.sonarcloud.io
- **SonarQube Docs**: https://docs.sonarqube.org
- **GitHub Actions**: https://docs.github.com/en/actions
- **Project Repository**: https://github.com/vamsigorle29/aceest-fitness-devops

---

**Need Help?** Check the workflow logs in GitHub Actions for detailed error messages.


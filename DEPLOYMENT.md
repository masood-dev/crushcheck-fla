# FLAMES Website Deployment Guide (100% FREE)

## 🎓 GitHub Student Pack (Recommended First Step)

**Get $200+ worth of free credits and services!**
- Visit: [education.github.com/pack](https://education.github.com/pack)
- Verify with your student email (.edu)
- Get free credits for: Azure, DigitalOcean, Heroku (credits), Namecheap domain, and more!

---

## 🚀 FREE Deployment Options

### Option 1: PythonAnywhere (Best for Flask - 100% FREE Forever)

**Why PythonAnywhere?**
- ✅ Specifically designed for Python/Flask apps
- ✅ Free tier never expires
- ✅ Easy custom domain setup
- ✅ No credit card required

**Steps:**

1. **Create Account**: [www.pythonanywhere.com](https://www.pythonanywhere.com) → Beginner (FREE)

2. **Upload Code**:
   - Go to "Files" tab
   - Create directory: `flames-website`
   - Upload all your files OR clone from GitHub:
     ```bash
     git clone https://github.com/YOUR-USERNAME/flames-website.git
     ```

3. **Set Up Web App**:
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set Source code: `/home/YOUR-USERNAME/flames-website`
   - Set Working directory: `/home/YOUR-USERNAME/flames-website`
   
4. **Configure WSGI**:
   - Click on WSGI configuration file link
   - Replace contents with:
     ```python
     import sys
     path = '/home/YOUR-USERNAME/flames-website'
     if path not in sys.path:
         sys.path.append(path)
     
     from flames_app.app import app as application
     ```

5. **Install Requirements**:
   - Open Bash console
   - Run:
     ```bash
     cd flames-website
     pip3 install --user -r flames_app/requirements.txt
     ```

6. **Connect Custom Domain** (lovehub.page):
   - In PythonAnywhere Web tab, add `lovehub.page` in "Domain names" section
   - In your domain registrar DNS settings:
     ```
     Type: CNAME
     Name: www
     Value: YOUR-USERNAME.pythonanywhere.com
     
     Type: A
     Name: @
     Value: 104.21.91.240 (check PythonAnywhere docs for current IP)
     ```

7. **Reload**: Click green "Reload" button

---

### Option 2: Render (FREE - Sleeps after 15 min inactivity)

**Steps:**

1. **Create Account**: [render.com](https://render.com) - No credit card for free tier

2. **Create Web Service**:
   - Connect GitHub repository
   - Name: `lovehub-flames`
   - Build Command: `pip install -r flames_app/requirements.txt`
   - Start Command: `gunicorn flames_app.app:app`
   - Select **FREE** tier

3. **Custom Domain** (lovehub.page):
   - Settings → Custom Domain → Add `lovehub.page`
   - Add DNS records in your domain registrar (Render provides them)

4. **GitHub Actions Auto-Deploy**:
   - Settings → Deploy Hook → Copy URL
   - GitHub repo: Settings → Secrets → New secret
   - Name: `RENDER_DEPLOY_HOOK_URL`, paste URL

**Note**: Free tier sleeps after 15 mins of inactivity (takes ~30s to wake up on first request)

---

### Option 3: Azure Static Web Apps (FREE with GitHub Student Pack)

**With GitHub Student Pack: $100 Azure credits!**

1. **Activate**: Via GitHub Student Pack → Azure for Students

2. **Deploy**:
   - Install Azure Static Web Apps extension in VS Code
   - Or use GitHub Actions (already configured)
   
3. **Custom Domain**: Free SSL certificate included

---

### Option 4: Google Cloud Run (FREE Tier)

**Free tier includes**:
- 2 million requests/month
- 360,000 GB-seconds memory
- 180,000 vCPU-seconds

**Quick Deploy**:
```bash
gcloud run deploy lovehub-flames --source . --platform managed --region us-central1 --allow-unauthenticated
```

Custom domain setup in Cloud Run console (free SSL included)

---

## 💰 Free Domain Options

**If you don't have lovehub.page yet:**

1. **GitHub Student Pack** → Namecheap: FREE .me domain for 1 year
2. **Freenom**: Free .tk, .ml, .ga, .cf domains (limited features)
3. **Cloudflare Pages**: Free subdomain (yourapp.pages.dev)

---

## 🔧 GitHub Actions (Auto-Deploy)

Already configured in `.github/workflows/deploy.yml`:
- Triggers on every push to main branch
- Works with Render (requires Deploy Hook URL in secrets)
- For PythonAnywhere: Manual deployment or use their API

---

## 📝 DNS Setup for lovehub.page

**In your domain registrar** (where you bought lovehub.page):

### For PythonAnywhere:
```
Type: CNAME
Name: www
Value: YOUR-USERNAME.pythonanywhere.com

Type: A  
Name: @
Value: 104.21.91.240
```

### For Render:
```
Type: CNAME
Name: www
Value: lovehub-flames.onrender.com

Type: CNAME
Name: @
Value: lovehub-flames.onrender.com
```

**DNS Propagation**: Wait 10-60 minutes after adding records

---

## 🎯 Recommendation

**Best Free Setup:**
1. ✅ Get **GitHub Student Pack** for free credits and domain
2. ✅ Deploy to **PythonAnywhere** (best free tier, no sleep)
3. ✅ Use Namecheap free domain from Student Pack OR your lovehub.page
4. ✅ Set up GitHub Actions for Render as backup

---

## 📊 Comparison

| Platform | Free Tier | Sleeps? | Custom Domain | SSL |
|----------|-----------|---------|---------------|-----|
| **PythonAnywhere** | ✅ Forever | ❌ No | ✅ Yes | ✅ Free |
| **Render** | ✅ Yes | ✅ After 15min | ✅ Yes | ✅ Free |
| **Google Cloud Run** | ✅ 2M req/mo | ❌ No | ✅ Yes | ✅ Free |
| **Azure (Student)** | ✅ $100 credit | ❌ No | ✅ Yes | ✅ Free |

---

## 🆘 Need Help?

- PythonAnywhere Docs: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- Render Docs: [render.com/docs](https://render.com/docs)
- GitHub Student Pack: [education.github.com/pack](https://education.github.com/pack)

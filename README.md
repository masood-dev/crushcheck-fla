# 🔥 FLAMES Calculator - Love Compatibility Game

A fun web application to calculate relationship compatibility using the classic FLAMES game algorithm.

## 🌟 Features

- Calculate relationship compatibility between two names
- Beautiful, responsive UI
- Real-time results
- Flask backend with RESTful API

## 🚀 Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/flames-website.git
cd flames-website
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r flames_app/requirements.txt
```

4. Run the app:
```bash
python flames_app/app.py
```

5. Open browser: `http://localhost:5000`

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- **PythonAnywhere** (Recommended - 100% Free)
- **Render** (Free tier with sleep)
- **Google Cloud Run** (Free tier)
- **Azure** (Free with GitHub Student Pack)

**All deployment options are 100% FREE!**

## 💻 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Hosting**: Multiple free options available
- **CI/CD**: GitHub Actions

## 📁 Project Structure

```
flames-website/
├── flames_app/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── static/
│   │   ├── script.js       # Frontend JavaScript
│   │   └── style.css       # Styling
│   └── templates/
│       ├── home.html       # Home page
│       ├── flames.html     # Calculator page
│       └── layout.html     # Base template
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions CI/CD
├── Procfile               # For cloud deployments
├── runtime.txt            # Python version
├── wsgi.py               # WSGI entry point
└── DEPLOYMENT.md         # Deployment guide
```

## 🎓 GitHub Student Pack Benefits

This project can be deployed 100% free using GitHub Student Pack benefits:
- Free domain from Namecheap (.me domain)
- $100 Azure credits
- DigitalOcean credits
- And much more!

Apply at: [education.github.com/pack](https://education.github.com/pack)

## 📝 License

MIT License - feel free to use this project for learning!

## 🤝 Contributing

Pull requests are welcome! Feel free to contribute.

## 🌐 Live Demo

Coming soon at: **lovehub.page**

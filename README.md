# Crushcheck? 🙄

## What's This About?

Remember those childhood games where you'd calculate if your crush likes you back using FLAMES? This is exactly that, but as a web app. I built this mainly to learn Flask and understand how these "magical" games actually work behind the scenes.

Turns out, these simple games have some pretty interesting logic. What seemed like magic when you were a kid is actually just string manipulation and some clever counting. Building this helped me understand algorithms in a fun way instead of just doing boring textbook problems.

## Why I Made This

It's one of my Friend's silly idea 😎

Honestly, I wanted to learn web development but most tutorial projects are either too simple (hello world) or too complex (build Instagram clone). This felt like a good middle ground - simple enough to finish, but complex enough to learn actual concepts.

Plus, the whole point isn't just writing code. I wanted to learn the full process: writing code, using Git properly, deploying to the cloud, making something that actually works online. It's more fun when you can share a real link with friends instead of just showing them code on your laptop.

**Check it out live:** [crushcheck](https://crushcheck-fla-b3b9hpdqa4c9ftdh.centralindia-01.azurewebsites.net)

### How the FLAMES Algorithm Works

![FLAMES Algorithm Flow](https://github.com/user-attachments/assets/ead584e2-cb3a-4dba-b714-885264ad00b0)

The algorithm is actually pretty smart when you break it down:
1. Take two names, remove spaces, make them lowercase
2. Cross out all the matching letters between both names
3. Count what's left and use that number to eliminate letters from "FLAMES"
4. Whatever letter remains is your "result"

It's simple but teaches you a lot about string processing, loops, and working with arrays.

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/crushcheck-fla.git
cd crushcheck-fla
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS / Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python -m flames_app.app
```

5. Open your browser at http://localhost:5000

## Project Structure

Here's how everything is organized:

```
crushcheck-fla/
├── flames_app/              # Main app folder
│   ├── app.py              # Flask routes and game logic
│   ├── database.py         # Secret note storage and password checks
│   ├── static/             # CSS and JavaScript files
│   └── templates/          # HTML templates
├── tests/                  # Basic route and security regression tests
├── Procfile               # For cloud deployment
├── requirements.txt        # Python packages needed
└── wsgi.py                # Entry point for production server
```

The structure is pretty standard for Flask apps. Templates go in `templates/`, CSS/JS goes in `static/`, and the main logic is in `app.py`.

## Deployment

I deployed this on **Microsoft Azure** because they have a free tier for students (Azure for Students gives you $100 credit).

Azure Web Apps made it pretty straightforward - you just push your code, and it handles the rest. The `Procfile`, `wsgi.py`, and GitHub Actions workflow are the pieces that tell Azure how to build and run the app. Once it's deployed, you get a real URL that you can share with anyone.

## Security Notes

- Secret notes now expire at read time, not just during startup cleanup.
- Rate limiting is applied to public POST endpoints to reduce spam and brute-force attempts.
- Password minimum length is 4 characters, and sender name limits are enforced on the server, not only in the browser.
- Basic security headers are set for production responses.

If you're a student like me, definitely check out Azure for Students. The free credits are great for learning and experimenting without worrying about bills.

Other options like Render or Railway are also pretty good if you want to try those instead. They all do similar things - take your code and make it live on the internet.

## Contributing

If you want to add features or improve something, go for it! Some ideas:
- Add more games (like compatibility by birthdate, zodiac signs, etc.)
- Make the UI look better
- Add animations
- Integrate some fun APIs

Fork it, mess around with it, break things, fix them. That's how you learn. Open an issue if you have questions or submit a pull request if you built something cool.

## License

MIT License - do whatever you want with this code.

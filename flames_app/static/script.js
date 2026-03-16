document.addEventListener('DOMContentLoaded', () => {
    const flamesForm = document.getElementById('flamesForm');
    if (flamesForm) {
        const resultContainer = document.getElementById('result');
        const resultTitle = document.getElementById('resultTitle');
        const resultMessage = document.getElementById('resultMessage');
        const resetBtn = document.getElementById('resetBtn');
        const calcBtn = document.getElementById('calcBtn');

        flamesForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Button loading state
            const originalBtnText = calcBtn.querySelector('span').innerText;
            calcBtn.querySelector('span').innerText = 'Calculating...';
            calcBtn.disabled = true;

            const name1 = document.getElementById('name1').value;
            const name2 = document.getElementById('name2').value;

            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name1, name2 }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                // Simulate a small delay for suspense
                setTimeout(() => {
                    showFlamesResult(data.result, data.message);
                    calcBtn.querySelector('span').innerText = originalBtnText;
                    calcBtn.disabled = false;
                }, 800);

            } catch (error) {
                console.error('Error:', error);
                alert('Something went wrong. Please try again.');
                calcBtn.querySelector('span').innerText = originalBtnText;
                calcBtn.disabled = false;
            }
        });

        resetBtn.addEventListener('click', () => {
            resultContainer.classList.add('hidden');
            flamesForm.classList.remove('hidden');
            flamesForm.reset();
            document.getElementById('name1').focus();
        });

        function showFlamesResult(result, message) {
            resultTitle.textContent = result;
            resultMessage.textContent = message;

            resultContainer.classList.remove('hidden');

            // Scroll to result if needed (on mobile)
            resultContainer.scrollIntoView({ behavior: 'smooth' });
        }
    }

    const zodiacForm = document.getElementById('zodiacForm');
    if (zodiacForm) {
        const zodiacResult = document.getElementById('zodiacResult');
        const zodiacBtn = document.getElementById('zodiacBtn');
        const zodiacReset = document.getElementById('zodiacReset');
        const swapSigns = document.getElementById('swapSigns');
        const sign1Field = document.getElementById('sign1');
        const sign2Field = document.getElementById('sign2');
        const sign1Label = document.getElementById('sign1Label');
        const sign2Label = document.getElementById('sign2Label');
        const zodiacScore = document.getElementById('zodiacScore');
        const zodiacVibe = document.getElementById('zodiacVibe');
        const zodiacInsight = document.getElementById('zodiacInsight');
        const scoreCircle = document.getElementById('scoreCircle');

        zodiacForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const originalBtnText = zodiacBtn.querySelector('span').innerText;
            zodiacBtn.querySelector('span').innerText = 'Reading Stars...';
            zodiacBtn.disabled = true;

            try {
                const response = await fetch('/zodiac-check', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sign1: sign1Field.value,
                        sign2: sign2Field.value
                    }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                setTimeout(() => {
                    showZodiacResult(data);
                    zodiacBtn.querySelector('span').innerText = originalBtnText;
                    zodiacBtn.disabled = false;
                }, 700);
            } catch (error) {
                console.error('Error:', error);
                alert('Something went wrong. Please try again.');
                zodiacBtn.querySelector('span').innerText = originalBtnText;
                zodiacBtn.disabled = false;
            }
        });

        swapSigns.addEventListener('click', () => {
            const currentSign1 = sign1Field.value;
            sign1Field.value = sign2Field.value;
            sign2Field.value = currentSign1;
        });

        zodiacReset.addEventListener('click', () => {
            zodiacResult.classList.add('hidden');
            zodiacForm.classList.remove('hidden');
            zodiacForm.reset();
            sign1Field.focus();
        });

        function showZodiacResult(data) {
            sign1Label.textContent = `${data.sign1} · ${data.element1}`;
            sign2Label.textContent = `${data.sign2} · ${data.element2}`;
            zodiacScore.textContent = `${data.score}%`;
            zodiacVibe.textContent = data.vibe;
            zodiacInsight.textContent = data.insight;
            scoreCircle.style.setProperty('--score', data.score);

            zodiacResult.classList.remove('hidden');
            zodiacResult.scrollIntoView({ behavior: 'smooth' });
        }
    }

    const secretNoteForm = document.getElementById('secretNoteForm');
    if (secretNoteForm) {
        const resultContainer = document.getElementById('result');
        const shareableLink = document.getElementById('shareableLink');
        const createBtn = document.getElementById('createBtn');
        const messageInput = document.getElementById('message');
        const charCount = document.getElementById('charCount');
        const copyBtn = document.getElementById('copyBtn');
        const createAnotherBtn = document.getElementById('createAnotherBtn');

        messageInput.addEventListener('input', () => {
            const count = messageInput.value.length;
            charCount.textContent = `${count} / 500 characters`;
            charCount.style.color = count > 450 ? '#ff6b6b' : '#666';
        });

        secretNoteForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const originalBtnText = createBtn.querySelector('span').innerText;
            createBtn.querySelector('span').innerText = 'Creating...';
            createBtn.disabled = true;

            const formData = {
                message: document.getElementById('message').value,
                password: document.getElementById('password').value,
                sender_name: document.getElementById('senderName').value || 'Someone Special'
            };

            try {
                const response = await fetch('/create-note', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Failed to create note');
                }

                shareableLink.value = new URL(data.note_path, window.location.origin).href;
                secretNoteForm.classList.add('hidden');
                resultContainer.classList.remove('hidden');
            } catch (error) {
                console.error('Error:', error);
                alert(error.message || 'Failed to create note. Please try again.');
            } finally {
                createBtn.querySelector('span').innerText = originalBtnText;
                createBtn.disabled = false;
            }
        });

        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(shareableLink.value);
                const originalText = copyBtn.innerText;
                copyBtn.innerText = 'Copied!';
                setTimeout(() => {
                    copyBtn.innerText = originalText;
                }, 2000);
            } catch (error) {
                console.error('Copy failed:', error);
                shareableLink.select();
                document.execCommand('copy');
            }
        });

        createAnotherBtn.addEventListener('click', () => {
            secretNoteForm.reset();
            charCount.textContent = '0 / 500 characters';
            charCount.style.color = '#666';
            secretNoteForm.classList.remove('hidden');
            resultContainer.classList.add('hidden');
        });
    }

    const unlockForm = document.getElementById('unlockForm');
    if (unlockForm) {
        const lockedView = document.getElementById('lockedView');
        const unlockedView = document.getElementById('unlockedView');
        const errorMsg = document.getElementById('errorMsg');
        const unlockBtn = document.getElementById('unlockBtn');
        const passwordInput = document.getElementById('passwordInput');
        const noteId = unlockForm.dataset.noteId;

        unlockForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            errorMsg.classList.add('hidden');

            const originalText = unlockBtn.querySelector('span').innerText;
            unlockBtn.querySelector('span').innerText = 'Unlocking...';
            unlockBtn.disabled = true;

            try {
                const response = await fetch('/unlock-note', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ note_id: noteId, password: passwordInput.value })
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || 'Incorrect password');
                }

                document.getElementById('senderName').textContent = data.sender_name;
                document.getElementById('secretMessage').textContent = data.message;
                document.getElementById('viewCount').textContent = `This message has been viewed ${data.view_count} time(s)`;

                lockedView.classList.add('hidden');
                unlockedView.classList.remove('hidden');
                unlockedView.style.animation = 'flipIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            } catch (error) {
                console.error('Error:', error);
                errorMsg.textContent = error.message || 'Something went wrong. Please try again.';
                errorMsg.classList.remove('hidden');
                passwordInput.value = '';
                passwordInput.focus();
            } finally {
                unlockBtn.querySelector('span').innerText = originalText;
                unlockBtn.disabled = false;
            }
        });
    }
});

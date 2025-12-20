function randomColor() {
  const colors = ["#ff6ec7", "#7cf5ff", "#7fff6e", "#ffd66e", "#c48bff"];
  return colors[Math.floor(Math.random() * colors.length)];
}

function triggerConfetti(count = 36) {
  const container = document.getElementById("confetti");
  if (!container) return;
  for (let i = 0; i < count; i++) {
    const piece = document.createElement("div");
    piece.className = "confetti";
    piece.style.left = Math.random() * 100 + "vw";
    piece.style.background = randomColor();
    piece.style.transform = `translateY(-${Math.random() * 80 + 20}px)`;
    piece.style.animationDelay = (Math.random() * 0.6) + "s";
    piece.style.rotate = Math.random() * 360 + "deg";
    container.appendChild(piece);
    setTimeout(() => piece.remove(), 1600);
  }
}

function triggerMassiveConfetti() {
  // Huge confetti explosion for victory
  for (let wave = 0; wave < 5; wave++) {
    setTimeout(() => triggerConfetti(50), wave * 200);
  }
}

// Simple WebAudio sounds
let audioCtx;
function getCtx() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = AudioContext ? new AudioContext() : null;
  }
  return audioCtx;
}

function playTone(freq = 440, duration = 0.2, type = 'sine', gain = 0.08) {
  const ctx = getCtx();
  if (!ctx) return;
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.type = type;
  osc.frequency.value = freq;
  g.gain.value = gain;
  osc.connect(g);
  g.connect(ctx.destination);
  osc.start();
  setTimeout(() => {
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.08);
    osc.stop(ctx.currentTime + 0.09);
  }, duration * 1000);
}

function triggerSound(kind) {
  if (kind === 'win') {
    playTone(523, 0.12, 'triangle', 0.12);
    setTimeout(() => playTone(659, 0.12, 'triangle', 0.12), 120);
    setTimeout(() => playTone(784, 0.16, 'triangle', 0.12), 240);
  } else if (kind === 'draw') {
    playTone(440, 0.12, 'sine', 0.09);
    setTimeout(() => playTone(440, 0.12, 'sine', 0.07), 120);
  } else if (kind === 'lose') {
    playTone(392, 0.12, 'sawtooth', 0.08);
    setTimeout(() => playTone(330, 0.16, 'sawtooth', 0.08), 140);
  } else if (kind === 'victory') {
    // Epic victory fanfare
    const melody = [
      {freq: 523, delay: 0},
      {freq: 659, delay: 150},
      {freq: 784, delay: 300},
      {freq: 1047, delay: 450},
      {freq: 784, delay: 650},
      {freq: 1047, delay: 800},
      {freq: 1319, delay: 1000}
    ];
    melody.forEach(note => {
      setTimeout(() => playTone(note.freq, 0.2, 'triangle', 0.15), note.delay);
    });
  }
}

// Button tap animation and click sound
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.style.transform = 'translateY(1px) scale(0.98)';
      setTimeout(() => { btn.style.transform = ''; }, 180);
      playTone(520, 0.06, 'sine', 0.05);
    }, { passive: true });
  });

  // PvP two-step move handler
  let p1Move = null;
  const p1Buttons = document.getElementById('p1-buttons');
  const p2Buttons = document.getElementById('p2-buttons');
  const pvpForm = document.getElementById('pvp-form');
  const ekaInput = document.getElementById('eka-input');
  const tokaInput = document.getElementById('toka-input');

  if (p1Buttons && p2Buttons && pvpForm) {
    p1Buttons.querySelectorAll('[data-move]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        p1Move = btn.getAttribute('data-move');
        ekaInput.value = p1Move;
        p1Buttons.style.opacity = '0.4';
        p1Buttons.style.pointerEvents = 'none';
        p2Buttons.style.opacity = '1';
        p2Buttons.style.pointerEvents = 'auto';
        playTone(600, 0.08, 'sine', 0.06);
      });
    });

    p2Buttons.querySelectorAll('[data-move]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        tokaInput.value = btn.getAttribute('data-move');
        pvpForm.submit();
      });
    });
  }
});

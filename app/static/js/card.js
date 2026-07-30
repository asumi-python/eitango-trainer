// ── Quiz AJAX flow ──

var quizArea = document.getElementById('quiz-area');

function initQuiz() {
  var revealBtn = document.getElementById('reveal-btn');

  if (revealBtn) {
    revealBtn.addEventListener('click', function () {
      document.getElementById('card-back').classList.remove('hidden');
      document.getElementById('answer-buttons').classList.remove('hidden');
      document.getElementById('reveal-section').classList.add('hidden');
    });
  }

  document.querySelectorAll('.score-btn, .master-btn').forEach(function (btn) {
    btn.addEventListener('click', handleAnswerClick);
  });
}

async function handleAnswerClick(e) {
  var btn = e.currentTarget;
  var isScore = btn.classList.contains('score-btn');
  var wordId = btn.dataset.wordId;
  var wordEnglish = btn.dataset.wordEnglish;
  var result = btn.dataset.result;

  setAnswerLoading(true, btn);

  try {
    var url = isScore ? '/api/score' : '/api/master';
    var body = isScore
      ? { word_id: wordId, word_english: wordEnglish, result: result }
      : { word_id: wordId, word_english: wordEnglish };

    var res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    var data = await res.json();

    if (data.message) showToast(data.message);

    await loadNextWord();
  } catch (err) {
    console.error(err);
    setAnswerLoading(false, null);
  }
}

function setAnswerLoading(loading, clickedBtn) {
  document.querySelectorAll('.score-btn, .master-btn').forEach(function (btn) {
    btn.disabled = loading;
    if (loading && btn === clickedBtn) {
      btn.dataset.origText = btn.textContent;
      btn.textContent = '読み込み中...';
      btn.classList.add('btn--loading');
    } else if (!loading) {
      btn.classList.remove('btn--loading');
      if (btn.dataset.origText) {
        btn.textContent = btn.dataset.origText;
        delete btn.dataset.origText;
      }
    }
  });
}

async function loadNextWord() {
  var card = document.getElementById('quiz-card');

  // Start exit animation and fetch in parallel
  if (card) card.classList.add('card--exit');

  var results = await Promise.all([
    sleep(190),
    fetch('/api/next-word').then(function (r) { return r.json(); })
  ]);
  var nextData = results[1];

  if (!nextData.word) {
    quizArea.innerHTML =
      '<div class="empty-state">' +
      '<p>すべての単語を覚えました！</p>' +
      '<a href="/words/new" class="btn btn--primary">新しい単語を登録する</a>' +
      '</div>';
    return;
  }

  // Update word content
  document.getElementById('quiz-word').textContent = nextData.word.english;
  document.getElementById('quiz-meaning').textContent = nextData.word.meaning;

  // Update data attributes on answer buttons
  document.querySelectorAll('.score-btn, .master-btn').forEach(function (btn) {
    btn.dataset.wordId = nextData.word.id;
    btn.dataset.wordEnglish = nextData.word.english;
  });

  // Toggle "覚えた" button visibility
  var masterBtn = document.querySelector('.master-btn');
  if (masterBtn) {
    if (nextData.settings.mastery_mode === 'manual') {
      masterBtn.classList.remove('hidden');
    } else {
      masterBtn.classList.add('hidden');
    }
  }

  // Reset card state
  document.getElementById('card-back').classList.add('hidden');
  document.getElementById('answer-buttons').classList.add('hidden');
  document.getElementById('reveal-section').classList.remove('hidden');
  setAnswerLoading(false, null);

  // Animate card in
  if (card) {
    card.classList.remove('card--exit');
    card.classList.add('card--enter');
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        card.classList.remove('card--enter');
      });
    });
  }
}

function showToast(message) {
  var toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(function () {
    requestAnimationFrame(function () {
      toast.classList.add('toast--show');
    });
  });

  setTimeout(function () {
    toast.classList.remove('toast--show');
    setTimeout(function () { toast.remove(); }, 300);
  }, 3000);
}

function sleep(ms) {
  return new Promise(function (resolve) { setTimeout(resolve, ms); });
}

// ── Settings page: show/hide streak input based on mastery mode ──
document.querySelectorAll('input[name="mastery_mode"]').forEach(function (radio) {
  radio.addEventListener('change', function () {
    var streakSection = document.getElementById('streak-section');
    if (streakSection) {
      streakSection.style.display = this.value === 'auto' ? 'flex' : 'none';
    }
  });
});

initQuiz();

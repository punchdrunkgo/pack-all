// Packo Blog — GA4 행동 로그 (blog/analytics.js)
// 모든 블로그 페이지에서 로드됨. gtag는 각 페이지 <head>에서 이미 초기화됨.
(function () {
  if (typeof gtag !== 'function') return;

  /* ── 1. 스크롤 깊이 (25 / 50 / 75 / 100%) ─────────────────── */
  var fired = {};
  window.addEventListener('scroll', function () {
    var el = document.documentElement;
    var depth = Math.round(((el.scrollTop || document.body.scrollTop) /
      (el.scrollHeight - el.clientHeight)) * 100);
    [25, 50, 75, 100].forEach(function (m) {
      if (depth >= m && !fired[m]) {
        fired[m] = true;
        gtag('event', 'scroll_depth', {
          depth_percent: m,
          page_path: location.pathname
        });
      }
    });
  }, { passive: true });

  /* ── 2. CTA 버튼 클릭 ────────────────────────────────────────── */
  document.querySelectorAll('.cta-btn').forEach(function (el) {
    el.addEventListener('click', function () {
      gtag('event', 'cta_click', {
        page_path: location.pathname,
        button_text: el.textContent.trim()
      });
    });
  });

  /* ── 3. 관련글 링크 클릭 ─────────────────────────────────────── */
  document.querySelectorAll('.post-footer a').forEach(function (el) {
    el.addEventListener('click', function () {
      gtag('event', 'related_post_click', {
        from_page: location.pathname,
        to_url: el.getAttribute('href'),
        link_text: el.textContent.trim().slice(0, 60)
      });
    });
  });

  /* ── 4. 블로그 목록 카드 클릭 (blog/index.html) ─────────────── */
  document.querySelectorAll('.post-card').forEach(function (el) {
    el.addEventListener('click', function () {
      var titleEl = el.querySelector('.post-title');
      gtag('event', 'post_card_click', {
        to_url: el.getAttribute('href'),
        post_title: titleEl ? titleEl.textContent.trim() : ''
      });
    });
  });

  /* ── 5. 글 끝까지 읽음 (CTA 섹션 진입 시) ───────────────────── */
  var cta = document.querySelector('.post-cta');
  if (cta && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries, obs) {
      if (entries[0].isIntersecting) {
        gtag('event', 'article_read_complete', {
          page_path: location.pathname
        });
        obs.disconnect();
      }
    }, { threshold: 0.5 }).observe(cta);
  }

  /* ── 6. 헤더 앱 로고 클릭 ───────────────────────────────────── */
  var logo = document.querySelector('.blog-logo');
  if (logo) {
    logo.addEventListener('click', function () {
      gtag('event', 'header_logo_click', { page_path: location.pathname });
    });
  }
})();

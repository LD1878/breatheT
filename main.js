(function () {
  'use strict';

  const qs = (s, ctx = document) => ctx.querySelector(s);
  const qsa = (s, ctx = document) => [...ctx.querySelectorAll(s)];

  const nav = qs('#main-nav');
  function updateNav() {
    if (!nav) return;
    const y = window.scrollY;
    nav.classList.toggle('nav-visible', y > 8);
    nav.classList.toggle('nav-scrolled', y > 40);
  }
  function updateNavOnDark() {
    if (!nav) return;
    const box = nav.getBoundingClientRect();
    const dark = [...document.querySelectorAll('.band-charcoal, .band-assess, footer.site-footer')].some((el) => {
      const r = el.getBoundingClientRect();
      return r.top < box.bottom && r.bottom > box.top;
    });
    document.documentElement.classList.toggle('nav-on-dark', dark);
  }
  window.addEventListener('scroll', () => { updateNav(); updateNavOnDark(); }, { passive: true });
  window.addEventListener('resize', updateNavOnDark);
  updateNav();
  updateNavOnDark();

  const ham = qs('#hamburger');
  const mNav = qs('#mobile-nav');
  ham?.addEventListener('click', () => {
    const open = mNav.classList.toggle('open');
    ham.setAttribute('aria-expanded', String(open));
  });
  qsa('#mobile-nav a').forEach((a) => {
    a.addEventListener('click', () => {
      mNav?.classList.remove('open');
      ham?.setAttribute('aria-expanded', 'false');
    });
  });

  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        revealObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -32px 0px' });
  qsa('.reveal').forEach((el) => revealObs.observe(el));

  const jumpLinks = qsa('.case-jump a');
  if (jumpLinks.length) {
    const jumpObs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        jumpLinks.forEach((a) => {
          if (a.hash === '#' + e.target.id) {
            a.setAttribute('aria-current', 'true');
            const bar = a.parentElement;
            bar.scrollLeft = a.offsetLeft - (bar.clientWidth - a.offsetWidth) / 2;
          } else {
            a.removeAttribute('aria-current');
          }
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    jumpLinks.forEach((a) => {
      const target = qs(a.hash);
      if (target) jumpObs.observe(target);
    });
  }

  requestAnimationFrame(() => {
    qsa('.reveal-hero').forEach((el, i) => {
      setTimeout(() => el.classList.add('visible'), 80 + i * 70);
    });
  });

  const LAYER_DATA = {
    W1: {
      title: 'PerliScratch',
      desc: 'A keyed lime-perlite coat so the insulation can grip the masonry.',
      thick: '3mm, 4mm, 5mm',
      lambda: '0.080 W/m·K',
      sd: '0.02 – 0.04 m',
      price: '£4.60 /m²'
    },
    W2: {
      title: 'PerliTherm',
      desc: 'The breathable insulating body of the wall system: expanded perlite bound with hydraulic lime.',
      thick: '50mm',
      lambda: '0.064 W/m·K',
      sd: '0.2 – 0.4 m',
      price: '£45.00 /m²'
    },
    W3: {
      title: 'AeroBond',
      desc: 'Adhesive and basecoat in one, for aerogel and mineral layers.',
      thick: '3mm, 4mm, 5mm, 6mm',
      lambda: '0.12 W/m·K',
      sd: '0.02 – 0.04 m',
      price: '£20.00 /m²'
    },
    W4: {
      title: 'AeroGel',
      desc: 'An ultra-thin thermal boost where reveals and junctions are tight.',
      thick: '10mm',
      lambda: '0.017 W/m·K',
      sd: '0.04 – 0.08 m',
      price: '£23.70 /m²'
    },
    W5: {
      title: 'PerliFinish',
      desc: 'A breathable lime finish, ready for decoration.',
      thick: '20mm',
      lambda: 'n/a',
      sd: '0.10 – 0.20 m',
      price: '£6.60 /m²'
    },
    F1: {
      title: 'PerliMat',
      desc: 'A vapour-open separator beneath the floor build-up.',
      thick: '3.5mm',
      lambda: 'n/a',
      sd: 'Vapour open',
      price: '£3 /m²'
    },
    F2: {
      title: 'PerliBase',
      desc: 'The insulating mineral underbase of the floor system.',
      thick: '75mm – 200mm',
      lambda: '0.045 W/m·K',
      sd: '0.3 – 0.6 m',
      price: '£59.25 /m²'
    },
    F3: {
      title: 'PerliStruct',
      desc: 'A structural lime-perlite screed that still lets vapour through.',
      thick: '30mm – 150mm',
      lambda: '0.080 – 0.090 W/m·K',
      sd: '0.20 – 0.40 m',
      price: 'from £46.00 /m²'
    },
    F4: {
      title: 'AeroBond',
      desc: 'Breathable adhesive for the aerogel layer.',
      thick: '5mm',
      lambda: '0.12 W/m·K',
      sd: '0.02 – 0.04 m',
      price: '£20.00 /m²'
    },
    F5: {
      title: 'AeroGel',
      desc: 'A thin thermal boost in a constrained floor build-up.',
      thick: '5mm',
      lambda: '0.017 W/m·K',
      sd: '0.04 – 0.08 m',
      price: '£23.25 /m²'
    },
    F6: {
      title: 'PerliScreed',
      desc: 'The vapour-open insulated floor finish.',
      thick: '75mm – 200mm',
      lambda: '0.045 W/m·K',
      sd: '0.3 – 0.6 m',
      price: '£59.25 /m² @75mm'
    }
  };

  function showLayer(id) {
    const d = LAYER_DATA[id];
    if (!d) return;
    const set = (sel, val) => { const el = qs(sel); if (el) el.textContent = val; };
    set('#lcTitle', d.title);
    set('#lcDesc', d.desc);
    set('#lcThick', d.thick);
    set('#lcLambda', d.lambda);
    set('#lcSd', d.sd);
    set('#lcPrice', d.price);
    qsa('.build-layer').forEach((btn) => {
      const on = btn.dataset.id === id;
      btn.classList.toggle('is-on', on);
      btn.setAttribute('aria-pressed', String(on));
    });
  }

  qsa('.build-layer').forEach((btn) => {
    btn.setAttribute('aria-pressed', btn.classList.contains('is-on') ? 'true' : 'false');
    btn.addEventListener('click', () => showLayer(btn.dataset.id));
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        showLayer(btn.dataset.id);
      }
    });
  });

  const wallsPanel = qs('#build-walls');
  const floorPanel = qs('#build-floor');
  qsa('button.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      const view = tab.dataset.view;
      qsa('button.tab').forEach((t) => {
        const on = t === tab;
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', String(on));
      });
      if (view === 'floor' && wallsPanel && floorPanel) {
        wallsPanel.hidden = true;
        wallsPanel.classList.remove('is-on');
        floorPanel.hidden = false;
        floorPanel.classList.add('is-on');
        showLayer('F2');
      } else if (wallsPanel && floorPanel) {
        floorPanel.hidden = true;
        floorPanel.classList.remove('is-on');
        wallsPanel.hidden = false;
        wallsPanel.classList.add('is-on');
        showLayer('W2');
      }
    });
  });
  if (floorPanel && !wallsPanel) showLayer('F2');

  const faqToggle = qs('#faqToggle');
  const faqMore = qs('#faq-more');
  if (faqMore && location.hash === '#faq-wta') {
    faqMore.hidden = false;
    faqToggle?.setAttribute('aria-expanded', 'true');
    if (faqToggle) faqToggle.textContent = 'Fewer questions';
    document.getElementById('faq-wta')?.scrollIntoView();
  }
  faqToggle?.addEventListener('click', () => {
    const open = faqMore.hasAttribute('hidden');
    if (open) {
      faqMore.removeAttribute('hidden');
      faqToggle.setAttribute('aria-expanded', 'true');
      faqToggle.textContent = 'Fewer questions';
    } else {
      faqMore.setAttribute('hidden', '');
      faqToggle.setAttribute('aria-expanded', 'false');
      faqToggle.textContent = 'More questions';
    }
  });

  const step1 = qs('#contactStep1');
  const step2 = qs('#contactStep2');
  const form = qs('#leadForm');

  function selectedRole() {
    return form ? qs('input[name="role"]:checked', form) : null;
  }

  function goStep2() {
    if (!step1 || !step2) return;
    if (!selectedRole()) {
      const first = qs('.role-choice', form);
      first?.classList.add('is-warn');
      qs('input[name="role"]', form)?.focus();
      return;
    }
    step1.hidden = true;
    step1.classList.remove('is-on');
    step2.hidden = false;
    step2.classList.add('is-on');
    qs('#c-name')?.focus();
  }

  function goStep1() {
    if (!step1 || !step2) return;
    step2.hidden = true;
    step2.classList.remove('is-on');
    step1.hidden = false;
    step1.classList.add('is-on');
  }

  qs('#contactNext')?.addEventListener('click', goStep2);
  qs('#contactBack')?.addEventListener('click', goStep1);

  function syncRoleChoices() {
    qsa('.role-choice').forEach((label) => {
      const on = !!label.querySelector('input:checked');
      label.classList.toggle('is-on', on);
    });
  }
  qsa('input[name="role"]').forEach((input) => {
    input.addEventListener('change', syncRoleChoices);
  });
  syncRoleChoices();

  function setRole(role) {
    if (!form || !role) return;
    const input = qs(`input[name="role"][value="${role}"]`, form);
    if (input) input.checked = true;
  }

  function rememberAudience(role) {
    if (!role) return;
    const field = qs('#audienceDoor');
    if (field) field.value = role;
    try { sessionStorage.setItem('bt-audience', role); } catch (err) { /* storage off */ }
  }

  try {
    const storedAudience = sessionStorage.getItem('bt-audience');
    if (storedAudience) {
      setRole(storedAudience);
      rememberAudience(storedAudience);
      syncRoleChoices();
    }
  } catch (err) { /* storage off */ }

  qsa('input[name="role"]').forEach((input) => {
    input.addEventListener('change', () => {
      if (input.checked) rememberAudience(input.value);
    });
  });

  qsa('[data-role]').forEach((el) => {
    el.addEventListener('click', () => {
      setRole(el.dataset.role);
      rememberAudience(el.dataset.role);
      if (el.getAttribute('href') === '#contact') goStep2();
    });
  });

  /* ---------------------------------------------------------------------
     Enquiry forms
     Every form marked [data-lead-form] posts its fields to Web3Forms, which
     emails them to LEAD.email. Set LEAD.accessKey to switch delivery on;
     until then, and whenever a send fails, the form hands the enquiry to
     the visitor's email app instead, so no lead is lost.

     Get a free key for hello@breathetherm.co.uk at https://web3forms.com
     (250 submissions a month, spam filtering included) and paste it below.
     To use a different provider, change endpoint and the body in sendLead().
     See FORMS.md for the setup step and how to add another form.
  --------------------------------------------------------------------- */
  const LEAD = {
    email: 'hello@breathetherm.co.uk',
    phone: '01285 407088',
    endpoint: 'https://api.web3forms.com/submit',
    accessKey: ''
  };

  const FIELD_LABELS = {
    name: 'Name', 'first-name': 'First name', email: 'Email', phone: 'Phone',
    postcode: 'Postcode', company: 'Company', practice: 'Practice',
    area: 'Area covered', trade: 'Main trade', project_stage: 'Project stage',
    message: 'Message', role: 'Enquiring as', audience: 'Audience',
    answers: 'Answers', consent: 'Happy to be contacted'
  };

  function fieldLabel(key) {
    return FIELD_LABELS[key] || key.replace(/[-_]/g, ' ').replace(/^./, (c) => c.toUpperCase());
  }

  function formDataOf(f) {
    const data = {};
    new FormData(f).forEach((value, key) => {
      if (key === 'botcheck') return;
      if (key === 'consent') { data[key] = 'Yes'; return; }
      const text = typeof value === 'string' ? value.trim() : value;
      if (!text) return;
      data[key] = data[key] ? `${data[key]}, ${text}` : text;
    });
    return data;
  }

  const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function fieldError(field, message) {
    const group = field.closest('.form-group') || field.parentNode;
    let err = group.querySelector('.form-error');
    if (!err) {
      err = document.createElement('span');
      err.className = 'form-error';
      err.setAttribute('role', 'alert');
      group.appendChild(err);
    }
    err.textContent = message;
    field.setAttribute('aria-invalid', 'true');
    const clear = () => {
      field.removeAttribute('aria-invalid');
      group.querySelector('.form-error')?.remove();
    };
    field.addEventListener('input', clear, { once: true });
    field.addEventListener('change', clear, { once: true });
  }

  function validateForm(f) {
    let firstBad = null;
    qsa('[required]', f).forEach((field) => {
      if (field.type === 'radio') return;
      let message = '';
      if (field.type === 'checkbox') {
        if (!field.checked) message = 'Please tick to continue.';
      } else if (!field.value.trim()) {
        message = 'This field is required.';
      } else if (field.type === 'email' && !EMAIL_PATTERN.test(field.value.trim())) {
        message = 'Enter a valid email address.';
      }
      const group = field.closest('.form-group') || field.parentNode;
      if (message) {
        fieldError(field, message);
        if (!firstBad) firstBad = field;
      } else {
        group.querySelector('.form-error')?.remove();
        field.removeAttribute('aria-invalid');
      }
    });
    if (firstBad) firstBad.focus();
    return !firstBad;
  }

  function enquirySubject(f, data) {
    const who = data.name || data['first-name'] || '';
    const what = f.dataset.formName || 'Website enquiry';
    return who ? `${what} — ${who}` : what;
  }

  function mailtoHref(subject, data) {
    const body = Object.keys(data)
      .filter((key) => key !== 'subject')
      .map((key) => `${fieldLabel(key)}: ${data[key]}`)
      .join('\n');
    return `mailto:${LEAD.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  function sendLead(f, data) {
    const payload = Object.assign({}, data, {
      subject: enquirySubject(f, data),
      from_name: 'breathetherm.co.uk',
      page: window.location.pathname,
      submitted_at: new Date().toISOString()
    });
    if (!LEAD.accessKey) return Promise.resolve({ ok: false, reason: 'unconfigured', payload });
    return fetch(LEAD.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(Object.assign({ access_key: LEAD.accessKey }, payload))
    })
      .then((res) => res.json().catch(() => ({})).then((body) => {
        if (!res.ok || body.success === false) throw new Error(body.message || `HTTP ${res.status}`);
        return { ok: true, payload };
      }))
      .catch((error) => ({ ok: false, reason: 'error', error, payload }));
  }

  function showPanel(f, panel) {
    f.hidden = true;
    panel.hidden = false;
    panel.style.display = 'block';
    panel.setAttribute('tabindex', '-1');
    panel.focus({ preventScroll: true });
  }

  function showFallback(f, result) {
    const link = mailtoHref(result.payload.subject, result.payload);
    f.hidden = true;
    let panel = f.parentNode.querySelector('.form-fallback');
    if (!panel) {
      panel = document.createElement('div');
      panel.className = 'form-fallback';
      f.parentNode.insertBefore(panel, f.nextSibling);
    }
    panel.textContent = '';

    const auto = f.dataset.fallbackAuto !== 'false';
    const heading = document.createElement('h3');
    heading.textContent = result.reason === 'error'
      ? 'That didn’t send — your details are safe'
      : 'One more step to send';
    const copy = document.createElement('p');
    if (result.reason === 'error') {
      copy.textContent = auto
        ? 'Our form service did not accept the message. Send it from your email app instead, or call us.'
        : 'Our form service did not accept the message. Email it to us instead, or carry on below.';
    } else {
      copy.textContent = auto
        ? 'Your email app is opening with your details. Press send and it reaches us.'
        : 'Email your details to us, or carry on — your answer is ready.';
    }
    const actions = document.createElement('p');
    actions.className = 'form-fallback-actions';

    const mail = document.createElement('a');
    mail.href = link;
    mail.textContent = `Email ${LEAD.email}`;
    actions.append(mail);

    if (f.dataset.fallbackLink) {
      const next = document.createElement('a');
      next.href = f.dataset.fallbackLink;
      next.textContent = f.dataset.fallbackLabel || 'Continue';
      actions.append(document.createTextNode(' · '), next);
    }

    const phone = document.createElement('a');
    phone.href = 'tel:01285407088';
    phone.textContent = `Call ${LEAD.phone}`;
    actions.append(document.createTextNode(' · '), phone);

    panel.append(heading, copy, actions);
    panel.setAttribute('tabindex', '-1');
    panel.focus({ preventScroll: true });

    if (auto) window.location.href = link;
  }

  function bindLeadForm(f) {
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (f.dataset.sending === 'true') return;
      if (f.querySelector('[name="botcheck"]')?.checked) return;

      if (step1 && !step1.hidden && !selectedRole()) { goStep2(); return; }
      if (step2 && step2.hidden) { goStep2(); return; }
      if (!validateForm(f)) return;

      const picked = selectedRole();
      if (picked) rememberAudience(picked.value);

      const data = formDataOf(f);
      const submit = f.querySelector('[type="submit"]');
      const label = submit ? submit.textContent : '';
      f.dataset.sending = 'true';
      f.setAttribute('aria-busy', 'true');
      if (submit) { submit.disabled = true; submit.textContent = 'Sending…'; }

      const result = await sendLead(f, data);

      f.dataset.sending = 'false';
      f.removeAttribute('aria-busy');
      if (submit) { submit.disabled = false; submit.textContent = label; }

      if (!result.ok) { showFallback(f, result); return; }

      const panel = f.dataset.success ? document.getElementById(f.dataset.success) : null;
      if (panel) showPanel(f, panel);
      else f.hidden = true;
      f.dispatchEvent(new CustomEvent('bt:lead-sent', { bubbles: true, detail: result.payload }));
    });
  }

  qsa('form[data-lead-form]').forEach(bindLeadForm);

  qsa('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const id = this.getAttribute('href');
      if (!id || id === '#') return;
      const target = qs(id);
      if (!target) return;
      e.preventDefault();
      const offset = target.getBoundingClientRect().top + window.scrollY - 72;
      window.scrollTo({ top: offset, behavior: 'smooth' });
    });
  });

  const mobileCta = qs('#mobileCta');
  const contact = qs('#contact');
  function updateMobileCta() {
    if (!mobileCta) return;
    const wide = window.matchMedia('(max-width: 768px)').matches;
    const pastHero = window.scrollY > 420;
    const contactBox = contact?.getBoundingClientRect();
    const contactIn = contactBox && contactBox.top < window.innerHeight && contactBox.bottom > 80;
    const explorer = qs('#explorer');
    const explorerBox = explorer?.getBoundingClientRect();
    const explorerIn = explorerBox && explorerBox.top < window.innerHeight - 80 && explorerBox.bottom > 120;
    const on = wide && pastHero && !contactIn && !explorerIn;
    mobileCta.classList.toggle('is-on', on);
    document.body.classList.toggle('has-mobile-cta', on);
  }
  window.addEventListener('scroll', updateMobileCta, { passive: true });
  window.addEventListener('resize', updateMobileCta);
  updateMobileCta();

  const openModal = (id) => {
    const overlay = qs(`#modal-${id}`);
    if (!overlay) return;
    overlay.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
    overlay.querySelector('a, button')?.focus();
  };
  const closeAllModals = () => {
    qsa('.modal-overlay').forEach((o) => o.classList.remove('modal-open'));
    document.body.style.overflow = '';
  };
  qsa('.path-trigger').forEach((btn) =>
    btn.addEventListener('click', () => openModal(btn.dataset.modal))
  );
  qsa('.modal-close').forEach((btn) =>
    btn.addEventListener('click', () => closeAllModals())
  );
  qsa('.modal-overlay').forEach((overlay) =>
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeAllModals();
    })
  );
  const quotes = qs('.quotes');
  if (quotes) {
    const btns = qsa('.quotes-btn');
    const updateQuoteBtns = () => {
      btns[0].disabled = quotes.scrollLeft <= 2;
      btns[1].disabled = quotes.scrollLeft + quotes.clientWidth >= quotes.scrollWidth - 2;
    };
    btns.forEach((btn) =>
      btn.addEventListener('click', () => {
        const step = qs('.quote', quotes).offsetWidth + parseFloat(getComputedStyle(quotes).columnGap);
        quotes.scrollBy({ left: step * Number(btn.dataset.dir), behavior: 'smooth' });
      })
    );
    quotes.addEventListener('scroll', updateQuoteBtns, { passive: true });
    window.addEventListener('resize', updateQuoteBtns);
    updateQuoteBtns();
  }

  const glQ = qs('#gl-q');
  if (glQ) {
    let glCat = '';
    const filterGlossary = () => {
      const q = glQ.value.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp(`(^|[^a-z])${q}`, 'i');
      let any = false;
      qsa('.gl-letter').forEach((sec) => {
        let shown = 0;
        qsa('.gl-card', sec).forEach((card) => {
          const ok = (!glCat || card.dataset.cat === glCat) && (!q || re.test(card.textContent));
          card.hidden = !ok;
          if (ok) shown++;
        });
        sec.hidden = !shown;
        qs(`.gl-az a[href="#${sec.id}"]`)?.classList.toggle('is-off', !shown);
        if (shown) any = true;
      });
      qs('#gl-empty').hidden = any;
    };
    glQ.addEventListener('input', filterGlossary);
    qsa('.gl-cat').forEach((btn) =>
      btn.addEventListener('click', () => {
        glCat = btn.dataset.cat;
        qsa('.gl-cat').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
        filterGlossary();
      })
    );
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeAllModals();
      mNav?.classList.remove('open');
      ham?.setAttribute('aria-expanded', 'false');
    }
  });
})();

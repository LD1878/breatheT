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
  window.addEventListener('scroll', updateNav, { passive: true });
  updateNav();

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
      lambda: '—',
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
  qsa('.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      const view = tab.dataset.view;
      qsa('.tab').forEach((t) => {
        const on = t === tab;
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', String(on));
      });
      if (view === 'floor') {
        wallsPanel.hidden = true;
        wallsPanel.classList.remove('is-on');
        floorPanel.hidden = false;
        floorPanel.classList.add('is-on');
        showLayer('F2');
      } else {
        floorPanel.hidden = true;
        floorPanel.classList.remove('is-on');
        wallsPanel.hidden = false;
        wallsPanel.classList.add('is-on');
        showLayer('W2');
      }
    });
  });

  const faqToggle = qs('#faqToggle');
  const faqMore = qs('#faq-more');
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
  const success = qs('#formSuccess');

  function selectedRole() {
    return qs('input[name="role"]:checked', form);
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

  qsa('[data-role]').forEach((el) => {
    el.addEventListener('click', () => {
      setRole(el.dataset.role);
      if (el.getAttribute('href') === '#contact') goStep2();
    });
  });

  function bindLeadForm(f, ok) {
    if (!f) return;
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (step1 && !step1.hidden && !selectedRole()) {
        goStep2();
        return;
      }
      if (step2 && step2.hidden) {
        goStep2();
        return;
      }
      let valid = true;
      qsa('[required]', this).forEach((field) => {
        if (field.type === 'radio') return;
        const group = field.closest('.form-group') || field.parentNode;
        let err = group.querySelector('.form-error');
        if (!field.value.trim()) {
          field.style.borderColor = '#FF643E';
          if (!err) {
            err = document.createElement('span');
            err.className = 'form-error';
            err.setAttribute('role', 'alert');
            err.textContent = 'This field is required.';
            group.appendChild(err);
          }
          field.addEventListener('input', () => {
            field.style.borderColor = '';
            if (err) err.remove();
          }, { once: true });
          valid = false;
        } else if (err) {
          field.style.borderColor = '';
          err.remove();
        }
      });
      if (!valid) return;
      f.hidden = true;
      if (ok) {
        ok.hidden = false;
        ok.style.display = 'block';
      }
    });
  }
  bindLeadForm(form, success);
  bindLeadForm(qs('#techPackForm'), qs('#techPackSuccess'));
  bindLeadForm(qs('#quizCapture'), qs('#formSuccess'));

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
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeAllModals();
      mNav?.classList.remove('open');
      ham?.setAttribute('aria-expanded', 'false');
    }
  });
})();

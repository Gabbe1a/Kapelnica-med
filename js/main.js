document.addEventListener('DOMContentLoaded', () => {

    // ── Form Submit Logic ──────────────────────────────────────────
    const form = document.getElementById('consultation-form');
    const errorDiv = document.getElementById('form-error');
    const successDiv = document.getElementById('form-success');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            errorDiv.style.display = 'none';
            errorDiv.textContent = '';

            const formData = new FormData(form);
            const name = formData.get('name').trim();
            const phone = formData.get('phone').trim();
            const email = formData.get('email').trim();

            if (!name || !phone || !email) {
                showError('Пожалуйста, заполните все поля.');
                return;
            }

            try {
                const response = await fetch('backend/process.php', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                if (result.success) {
                    form.style.display = 'none';
                    successDiv.style.display = 'block';
                    successDiv.textContent = result.message || 'Заявка успешно отправлена!';
                } else {
                    showError(result.message || 'Произошла ошибка.');
                }
            } catch (error) {
                console.error('Error submitting form:', error);
                showError('Ошибка соединения с сервером.');
            }
        });
    }

    function showError(msg) {
        errorDiv.textContent = msg;
        errorDiv.style.display = 'block';
    }

    // ── FAQ Accordion Logic ────────────────────────────────────────
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const header = item.querySelector('.faq-header');
        if (!header) return;
        header.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            faqItems.forEach(faq => {
                faq.classList.remove('active');
                const toggleBtn = faq.querySelector('.faq-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#004728" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
                }
            });

            if (!isActive) {
                item.classList.add('active');
                const toggleBtn = item.querySelector('.faq-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#004728" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
                }
            }
        });
    });

    // ── Footer Accordion Logic (Mobile) ─────────────────────────────
    const footerAccordions = document.querySelectorAll('.footer-col-accordion');
    footerAccordions.forEach(item => {
        const header = item.querySelector('.footer-col-header');
        if (!header) return;
        
        header.addEventListener('click', () => {
            if (window.innerWidth > 768) return; // Only apply on mobile
            
            const isActive = item.classList.contains('active');

            footerAccordions.forEach(acc => {
                acc.classList.remove('active');
                const toggleBtn = acc.querySelector('.footer-col-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#004728" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
                }
            });

            if (!isActive) {
                item.classList.add('active');
                const toggleBtn = item.querySelector('.footer-col-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#004728" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line></svg>';
                }
            }
        });
    });

    // ── Licenses Slider (Carousel) Logic ───────────────────────────
    const slider = document.querySelector('.licenses-slider');
    const btnPrev = document.querySelector('.slider-btn-prev');
    const btnNext = document.querySelector('.slider-btn-next');

    if (slider && btnPrev && btnNext) {
        // Make slider scrollable (hide scrollbar visually)
        slider.style.overflowX = 'auto';
        slider.style.scrollbarWidth = 'none'; // Firefox
        slider.style.msOverflowStyle = 'none'; // IE

        const getScrollAmount = () => {
            const firstCard = slider.firstElementChild;
            if (firstCard) {
                const cardWidth = firstCard.offsetWidth;
                const gap = parseInt(getComputedStyle(slider).gap) || 32;
                return cardWidth + gap;
            }
            return 420;
        };

        btnNext.addEventListener('click', () => {
            slider.scrollBy({ left: getScrollAmount(), behavior: 'smooth' });
        });

        btnPrev.addEventListener('click', () => {
            slider.scrollBy({ left: -getScrollAmount(), behavior: 'smooth' });
        });

        const updateButtons = () => {
            const atStart = slider.scrollLeft <= 0;
            const atEnd = slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 2;
            btnPrev.style.opacity = atStart ? '0.4' : '1';
            btnPrev.style.cursor = atStart ? 'not-allowed' : 'pointer';
            btnNext.style.opacity = atEnd ? '0.4' : '1';
            btnNext.style.cursor = atEnd ? 'not-allowed' : 'pointer';
        };

        slider.addEventListener('scroll', updateButtons, { passive: true });
        updateButtons();
    }

    // ── Mobile Menu & Accordions ────────────────────────────────────────────────
    const menuBtn = document.getElementById('mobileMenuBtn');
    const overlay = document.getElementById('mobileNavOverlay');
    const closeBtn = document.getElementById('mobileNavClose');

    function openMenu() {
        if(overlay) overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        if(overlay) overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (menuBtn) menuBtn.addEventListener('click', openMenu);
    if (closeBtn) closeBtn.addEventListener('click', closeMenu);
    
    // Accordion Logic
    const accordions = document.querySelectorAll('.mobile-accordion-btn');
    accordions.forEach(btn => {
        btn.addEventListener('click', () => {
            const parent = btn.parentElement;
            parent.classList.toggle('active');
        });
    });

    const subAccordions = document.querySelectorAll('.mobile-sub-btn');
    subAccordions.forEach(btn => {
        btn.addEventListener('click', () => {
            const parent = btn.parentElement;
            parent.classList.toggle('active');
        });
    });

    // Close menu when clicking a simple link
    const mobileLinks = document.querySelectorAll('.mobile-nav-link-item, .mobile-sub-link');
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    const dripSheet = document.getElementById('dripSheet');
    const dripSheetForm = document.getElementById('dripSheetForm');
    const dripSheetOpeners = document.querySelectorAll('.js-open-drip-sheet');
    let dripSheetPreviousFocus = null;

    const setDripSheetState = (stateName) => {
        if (!dripSheet) return;

        dripSheet.querySelectorAll('[data-sheet-state]').forEach(state => {
            state.classList.toggle('is-active', state.dataset.sheetState === stateName);
        });
    };

    const openDripSheet = (e) => {
        if (e && e.preventDefault) {
            e.preventDefault();
        }
        if (!dripSheet) return;

        dripSheetPreviousFocus = document.activeElement;
        setDripSheetState('form');
        dripSheet.classList.add('is-active');
        dripSheet.setAttribute('aria-hidden', 'false');
        document.body.classList.add('sheet-open');

        const firstInput = dripSheet.querySelector('.sheet-input');
        if (firstInput) {
            window.setTimeout(() => firstInput.focus(), 80);
        }
    };

    const closeDripSheet = () => {
        if (!dripSheet) return;

        dripSheet.classList.remove('is-active');
        dripSheet.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('sheet-open');

        if (dripSheetForm) {
            dripSheetForm.reset();
            dripSheetForm.querySelectorAll('.sheet-input').forEach(input => input.classList.remove('is-invalid'));
            const submit = dripSheetForm.querySelector('.sheet-submit');
            if (submit) {
                submit.disabled = false;
                submit.textContent = 'Отправить заявку';
            }
        }

        if (dripSheetPreviousFocus && typeof dripSheetPreviousFocus.focus === 'function') {
            dripSheetPreviousFocus.focus();
        }
    };

    dripSheetOpeners.forEach(button => {
        button.addEventListener('click', openDripSheet);
    });

    if (dripSheet) {
        dripSheet.querySelectorAll('[data-sheet-close]').forEach(button => {
            button.addEventListener('click', closeDripSheet);
        });

        const retryButton = dripSheet.querySelector('[data-sheet-retry]');
        if (retryButton) {
            retryButton.addEventListener('click', () => {
                setDripSheetState('form');
                const firstInput = dripSheet.querySelector('.sheet-input');
                if (firstInput) firstInput.focus();
            });
        }

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && dripSheet.classList.contains('is-active')) {
                closeDripSheet();
            }
        });
    }

    if (dripSheetForm) {
        dripSheetForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const requiredFields = dripSheetForm.querySelectorAll('.sheet-input[required]');
            let isValid = true;

            requiredFields.forEach(input => {
                const hasValue = input.value.trim().length > 0;
                input.classList.toggle('is-invalid', !hasValue);
                if (!hasValue) isValid = false;
            });

            const agreement = dripSheetForm.querySelector('.sheet-checkbox');
            if (agreement && !agreement.checked) {
                isValid = false;
            }

            if (!isValid) return;

            const submit = dripSheetForm.querySelector('.sheet-submit');
            if (submit) {
                submit.disabled = true;
                submit.textContent = 'Отправляем...';
            }

            const formData = new FormData(dripSheetForm);

            try {
                const response = await fetch(dripSheetForm.action, {
                    method: 'POST',
                    body: formData
                });
                const contentType = response.headers.get('content-type') || '';
                const result = contentType.includes('application/json') ? await response.json() : { success: response.ok };

                setDripSheetState(response.ok && result.success ? 'success' : 'error');
            } catch (error) {
                console.error('Error submitting drip sheet:', error);
                setDripSheetState('error');
            } finally {
                if (submit) {
                    submit.disabled = false;
                    submit.textContent = 'Отправить заявку';
                }
            }
        });
    }

    // Consultation Modal Logic
    const consultModal = document.getElementById('consultationModal');
    const btnSignup = document.getElementById('btn-signup');
    const consultCloseButtons = document.querySelectorAll('[data-consult-close]');
    const consultForm = document.getElementById('consultForm');
    const consultStates = document.querySelectorAll('.consultation-state-form, .consultation-state-result');
    const consultRetryButtons = document.querySelectorAll('[data-consult-retry]');

    function openConsultModal(e) {
        if (e) e.preventDefault();
        if (!consultModal) return;
        consultModal.classList.add('is-active');
        document.body.style.overflow = 'hidden';
        setConsultState('form');
    }

    function closeConsultModal() {
        if (!consultModal) return;
        consultModal.classList.remove('is-active');
        document.body.style.overflow = '';
    }

    function setConsultState(stateName) {
        consultStates.forEach(state => {
            if (state.dataset.consultState === stateName) {
                state.classList.add('is-active');
            } else {
                state.classList.remove('is-active');
            }
        });
    }

    if (btnSignup) {
        btnSignup.addEventListener('click', openConsultModal);
    }

    // Attach to any element with js-open-consult-modal class just in case
    document.querySelectorAll('.js-open-consult-modal').forEach(btn => {
        btn.addEventListener('click', openConsultModal);
    });

    consultCloseButtons.forEach(btn => {
        btn.addEventListener('click', closeConsultModal);
    });

    consultRetryButtons.forEach(btn => {
        btn.addEventListener('click', () => setConsultState('form'));
    });

    if (consultForm) {
        consultForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const requiredFields = consultForm.querySelectorAll('.consultation-input[required]');
            let isValid = true;

            requiredFields.forEach(input => {
                const hasValue = input.value.trim().length > 0;
                input.classList.toggle('is-invalid', !hasValue);
                if (!hasValue) isValid = false;
            });

            const agreement = consultForm.querySelector('.consultation-checkbox');
            if (agreement && !agreement.checked) {
                isValid = false;
            }

            if (!isValid) return;
            
            const submit = consultForm.querySelector('[type="submit"]');
            if (submit) {
                submit.disabled = true;
                submit.textContent = 'Отправка...';
            }

            const formData = new FormData(consultForm);

            try {
                const response = await fetch(consultForm.action, {
                    method: 'POST',
                    body: formData
                });
                const contentType = response.headers.get('content-type') || '';
                const result = contentType.includes('application/json') ? await response.json() : { success: response.ok };

                setConsultState(response.ok && result.success ? 'success' : 'error');
            } catch (error) {
                console.error('Error submitting consultation form:', error);
                setConsultState('error');
            } finally {
                if (submit) {
                    submit.disabled = false;
                    submit.textContent = 'Отправить заявку';
                }
            }
        });
    }

    // Phone Mask Logic
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (this.value === '') {
                this.value = '+7 ';
            }
        });

        input.addEventListener('blur', function() {
            if (this.value === '+7 ' || this.value === '+7') {
                this.value = '';
            }
        });

        input.addEventListener('input', function (e) {
            let val = this.value.replace(/\D/g, '');
            let res = '';
            
            if (val.length === 0) {
                this.value = '+7 ';
                return;
            }

            if (val[0] === '8' || val[0] === '9') {
                if (val[0] === '9') val = '7' + val;
                else val = '7' + val.substring(1);
            } else if (val[0] !== '7') {
                val = '7' + val;
            }

            res = '+7 ';
            
            if (val.length > 1) {
                res += '(' + val.substring(1, 4);
            }
            if (val.length >= 5) {
                res += ') ' + val.substring(4, 7);
            }
            if (val.length >= 8) {
                res += '-' + val.substring(7, 9);
            }
            if (val.length >= 10) {
                res += '-' + val.substring(9, 11);
            }
            
            this.value = res;
        });
        
        input.addEventListener('keydown', function(e) {
            if (e.keyCode === 8 && this.value.length <= 3) {
                e.preventDefault();
            }
        });
    });
});




document.addEventListener('DOMContentLoaded', () => {
    // Search Data Catalog
    const searchCatalog = [
        { title: 'Капельница «Золушка»', keywords: 'золушка красота омоложение кожа', type: 'drip' },
        { title: 'Капельница «Детокс»', keywords: 'детокс отравление очищение печень', type: 'drip' },
        { title: 'Капельница «Иммунитет +»', keywords: 'иммунитет здоровье простуда витамины', type: 'drip' },
        { title: 'Снятие похмельного синдрома', keywords: 'похмелье алкоголь интоксикация утро', type: 'drip' },
        { title: 'Капельница «Железо»', keywords: 'железо анемия слабость усталость', type: 'drip' },
        { title: 'Капельница «Энергия»', keywords: 'энергия усталость слабость силы бодрость', type: 'drip' },
        { title: 'Выезд на дом', keywords: 'дом выезд на дом врач медсестра', type: 'service' },
        { title: 'Сдача анализов', keywords: 'анализы кровь чек-ап', type: 'service' }
    ];

    
    
    // Global Search Dropdown Logic
    const searchDropdown = document.getElementById('searchDropdown');
    const globalSearchInput = document.getElementById('globalSearchInput');
    const searchDropdownClose = document.getElementById('searchDropdownClose');
    const searchHints = document.getElementById('searchHints');
    const searchResults = document.getElementById('searchResults');
    const searchNoResults = document.getElementById('searchNoResults');
    const hintTags = document.querySelectorAll('.search-hint-tag');

    const headerSearchOpeners = document.querySelectorAll('.js-open-search-modal');
    const footerSearchInput = document.querySelector('.footer-search-input');
    const mobileSearchInput = document.querySelector('.mobile-search-input');

    let searchOpenScrollY = 0;
    
    function openSearchDropdown(isFooter) {
        if (!searchDropdown) return;
        
        searchOpenScrollY = window.scrollY;
        
        // Reset dynamic styles
        searchDropdown.style.bottom = '';
        searchDropdown.style.left = '';
        searchDropdown.style.width = '';
        
        if (isFooter && footerSearchInput) {
            searchDropdown.classList.add('footer-active');
            const rect = footerSearchInput.getBoundingClientRect();
            // Position exactly above the footer input
            searchDropdown.style.bottom = (window.innerHeight - rect.top + 10) + 'px';
            searchDropdown.style.left = rect.left + 'px';
            
            // On desktop, limit width to match input approximately, 
            // but searchDropdown has max-width: 400px.
            // Let's ensure it has at least the input width:
            searchDropdown.style.width = Math.max(rect.width, 300) + 'px';
        } else {
            searchDropdown.classList.remove('footer-active');
        }

        searchDropdown.classList.add('active');
        setTimeout(() => { if (globalSearchInput) globalSearchInput.focus(); }, 50);
    }

    function closeSearchDropdown() {
        if (!searchDropdown) return;
        searchDropdown.classList.remove('active');
        if (globalSearchInput) globalSearchInput.value = '';
        if (footerSearchInput) footerSearchInput.value = '';
        if (mobileSearchInput) mobileSearchInput.value = '';
        renderResults('');
    }

    // Hide on scroll with a threshold to ignore keyboard-triggered scrolls on mobile
    window.addEventListener('scroll', () => {
        if (searchDropdown && searchDropdown.classList.contains('active')) {
            if (Math.abs(window.scrollY - searchOpenScrollY) > 50) {
                closeSearchDropdown();
            }
        }
    }, { passive: true });

    headerSearchOpeners.forEach(opener => {
        opener.addEventListener('click', (e) => {
            e.preventDefault();
            openSearchDropdown(false);
        });
    });

    if (footerSearchInput) {
        footerSearchInput.addEventListener('focus', () => {
            openSearchDropdown(true);
            if (globalSearchInput) globalSearchInput.value = footerSearchInput.value;
            renderResults(footerSearchInput.value);
        });
        footerSearchInput.addEventListener('input', (e) => {
            if (globalSearchInput) globalSearchInput.value = e.target.value;
            openSearchDropdown(true);
            renderResults(e.target.value);
        });
    }

    if (mobileSearchInput) {
        mobileSearchInput.addEventListener('focus', () => {
            openSearchDropdown(false);
            if (globalSearchInput) globalSearchInput.value = mobileSearchInput.value;
            renderResults(mobileSearchInput.value);
        });
        mobileSearchInput.addEventListener('input', (e) => {
            if (globalSearchInput) globalSearchInput.value = e.target.value;
            openSearchDropdown(false);
            renderResults(e.target.value);
        });
    }

    if (searchDropdownClose) {
        searchDropdownClose.addEventListener('click', closeSearchDropdown);
    }

    document.addEventListener('click', (e) => {
        if (searchDropdown && searchDropdown.classList.contains('active')) {
            const isClickInside = searchDropdown.contains(e.target);
            const isOpener = Array.from(headerSearchOpeners).some(opener => opener.contains(e.target));
            const isFooterInput = footerSearchInput && footerSearchInput.contains(e.target);
            const isMobileInput = mobileSearchInput && mobileSearchInput.contains(e.target);
            
            if (!isClickInside && !isOpener && !isFooterInput && !isMobileInput) {
                closeSearchDropdown();
            }
        }
    });

    function renderResults(query) {
        if (!searchHints || !searchResults || !searchNoResults) return;
        if (!query) {
            searchHints.style.display = "block";
            searchResults.style.display = "none";
            searchNoResults.style.display = "none";
            return;
        }

        searchHints.style.display = "none";
        
        const filtered = searchCatalog.filter(item => {
            return item.title.toLowerCase().includes(query.toLowerCase()) || item.keywords.toLowerCase().includes(query.toLowerCase());
        });

        if (filtered.length === 0) {
            searchResults.style.display = "none";
            searchNoResults.style.display = "block";
            return;
        }

        searchNoResults.style.display = "none";
        searchResults.style.display = "flex";

        searchResults.innerHTML = filtered.map(item => `
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title">${item.title}</div>
                    <div class="search-result-type">${item.type === 'drip' ? 'Капельница на дому' : 'Услуга'}</div>
                </div>
            </a>
        `).join('');

        searchResults.querySelectorAll('.js-open-drip-sheet').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSearchDropdown();
                // Close mobile menu if open
                const mobileNavClose = document.getElementById('mobileNavClose');
                if (mobileNavClose) mobileNavClose.click();
                
                const dripBtn = document.getElementById('open-drip-sheet');
                if(dripBtn) dripBtn.click();
            });
        });
    }

    if (globalSearchInput) {
        globalSearchInput.addEventListener('input', (e) => {
            const val = e.target.value;
            if (footerSearchInput) footerSearchInput.value = val;
            if (mobileSearchInput) mobileSearchInput.value = val;
            renderResults(val);
        });
    }

    hintTags.forEach(tag => {
        tag.addEventListener('click', () => {
            if (globalSearchInput) globalSearchInput.value = tag.textContent;
            renderResults(tag.textContent);
        });
    });
});
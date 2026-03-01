// ==UserScript==
// @name         小红书专注模式
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  仅在小红书首页推荐页显示遮罩，搜索后或进入其他页面自动隐藏
// @author       Claude
// @match        *://www.xiaohongshu.com/*
// @grant        GM_addStyle
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';

    GM_addStyle(`
    #xhs-focus-overlay {
      position: fixed;
      top: var(--xhs-header-height, 60px);
      left: 0; right: 0; bottom: 0;
      z-index: 99999;
      background: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      transition: opacity 0.3s ease, visibility 0.3s ease;
    }
    #xhs-focus-overlay.hidden {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }
    #xhs-focus-overlay .focus-icon { font-size: 48px; line-height: 1; }
    #xhs-focus-overlay .focus-title {
      font-size: 20px; font-weight: 600; color: #1a1a1a;
      font-family: "PingFang SC", "Hiragino Sans GB", sans-serif;
    }
    #xhs-focus-overlay .focus-hint {
      font-size: 14px; color: #999;
      font-family: "PingFang SC", "Hiragino Sans GB", sans-serif;
    }
  `);

    // 只有 /explore 页才显示遮罩
    function isExplorePage() {
        return location.pathname === '/explore' || location.pathname === '/explore/';
    }

    function getHeaderHeight() {
        const selectors = ['header', '.header', '#header', 'nav', '[class*="header"]'];
        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) { const h = el.getBoundingClientRect().height; if (h > 20) return h; }
        }
        return 60;
    }

    function createOverlay() {
        if (document.getElementById('xhs-focus-overlay')) return;
        document.documentElement.style.setProperty('--xhs-header-height', getHeaderHeight() + 'px');
        const overlay = document.createElement('div');
        overlay.id = 'xhs-focus-overlay';
        overlay.innerHTML = `
      <div class="focus-icon">🔍</div>
      <div class="focus-title">专注模式已开启</div>
      <div class="focus-hint">请在搜索框输入关键词，只看你真正想看的内容</div>
    `;
        document.body.appendChild(overlay);
    }

    function updateOverlay() {
        const overlay = document.getElementById('xhs-focus-overlay');
        if (!overlay) return;
        if (isExplorePage()) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }

    // 监听 SPA 路由变化
    let lastUrl = location.href;
    function onUrlChange() {
        if (location.href === lastUrl) return;
        lastUrl = location.href;
        updateOverlay();
    }

    ['pushState', 'replaceState'].forEach((method) => {
        const original = history[method];
        history[method] = function (...args) { original.apply(this, args); onUrlChange(); };
    });
    window.addEventListener('popstate', onUrlChange);

    function init() {
        createOverlay();
        updateOverlay();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
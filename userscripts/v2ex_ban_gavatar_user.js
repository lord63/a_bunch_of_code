// ==UserScript==
// @name         V2EX 屏蔽默认头像（主题列表 + TopicsHot + 回复）
// @namespace    https://example.com/
// @version      0.4.0
// @description  屏蔽使用 gravatar 默认头像（/gravatar/）的���目：主题列表、TopicsHot、以及主题正文回复。支持“直接隐藏”或“显示占位”模式切换。
// @match        https://www.v2ex.com/*
// @match        https://v2ex.com/*
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_registerMenuCommand
// ==/UserScript==

(() => {
    'use strict';

    const MODE_KEY = 'v2ex_hide_default_avatar_mode';
    const Mode = { HIDE: 'hide', PLACEHOLDER: 'placeholder' };
    const DEFAULT_MODE = Mode.PLACEHOLDER;

    function getMode() {
        return GM_getValue(MODE_KEY, DEFAULT_MODE);
    }

    function setMode(mode) {
        GM_setValue(MODE_KEY, mode);
    }

    function isDefaultAvatarUrl(url) {
        if (!url) return false;
        return url.includes('cdn.v2ex.com/gravatar/') || url.includes('/gravatar/');
    }

    function detectCellKind(cell) {
        // 返回 'topic' | 'reply' | null
        if (!(cell instanceof HTMLElement)) return null;
        if (!cell.matches('div.cell')) return null;
        if (!cell.querySelector('img.avatar')) return null;

        // 回复：你给的例子 id="r_17335973"
        if (cell.id && cell.id.startsWith('r_')) return 'reply';

        // ��题/热榜：存在指向 /t/ 的链接（topic-link / item_title / item_hot_topic_title 等）
        const hasTopicLink =
            cell.querySelector('a.topic-link') ||
            cell.querySelector('.item_title a[href^="/t/"]') ||
            cell.querySelector('.item_hot_topic_title a[href^="/t/"]') ||
            cell.querySelector('a[href^="/t/"]'); // 兜底（在有 avatar 的前提下）

        if (hasTopicLink) return 'topic';

        return null;
    }

    function buildPlaceholder(originalCell, kind) {
        const ph = document.createElement('div');
        ph.className = (originalCell.className || 'cell') + ' tm-default-avatar-blocked';
        if (originalCell.getAttribute('style')) ph.setAttribute('style', originalCell.getAttribute('style'));

        const img = originalCell.querySelector('img.avatar');
        const size = img?.getAttribute('width') || '48';

        const label = kind === 'reply' ? '已屏蔽一条回复（默认头像）' : '已屏蔽一条主题（默认头像）';

        ph.innerHTML = `
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tbody>
          <tr>
            <td width="${size}" valign="top" align="center">
              <div style="width:${size}px;height:${size}px;line-height:${size}px;text-align:center;border-radius:4px;background:#f2f2f2;color:#888;font-size:12px;">
                隐藏
              </div>
            </td>
            <td width="10"></td>
            <td width="auto" valign="top" align="left" style="color:#666;">
              <div style="font-size:13px; margin-bottom:4px;">
                ${label}
              </div>
              <div style="font-size:12px;">
                <a href="javascript:void(0)" class="tm-unblock">点击展开</a>
              </div>
            </td>
            <td width="70" align="right" valign="middle"></td>
          </tr>
        </tbody>
      </table>
    `.trim();

        ph.querySelector('.tm-unblock').addEventListener('click', () => {
            ph.replaceWith(originalCell);
            originalCell.style.removeProperty('display');
        });

        return ph;
    }

    function processCell(cell, mode) {
        if (!cell || cell.dataset.tmProcessed === '1') return;

        const kind = detectCellKind(cell);
        if (!kind) return;

        const avatarImg = cell.querySelector('img.avatar');
        const url = avatarImg?.currentSrc || avatarImg?.src || '';
        if (!isDefaultAvatarUrl(url)) {
            cell.dataset.tmProcessed = '1';
            return;
        }

        if (mode === Mode.HIDE) {
            cell.style.display = 'none';
            cell.dataset.tmProcessed = '1';
            return;
        }

        if (mode === Mode.PLACEHOLDER) {
            const ph = buildPlaceholder(cell, kind);
            cell.dataset.tmProcessed = '1';
            cell.replaceWith(ph);
            return;
        }

        cell.dataset.tmProcessed = '1';
    }

    function scanAndProcess(mode) {
        const cells = document.querySelectorAll('div.cell');
        for (const cell of cells) processCell(cell, mode);
    }

    function registerMenu() {
        GM_registerMenuCommand('模式：直接隐藏（整条不显示）', () => {
            setMode(Mode.HIDE);
            location.reload();
        });
        GM_registerMenuCommand('模式：显示占位（可点击展开）', () => {
            setMode(Mode.PLACEHOLDER);
            location.reload();
        });
    }

    function observe(mode) {
        const obs = new MutationObserver((mutations) => {
            for (const m of mutations) {
                for (const node of m.addedNodes) {
                    if (!(node instanceof HTMLElement)) continue;

                    if (node.matches?.('div.cell')) processCell(node, mode);

                    const cells = node.querySelectorAll?.('div.cell');
                    if (cells?.length) for (const cell of cells) processCell(cell, mode);
                }
            }
        });

        obs.observe(document.documentElement, { childList: true, subtree: true });
    }

    const mode = getMode();
    registerMenu();
    scanAndProcess(mode);
    observe(mode);
})();
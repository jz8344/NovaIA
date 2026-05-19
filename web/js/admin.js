const API_BASE = '/api/admin';

class NovaAdmin {
    constructor() {
        this.setupTabs();
        this.setupExtensions();
        this.setupInventory();
        this.setupPrompts();
        this.setupTools();
        this.setupSessions();
        this.setupLogs();
        this.loadExtensions();
    }

    async api(method, path, body = null) {
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (body) options.body = JSON.stringify(body);
        const res = await fetch(`${API_BASE}${path}`, options);
        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(err.detail || 'Error de API');
        }
        return res.json();
    }

    toast(message, type = 'success') {
        document.querySelectorAll('.toast').forEach(t => t.remove());
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3500);
    }

    // ── TABS ──────────────────────────────────────────────────────────────────

    setupTabs() {
        document.querySelectorAll('.admin-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.admin-panel').forEach(p => p.classList.remove('active'));
                tab.classList.add('active');
                const panel = document.getElementById(`panel-${tab.dataset.tab}`);
                if (panel) panel.classList.add('active');
                this.onTabChange(tab.dataset.tab);
            });
        });
    }

    onTabChange(tab) {
        switch (tab) {
            case 'extensions': this.loadExtensions(); break;
            case 'inventory':  this.loadInventory();  break;
            case 'prompts':    this.loadPrompts();    break;
            case 'tools':      this.loadTools();      break;
            case 'sessions':   this.loadSessions();   break;
            case 'logs':       this.loadLogs();       break;
        }
    }

    // ── EXTENSIONS ────────────────────────────────────────────────────────────

    setupExtensions() {
        document.getElementById('formAddExtension').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name:       document.getElementById('extName').value.trim(),
                extension:  document.getElementById('extNumber').value.trim(),
                department: document.getElementById('extDept').value.trim(),
                email:      document.getElementById('extEmail').value.trim()
            };
            if (!data.name || !data.extension) {
                this.toast('Nombre y extensión son requeridos', 'error');
                return;
            }
            try {
                await this.api('POST', '/extensions', data);
                this.toast('Extensión agregada correctamente');
                e.target.reset();
                await this.loadExtensions();
            } catch (err) {
                this.toast(`Error: ${err.message}`, 'error');
            }
        });
    }

    async loadExtensions() {
        try {
            const data = await this.api('GET', '/extensions');
            const tbody = document.getElementById('extensionsBody');
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No hay extensiones registradas</td></tr>';
                return;
            }
            tbody.innerHTML = data.map(ext => `
                <tr>
                    <td><strong>${ext.name}</strong></td>
                    <td><span class="extension-badge">${ext.extension}</span></td>
                    <td>${ext.department || '—'}</td>
                    <td>${ext.email || '—'}</td>
                    <td><span class="status-badge ${ext.available ? 'active' : 'inactive'}">${ext.available ? 'Disponible' : 'No disponible'}</span></td>
                    <td><button class="btn-delete" onclick="window.admin.deleteExtension(${ext.id})" title="Eliminar">×</button></td>
                </tr>
            `).join('');
        } catch (err) {
            this.toast(`Error cargando extensiones: ${err.message}`, 'error');
        }
    }

    async deleteExtension(id) {
        if (!confirm('¿Eliminar esta extensión?')) return;
        try {
            await this.api('DELETE', `/extensions/${id}`);
            this.toast('Extensión eliminada');
            await this.loadExtensions();
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    // ── INVENTORY ─────────────────────────────────────────────────────────────

    setupInventory() {
        document.getElementById('formAddProduct').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                product_name: document.getElementById('prodName').value.trim(),
                description:  document.getElementById('prodDesc').value.trim(),
                price:        parseFloat(document.getElementById('prodPrice').value) || 0,
                stock:        parseInt(document.getElementById('prodStock').value) || 0,
                category:     document.getElementById('prodCategory').value.trim()
            };
            if (!data.product_name) {
                this.toast('El nombre del producto es requerido', 'error');
                return;
            }
            try {
                await this.api('POST', '/inventory', data);
                this.toast('Producto agregado correctamente');
                e.target.reset();
                await this.loadInventory();
            } catch (err) {
                this.toast(`Error: ${err.message}`, 'error');
            }
        });
    }

    async loadInventory() {
        try {
            const data = await this.api('GET', '/inventory');
            const tbody = document.getElementById('inventoryBody');
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No hay productos en inventario</td></tr>';
                return;
            }
            tbody.innerHTML = data.map(item => `
                <tr>
                    <td>
                        <strong>${item.product_name}</strong>
                        ${item.description ? `<div style="font-size:0.75rem;color:var(--text-muted)">${item.description}</div>` : ''}
                    </td>
                    <td>${item.category || '—'}</td>
                    <td>$${parseFloat(item.price).toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
                    <td><span class="stock-badge ${item.stock > 5 ? 'high' : item.stock > 0 ? 'medium' : 'low'}">${item.stock}</span></td>
                    <td><button class="btn-delete" onclick="window.admin.deleteProduct(${item.id})" title="Eliminar">×</button></td>
                </tr>
            `).join('');
        } catch (err) {
            this.toast(`Error cargando inventario: ${err.message}`, 'error');
        }
    }

    async deleteProduct(id) {
        if (!confirm('¿Eliminar este producto?')) return;
        try {
            await this.api('DELETE', `/inventory/${id}`);
            this.toast('Producto eliminado');
            await this.loadInventory();
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    // ── PROMPTS ───────────────────────────────────────────────────────────────

    setupPrompts() {
        document.getElementById('promptSelect').addEventListener('change', async (e) => {
            if (e.target.value) await this.loadPromptContent(e.target.value);
        });

        document.getElementById('btnSavePrompt').addEventListener('click', async () => {
            const name    = document.getElementById('promptSelect').value;
            const content = document.getElementById('promptEditor').value;
            if (!name || !content) {
                this.toast('Selecciona un prompt y agrega contenido', 'error');
                return;
            }
            try {
                await this.api('PUT', `/prompts/${name}`, { name, content });
                this.toast('Prompt guardado correctamente');
            } catch (err) {
                this.toast(`Error: ${err.message}`, 'error');
            }
        });

        document.getElementById('btnDeletePrompt').addEventListener('click', async () => {
            const name = document.getElementById('promptSelect').value;
            if (!name) return;
            if (!confirm(`¿Eliminar el prompt "${name}"? Esta acción no se puede deshacer.`)) return;
            this.toast('Los prompts de archivo no se pueden eliminar desde aquí', 'error');
        });
    }

    async loadPrompts() {
        try {
            const prompts = await this.api('GET', '/prompts');
            const select  = document.getElementById('promptSelect');
            select.innerHTML = prompts.map(p =>
                `<option value="${p}">${p}</option>`
            ).join('');
            if (prompts.length > 0) {
                const defaultPrompt = prompts.includes('nova_default') ? 'nova_default' : prompts[0];
                select.value = defaultPrompt;
                await this.loadPromptContent(defaultPrompt);
            }
        } catch (err) {
            this.toast(`Error cargando prompts: ${err.message}`, 'error');
        }
    }

    async loadPromptContent(name) {
        try {
            const data = await this.api('GET', `/prompts/${name}`);
            document.getElementById('promptEditor').value = data.content;
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    // ── TOOLS ─────────────────────────────────────────────────────────────────

    setupTools() {
        document.getElementById('btnSaveTools').addEventListener('click', async () => {
            const content = document.getElementById('toolsEditor').value;
            try {
                JSON.parse(content);
                this.toast('Los cambios en tools requieren reiniciar el servidor para aplicarse', 'success');
            } catch {
                this.toast('JSON inválido. Verifica la sintaxis antes de guardar.', 'error');
            }
        });
    }

    async loadTools() {
        try {
            const res = await fetch('/static/js/../../../config/tools/default_tools.json');
            if (res.ok) {
                document.getElementById('toolsEditor').value = JSON.stringify(await res.json(), null, 2);
                return;
            }
        } catch {}
        try {
            const res = await fetch('/api/admin/tools');
            if (res.ok) {
                document.getElementById('toolsEditor').value = JSON.stringify(await res.json(), null, 2);
                return;
            }
        } catch {}
        document.getElementById('toolsEditor').value = '{\n  "tools": []\n}';
    }

    // ── SESSIONS ──────────────────────────────────────────────────────────────

    setupSessions() {
        document.getElementById('btnRefreshSessions').addEventListener('click', () => this.loadSessions());
    }

    async loadSessions() {
        try {
            const data  = await this.api('GET', '/sessions');
            const tbody = document.getElementById('sessionsBody');
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Sin sesiones activas</td></tr>';
                return;
            }
            tbody.innerHTML = data.map(s => `
                <tr>
                    <td style="font-family:monospace;font-size:0.75rem">${s.session_id.substring(0, 12)}…</td>
                    <td>${s.source === 'web' ? '🌐 Web' : '📞 Asterisk'}</td>
                    <td>${s.duration}s</td>
                    <td><span class="status-badge ${s.active ? 'active' : 'inactive'}">${s.active ? 'Activa' : 'Finalizada'}</span></td>
                </tr>
            `).join('');
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    // ── LOGS ──────────────────────────────────────────────────────────────────

    setupLogs() {
        document.getElementById('btnRefreshLogs').addEventListener('click', () => this.loadLogs());
    }

    async loadLogs() {
        try {
            const data  = await this.api('GET', '/logs?limit=50');
            const tbody = document.getElementById('logsBody');
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Sin registros de llamadas</td></tr>';
                return;
            }
            tbody.innerHTML = data.map(log => `
                <tr>
                    <td>${new Date(log.created_at).toLocaleString('es-MX')}</td>
                    <td>${log.source === 'web' ? '🌐 Web' : '📞 Asterisk'}</td>
                    <td>${parseFloat(log.duration || 0).toFixed(1)}s</td>
                    <td style="font-size:0.75rem">${log.actions_taken || '—'}</td>
                </tr>
            `).join('');
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.admin = new NovaAdmin();
});

const API_BASE = '/api/admin';

class NovaAdmin {
    constructor() {
        this.currentTab = 'extensions';
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupExtensions();
        this.setupInventory();
        this.setupPrompts();
        this.setupTools();
        this.setupSessions();
        this.setupLogs();

        this.loadExtensions();
    }

    setupTabs() {
        document.querySelectorAll('.admin-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.admin-panel').forEach(p => p.classList.remove('active'));

                tab.classList.add('active');
                const panelId = `panel-${tab.dataset.tab}`;
                const panel = document.getElementById(panelId);
                if (panel) {
                    panel.classList.add('active');
                    panel.style.animation = 'none';
                    panel.offsetHeight;
                    panel.style.animation = null;
                }

                this.currentTab = tab.dataset.tab;
                this.onTabChange(tab.dataset.tab);
            });
        });
    }

    onTabChange(tab) {
        switch (tab) {
            case 'extensions': this.loadExtensions(); break;
            case 'inventory': this.loadInventory(); break;
            case 'prompts': this.loadPrompts(); break;
            case 'tools': this.loadTools(); break;
            case 'sessions': this.loadSessions(); break;
            case 'logs': this.loadLogs(); break;
        }
    }

    setupExtensions() {
        document.getElementById('btnAddExtension').addEventListener('click', async () => {
            const data = {
                name: document.getElementById('extName').value.trim(),
                extension: document.getElementById('extNumber').value.trim(),
                department: document.getElementById('extDept').value.trim(),
                email: document.getElementById('extEmail').value.trim()
            };

            if (!data.name || !data.extension) {
                this.toast('Nombre y extensión son requeridos', 'error');
                return;
            }

            try {
                await this.api('POST', '/extensions', data);
                this.toast('Extensión agregada correctamente');
                document.getElementById('formAddExtension').reset();
                this.loadExtensions();
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
                    <td>${ext.name}</td>
                    <td style="font-weight:600; color: var(--accent-primary);">${ext.extension}</td>
                    <td>${ext.department || '—'}</td>
                    <td>${ext.email || '—'}</td>
                    <td>
                        <span style="color: ${ext.available ? 'var(--success)' : 'var(--error)'}">
                            ${ext.available ? '● Disponible' : '○ No disponible'}
                        </span>
                    </td>
                    <td>
                        <button class="btn-danger" onclick="admin.deleteExtension(${ext.id})">Eliminar</button>
                    </td>
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
            this.loadExtensions();
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    setupInventory() {
        document.getElementById('btnAddProduct').addEventListener('click', async () => {
            const data = {
                product_name: document.getElementById('prodName').value.trim(),
                description: document.getElementById('prodDesc').value.trim(),
                price: parseFloat(document.getElementById('prodPrice').value) || 0,
                stock: parseInt(document.getElementById('prodStock').value) || 0,
                category: document.getElementById('prodCategory').value.trim()
            };

            if (!data.product_name) {
                this.toast('El nombre del producto es requerido', 'error');
                return;
            }

            try {
                await this.api('POST', '/inventory', data);
                this.toast('Producto agregado correctamente');
                document.getElementById('formAddProduct').reset();
                this.loadInventory();
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
                        <div style="font-weight: 500;">${item.product_name}</div>
                        <div style="font-size: 0.75rem; color: var(--text-muted);">${item.description || ''}</div>
                    </td>
                    <td>${item.category || '—'}</td>
                    <td style="font-weight: 600; color: var(--success);">$${parseFloat(item.price).toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
                    <td>
                        <span style="color: ${item.stock > 0 ? 'var(--text-primary)' : 'var(--error)'}">
                            ${item.stock} ${item.stock > 0 ? 'uds.' : '(Agotado)'}
                        </span>
                    </td>
                    <td>
                        <button class="btn-danger" onclick="admin.deleteProduct(${item.id})">Eliminar</button>
                    </td>
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
            this.loadInventory();
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    setupPrompts() {
        document.getElementById('btnSavePrompt').addEventListener('click', async () => {
            const select = document.getElementById('promptSelect');
            const name = select.value;
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

        document.getElementById('promptSelect').addEventListener('change', async (e) => {
            if (e.target.value) {
                await this.loadPromptContent(e.target.value);
            }
        });
    }

    async loadPrompts() {
        try {
            const prompts = await this.api('GET', '/prompts');
            const select = document.getElementById('promptSelect');
            select.innerHTML = prompts.map(p =>
                `<option value="${p}" ${p === 'nova_default' ? 'selected' : ''}>${p}</option>`
            ).join('');

            if (prompts.length > 0) {
                await this.loadPromptContent(prompts.includes('nova_default') ? 'nova_default' : prompts[0]);
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

    setupTools() {
        document.getElementById('btnSaveTools').addEventListener('click', async () => {
            const content = document.getElementById('toolsEditor').value;
            try {
                JSON.parse(content);
                const response = await fetch('/static/tools/default_tools.json', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: content
                });
                this.toast('Nota: Los cambios en tools requieren reiniciar el servidor');
            } catch (err) {
                if (err instanceof SyntaxError) {
                    this.toast('JSON inválido. Verifica la sintaxis.', 'error');
                } else {
                    this.toast(`Error: ${err.message}`, 'error');
                }
            }
        });
    }

    async loadTools() {
        try {
            const response = await fetch('/static/tools/default_tools.json');
            if (response.ok) {
                const text = await response.text();
                document.getElementById('toolsEditor').value = JSON.stringify(JSON.parse(text), null, 2);
            }
        } catch {
            try {
                const response = await fetch('/config/tools/default_tools.json');
                if (response.ok) {
                    const text = await response.text();
                    document.getElementById('toolsEditor').value = text;
                }
            } catch (err) {
                document.getElementById('toolsEditor').value = '{\n  "tools": []\n}';
            }
        }
    }

    setupSessions() {
        document.getElementById('btnRefreshSessions').addEventListener('click', () => this.loadSessions());
    }

    async loadSessions() {
        try {
            const data = await this.api('GET', '/sessions');
            const tbody = document.getElementById('sessionsBody');

            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Sin sesiones activas</td></tr>';
                return;
            }

            tbody.innerHTML = data.map(s => `
                <tr>
                    <td style="font-family: monospace; font-size: 0.75rem;">${s.session_id.substring(0, 12)}...</td>
                    <td>${s.source === 'web' ? '🌐 Web' : '📞 Asterisk'}</td>
                    <td>${s.duration}s</td>
                    <td>
                        <span style="color: ${s.active ? 'var(--success)' : 'var(--text-muted)'}">
                            ${s.active ? '● Activa' : '○ Finalizada'}
                        </span>
                    </td>
                </tr>
            `).join('');
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    setupLogs() {
        document.getElementById('btnRefreshLogs').addEventListener('click', () => this.loadLogs());
    }

    async loadLogs() {
        try {
            const data = await this.api('GET', '/logs');
            const tbody = document.getElementById('logsBody');

            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Sin registros de llamadas</td></tr>';
                return;
            }

            tbody.innerHTML = data.map(log => `
                <tr>
                    <td>${new Date(log.created_at).toLocaleString('es-MX')}</td>
                    <td>${log.source === 'web' ? '🌐 Web' : '📞 Asterisk'}</td>
                    <td>${log.duration.toFixed(1)}s</td>
                    <td style="font-size: 0.75rem;">${log.actions_taken}</td>
                </tr>
            `).join('');
        } catch (err) {
            this.toast(`Error: ${err.message}`, 'error');
        }
    }

    async api(method, path, body = null) {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${API_BASE}${path}`, options);
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(error.detail || 'Error de API');
        }
        return response.json();
    }

    toast(message, type = 'success') {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3500);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.admin = new NovaAdmin();
});

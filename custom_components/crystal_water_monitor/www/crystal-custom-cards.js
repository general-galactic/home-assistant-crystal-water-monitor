const CARD_VERSION = "1.0.6";

const BADGE_OPTIONS = [
  { key: "ph",              labelKey: "badge.ph",         suffix: "",     entitySuffix: "_ph" },
  { key: "orp",             labelKey: "badge.orp",        suffix: " mV",  entitySuffix: "_orp" },
  { key: "waterTemp",       labelKey: "badge.temp",       suffix: "°F",   entitySuffix: "_water_temperature" },
  { key: "freeChlorine",    labelKey: "badge.chlorine",   suffix: " ppm", entitySuffix: "_free_chlorine" },
  { key: "totalAlkalinity", labelKey: "badge.alkalinity", suffix: " ppm", entitySuffix: "_total_alkalinity" },
  { key: "totalHardness",   labelKey: "badge.hardness",   suffix: " ppm", entitySuffix: "_total_hardness" },
  { key: "cyanuricAcid",    labelKey: "badge.cya",        suffix: " ppm", entitySuffix: "_cyanuric_acid" },
  { key: "salt",            labelKey: "badge.salt",       suffix: " ppm", entitySuffix: "_salt" },
  { key: "lsi",             labelKey: "badge.lsi",        suffix: "",     entitySuffix: "_lsi" },
];

const TRANSLATIONS = {
  en: {
    "editor.pool_label": "Pool or Hot Tub",
    "editor.transparent": "Transparent background",
    "editor.show_description": "Show description",
    "editor.show_icons": "Show icons",
    "editor.show_logo": "Show logo",
    "card.no_vessel_selected": "Select a vessel in the card editor.",
    "card.entity_not_found": "Water Status entity not found for this vessel.",
    "card.actions_entity_not_found": "Entity not found for this vessel.",
    "card.no_actions": "No actions needed.",
    "card.actions_header": "Actions",
    "card.just_now": "just now",
    "card.minutes_ago_one": "1 minute ago",
    "card.minutes_ago_other": "{n} minutes ago",
    "card.hours_ago_one": "1 hour ago",
    "card.hours_ago_other": "{n} hours ago",
    "card.days_ago_one": "1 day ago",
    "card.days_ago_other": "{n} days ago",
    "card.years_ago_one": "1 year ago",
    "card.years_ago_other": "{n} years ago",
    "editor.badges": "Badges",
    "editor.badge_position": "Badge position",
    "editor.badge_position_left": "Left",
    "editor.badge_position_right": "Right",
    "editor.badge_position_bottom": "Bottom",
    "editor.time_range": "Time range",
    "card.open_app": "Open Crystal App",
    "graph.ph": "pH",
    "graph.orp": "ORP",
    "graph.temp": "Water Temperature",
    "badge.ph": "pH",
    "badge.orp": "ORP",
    "badge.temp": "Temp",
    "badge.chlorine": "FC",
    "badge.alkalinity": "TA",
    "badge.hardness": "TH",
    "badge.cya": "CYA",
    "badge.salt": "Salt",
    "badge.lsi": "LSI",
  },
  es: {
    "editor.pool_label": "Piscina o bañera de hidromasaje",
    "editor.transparent": "Fondo transparente",
    "editor.show_description": "Mostrar descripción",
    "editor.show_icons": "Mostrar iconos",
    "editor.show_logo": "Mostrar logotipo",
    "card.no_vessel_selected": "Seleccione un depósito en el editor de tarjetas.",
    "card.entity_not_found": "No se encontró la entidad de estado del agua para este depósito.",
    "card.actions_entity_not_found": "No se encontró la entidad para este depósito.",
    "card.no_actions": "No se necesitan acciones.",
    "card.actions_header": "Acciones",
    "card.just_now": "ahora mismo",
    "card.minutes_ago_one": "hace 1 minuto",
    "card.minutes_ago_other": "hace {n} minutos",
    "card.hours_ago_one": "hace 1 hora",
    "card.hours_ago_other": "hace {n} horas",
    "card.days_ago_one": "hace 1 día",
    "card.days_ago_other": "hace {n} días",
    "card.years_ago_one": "hace 1 año",
    "card.years_ago_other": "hace {n} años",
    "editor.badges": "Insignias",
    "editor.badge_position": "Posición de insignias",
    "editor.badge_position_left": "Izquierda",
    "editor.badge_position_right": "Derecha",
    "editor.badge_position_bottom": "Abajo",
    "editor.time_range": "Rango de tiempo",
    "card.open_app": "Abrir Crystal App",
    "graph.ph": "pH",
    "graph.orp": "ORP",
    "graph.temp": "Temperatura del agua",
    "badge.ph": "pH",
    "badge.orp": "ORP",
    "badge.temp": "Temp",
    "badge.chlorine": "FC",
    "badge.alkalinity": "TA",
    "badge.hardness": "TH",
    "badge.cya": "CYA",
    "badge.salt": "Sal",
    "badge.lsi": "LSI",
  },
  fr: {
    "editor.pool_label": "Piscine ou spa",
    "editor.transparent": "Arrière-plan transparent",
    "editor.show_description": "Afficher la description",
    "editor.show_icons": "Afficher les icônes",
    "editor.show_logo": "Afficher le logo",
    "card.no_vessel_selected": "Sélectionnez un bassin dans l'éditeur de carte.",
    "card.entity_not_found": "Entité d'état de l'eau introuvable pour ce bassin.",
    "card.actions_entity_not_found": "Entité introuvable pour ce bassin.",
    "card.no_actions": "Aucune action requise.",
    "card.actions_header": "Actions",
    "card.just_now": "à l'instant",
    "card.minutes_ago_one": "il y a 1 minute",
    "card.minutes_ago_other": "il y a {n} minutes",
    "card.hours_ago_one": "il y a 1 heure",
    "card.hours_ago_other": "il y a {n} heures",
    "card.days_ago_one": "il y a 1 jour",
    "card.days_ago_other": "il y a {n} jours",
    "card.years_ago_one": "il y a 1 an",
    "card.years_ago_other": "il y a {n} ans",
    "editor.badges": "Badges",
    "editor.badge_position": "Position des badges",
    "editor.badge_position_left": "Gauche",
    "editor.badge_position_right": "Droite",
    "editor.badge_position_bottom": "Bas",
    "editor.time_range": "Plage de temps",
    "card.open_app": "Ouvrir Crystal App",
    "graph.ph": "pH",
    "graph.orp": "ORP",
    "graph.temp": "Température de l'eau",
    "badge.ph": "pH",
    "badge.orp": "ORP",
    "badge.temp": "Temp",
    "badge.chlorine": "FC",
    "badge.alkalinity": "TA",
    "badge.hardness": "TH",
    "badge.cya": "CYA",
    "badge.salt": "Sel",
    "badge.lsi": "LSI",
  },
};

function t(hass, key, vars) {
  const lang = (hass?.language ?? "en").split("-")[0];
  const str = (TRANSLATIONS[lang] ?? TRANSLATIONS["en"])[key] ?? key;
  if (!vars) return str;
  return Object.entries(vars).reduce((s, [k, v]) => s.replace(`{${k}}`, v), str);
}

function _wordmarkUrl() {
  return "/crystal_water_monitor/images/CWM_icon_wordmark_color.svg";
}

// --- Editor ---

class CrystalDiscCardEditor extends HTMLElement {

  set hass(hass) {
    this._hass = hass;
    const selector = this.shadowRoot?.querySelector("ha-selector");
    if (selector) selector.hass = hass;
  }

  setConfig(config) {
    this._config = config;
    this._render();
  }

  _dispatch(patch) {
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: { ...this._config, ...patch } },
      bubbles: true,
      composed: true,
    }));
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const badges = this._config?.badges ?? ["ph", "orp", "waterTemp"];
    const badgePos = this._config?.badge_position ?? "right";

    this.shadowRoot.innerHTML = `
      <style>
        .row { padding: 8px 0; }
        .checkbox-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; font-size: 14px; }
        .checkbox-row label { cursor: pointer; }
        .section-label { font-size: 12px; font-weight: 600; color: var(--secondary-text-color); text-transform: uppercase; letter-spacing: 0.05em; padding: 12px 0 4px; }
        .badge-grid { display: flex; flex-wrap: wrap; gap: 8px; padding: 4px 0 8px; }
        .badge-chip { display: flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 16px; border: 1px solid var(--divider-color); font-size: 13px; cursor: pointer; user-select: none; }
        .badge-chip.selected { background: var(--primary-color); color: white; border-color: var(--primary-color); }
        .position-row { display: flex; gap: 8px; padding: 4px 0 8px; }
        .pos-btn { flex: 1; padding: 6px; border-radius: 8px; border: 1px solid var(--divider-color); font-size: 13px; cursor: pointer; text-align: center; background: none; color: var(--primary-text-color); }
        .pos-btn.selected { background: var(--primary-color); color: white; border-color: var(--primary-color); }
      </style>
      <div class="row">
        <ha-selector label="${t(this._hass, "editor.pool_label")}"></ha-selector>
      </div>
      <div class="checkbox-row">
        <input type="checkbox" id="transparent" ${this._config?.transparent ? "checked" : ""} />
        <label for="transparent">${t(this._hass, "editor.transparent")}</label>
      </div>
      <div class="section-label">${t(this._hass, "editor.badges")}</div>
      <div class="badge-grid">
        ${BADGE_OPTIONS.map(b => `
          <div class="badge-chip ${badges.includes(b.key) ? "selected" : ""}" data-badge="${b.key}">${t(this._hass, b.labelKey)}</div>
        `).join("")}
      </div>
      <div class="section-label">${t(this._hass, "editor.badge_position")}</div>
      <div class="position-row">
        ${["left","right","bottom"].map(p => `
          <button class="pos-btn ${badgePos === p ? "selected" : ""}" data-pos="${p}">
            ${t(this._hass, "editor.badge_position_" + p)}
          </button>
        `).join("")}
      </div>
    `;

    const selector = this.shadowRoot.querySelector("ha-selector");
    if (this._hass) selector.hass = this._hass;
    selector.selector = { device: { integration: "crystal_water_monitor" } };
    selector.value = this._config?.device_id || "";
    selector.label = t(this._hass, "editor.pool_label");
    selector.addEventListener("value-changed", (e) => this._dispatch({ device_id: e.detail.value }));

    this.shadowRoot.querySelector("#transparent").addEventListener("change", (e) =>
      this._dispatch({ transparent: e.target.checked })
    );

    this.shadowRoot.querySelectorAll(".badge-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        const key = chip.dataset.badge;
        const current = this._config?.badges ?? ["ph", "orp", "waterTemp"];
        const next = current.includes(key) ? current.filter(k => k !== key) : [...current, key];
        this._dispatch({ badges: next });
      });
    });

    this.shadowRoot.querySelectorAll(".pos-btn").forEach(btn => {
      btn.addEventListener("click", () => this._dispatch({ badge_position: btn.dataset.pos }));
    });
  }
}

if (!customElements.get("crystal-disc-card-editor")) customElements.define("crystal-disc-card-editor", CrystalDiscCardEditor);


class CrystalDiscCard extends HTMLElement {

  static getConfigElement() {
    return document.createElement("crystal-disc-card-editor");
  }

  static getStubConfig() {
    return { device_id: "", transparent: false, badges: ["ph", "orp", "waterTemp"], badge_position: "right" };
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 3;
  }

  connectedCallback() {
    this._tickInterval = setInterval(() => this._tickLastUpdated(), 60000);
  }

  disconnectedCallback() {
    clearInterval(this._tickInterval);
  }

  _relativeTime(iso) {
    if (!iso) return "";
    const diffMs = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diffMs / 60000);
    if (mins < 1) return t(this._hass, "card.just_now");
    if (mins < 60) return mins === 1 ? t(this._hass, "card.minutes_ago_one") : t(this._hass, "card.minutes_ago_other", { n: mins });
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs === 1 ? t(this._hass, "card.hours_ago_one") : t(this._hass, "card.hours_ago_other", { n: hrs });
    const days = Math.floor(hrs / 24);
    if (days < 365) return days === 1 ? t(this._hass, "card.days_ago_one") : t(this._hass, "card.days_ago_other", { n: days });
    const years = Math.floor(days / 365);
    return years === 1 ? t(this._hass, "card.years_ago_one") : t(this._hass, "card.years_ago_other", { n: years });
  }

  _tickLastUpdated() {
    const el = this.shadowRoot?.querySelector("#crystal-last-updated");
    if (!el) return;
    const entity = this._findWaterStatusEntity();
    if (!entity) return;
    el.textContent = this._relativeTime(entity.attributes.lastUpdatedDate);
  }

  _findWaterStatusEntity() {
    if (!this._hass || !this._config?.device_id) return null;
    const deviceId = this._config.device_id;
    return Object.values(this._hass.states).find((state) => {
      const entityDeviceId = this._hass.entities?.[state.entity_id]?.device_id;
      return entityDeviceId === deviceId && state.entity_id.endsWith("_water_status");
    });
  }

  _findEntityBySuffix(deviceId, suffix) {
    return Object.values(this._hass.states).find((state) => {
      const entityDeviceId = this._hass.entities?.[state.entity_id]?.device_id;
      return entityDeviceId === deviceId && state.entity_id.endsWith(suffix);
    });
  }

  _renderBadges(deviceId, badgeKeys, position) {
    if (!badgeKeys?.length) return { html: "", position };
    const pos = position ?? "right";

    const items = badgeKeys.map(key => {
      const def = BADGE_OPTIONS.find(b => b.key === key);
      if (!def) return null;
      const entity = this._findEntityBySuffix(deviceId, def.entitySuffix);
      const rawValue = entity ? parseFloat(entity.state) : NaN;
      const value = Number.isFinite(rawValue) ? rawValue : null;
      const display = value != null ? (Number.isInteger(value) ? value : value.toFixed(1)) : "—";
      // colour the badge label by status attribute
      const status = entity?.attributes?.status ?? "ok";
      const statusColor = { really_low: "#da1f1f", low: "#f67d00", high: "#f67d00", really_high: "#da1f1f" }[status];
      const bg = statusColor ?? "var(--secondary-background-color)";
      const textColor = statusColor ? "white" : "var(--primary-text-color)";
      const labelColor = statusColor ? "white" : "#2166aa";
      return `
        <div style="
          background: ${bg};
          border-radius: 999px;
          border: 1px solid var(--divider-color);
          padding: 6px 14px;
          display: flex;
          flex-direction: row;
          align-items: center;
          gap: 8px;
          white-space: nowrap;
        ">
          <span style="font-size:13px;font-weight:600;color:${labelColor};">${t(this._hass, def.labelKey)}</span>
          <span style="font-size:13px;color:${textColor};">${display}${def.suffix && value != null ? `<span style="font-size:11px;"> ${def.suffix}</span>` : ""}</span>
        </div>`;
    }).filter(Boolean).join("");

    const isVertical = pos === "left" || pos === "right";
    const containerStyle = isVertical
      ? "display:flex;flex-direction:column;gap:6px;justify-content:center;"
      : "display:flex;flex-direction:row;gap:6px;justify-content:center;padding-top:8px;";

    return { html: `<div style="${containerStyle}">${items}</div>`, position: pos };
  }

  _discUrl(color) {
    const colorName = ["blue", "orange", "red", "gray"].includes(color) ? color : "blue";
    return `/crystal_water_monitor/images/disc-${colorName}.svg`;
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });

    const entity = this._findWaterStatusEntity();
    const transparent = this._config?.transparent;
    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div style="padding:16px;color:var(--secondary-text-color)">
            ${this._config?.device_id ? t(this._hass, "card.entity_not_found") : t(this._hass, "card.no_vessel_selected")}
          </div>
        </ha-card>`;
      return;
    }

    const disc = entity.attributes;
    const color = disc.waterStatusColor || "gray";
    const discUrl = this._discUrl(color);
    const name = disc.name || entity.attributes.friendly_name || "";
    const text = disc.text || entity.state || "";
    const vesselId = disc.vesselId;
    const isMobileApp = /HomeAssistant\/\d/.test(navigator.userAgent);
    const appUrl = isMobileApp && vesselId ? `https://cwmu.us/app/vessels/${vesselId}` : null;

    const lastUpdated = this._relativeTime(disc.lastUpdatedDate);
    const deviceId = this._config?.device_id;
    const badgeKeys = this._config?.badges ?? ["ph", "orp", "waterTemp"];
    const badgePos = this._config?.badge_position ?? "right";
    const { html: badgeHtml } = this._renderBadges(deviceId, badgeKeys, badgePos);

    const tempC = disc.tempC;
    const tempF = tempC != null ? ((tempC * 9) / 5 + 32).toFixed(0) : null;
    const temp = tempF != null ? `<div style="position:relative;display:inline-block;"><span style="font-size:51px;font-weight:500;line-height:1;">${tempF}</span><span style="position:absolute;top:4px;left:100%;font-size:18px;font-weight:300;line-height:1;margin-left:2px;">°F</span></div>` : "";

    const discEl = `
        <div style="position: relative; width: 240px; height: 240px; flex-shrink:0;${appUrl ? "cursor:pointer;" : ""}" ${appUrl ? `data-app-url="${appUrl}"` : ""}>
          <img src="${discUrl}" style="width: 100%; height: 100%; pointer-events:none;" />
          <div style="
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            color: white;
            text-align: center;
            padding: 38px 40px 36px;
            box-sizing: border-box;
          ">
            <div style="font-size: 15px; font-weight: 400;">${name}</div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:0px;">
              <div style="display:flex;justify-content:center;">${temp}</div>
              <div style="font-size: 18px;">${text}</div>
            </div>
            <div id="crystal-last-updated" style="font-size: 13px; opacity: 0.85;">${lastUpdated}</div>
          </div>
        </div>`;

    const isRow = badgePos === "left" || badgePos === "right";
    const inner = `
      <div style="display:flex;flex-direction:${isRow ? "row" : "column"};justify-content:center;align-items:center;padding:24px;gap:12px;">
        ${badgePos === "left" ? badgeHtml : ""}
        ${discEl}
        ${badgePos === "right" ? badgeHtml : ""}
        ${badgePos === "bottom" ? badgeHtml : ""}
      </div>
    `;

    if (transparent) {
      this.shadowRoot.innerHTML = `<div style="background:transparent;">${inner}</div>`;
    } else {
      this.shadowRoot.innerHTML = `<ha-card>${inner}</ha-card>`;
    }

    if (appUrl) {
      this.shadowRoot.querySelector("[data-app-url]")?.addEventListener("click", () => {
        window.open(appUrl, "_blank");
      });
    }
  }
}

if (!customElements.get("crystal-disc-card")) customElements.define("crystal-disc-card", CrystalDiscCard);

// --- Actions Card Editor ---

class CrystalActionsCardEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    const selector = this.shadowRoot?.querySelector("ha-selector");
    if (selector) selector.hass = hass;
  }

  setConfig(config) {
    this._config = config;
    this._render();
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        .checkbox-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; font-size: 14px; }
        .checkbox-row label { cursor: pointer; }
      </style>
      <div style="padding:8px 0"><ha-selector label="${t(this._hass, "editor.pool_label")}"></ha-selector></div>
      <div class="checkbox-row">
        <input type="checkbox" id="show_details" ${this._config?.show_details !== false ? "checked" : ""} />
        <label for="show_details">${t(this._hass, "editor.show_description")}</label>
      </div>
      <div class="checkbox-row">
        <input type="checkbox" id="show_icons" ${this._config?.show_icons !== false ? "checked" : ""} />
        <label for="show_icons">${t(this._hass, "editor.show_icons")}</label>
      </div>
      <div class="checkbox-row">
        <input type="checkbox" id="show_logo" ${this._config?.show_logo !== false ? "checked" : ""} />
        <label for="show_logo">${t(this._hass, "editor.show_logo")}</label>
      </div>
    `;
    const selector = this.shadowRoot.querySelector("ha-selector");
    if (this._hass) selector.hass = this._hass;
    selector.selector = { device: { integration: "crystal_water_monitor" } };
    selector.value = this._config?.device_id || "";
    selector.label = t(this._hass, "editor.pool_label");
    selector.addEventListener("value-changed", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, device_id: e.detail.value } },
        bubbles: true,
        composed: true,
      }));
    });
    this.shadowRoot.querySelector("#show_details").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, show_details: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
    this.shadowRoot.querySelector("#show_icons").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, show_icons: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
    this.shadowRoot.querySelector("#show_logo").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, show_logo: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
  }
}

if (!customElements.get("crystal-actions-card-editor")) customElements.define("crystal-actions-card-editor", CrystalActionsCardEditor);

// --- Actions Card ---

class CrystalActionsCard extends HTMLElement {
  static getConfigElement() {
    return document.createElement("crystal-actions-card-editor");
  }

  static getStubConfig() {
    return { device_id: "", show_details: true };
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 3;
  }

  _findWaterStatusEntity() {
    if (!this._hass || !this._config?.device_id) return null;
    const deviceId = this._config.device_id;
    return Object.values(this._hass.states).find((state) => {
      const entityDeviceId = this._hass.entities?.[state.entity_id]?.device_id;
      return entityDeviceId === deviceId && state.entity_id.endsWith("_water_status");
    });
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });

    const entity = this._findWaterStatusEntity();

    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div style="padding:16px;color:var(--secondary-text-color)">
            ${this._config?.device_id ? t(this._hass, "card.actions_entity_not_found") : t(this._hass, "card.no_vessel_selected")}
          </div>
        </ha-card>`;
      return;
    }

    const actions = entity.attributes.actions || [];
    const vesselName = entity.attributes.name || "";
    const vesselId = entity.attributes.vesselId;
    const showDetails = this._config?.show_details !== false;
    const showIcons = this._config?.show_icons !== false;
    const showLogo = this._config?.show_logo !== false;
    const isMobileApp = /HomeAssistant\/\d/.test(navigator.userAgent);

    const rows = actions.length === 0
      ? `<div style="padding:16px;color:var(--secondary-text-color)">${t(this._hass, "card.no_actions")}</div>`
      : actions.map((a) => `
          <div style="
            display: flex;
            align-items: center;
            padding: 12px 16px;
            border-bottom: 1px solid var(--divider-color);
            gap: 12px;
          ">
            ${showIcons && a.iconUrl ? `<img src="${a.iconUrl}" style="width:36px;height:36px;border-radius:50%;flex-shrink:0;" />` : ""}
            <div>
              <div style="font-size:14px;font-weight:600;">${a.title || ""}</div>
              ${showDetails && a.details ? `<div style="font-size:12px;color:var(--secondary-text-color);margin-top:2px;">${a.details}</div>` : ""}
            </div>
          </div>
        `).join("");

    this.shadowRoot.innerHTML = `
      <ha-card>
        <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;">
          <div>
            <div style="font-size:16px;font-weight:600;">${vesselName}</div>
            <div style="font-size:12px;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:0.05em;margin-top:2px;">${t(this._hass, "card.actions_header")}</div>
          </div>
          ${showLogo ? `<img src="${_wordmarkUrl()}" style="height:30px;" />` : ""}
        </div>
        ${rows}
        ${isMobileApp && vesselId ? `
          <div style="padding:10px 16px;text-align:center;">
            <a href="https://cwmu.us/app/vessels/${vesselId}"
               style="font-size:12px;color:var(--primary-color);text-decoration:none;">
              ${t(this._hass, "card.open_app")}
            </a>
          </div>
        ` : ""}
      </ha-card>
    `;
  }
}

if (!customElements.get("crystal-actions-card")) customElements.define("crystal-actions-card", CrystalActionsCard);

// --- Graph Card Base ---

class CrystalGraphCardBase extends HTMLElement {
  constructor() {
    super();
  }

  static getConfigElement(editorTag) {
    return document.createElement(editorTag);
  }

  static getStubConfig() {
    return { device_id: "" };
  }

  set hass(hass) {
    this._hass = hass;
    this._render().catch(() => {});
  }

  setConfig(config) {
    this._config = config;
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
  }

  getCardSize() { return 3; }

  _findEntity() {
    if (!this._hass || !this._config?.device_id) return null;
    const deviceId = this._config.device_id;
    return Object.values(this._hass.states).find((state) => {
      const entityDeviceId = this._hass.entities?.[state.entity_id]?.device_id;
      return entityDeviceId === deviceId && state.entity_id.endsWith(this.constructor.entitySuffix);
    });
  }

  async _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const entity = this._findEntity();

    if (!entity) {
      this.shadowRoot.innerHTML = this._config?.device_id
        ? ""
        : `<ha-card><div style="padding:16px;color:var(--secondary-text-color)">${t(this._hass, "card.no_vessel_selected")}</div></ha-card>`;
      return;
    }

    const cardConfig = {
      type: "history-graph",
      entities: [{ entity: entity.entity_id, color: "#2166aa" }],
      title: t(this._hass, this.constructor.labelKey),
      hours_to_show: this._config?.hours_to_show ?? 24,
      min_y_axis: this.constructor.minY,
      max_y_axis: this.constructor.maxY,
      extend_to: false,
    };

    if (!this._graphCard || this._lastEntityId !== entity.entity_id || this._lastHours !== (this._config?.hours_to_show ?? 24)) {
      this._lastEntityId = entity.entity_id;
      this._lastHours = this._config?.hours_to_show ?? 24;
      const helpers = await window.loadCardHelpers?.();
      if (!helpers) return;
      this._graphCard = await helpers.createCardElement(cardConfig);
      this._graphCard.hass = this._hass;
      this.shadowRoot.innerHTML = `<div style="position:relative;"><img src="${_wordmarkUrl()}" style="position:absolute;top:12px;right:56px;height:20px;opacity:0.5;z-index:1;pointer-events:none;" /></div>`;
      this.shadowRoot.querySelector("div").appendChild(this._graphCard);
    } else {
      this._graphCard.hass = this._hass;
    }
  }
}

// --- Shared Graph Card Editor ---

class CrystalGraphCardEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    const s = this.shadowRoot?.querySelector("ha-selector");
    if (s) s.hass = hass;
  }
  setConfig(config) { this._config = config; this._render(); }

  _dispatch(patch) {
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: { ...this._config, ...patch } },
      bubbles: true, composed: true,
    }));
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const hours = this._config?.hours_to_show ?? 24;
    this.shadowRoot.innerHTML = `
      <style>
        .row { padding: 8px 0; }
        .section-label { font-size:12px;font-weight:600;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:0.05em;padding:12px 0 4px; }
        .hours-row { display:flex;gap:8px;padding:4px 0; }
        .hours-btn { flex:1;padding:6px;border-radius:8px;border:1px solid var(--divider-color);font-size:13px;cursor:pointer;text-align:center;background:none;color:var(--primary-text-color); }
        .hours-btn.selected { background:#2166aa;color:white;border-color:#2166aa; }
      </style>
      <div class="row"><ha-selector label="${t(this._hass, "editor.pool_label")}"></ha-selector></div>
      <div class="section-label">${t(this._hass, "editor.time_range")}</div>
      <div class="hours-row">
        ${[6, 12, 24, 48, 72].map(h => `
          <button class="hours-btn ${hours === h ? "selected" : ""}" data-hours="${h}">${h}h</button>
        `).join("")}
      </div>
    `;
    const s = this.shadowRoot.querySelector("ha-selector");
    if (this._hass) s.hass = this._hass;
    s.selector = { device: { integration: "crystal_water_monitor" } };
    s.value = this._config?.device_id || "";
    s.addEventListener("value-changed", (e) => this._dispatch({ device_id: e.detail.value }));
    this.shadowRoot.querySelectorAll(".hours-btn").forEach(btn => {
      btn.addEventListener("click", () => this._dispatch({ hours_to_show: parseInt(btn.dataset.hours) }));
    });
  }
}
if (!customElements.get("crystal-graph-card-editor")) customElements.define("crystal-graph-card-editor", CrystalGraphCardEditor);

// --- pH Graph Card ---

class CrystalPhGraphCard extends CrystalGraphCardBase {
  static entitySuffix = "_ph";
  static labelKey = "graph.ph";
  static minY = 6;
  static maxY = 8;
  static getConfigElement() { return document.createElement("crystal-graph-card-editor"); }
  static getStubConfig() { return { device_id: "", hours_to_show: 24 }; }
}
if (!customElements.get("crystal-ph-graph-card")) customElements.define("crystal-ph-graph-card", CrystalPhGraphCard);

// --- ORP Graph Card ---

class CrystalOrpGraphCard extends CrystalGraphCardBase {
  static entitySuffix = "_orp";
  static labelKey = "graph.orp";
  static minY = 0;
  static maxY = 1000;
  static getConfigElement() { return document.createElement("crystal-graph-card-editor"); }
  static getStubConfig() { return { device_id: "", hours_to_show: 24 }; }
}
if (!customElements.get("crystal-orp-graph-card")) customElements.define("crystal-orp-graph-card", CrystalOrpGraphCard);

// --- Temp Graph Card ---

class CrystalTempGraphCard extends CrystalGraphCardBase {
  static entitySuffix = "_water_temperature";
  static labelKey = "graph.temp";
  static minY = 50;
  static maxY = 104;
  static getConfigElement() { return document.createElement("crystal-graph-card-editor"); }
  static getStubConfig() { return { device_id: "", hours_to_show: 24 }; }
}
if (!customElements.get("crystal-temp-graph-card")) customElements.define("crystal-temp-graph-card", CrystalTempGraphCard);

function _crystalEntitySuggestion(type, suffix) {
  return (hass, entityId) => {
    const entry = hass.entities?.[entityId];
    if (entry?.platform !== "crystal_water_monitor") return null;
    if (!entry.entity_id.endsWith(suffix)) return null;
    return { config: { type: `custom:${type}`, device_id: entry.device_id } };
  };
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: "crystal-disc-card",
  name: "Crystal Disc",
  description: "Water status disc for Crystal Water Monitor",
  getEntitySuggestion: _crystalEntitySuggestion("crystal-disc-card", "_water_status"),
});
window.customCards.push({
  type: "crystal-ph-graph-card",
  name: "Crystal pH Graph",
  description: "24h pH history for a Crystal Water Monitor vessel",
  getEntitySuggestion: _crystalEntitySuggestion("crystal-ph-graph-card", "_ph"),
});
window.customCards.push({
  type: "crystal-orp-graph-card",
  name: "Crystal ORP Graph",
  description: "24h ORP history for a Crystal Water Monitor vessel",
  getEntitySuggestion: _crystalEntitySuggestion("crystal-orp-graph-card", "_orp"),
});
window.customCards.push({
  type: "crystal-temp-graph-card",
  name: "Crystal Temp Graph",
  description: "24h water temperature history for a Crystal Water Monitor vessel",
  getEntitySuggestion: _crystalEntitySuggestion("crystal-temp-graph-card", "_watertemp"),
});
window.customCards.push({
  type: "crystal-actions-card",
  name: "Crystal Actions",
  description: "Recommended actions for a Crystal Water Monitor vessel",
  getEntitySuggestion: _crystalEntitySuggestion("crystal-actions-card", "_water_status"),
});

console.info(`%c CRYSTAL-CUSTOM-CARDS %c ${CARD_VERSION} `, "color:white;background:#2d7fc1;font-weight:700", "color:#2d7fc1;background:white;font-weight:700");

const CARD_VERSION = "1.0.4";

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
  },
};

function t(hass, key, vars) {
  const lang = (hass?.language ?? "en").split("-")[0];
  const str = (TRANSLATIONS[lang] ?? TRANSLATIONS["en"])[key] ?? key;
  if (!vars) return str;
  return Object.entries(vars).reduce((s, [k, v]) => s.replace(`{${k}}`, v), str);
}

function _wordmarkUrl() {
  return "/crystal_water_monitor/CWM_icon_wordmark_color.svg";
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

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        .row { padding: 8px 0; }
        .checkbox-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; font-size: 14px; }
        .checkbox-row label { cursor: pointer; }
      </style>
      <div class="row">
        <ha-selector label="${t(this._hass, "editor.pool_label")}"></ha-selector>
      </div>
      <div class="checkbox-row" style="margin-top:8px;">
        <input type="checkbox" id="transparent" ${this._config?.transparent ? "checked" : ""} />
        <label for="transparent">${t(this._hass, "editor.transparent")}</label>
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

    this.shadowRoot.querySelector("#transparent").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, transparent: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
  }
}

if (!customElements.get("crystal-disc-card-editor")) customElements.define("crystal-disc-card-editor", CrystalDiscCardEditor);


class CrystalDiscCard extends HTMLElement {

  static getConfigElement() {
    return document.createElement("crystal-disc-card-editor");
  }

  static getStubConfig() {
    return { device_id: "", transparent: false };
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

  _discUrl(color) {
    const name = ["blue", "orange", "red", "gray"].includes(color) ? color : "blue";
    return `/crystal_water_monitor/disc-${name}.svg`;
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
    const lastUpdated = (() => {
      const iso = disc.lastUpdatedDate;
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
    })();
    const tempC = disc.tempC;
    const tempF = tempC != null ? ((tempC * 9) / 5 + 32).toFixed(0) : null;
    const temp = tempF != null ? `${tempF}°F` : "";

    const inner = `
      <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 24px;
      ">
        <div style="position: relative; width: 240px; height: 240px;">
          <img src="${discUrl}" style="width: 100%; height: 100%;" />
          <div style="
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
            padding: 40px;
            box-sizing: border-box;
          ">
            <div style="font-size: 13px; font-weight: 600; margin-bottom: 6px;">${name}</div>
            <div style="font-size: 44px; font-weight: 700; line-height: 1;">${temp}</div>
            <div style="font-size: 13px; margin-top: 6px;">${text}</div>
            <div style="font-size: 11px; margin-top: 10px; opacity: 0.85;">${lastUpdated}</div>
          </div>
        </div>

      </div>
    `;

    if (transparent) {
      this.shadowRoot.innerHTML = `<div style="background:transparent;">${inner}</div>`;
    } else {
      this.shadowRoot.innerHTML = `<ha-card>${inner}</ha-card>`;
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
    const showDetails = this._config?.show_details !== false;
    const showIcons = this._config?.show_icons !== false;
    const showLogo = this._config?.show_logo !== false;

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
      </ha-card>
    `;
  }
}

if (!customElements.get("crystal-actions-card")) customElements.define("crystal-actions-card", CrystalActionsCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "crystal-disc-card",
  name: "Crystal Disc",
  description: "Water status disc for Crystal Water Monitor",
});
window.customCards.push({
  type: "crystal-actions-card",
  name: "Crystal Actions",
  description: "Recommended actions for a Crystal Water Monitor vessel",
});

console.info(`%c CRYSTAL-CUSTOM-CARDS %c ${CARD_VERSION} `, "color:white;background:#2d7fc1;font-weight:700", "color:#2d7fc1;background:white;font-weight:700");
